import random
from collections import deque
from mtdnetwork.mtd.completetopologyshuffle import CompleteTopologyShuffle
from mtdnetwork.mtd.ipshuffle import IPShuffle
from mtdnetwork.mtd.hosttopologyshuffle import HostTopologyShuffle
from mtdnetwork.mtd.portshuffle import PortShuffle
from mtdnetwork.mtd.osdiversity import OSDiversity
from mtdnetwork.mtd.servicediversity import ServiceDiversity
from mtdnetwork.mtd.usershuffle import UserShuffle
from mtdnetwork.mtd.osdiversityassignment import OSDiversityAssignment
from mtdnetwork.data.constants import MTD_TRIGGER_INTERVAL
from heapq import heappush, heappop


class MTDScheme:

    def __init__(self, scheme: str, network, mtd_trigger_interval=None, mtd_trigger_std=0.5, custom_strategies=None, security_metric_record=None):
        self._scheme = scheme
        self._mtd_trigger_interval = mtd_trigger_interval
        self._mtd_trigger_std = mtd_trigger_std
        self._mtd_register_scheme = None
        self._mtd_strategies = [
                                CompleteTopologyShuffle,
                                # HostTopologyShuffle,
                                IPShuffle,
                                OSDiversity,
                                # PortShuffle,
                                # OSDiversityAssignment,
                                ServiceDiversity,
                                # UserShuffle
                                ]
        self._mtd_custom_strategies = custom_strategies
        # One instance per strategy class per scheme (= per run). Registration
        # used to construct a fresh instance every cycle, which silently reset
        # any state a mechanism carries across mutations — most visibly
        # OSDiversityAssignment's last_result/_checkpoint ladder, which is
        # *designed* to re-solve its MIP only at compromise-ratio checkpoints
        # but was re-solving on all 75 mutations of a 15 000 s run (cost audit,
        # 2026-07-29). No lineage paper touches mechanism lifecycle; the cache
        # is scoped to the scheme object so runs stay independent (SIM-05).
        self._mtd_instances = {}
        self.network = network
        self._init_mtd_scheme(scheme)
        self._security_metric_record = security_metric_record

    def _init_mtd_scheme(self, scheme):
        """
        assign an MTD scheme based on the parameter
        """
        if self._mtd_custom_strategies is None:
            self._mtd_custom_strategies = self._mtd_strategies
        if self._mtd_trigger_interval is None:
            self._mtd_trigger_interval, self._mtd_trigger_std = MTD_TRIGGER_INTERVAL[scheme]
        if scheme == 'simultaneous':
            self._mtd_register_scheme = self._register_mtd_simultaneously
        elif scheme == 'random':
            self._mtd_register_scheme = self._register_mtd_randomly
        elif scheme == 'alternative':

            self._mtd_custom_strategies = deque(self._mtd_custom_strategies)
            self._mtd_register_scheme = self._register_mtd_alternatively
        elif scheme == 'single':
            self._mtd_register_scheme = self._register_mtd_single
        elif scheme == 'mtd_ai':
            self._mtd_register_scheme = self._register_mtd_ai


    def _mtd_register(self, mtd):
        """
        register an MTD strategy to the queue
        """
        if isinstance(mtd, type):
            mtd_strategy = self._mtd_instances.get(mtd)
            if mtd_strategy is None:
                mtd_strategy = mtd(network=self.network)
                self._mtd_instances[mtd] = mtd_strategy
        else:
            mtd_strategy = mtd
        heappush(self.network.get_mtd_queue(), (mtd_strategy.get_priority(), mtd_strategy))

    def _register_mtd_simultaneously(self):
        """
        register all MTDs for simultaneous scheme
        """
        if self._security_metric_record is not None:
            for mtd in self._mtd_custom_strategies:
                self._security_metric_record.increment_metric(mtd.__name__)

        for mtd in self._mtd_custom_strategies:
            self._mtd_register(mtd=mtd)
        return self.network.get_mtd_queue()

    def _register_mtd_randomly(self):
        """
        register an MTD for random scheme
        """
        mtd = random.choice(self._mtd_custom_strategies)

        if self._security_metric_record is not None:
            self._security_metric_record.increment_metric(mtd.__name__)

        self._mtd_register(mtd=mtd)

    def _register_mtd_alternatively(self):
        """
        register an MTD for alternative scheme
        """
        mtd = self._mtd_custom_strategies.popleft()
        self._mtd_register(mtd=mtd)
        self._mtd_custom_strategies.append(mtd)

    def _register_mtd_single(self):
        self._mtd_register(mtd=self._mtd_custom_strategies)

    def _register_mtd_ai(self, mtd_technique):
        """
        register an MTD for AI scheme

        Returns the strategy that was enqueued, so a caller can name it without
        having to call this method a second time (MTDAI-08).
        """
        strategy = self._mtd_custom_strategies[mtd_technique - 1]
        if self._security_metric_record is not None:
            self._security_metric_record.increment_metric(strategy.__name__)

        self._mtd_register(mtd=strategy)
        return strategy

    def trigger_suspended_mtd(self):
        """
        trigger an MTD from suspended list
        """
        suspend_dict = self.network.get_suspended_mtd()
        mtd = suspend_dict[min(suspend_dict.keys())]
        del suspend_dict[min(suspend_dict.keys())]
        return mtd

    def trigger_mtd(self):
        """
        trigger an MTD from mtd queue
        """
        return heappop(self.network.get_mtd_queue())[1]

    def suspend_mtd(self, mtd_strategy):
        """
        put an MTD into the suspended list
        """
        self.network.get_mtd_stats().add_total_suspended()
        self.network.get_suspended_mtd()[mtd_strategy.get_priority()] = mtd_strategy

    def register_mtd(self, mtd_action=None):
        """
        call an MTD register scheme function

        The register scheme's own return value is propagated so the AI path can
        recover which strategy it enqueued; the other schemes return nothing and
        their callers ignore it.
        """
        if mtd_action is not None:
            return self._mtd_register_scheme(mtd_action)
        return self._mtd_register_scheme()

    def get_scheme(self):
        return self._scheme

    def get_mtd_trigger_interval(self):
        return self._mtd_trigger_interval

    def get_mtd_trigger_std(self):
        return self._mtd_trigger_std

    def set_mtd_strategies(self, mtd):
        self._mtd_strategies = mtd
