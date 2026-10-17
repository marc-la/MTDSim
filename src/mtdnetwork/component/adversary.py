import collections
import logging
from mtdnetwork.statistic.attack_statistics import AttackStatistics
from mtdnetwork.data.constants import HACKER_ATTACK_ATTEMPT_MULTIPLER


class ExploitYieldLedger:
    """Read-only, within-run accounting of WHERE the compound-exploit learner's
    bought successes land — attached for measurement only, never part of the
    modelled attacker state (S2 freeze), so it is set lazily (not in
    ``Adversary.__init__``) and a pristine adversary is byte-identical.

    One entry per EXPLOIT_VULN roll that actually rolls at the consult site. The
    attribution is by probability mass, not by an observed draw: a boosted success
    drew ``u < p_eff`` and would also have succeeded at base iff ``u < c``, so the
    probability it was *bought by learning* (would have failed at base) is
    ``1 - c / p_eff``. Summing that over the run's successful boosted rolls gives the
    expected number of learning-attributable successes, split by whether the target
    host was already owned. No RNG is drawn and no control flow is changed — the
    ledger only reads. See
    docs/implementation/pipeline/ogasp/exploit_learning_yield_prereg.md.
    """

    def __init__(self):
        self.attempts = 0                    # rolls reaching the site (an actual roll)
        self.attempts_on_owned = 0           # rolls aimed at a host already owned
        self.boosted_rolls = 0               # rolls the boost shaped (p_eff is not None)
        self.boosted_successes = 0
        self.attributable_mass = 0.0         # E[learning-bought successes]
        self.attributable_mass_owned = 0.0   # ...landing on an already-owned host
        # fresh-host mass is (attributable_mass - attributable_mass_owned)
        # Host ids that received at least one boosted success — the concentration
        # read: how few hosts absorb the mass, and (intersected with the final
        # compromised set post-run) how few of them convert to breadth.
        self.boosted_success_hosts = set()

    def record(self, *, host_id, c, p_eff, success, host_owned):
        # "Owned" is membership in the attacker's compromised set, read per roll but
        # updated only AFTER the exploit loop, so it reads as "was this host already
        # owned coming INTO this visit" — the right sense for the yield split. (The
        # substrate's own check_compromised() is deliberately NOT consulted: it
        # mutates host state, and it conflates "already owned" with "being
        # compromised during this very visit".)
        self.attempts += 1
        if host_owned:
            self.attempts_on_owned += 1
        if p_eff is None:
            return  # base roll: the boost did not shape it, so no attributable mass
        self.boosted_rolls += 1
        if success:
            self.boosted_successes += 1
            self.boosted_success_hosts.add(host_id)
            mass = 1.0 - c / p_eff  # P(bought by learning | this boosted success)
            self.attributable_mass += mass
            if host_owned:
                self.attributable_mass_owned += mass

    def summary(self):
        owned_frac = self.attempts_on_owned / self.attempts if self.attempts else 0.0
        return {
            "ledger_attempts": self.attempts,
            "ledger_attempts_on_owned": self.attempts_on_owned,
            "ledger_owned_attempt_frac": owned_frac,
            "ledger_boosted_rolls": self.boosted_rolls,
            "ledger_boosted_successes": self.boosted_successes,
            "ledger_boosted_success_host_count": len(self.boosted_success_hosts),
            "attributable_mass": self.attributable_mass,
            "attributable_mass_owned": self.attributable_mass_owned,
            "attributable_mass_fresh": self.attributable_mass - self.attributable_mass_owned,
        }


class Adversary:
    def __init__(self, network, attack_threshold):
        self.network = network
        self._compromised_users = []
        self._compromised_hosts = []
        self._host_stack = []
        self._attack_counter = [0 for n in range(len(self.network.get_graph().nodes()))]
        self._stop_attack = []
        self._attack_threshold = attack_threshold
        self._pivot_host_id = -1
        self._curr_host_id = -1
        self.curr_host = None
        self._curr_ports = []
        self._curr_vulns = []
        self._max_attack_attempts = HACKER_ATTACK_ATTEMPT_MULTIPLER * network.get_total_nodes()
        self._curr_attempts = 0
        self.target_compromised = False
        self.observed_changes = {}

        # Compound-exploit-learning memory (default-off; see
        # docs/implementation/pipeline/ogasp/exploit_learning.md).
        # `n(vuln.id)`: the count of prior *successful* exploits per vulnerability
        # TYPE, keyed on the uuid preserved across `Vulnerability.copy()`, so it is
        # cross-host per-type knowledge. It persists across MTD mutations by design
        # (no decay term) — diversity resists this learner structurally, by changing
        # which types live on which hosts, not by decaying the memory.
        self._exploit_learning_enabled = False
        self._exploit_learning_rate = 0.0            # lambda: per-success odds multiplier
        self._exploit_type_counts = collections.Counter()

        self._attack_stats = AttackStatistics()
        self._curr_process = 'SCAN_HOST'

    def swap_hosts_in_compromised_hosts(self, host_id, other_host_id):
        """
        Update the adversary's host-id-keyed state for a host-topology shuffle.

        `HostTopologyShuffle` swaps two `Host` instances between node ids, so every
        piece of adversary state keyed by host id has to move with them. Only
        `_compromised_hosts` was remapped, leaving `_pivot_host_id`, `_host_stack`,
        `_stop_attack` and `_attack_counter` pointing at whatever now occupies those
        ids — the adversary kept pivoting through a host it no longer owned, queued
        the wrong targets, and carried another host's attempt count and give-up
        status. (Observed: 20 of 38 shuffles left the pivot on a host absent from
        `compromised_hosts`.) The strategy is commented out of the default set, so
        this was latent rather than active.

        D-31 (mtd_write_surfaces.md §c): the remap must mutate the existing list
        objects, never rebind them. `network.update_reachable_compromise`
        (network.py) assigns the adversary's `_compromised_hosts` list object to
        `network.compromised_hosts`, so the two are one list; rebinding here left
        the network holding the pre-swap ids, and `update_reachable_mtd` then
        rebuilt `reachable` from those stale ids, erasing the foothold from the
        visibility model. Slice assignment keeps the alias intact (D-02: the
        foothold stays compromised through the network change).
        """
        def swapped(i):
            if i == host_id:
                return other_host_id
            if i == other_host_id:
                return host_id
            return i

        self._compromised_hosts[:] = [swapped(i) for i in self._compromised_hosts]
        self._host_stack[:] = [swapped(i) for i in self._host_stack]
        self._stop_attack[:] = [swapped(i) for i in self._stop_attack]
        self._pivot_host_id = swapped(self._pivot_host_id)
        self._curr_host_id = swapped(self._curr_host_id)

        # The attempt counter is indexed by host id, so the two entries swap too.
        counter = self._attack_counter
        if 0 <= host_id < len(counter) and 0 <= other_host_id < len(counter):
            counter[host_id], counter[other_host_id] = (
                counter[other_host_id], counter[host_id],
            )

    def get_compromised_hosts(self):
        return self._compromised_hosts

    def get_statistics(self):
        return self._attack_stats.get_record()

    # private
    def get_attack_stats(self):
        return self._attack_stats

    def get_host_stack(self):
        return self._host_stack

    def get_curr_host_id(self):
        return self._curr_host_id

    def get_curr_ports(self):
        return self._curr_ports

    def get_curr_attempts(self):
        return self._curr_attempts

    def get_stop_attack(self):
        return self._stop_attack

    def get_attack_threshold(self):
        return self._attack_threshold

    def get_curr_vulns(self):
        return self._curr_vulns

    def get_max_attack_attempts(self):
        return self._max_attack_attempts

    def get_curr_process(self):
        return self._curr_process

    def get_attack_counter(self):
        return self._attack_counter

    def get_pivot_host_id(self):
        return self._pivot_host_id

    def get_compromised_users(self):
        return self._compromised_users

    # public
    def get_curr_host(self):
        return self.curr_host

    def get_network(self):
        return self.network

    # setter
    def set_curr_host_id(self, host_id):
        self._curr_host_id = host_id

    def set_curr_host(self, host):
        self.curr_host = host

    def set_pivot_host_id(self, host_id):
        self._pivot_host_id = host_id

    def set_curr_ports(self, ports):
        self._curr_ports = ports

    def set_curr_vulns(self, vulns):
        self._curr_vulns = vulns

    def set_curr_attempts(self, curr_attempts):
        self._curr_attempts = curr_attempts

    def set_host_stack(self, host_stack):
        self._host_stack = host_stack

    def set_curr_process(self, curr_process):
        self._curr_process = curr_process

    # --- Compound-exploit-learning (default-off) ---------------------------
    # The mechanism raises the success probability of the EXPLOIT_VULN roll on a
    # cross-host re-encounter of a vulnerability TYPE the attacker has already
    # exploited. It is a deliberate design extension beyond the published lineage
    # (Marc, 2026-08-11) — NOT a fidelity restoration of Zhang's per-type time
    # discount. See docs/implementation/pipeline/ogasp/exploit_learning.md.

    def enable_exploit_learning(self, rate):
        """Turn the mechanism on and set lambda (the per-success odds multiplier).

        Left off by every native / baseline / golden path, so those stay
        byte-identical. `rate == 0` is the exact ablation arm: `effective_exploit_prob`
        returns None for it, routing the roll through the unchanged
        `random.random() < complexity` comparison, so an enabled-but-zero run is
        bit-identical to a disabled one.
        """
        self._exploit_learning_enabled = True
        self._exploit_learning_rate = rate

    def is_exploit_learning_enabled(self):
        return self._exploit_learning_enabled

    def get_exploit_learning_rate(self):
        return self._exploit_learning_rate

    def get_exploit_type_count(self, vuln_id):
        return self._exploit_type_counts[vuln_id]

    def record_exploit_success(self, vuln_id):
        """Bank one successful exploit of this vulnerability type (RNG-free)."""
        self._exploit_type_counts[vuln_id] += 1

    # --- Yield ledger (measurement-only; attached lazily, never __init__) ----
    # The ledger is instrumentation, not attacker state: it records where the
    # learner's bought successes land without drawing RNG or changing control
    # flow. It is attached lazily so a pristine adversary carries no such field
    # and the S2 frozen-state guard stays byte-identical — the ledger is not part
    # of the model, only of a measurement run. See ExploitYieldLedger.

    def enable_exploit_ledger(self):
        """Attach a fresh read-only yield ledger to this run and return it."""
        self._exploit_ledger = ExploitYieldLedger()
        return self._exploit_ledger

    def get_exploit_ledger(self):
        """The attached yield ledger, or None on every run that did not enable one
        (which is every native / baseline / golden path, so they are untouched)."""
        return getattr(self, "_exploit_ledger", None)

    def effective_exploit_prob(self, vuln):
        """The shaped success threshold for `vuln`, or None to use the base one.

        Returns None whenever the roll must stay byte-identical to the
        no-mechanism path — the mechanism is disabled, or the compounding factor
        is exactly 1 (lambda == 0, the exact ablation; or n == 0, identity at
        first encounter). Otherwise the exploit ODDS compound multiplicatively in
        the number of prior successful exploits of this type:

            o = (c / (1 - c)) * (1 + lambda) ** n
            p_eff = o / (1 + o)

        so p_eff(0) = c exactly, p_eff is monotone in n, and p_eff -> 1 as n grows
        — a long, persistent, compounding advantage that saturates only in the
        limit. No RNG is consumed here (SIM-05).
        """
        if not self._exploit_learning_enabled:
            return None
        n = self._exploit_type_counts[vuln.id]
        factor = (1.0 + self._exploit_learning_rate) ** n
        if factor == 1.0:
            # lambda == 0 (exact ablation) or n == 0 (identity at first encounter):
            # hand back None so the roll compares against the unchanged base
            # threshold rather than a float that only algebraically equals it.
            return None
        c = vuln.complexity
        if c >= 1.0:
            return None
        odds = (c / (1.0 - c)) * factor
        return odds / (1.0 + odds)
