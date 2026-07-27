import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)

import simpy
import logging
import random
from mtdsim.component.time_generator import exponential_variates
from mtdsim.data.constants import ATTACK_DURATION


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

    def _execute_scan_host(self):
        """
        Starts the Network enumeration stage.
        Sets up the order of hosts that the hacker will attempt to compromise
        The order is sorted by distance from the exposed endpoints which is done
        in the function adversary.network.host_scan().
        If the scan returns nothing from the scan, then the attacker will stop
        """
        adversary = self.adversary
        compromised_hosts = adversary.get_compromised_hosts()
        stop_attack = adversary.get_stop_attack()
        network = adversary.get_network()

        adversary.set_pivot_host_id(-1)
        visible_network = network.get_hacker_visible_graph()
        # scan_time = constants.NETWORK_HOST_DISCOVER_TIME * visible_network.number_of_nodes()
        uncompromised_hosts = []
        # Add every uncompromised host that is reachable and is not an exposed or compromised host.
        # De-duplicated: a host adjacent to k compromised hosts was previously queued k
        # times, and _execute_enum_host ticks the per-host attempt counter once per pop —
        # so a single scan could burn a host's entire give-up budget (multiplicities up
        # to 10 observed under MTD) without the adversary attacking it any more often.
        # The exposed-endpoint append below and _execute_scan_neighbors' merge both
        # already de-duplicate; this loop was the outlier.
        seen = set()
        for c_host in compromised_hosts:
            for neighbor in network.graph.neighbors(c_host):
                if neighbor in seen or neighbor in compromised_hosts:
                    continue
                if neighbor in network.exposed_endpoints:
                    continue
                if len(network.get_path_from_exposed(neighbor, graph=visible_network)[0]) > 0:
                    seen.add(neighbor)
                    uncompromised_hosts.append(neighbor)

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
        if len(adversary.get_host_stack()) > 0:
            self._enum_host()
        else:
            # terminate the whole process
            if self.logging:
                logging.info("Adversary: Cannot discover new hosts!")
            return

    def _execute_enum_host(self):
        """
        Starts enumerating each host by popping off the host id from the top of the host stack
        time for host hopping required
        Checks if the Hacker has already compromised and backdoored the target host
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
        # Sets node as unattackable if it has been attacked too many times.
        #
        # Brown 2023 (§III-C(2), Table I; §V-C): give up on a host after 10 failed
        # attempts in Scenario 1 (the general attack), and NEVER give up on the target
        # node in Scenario 2 (the targeted attack). The guard here previously read
        # `curr_host_id != target_node and network_type == 0`, which inverted that: it
        # applied the give-up rule ONLY in the targeted network and never in the
        # general one — so in every scenario built from `Network`/`TimeNetwork`
        # (network_type 1) no host was ever given up, and hosts were observed being
        # re-enumerated up to 50 times against Brown's bound of 10.
        #
        # Restored to Brown's polarity: give up on any host that hits the threshold,
        # unless it is the target node of a targeted network.
        adversary.get_attack_counter()[adversary.get_curr_host_id()] += 1
        if adversary.get_attack_counter()[
                adversary.get_curr_host_id()] >= adversary.get_attack_threshold():
            is_protected_target = (network.network_type == 0 and
                                   adversary.get_curr_host_id() == network.get_target_node())
            if not is_protected_target and \
                    adversary.get_curr_host_id() not in adversary.get_stop_attack():
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
            self._enum_host()
        else:
            # Attack event triggered
            self._scan_port()

    def _execute_scan_port(self):
        """
        Starts a port scan on the target host
        Checks if a compromised user has reused their credentials on the target host
        Phase 1
        """
        adversary = self.adversary
        adversary.set_curr_ports(adversary.get_curr_host().port_scan())
        user_reuse = adversary.get_curr_host().can_auto_compromise_with_users(
            adversary.get_compromised_users())
        if user_reuse:
            self.update_compromise_progress(self.env.now, self._proceed_time)
            self._scan_neighbors()
            return
        self._exploit_vuln()

    def _execute_exploit_vuln(self, vulns):
        """
        Finds the top 5 vulnerabilities based on RoA score and have not been exploited yet that the
        Tries exploiting the vulnerabilities to compromise the host
        Checks if the adversary was able to successfully compromise the host
        Phase 2
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
                self.env.process(self._handle_interrupt(start_time, self.adversary.get_curr_process()))
                return
            # R2-attacker: don't keep iterating vulns past sim end.
            if self.end_event.triggered:
                return
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
        if not vulns:
            # No vulnerabilities to try, so the loop above appended nothing — yet
            # check_compromised() below can still return True (the host's services
            # may already be over threshold), and update_compromise_progress
            # back-patches the LAST record. Without a row of its own, the compromise
            # was stamped onto the preceding SCAN_PORT row — asserting a compromise
            # for a SCAN_PORT that had explicitly failed its credential-reuse check,
            # since EXPLOIT_VULN is only reached when SCAN_PORT found no reuse.
            # Record the phase (zero duration: nothing was attempted) so every
            # dispatched verb owns exactly one row and the back-patch is correct.
            now = self.env.now + self._proceed_time
            self.adversary.get_attack_stats().append_attack_operation_record(
                self.adversary.get_curr_process(), now, now, self.adversary)
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
            self._scan_neighbors()
        else:
            self._brute_force()

    def _execute_brute_force(self):
        """
        Tries bruteforcing a login for a short period of time using previous passwords from compromised user accounts to guess a new login.
        Checks if credentials for a user account has been successfully compromised.
        Phase 3
        """
        adversary = self.adversary
        _brute_force_result = adversary.get_curr_host().compromise_with_users(
            adversary.get_compromised_users())
        if _brute_force_result:
            self.update_compromise_progress(self.env.now, self._proceed_time)
            self._scan_neighbors()
        else:
            self._enum_host()

    def _execute_scan_neighbors(self):
        """
        Starts scanning for neighbors from a host that the hacker can pivot to
        Puts the new neighbors discovered to the start of the host stack.
        """
        adversary = self.adversary
        stop_attack = adversary.get_stop_attack()
        # Hosts the adversary has given up on stay given up. _execute_scan_host filters
        # `stop_attack` when it builds the queue, but this verb prepended raw discovery
        # output straight back onto the stack — so a blacklisted host re-entered the
        # queue and was attacked again, defeating the give-up rule from a sibling verb.
        found_neighbors = [
            node_id
            for node_id in adversary.get_curr_host().discover_neighbors()
            if node_id not in stop_attack
        ]
        new__host_stack = found_neighbors + [
            node_id
            for node_id in adversary.get_host_stack()
            if node_id not in found_neighbors and node_id not in stop_attack
        ]
        adversary.set_host_stack(new__host_stack)
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
