import logging
from mtdsim.statistic.attack_statistics import AttackStatistics
from mtdsim.data.constants import HACKER_ATTACK_ATTEMPT_MULTIPLER


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
        """
        def swapped(i):
            if i == host_id:
                return other_host_id
            if i == other_host_id:
                return host_id
            return i

        self._compromised_hosts = [swapped(i) for i in self._compromised_hosts]
        self._host_stack = [swapped(i) for i in self._host_stack]
        self._stop_attack = [swapped(i) for i in self._stop_attack]
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
