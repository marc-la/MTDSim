from mtdnetwork.mtd import MTD


class ServiceDiversity(MTD):
    def __init__(self, network=None, shuffles=50):
        self.shuffles = shuffles
        super().__init__(name="ServiceDiversity",
                         mtd_type='diversity',
                         resource_type='application',
                         network=network)

    def mtd_operation(self, adversary=None):
        service_generator = self.network.get_service_generator()
        hosts = self.network.get_hosts()
        for host_id, host_instance in hosts.items():
            if host_id in self.network.exposed_endpoints:
                continue
            for node_id in range(host_instance.total_nodes):
                if node_id == host_instance.target_node:
                    continue
                # Zhang 2023 §4.3.1.3 (IS-MTD-05): re-configure services "with
                # different versions" — the version pool is the diversity space.
                # The inherited latest-version-only replacement is documented
                # nowhere and systematically shrinks the vuln surface. D-05 fix
                # (Marc, 2026-07-29): draw a random compatible service at a
                # random version, the same draw host generation uses.
                host_instance.graph.nodes[node_id]["service"] = service_generator.get_random_service(
                    host_instance.os_type,
                    host_instance.os_version
                )
        # Update Attack Path Exposure for target networks
        if self.network.get_network_type() == 0:
            self.network.add_attack_path_exposure()
        self.network.add_shortest_path()