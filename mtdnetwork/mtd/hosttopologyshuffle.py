from mtdnetwork.mtd import MTD
import random


class HostTopologyShuffle(MTD):
    """
    Swaps hosts in the network.
    """

    def __init__(self, network=None):
        super().__init__(name="HostTopologyShuffle",
                         mtd_type='shuffle',
                         resource_type='network',
                         network=network)

    def random_different_host_id(self, curr_host_id, hosts_list):
        other_host_id = random.choice(hosts_list)
        if other_host_id == curr_host_id:
            return self.random_different_host_id(curr_host_id, hosts_list)
        return other_host_id

    def mtd_operation(self, adversary=None):
        hosts = self.network.get_hosts()
        layer_dict = self.network.get_layers()
        cur_layer = -1
        exposed_endpoints = self.network.exposed_endpoints
        seen = []
        host_id_list_in_layer = []

        for host_id, host_instance in hosts.items():
            if layer_dict[host_id] != cur_layer:
                cur_layer = layer_dict[host_id]
                host_id_list_in_layer = []
                for host in hosts:
                    if layer_dict[host] == cur_layer and host not in seen:
                        host_id_list_in_layer.append(host)
            if host_id in seen or host_id in exposed_endpoints:
                continue
            if len(host_id_list_in_layer) == 1:
                continue
            other_host_id = self.random_different_host_id(host_id, host_id_list_in_layer)
            if other_host_id in seen or other_host_id in exposed_endpoints:
                continue
            other_host_instance = hosts[other_host_id]

            host_instance.host_id = other_host_id
            other_host_instance.host_id = host_id

            self.network.graph.nodes[host_id]["host"] = other_host_instance
            self.network.graph.nodes[other_host_id]["host"] = host_instance

            seen.append(host_id)
            seen.append(other_host_id)
            host_id_list_in_layer.remove(host_id)
            host_id_list_in_layer.remove(other_host_id)

            self._swap_compromised_ids(adversary, host_id, other_host_id)

        # The compromised set now carries the swapped ids, so the visibility
        # model is rebuilt from it (D-02: the foothold keeps its contents and its
        # new graph neighbours become visible through `reachable`).
        self.network.update_reachable_mtd()

        # Update Attack Path Exposure for target networks
        if self.network.get_network_type() == 0:
            self.network.add_attack_path_exposure()
        self.network.add_shortest_path()

        # The id->instance mapping moved, so the per-id ip feed the reactive
        # arm reads (`scorer.current_hosts_ip`) is refreshed the way
        # CompleteTopologyShuffle and IPShuffle refresh it.
        self.network.update_current_hosts_ip(
            [host_instance.ip for host_instance in self.network.get_hosts().values()]
        )

    def _swap_compromised_ids(self, adversary, host_id, other_host_id):
        """Move the compromise bookkeeping with the swapped instances (D-31).

        The adversary remaps its id-keyed state in place, which keeps
        `network.compromised_hosts` current whenever it is the alias that
        `update_reachable_compromise` establishes. Before the first compromise
        (or with no adversary attached) the network holds a separate list, so
        it is remapped in place here as well; nothing is ever rebound.
        """
        if adversary is not None:
            adversary.swap_hosts_in_compromised_hosts(host_id, other_host_id)
        network_list = self.network.compromised_hosts
        if adversary is None or network_list is not adversary.get_compromised_hosts():
            network_list[:] = [
                other_host_id if i == host_id else host_id if i == other_host_id else i
                for i in network_list
            ]