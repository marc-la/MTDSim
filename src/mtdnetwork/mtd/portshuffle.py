from mtdnetwork.mtd import MTD
from mtdnetwork.component import host


class PortShuffle(MTD):

    def __init__(self, network=None):
        super().__init__(name="PortShuffle",
                         mtd_type='shuffle',
                         resource_type='application',
                         network=network)

    def mtd_operation(self, adversary=None):
        hosts = self.network.get_hosts()

        for host_id, host_instance in hosts.items():
            # Do not change exposed endpoints as other organisations might
            # require to be fixed. Keyed on the graph key (as IPShuffle), not
            # host_instance.host_id, so the exemption cannot desync from the
            # network's endpoint set after a HostTopologyShuffle swap
            # (ruled 2026-08-27; see docs/implementation/mtd_write_surfaces.md).
            if host_id in self.network.exposed_endpoints:
                continue
            new_ports = []
            for node_id in host_instance.graph.nodes:
                if node_id == host_instance.target_node:
                    continue
                new_port = host.Host.get_random_port(
                    existing_ports=new_ports
                )
                new_ports.append(new_port)
                host_instance.graph.nodes[node_id]["port"] = new_port
