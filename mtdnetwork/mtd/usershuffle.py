from mtdnetwork.mtd import MTD
import random


class UserShuffle(MTD):
    def __init__(self, network=None):
        super().__init__(name="UserShuffle",
                         mtd_type='shuffle',
                         resource_type='reserve',
                         network=network)

    def mtd_operation(self, adversary=None):
        hosts = self.network.get_hosts()

        # D-23 family rule (Marc, 2026-08-27, R2): the exposed endpoints are
        # exempt — keyed on the graph key, as IPShuffle does. Internal hosts
        # re-draw from the same network.users_list pool (R1): a harvested
        # credential stays valid wherever that account re-seats, and the
        # adversary's holdings are untouched (D-02).
        for host_id, host_instance in hosts.items():
            if host_id in self.network.exposed_endpoints:
                continue
            host_instance.set_host_users(
                random.choices(
                    self.network.users_list,
                    k=self.network.users_per_host
                )
            )
