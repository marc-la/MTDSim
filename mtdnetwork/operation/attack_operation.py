import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)

import simpy
import logging
import random
from mtdnetwork.component.time_generator import exponential_variates
from mtdnetwork.data.constants import ATTACK_DURATION


# --- Carved action surface -------------------------------------------------
# The inherited attack module is a self-driving FSM: each _execute_* core
# hard-calls its own successor (the "tail-call"), so the six verbs run only in
# the order the calls impose. The carve separates each verb's executable core
# (_do_*, which performs the action and RETURNS its branch outcome) from that
# succession (the _execute_* wrapper, which reads the outcome and dispatches to
# the native successor). The native wrappers reproduce the pre-carve behaviour
# bit-for-bit; a controller instead calls the cores (via step()) and owns the
# succession itself — the third lever from
# docs/implementation/pipeline/ogasp/action_layer_anatomy.md §3.3.
#
# EXPLOIT_VULN has three outcomes, not two, so it cannot use a bare bool: an MTD
# interrupt or sim-end can halt it mid-attempt, in which case the native code
# returns WITHOUT dispatching a successor.
EXPLOIT_COMPROMISED = 'EXPLOIT_COMPROMISED'      # host compromised -> native: SCAN_NEIGHBOR
EXPLOIT_UNCOMPROMISED = 'EXPLOIT_UNCOMPROMISED'  # not compromised  -> native: BRUTE_FORCE
EXPLOIT_HALTED = 'EXPLOIT_HALTED'                # interrupt/sim-end -> native: no succession

# step() returns this when the sim ended DURING the verb, so the verb never acted.
# It must be distinguishable from a verb's legitimate outcome: _do_scan_neighbors
# returns None as its no-branch result, and a verb that completes may itself fire
# end_event (via update_compromise_progress) — a driver inferring "aborted" from
# end_event.triggered would discard that completed verb's real outcome.
# Controller-facing only; the native FSM never sees it.
STEP_ABORTED = 'STEP_ABORTED'


class ActionContextError(RuntimeError):
    """Raised when a verb's core is invoked without the shared adversary state it
    assumes (its precondition, per action_layer_anatomy.md §2.2). The native FSM
    guarantees preconditions by call order; a controller driving verbs out of
    that order must satisfy them itself. This converts the silent degenerations
    and AttributeError crashes catalogued in §3.3 into a loud failure at the
    point of misuse. Controller-facing only — the native path never raises it."""


class AttackOperation:
    def __init__(self, env, end_event, adversary, proceed_time=0):
        """

        :param env: the parameter to facilitate simPY env framework
        :param adversary: the simulation attacker
        :param proceed_time: the time to proceed attack simulation
        """

        self.env = env
        self.end_event = end_event
        self.adversary = adversary
        self._attack_process = None
        self._interrupted_mtd = None
        self._proceed_time = proceed_time
        self.logging = False
 

    def proceed_attack(self):
        if self.adversary.get_curr_process() == 'SCAN_HOST':
            self._scan_host()
        elif self.adversary.get_curr_process() == 'ENUM_HOST':
            self._enum_host()
        elif self.adversary.get_curr_process() == 'SCAN_PORT':
            self._scan_port()
        elif self.adversary.get_curr_process() == 'SCAN_NEIGHBOR':
            self._scan_neighbors()
        elif self.adversary.get_curr_process() == 'EXPLOIT_VULN':
            self._exploit_vuln()
        elif self.adversary.get_curr_process() == 'BRUTE_FORCE':
            self._brute_force()

    def _execute_attack_action(self, time, attack_action):
        """
        a function to execute a given time-consuming attack action
        :param time: The time duration before executing an attack action.
        :param attack_action: attack action
        """
        start_time = self.env.now + self._proceed_time
        try:
            if self.logging:
                logging.info("Adversary: Start %s at %.1fs." % (self.adversary.get_curr_process(), start_time))
            yield self.env.timeout(time)
        except simpy.Interrupt:
            self.env.process(self._handle_interrupt(start_time, self.adversary.get_curr_process()))
            return
        # R2-attacker: don't progress the attack chain past sim termination.
        if self.end_event.triggered:
            return
        finish_time = self.env.now + self._proceed_time
        if self.logging:
            logging.info("Adversary: Processed %s at %.1fs." % (self.adversary.get_curr_process(), finish_time))
        self.adversary.get_attack_stats().append_attack_operation_record(self.adversary.get_curr_process(), start_time,
                                                                         finish_time, self.adversary)
        attack_action()

    def _scan_host(self):
        """
        raise an SCAN_HOST action
        """
        self.adversary.set_curr_process('SCAN_HOST')
        self._attack_process = self.env.process(self._execute_attack_action(ATTACK_DURATION['SCAN_HOST'],
                                                                            self._execute_scan_host))

    def _enum_host(self):
        """
        raise an ENUM_HOST action
        """
        if len(self.adversary.get_host_stack()) > 0:
            self.adversary.set_curr_process('ENUM_HOST')
            self._attack_process = self.env.process(self._execute_attack_action(ATTACK_DURATION['ENUM_HOST'],
                                                                                self._execute_enum_host))
        else:
            self._scan_host()

    def _scan_port(self):
        """
        raise an SCAN_PORT action 
        """
        self.adversary.set_curr_process('SCAN_PORT')
        self._attack_process = self.env.process(self._execute_attack_action(ATTACK_DURATION['SCAN_PORT'],
                                                                            self._execute_scan_port))

    def _exploit_vuln(self):
        """
        raise an EXPLOIT_VULN action
        """
        # exploit_time = exponential_variates(ATTACK_DURATION['EXPLOIT_VULN'][0], ATTACK_DURATION['EXPLOIT_VULN'][1])
        adversary = self.adversary
        adversary.set_curr_vulns(adversary.get_curr_host().get_vulns(adversary.get_curr_ports()))
        self.adversary.set_curr_process('EXPLOIT_VULN')
        self._attack_process = self.env.process(self._execute_exploit_vuln(adversary.get_curr_vulns()))

    def _brute_force(self):
        """
        raise an BRUTE_FORCE action
        """
        self.adversary.set_curr_process('BRUTE_FORCE')
        self._attack_process = self.env.process(self._execute_attack_action(ATTACK_DURATION['BRUTE_FORCE'],
                                                                            self._execute_brute_force))

    def _scan_neighbors(self):
        """
        raise an SCAN_NEIGHBOR action
        """
        self.adversary.set_curr_process('SCAN_NEIGHBOR')
        self._attack_process = self.env.process(self._execute_attack_action(ATTACK_DURATION['SCAN_NEIGHBOR'],
                                                                            self._execute_scan_neighbors))

    def _handle_interrupt(self, start_time, name):
        """
        a function to handle the interrupt of the attack action caused by MTD operations
        :param start_time: the start time of the attack action
        :param name: the name of the attack action
        """
        adversary = self.adversary
        adversary.get_attack_stats().append_attack_operation_record(name, start_time,
                                                                    self.env.now + self._proceed_time,
                                                                    adversary, self._interrupted_mtd)
        # confusion penalty caused by MTD operation
        yield self.env.timeout(exponential_variates(ATTACK_DURATION['PENALTY'], 0.5))

        # R2-attacker: same gate as _execute_attack_action — don't restart
        # phases past sim end.
        if self.end_event.triggered:
            return

        if self._interrupted_mtd.get_resource_type() == 'network':
            self._interrupted_mtd = None
            adversary.set_curr_host_id(-1)
            adversary.set_curr_host(None)
            if self.logging:
                logging.info('Adversary: Restarting with SCAN_HOST at %.1fs!' % (self.env.now + self._proceed_time))
            self._scan_host()
        elif self._interrupted_mtd.get_resource_type() == 'application':
            self._interrupted_mtd = None
            if self.logging:
                logging.info('Adversary: Restarting with SCAN_PORT at %.1fs!' % (self.env.now + self._proceed_time))
            self._scan_port()

    def _do_scan_host(self):
        """
        SCAN_HOST core. Starts the Network enumeration stage.
        Sets up the order of hosts that the hacker will attempt to compromise
        The order is sorted by distance from the exposed endpoints which is done
        in the function adversary.network.host_scan().

        Returns True if hosts were discovered (host_stack now non-empty), else
        False. Native succession: True -> ENUM_HOST; False -> terminate ("cannot
        discover new hosts"). Precondition: none — it manufactures its own
        host_stack from network state.
        """
        adversary = self.adversary
        compromised_hosts = adversary.get_compromised_hosts()
        stop_attack = adversary.get_stop_attack()
        network = adversary.get_network()

        adversary.set_pivot_host_id(-1)
        visible_network = network.get_hacker_visible_graph()
        # scan_time = constants.NETWORK_HOST_DISCOVER_TIME * visible_network.number_of_nodes()
        uncompromised_hosts = []
        # Add every uncompromised host that is reachable and is not an exposed or compromised host
        for c_host in compromised_hosts:
            uncompromised_hosts = uncompromised_hosts + [
                neighbor
                for neighbor in network.graph.neighbors(c_host)
                if neighbor not in compromised_hosts and neighbor not in network.exposed_endpoints and
                   len(network.get_path_from_exposed(neighbor, graph=visible_network)[0]) > 0
            ]

        # Add random element from 0 to 1 so the scan does not return the same order of hosts each time for the hacker
        uncompromised_hosts = sorted(
            uncompromised_hosts,
            key=lambda host_id: network.get_path_from_exposed(host_id, graph=visible_network)[1] + random.random()
        )

        uncompromised_hosts = uncompromised_hosts + [
            ex_node
            for ex_node in network.exposed_endpoints
            if ex_node not in compromised_hosts
        ]
        discovered_hosts = [n for n in uncompromised_hosts if n not in stop_attack]

        adversary.set_host_stack(discovered_hosts)
        return len(adversary.get_host_stack()) > 0

    def _execute_scan_host(self):
        """
        Native FSM wrapper for SCAN_HOST: run the core, then dispatch to the
        inherited successor. Behaviour is bit-identical to the pre-carve core.
        If the scan returns nothing, the attacker stops.
        """
        if self._do_scan_host():
            self._enum_host()
        else:
            # terminate the whole process
            if self.logging:
                logging.info("Adversary: Cannot discover new hosts!")
            return

    def _do_enum_host(self):
        """
        ENUM_HOST core. Starts enumerating each host by popping off the host id
        from the top of the host stack (time for host hopping required). Ticks
        the attack counter (and the give-up list, targeted network only), resets
        per-host working state, and sets the pivot. Checks if the Hacker has
        already compromised and backdoored the target host; if so, records the
        re-control progress here.

        Returns True if the enumerated host was already compromised (native ->
        loop ENUM_HOST), False if it is a fresh host to attack (native ->
        SCAN_PORT). Precondition: a non-empty host_stack (the raise _enum_host
        re-routes to SCAN_HOST when the stack is empty).
        """
        adversary = self.adversary
        network = adversary.get_network()
        adversary.set_host_stack(network.sort_by_distance_from_exposed_and_pivot_host(
            adversary.get_host_stack(),
            adversary.get_compromised_hosts(),
            pivot_host_id=adversary.get_pivot_host_id()
        ))
        adversary.set_curr_host_id(adversary.get_host_stack().pop(0))
        adversary.set_curr_host(network.get_host(adversary.get_curr_host_id()))
        # Sets node as unattackable if has been attack too many times
        adversary.get_attack_counter()[adversary.get_curr_host_id()] += 1
        if adversary.get_attack_counter()[
            adversary.get_curr_host_id()] == adversary.get_attack_threshold():
            # target node feature
            if adversary.get_curr_host_id() != network.get_target_node() and network.network_type == 0:
                adversary.get_stop_attack().append(adversary.get_curr_host_id())

        # Checks if max attack attempts has been reached, empty stacks if reached
        # if adversary.get_curr_attempts() >= adversary.get_max_attack_attempts():
        #     adversary.set_host_stack([])
        #     return
        adversary.set_curr_ports([])
        adversary.set_curr_vulns([])

        # Sets the next host that the Hacker will pivot from to compromise other hosts
        # The pivot host needs to be a compromised host that the hacker can access
        self._set_next_pivot_host()

        if adversary.get_curr_host().compromised:
            self.update_compromise_progress(self.env.now, self._proceed_time)
            return True
        return False

    def _execute_enum_host(self):
        """
        Native FSM wrapper for ENUM_HOST: run the core, then dispatch. An
        already-compromised host loops back to ENUM_HOST; a fresh host triggers
        the attack proper (SCAN_PORT). Bit-identical to the pre-carve core.
        """
        if self._do_enum_host():
            self._enum_host()
        else:
            # Attack event triggered
            self._scan_port()

    def _do_scan_port(self):
        """
        SCAN_PORT core. Starts a port scan on the target host and checks whether
        a compromised user has reused their credentials on it. On a reuse hit,
        records the compromise progress here. Phase 1.

        Returns True if credential reuse compromised the host (native ->
        SCAN_NEIGHBOR), False otherwise (native -> EXPLOIT_VULN). Precondition:
        curr_host set (by ENUM_HOST).
        """
        adversary = self.adversary
        adversary.set_curr_ports(adversary.get_curr_host().port_scan())
        user_reuse = adversary.get_curr_host().can_auto_compromise_with_users(
            adversary.get_compromised_users())
        if user_reuse:
            self.update_compromise_progress(self.env.now, self._proceed_time)
            return True
        return False

    def _execute_scan_port(self):
        """
        Native FSM wrapper for SCAN_PORT: run the core, then dispatch. Reuse
        expands from the freshly-owned host (SCAN_NEIGHBOR); no reuse falls
        through to the exploit attempt (EXPLOIT_VULN). Bit-identical.
        """
        if self._do_scan_port():
            self._scan_neighbors()
        else:
            self._exploit_vuln()

    def _do_exploit_vuln(self, vulns, driven=False):
        """
        EXPLOIT_VULN core (generator). Finds the top 5 vulnerabilities based on
        RoA score and not yet exploited, tries exploiting them to compromise the
        host, and checks whether the adversary succeeded. On compromise, applies
        the exploitability bookkeeping and records the progress here. Phase 2.

        Returns one of EXPLOIT_COMPROMISED / EXPLOIT_UNCOMPROMISED / EXPLOIT_HALTED.
        EXPLOIT_HALTED means an MTD interrupt was raised or the sim ended mid-attempt
        — the native code returns without dispatching a successor, so the caller
        must NOT dispatch either. Precondition: curr_host set (by ENUM_HOST) and
        curr_ports populated (by SCAN_PORT); empty curr_ports yields no vulns and
        the attempt degenerates to EXPLOIT_UNCOMPROMISED (native falls to BRUTE_FORCE).

        ``driven`` (controller-facing, set only by step()): on an MTD interrupt,
        **re-raise** simpy.Interrupt instead of spawning the native
        _handle_interrupt recovery, so the movement-layer driver owns succession
        (reading the interrupt as a failure verdict) exactly as it does for the
        other five verbs — no rogue native chain runs behind the driver. The
        native _execute_exploit_vuln keeps the default (driven=False), so the
        native FSM path — and the baseline/golden scenarios — stay byte-identical.
        """
        adversary = self.adversary
        for vuln in vulns:
            exploit_time = exponential_variates(vuln.exploit_time(host=adversary.get_curr_host()), 0.5)
            start_time = self.env.now + self._proceed_time
            try:
                if self.logging:
                    logging.info(
                    "Adversary: Start %s %s on host %s at %.1fs." % (self.adversary.get_curr_process(), vuln.id,
                                                                     self.adversary.get_curr_host_id(), start_time))
                yield self.env.timeout(exploit_time)
            except simpy.Interrupt:
                if driven:
                    # Driven mode: let the interrupt propagate to the driver, which
                    # owns succession (interrupt-as-failure). Do NOT spawn the
                    # native recovery — it would re-dispatch verbs behind the driver.
                    raise
                self.env.process(self._handle_interrupt(start_time, self.adversary.get_curr_process()))
                return EXPLOIT_HALTED
            # R2-attacker: don't keep iterating vulns past sim end.
            if self.end_event.triggered:
                return EXPLOIT_HALTED
            finish_time = self.env.now + self._proceed_time
            if self.logging:
                logging.info(
                "Adversary: Processed %s %s on host %s at %.1fs." % (self.adversary.get_curr_process(), vuln.id,
                                                                     self.adversary.get_curr_host_id(), finish_time))
            self.adversary.get_attack_stats().append_attack_operation_record(self.adversary.get_curr_process(),
                                                                             start_time,
                                                                             finish_time, self.adversary)
            vuln.network(host=adversary.get_curr_host())
            # cumulative vulnerability exploitation attempts
            adversary.set_curr_attempts(adversary.get_curr_attempts() + 1)
        if adversary.get_curr_host().check_compromised():
            for vuln in adversary.get_curr_vulns():
                if vuln.is_exploited():
                    if vuln.exploitability == vuln.cvss / 5.5:
                        vuln.exploitability = (1 - vuln.exploitability) / 2 + vuln.exploitability
                        if vuln.exploitability > 1:
                            vuln.exploitability = 1
                        # todo: record vulnerability roa, impact, and complexity
                        self.adversary.get_network().get_scorer().add_vuln_compromise(self.env.now, vuln)

            self.update_compromise_progress(self.env.now, self._proceed_time)
            return EXPLOIT_COMPROMISED
        return EXPLOIT_UNCOMPROMISED

    def _execute_exploit_vuln(self, vulns):
        """
        Native FSM wrapper for EXPLOIT_VULN (generator): delegate to the core
        with `yield from` (preserving every per-vuln timeout yield in order),
        then dispatch on its outcome. Compromise expands (SCAN_NEIGHBOR); failure
        falls to the credential fallback (BRUTE_FORCE); a halt (interrupt/sim-end)
        dispatches nothing. Bit-identical to the pre-carve core.
        """
        outcome = yield from self._do_exploit_vuln(vulns)
        if outcome == EXPLOIT_COMPROMISED:
            self._scan_neighbors()
        elif outcome == EXPLOIT_UNCOMPROMISED:
            self._brute_force()
        # EXPLOIT_HALTED: interrupt spawned or sim ended; no succession.

    def _do_brute_force(self):
        """
        BRUTE_FORCE core. Tries bruteforcing a login for a short period using
        previous passwords from compromised user accounts to guess a new login,
        and checks whether a user account was successfully compromised. On
        success, records the compromise progress here. Phase 3.

        Returns True if the host was compromised (native -> SCAN_NEIGHBOR), False
        otherwise (native -> ENUM_HOST, abandoning this host). Precondition:
        curr_host set (by ENUM_HOST).
        """
        adversary = self.adversary
        _brute_force_result = adversary.get_curr_host().compromise_with_users(
            adversary.get_compromised_users())
        if _brute_force_result:
            self.update_compromise_progress(self.env.now, self._proceed_time)
            return True
        return False

    def _execute_brute_force(self):
        """
        Native FSM wrapper for BRUTE_FORCE: run the core, then dispatch. Success
        expands (SCAN_NEIGHBOR); failure abandons the host and takes the next
        (ENUM_HOST). Bit-identical to the pre-carve core.
        """
        if self._do_brute_force():
            self._scan_neighbors()
        else:
            self._enum_host()

    def _do_scan_neighbors(self):
        """
        SCAN_NEIGHBOR core. Starts scanning for neighbors from a host that the
        hacker can pivot to, and puts the new neighbors discovered to the start
        of the host stack.

        No branch — native succession is always ENUM_HOST. Returns None.
        Precondition: curr_host set (and semantically only meaningful on a
        just-compromised host).
        """
        adversary = self.adversary
        found_neighbors = adversary.get_curr_host().discover_neighbors()
        new__host_stack = found_neighbors + [
            node_id
            for node_id in adversary.get_host_stack()
            if node_id not in found_neighbors
        ]
        adversary.set_host_stack(new__host_stack)

    def _execute_scan_neighbors(self):
        """
        Native FSM wrapper for SCAN_NEIGHBOR: run the core, then dispatch to the
        sole successor (ENUM_HOST). Bit-identical to the pre-carve core.
        """
        self._do_scan_neighbors()
        self._enum_host()

    def _set_next_pivot_host(self):
        """
        Sets the next host that the Hacker will pivot from to compromise other hosts
        The pivot host needs to be a compromised host that the hacker can access
        """
        adversary = self.adversary
        neighbors = list(adversary.get_network().get_neighbors(adversary.get_curr_host_id()))
        if adversary.get_pivot_host_id() in neighbors:
            return
        for n in neighbors:
            if n in adversary.get_compromised_hosts():
                adversary.set_pivot_host_id(n)
                return
        adversary.set_pivot_host_id(-1)

    def update_compromise_progress(self, now, proceed_time):
        """
        Updates the Hackers progress state when it compromises a host.
        """
        adversary = self.adversary
        adversary._pivot_host_id = adversary.get_curr_host_id()
        if adversary.get_curr_host_id() not in adversary.get_compromised_hosts():
            adversary.get_compromised_hosts().append(adversary.get_curr_host_id())
            adversary.get_attack_stats().update_compromise_host(adversary.curr_host)
            if self.logging:
                logging.info(
                "Adversary: Host %i has been compromised at %.1fs!" % (
                    adversary.get_curr_host_id(), now + proceed_time))
            adversary.get_network().update_reachable_compromise(
                adversary.get_curr_host_id(), adversary.get_compromised_hosts())

            for user in adversary.get_curr_host().get_compromised_users():
                if user not in adversary.get_compromised_users():
                    adversary.get_attack_stats().update_compromise_user(user)
            adversary._compromised_users = list(set(
                adversary.get_compromised_users() + adversary.get_curr_host().get_compromised_users()))
            if adversary.get_network().is_compromised(adversary.get_compromised_hosts()):
                # terminate the whole process
                if not self.end_event.triggered:  # Check if the event has not been triggered yet
                    self.end_event.succeed()
                return

            # If target network, set adversary as done once adversary has compromised target node
            # if self.network.get_target_node() == self._curr_host_id:
            # if self.network.get_network_type() == 0:
            #      # terminate the whole process
            #     self.target_compromised = True
            #     self.end_event.succeed()
            #     return
            #

    # --- Controller-facing surface (never called by the native FSM) ---------
    def assert_action_context(self, verb):
        """Precondition guard. Raise ActionContextError if `verb`'s core would run
        without the shared adversary state it assumes (anatomy §2.2). The native
        FSM guarantees these by call order and never calls this; a controller
        driving verbs out of native order calls it (directly, or via step()) to
        fail loudly instead of degenerating silently or crashing with a bare
        AttributeError deep in the substrate.
        """
        adversary = self.adversary
        if verb == 'SCAN_HOST':
            return  # root: manufactures its own host_stack from network state
        if verb == 'ENUM_HOST':
            if len(adversary.get_host_stack()) == 0:
                raise ActionContextError(
                    "ENUM_HOST requires a non-empty host_stack; none present "
                    "(SCAN_HOST/SCAN_NEIGHBOR fill it).")
            return
        if verb in ('SCAN_PORT', 'BRUTE_FORCE', 'SCAN_NEIGHBOR'):
            if adversary.get_curr_host() is None:
                raise ActionContextError(
                    "%s requires curr_host to be set (ENUM_HOST sets it)." % verb)
            return
        if verb == 'EXPLOIT_VULN':
            if adversary.get_curr_host() is None:
                raise ActionContextError(
                    "EXPLOIT_VULN requires curr_host to be set (ENUM_HOST sets it).")
            if len(adversary.get_curr_ports()) == 0:
                raise ActionContextError(
                    "EXPLOIT_VULN requires curr_ports populated by SCAN_PORT; empty "
                    "curr_ports yields no vulns and degenerates to BRUTE_FORCE silently.")
            return
        raise ActionContextError("unknown verb %r" % verb)

    def step(self, verb):
        """Drivability primitive: perform one verb with its native time cost and
        RETURN its outcome (a _do_* return value), WITHOUT dispatching a successor
        — the third lever from anatomy §3.3. A SimPy generator: drive it from a
        controller process with `outcome = yield from attack_operation.step(verb)`,
        then choose the next verb yourself (that choice is the driver's job, out of
        this module's scope).

        Fails loudly (assert_action_context) if the verb's precondition is unmet,
        and records each verb in the attack stats exactly as the native path does,
        so a driven run is observable in the same attack_record.

        Returns ``STEP_ABORTED`` if the simulation ended during the verb, so the verb
        never acted. Callers must test for that sentinel rather than inferring an
        abort from ``end_event.triggered``: three cores call
        ``update_compromise_progress``, which can fire ``end_event`` on a verb that
        completed successfully, and treating that as an abort discards the outcome.

        Interrupt handling (driven): an MTD interrupt propagates out of step() as
        simpy.Interrupt for every verb — including EXPLOIT_VULN, which runs its
        core with driven=True so it re-raises rather than spawning the native
        recovery chain. The driver catches the interrupt and owns succession
        (reading it as a failure verdict). The native FSM path is untouched, so
        the baseline/golden scenarios stay byte-identical.
        """
        self.assert_action_context(verb)
        adversary = self.adversary
        if verb == 'EXPLOIT_VULN':
            # EXPLOIT_VULN times per-vuln inside its core (no single outer timeout).
            adversary.set_curr_process('EXPLOIT_VULN')
            adversary.set_curr_vulns(
                adversary.get_curr_host().get_vulns(adversary.get_curr_ports()))
            outcome = yield from self._do_exploit_vuln(
                adversary.get_curr_vulns(), driven=True)
            return outcome
        cores = {
            'SCAN_HOST': self._do_scan_host,
            'ENUM_HOST': self._do_enum_host,
            'SCAN_PORT': self._do_scan_port,
            'BRUTE_FORCE': self._do_brute_force,
            'SCAN_NEIGHBOR': self._do_scan_neighbors,
        }
        adversary.set_curr_process(verb)
        start_time = self.env.now + self._proceed_time
        yield self.env.timeout(ATTACK_DURATION[verb])
        # R2-attacker: same gate as _execute_attack_action — don't act past sim end.
        # Returns the STEP_ABORTED sentinel, not None: None is _do_scan_neighbors'
        # legitimate no-branch outcome, and a driver cannot re-derive "aborted" from
        # end_event.triggered because a verb that RAN may have fired end_event itself.
        if self.end_event.triggered:
            return STEP_ABORTED
        finish_time = self.env.now + self._proceed_time
        adversary.get_attack_stats().append_attack_operation_record(
            verb, start_time, finish_time, adversary)
        return cores[verb]()

    def get_proceed_time(self):
        return self._proceed_time

    def set_proceed_time(self, proceed_time):
        self._proceed_time = proceed_time

    def get_attack_process(self):
        return self._attack_process

    def set_attack_process(self, attack_process):
        self._attack_process = attack_process

    def set_interrupted_mtd(self, mtd):
        self._interrupted_mtd = mtd

    def get_adversary(self):
        return self.adversary
