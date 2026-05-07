from mtdsim.sim.time_generator import exponential_variates
import logging
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)

import simpy
from mtdsim.defender.mtd_scheme import MTDScheme
from mtdsim.stats.evaluation import Evaluation
import numpy as np
import random

class MTDOperation:

    def __init__(self,security_metrics_record,env, end_event, network, attack_operation, scheme, adversary, proceed_time=0,
                 mtd_trigger_interval=None, custom_strategies=None, event_logger=None):
        """

        :param env: the parameter to facilitate simPY env framework
        :param network: the simulation network
        :param attack_operation: the attack operation
        :param scheme:alternatively, simultaneously, randomly
        :param proceed_time:the time to proceed MTD simulation
        :param custom_strategies:specific MTD priority strategy for alternative scheme or single scheme
        :param mtd_trigger_interval:the interval to trigger MTD operations
        :param adversary: the adversary
        :param event_logger: optional EventLogger sidecar for replay viz
        """
        self.env = env
        self.end_event = end_event
        self.network = network
        self.attack_operation = attack_operation
        self.adversary = adversary
        self.logging = False
        self.event_logger = event_logger

        self.security_metric_record = security_metrics_record
        self._mtd_scheme = MTDScheme(network=network, scheme=scheme, mtd_trigger_interval=mtd_trigger_interval,
                                     custom_strategies=custom_strategies, security_metric_record=self.security_metric_record)
        self._proceed_time = proceed_time

        self.application_layer_resource = simpy.Resource(self.env, 1)
        self.network_layer_resource = simpy.Resource(self.env, 1)
        self.reserve_resource = simpy.Resource(self.env, 1)

        # Tracks MTDs that have emitted mtd_deployed but not yet emitted a
        # terminal event. Used by drain_in_flight() at sim teardown so that
        # processes abandoned mid-execution (because env.run returned via
        # AnyOf) still get a matching mtd_aborted in the trace.
        self._in_flight_deployments: dict[str, "MTD"] = {}

        self.evaluation = Evaluation(self.network, self.adversary, self.security_metric_record)

    def _emit(self, event_type, **kwargs):
        if self.event_logger is not None:
            self.event_logger.emit(event_type, t=self.env.now + self._proceed_time, **kwargs)

    def _emit_alloc_state(self, action, mtd):
        """Snapshot scheduler+allocator state for post-hoc debugging.

        Lets the replay-log linter detect imbalanced trigger/release pairs
        without re-instrumenting the simulator. Cheap: a few ints + lists.
        """
        if self.event_logger is None:
            return
        unfinished = {
            rt: m.get_name() for rt, m in self.network.get_unfinished_mtd().items()
        }
        self._emit(
            'mtd_alloc_state',
            action=action,
            mtd_name=mtd.get_name() if mtd is not None else None,
            resource_type=mtd.get_resource_type() if mtd is not None else None,
            queue_depth=len(self.network.get_mtd_queue()),
            suspended=sorted(self.network.get_suspended_mtd().keys()),
            unfinished=unfinished,
            app_users=len(self.application_layer_resource.users),
            net_users=len(self.network_layer_resource.users),
            reserve_users=len(self.reserve_resource.users),
        )

    def proceed_mtd(self):
        if self.network.get_unfinished_mtd():
            for k, v in self.network.get_unfinished_mtd().items():
                self._mtd_scheme.suspend_mtd(v)
        if self._mtd_scheme.get_scheme() == 'simultaneous':
            self.env.process(self._mtd_batch_trigger_action())
            self.evaluation.get_metrics(self.env)
        elif self._mtd_scheme.get_scheme() == 'None': # Not run any mtd (No MTD)
            self.evaluation.get_metrics(self.env)
        else:
            self.env.process(self._mtd_trigger_action())
            self.evaluation.get_metrics(self.env)


    def _mtd_trigger_action(self):
        """
        trigger an MTD strategy in a given exponential time (next_mtd) in the queue
        Select Execute or suspend/discard MTD strategy
        based on the given resource occupation condition
        """

        while True:
            # terminate the simulation if the network is compromised
            if self.network.is_compromised(compromised_hosts=self.attack_operation.get_adversary().get_compromised_hosts()):
                if not self.end_event.triggered:  # Check if the event has not been triggered yet
                    self.end_event.succeed()
                # Stop scheduling new MTDs once the end_event has fired; the
                # batch variant already does this. Without the return, every
                # subsequent trigger spawns an _mtd_execute_action that bails
                # out before mtd_completed, producing orphan deploys.
                return

            # register an MTD
            if not self.network.get_mtd_queue():
                self._mtd_scheme.register_mtd()
            # trigger an MTD
            if self.network.get_suspended_mtd():
                mtd = self._mtd_scheme.trigger_suspended_mtd()
            else:
                mtd = self._mtd_scheme.trigger_mtd()

            if self.logging:
                logging.info('MTD: %s triggered %.1fs' % (mtd.get_name(), self.env.now + self._proceed_time))

            resource = self._get_mtd_resource(mtd)
            if len(resource.users) == 0:
                self._emit_alloc_state('trigger_execute', mtd)
                self.env.process(self._mtd_execute_action(env=self.env, mtd=mtd))
            else:
                # suspend if suspended dict doesn't have the same MTD.
                # else discard
                if mtd.get_priority() not in self.network.get_suspended_mtd():
                    self._mtd_scheme.suspend_mtd(mtd)
                    self._emit_alloc_state('suspend', mtd)

                    if self.logging:
                        logging.info('MTD: %s suspended at %.1fs due to resource occupation' %
                                 (mtd.get_name(), self.env.now + self._proceed_time))

            # exponential time interval for triggering MTD operations
            yield self.env.timeout(exponential_variates(self._mtd_scheme.get_mtd_trigger_interval(),
                                                        self._mtd_scheme.get_mtd_trigger_std()))

    def _mtd_batch_trigger_action(self):
        """
        trigger all MTDs at a time with a fixed priority
        """
        while True:
            # terminate the simulation if the network is compromised
            if self.network.is_compromised(
                    compromised_hosts=self.attack_operation.get_adversary().get_compromised_hosts()):
                return
            

            suspension_queue = self.network.get_suspended_mtd()
            if suspension_queue:
                # triggering the suspended MTDs by priority
                suspended_mtd_priorities = sorted(suspension_queue.keys())
                for priority in suspended_mtd_priorities:
                    resource = self._get_mtd_resource(mtd=suspension_queue[priority])
                    if len(resource.users) == 0:
                        mtd = self._mtd_scheme.trigger_suspended_mtd()
                        if self.logging:
                            logging.info('MTD: %s triggered %.1fs' % (mtd.get_name(), self.env.now + self._proceed_time))
                        yield self.env.process(self._mtd_execute_action(env=self.env, mtd=mtd))
            else:
                # register and trigger all MTDs
                if not self.network.get_suspended_mtd() and not self.network.get_mtd_queue():
                    self._mtd_scheme.register_mtd()
                while self.network.get_mtd_queue():
                    mtd = self._mtd_scheme.trigger_mtd()
                    if self.logging:
                        logging.info('MTD: %s triggered %.1fs' % (mtd.get_name(), self.env.now + self._proceed_time))
                    resource = self._get_mtd_resource(mtd=mtd)
                    if len(resource.users) == 0:
                        # execute MTD
                        self._emit_alloc_state('trigger_execute', mtd)
                        self.env.process(self._mtd_execute_action(env=self.env, mtd=mtd))
                    else:
                        # suspend MTD if resource is occupied
                        self._mtd_scheme.suspend_mtd(mtd_strategy=mtd)
                        self._emit_alloc_state('suspend', mtd)
                        if self.logging:
                            logging.info('MTD: %s suspended at %.1fs due to resource occupation' %
                                    (mtd.get_name(), self.env.now + self._proceed_time))

            # exponential distribution for triggering MTD operations
            yield self.env.timeout(exponential_variates(self._mtd_scheme.get_mtd_trigger_interval(),
                                                        self._mtd_scheme.get_mtd_trigger_std()))

    # Multiple of the configured execution mean beyond which we consider an
    # MTD "stuck" and abort with a loud assertion. SimPy timeouts are exact,
    # so the only way to exceed this is a synchronous mtd_operation() that
    # blocks on something CPU-bound or a re-yield inside it. Fail loud
    # rather than silently producing orphan deploys.
    _MTD_EXECUTION_BUDGET_MULTIPLIER = 5.0

    def _mtd_execute_action(self, env, mtd):
        """
        Action for executing MTD
        """
        # deploy mtd
        self.network.set_unfinished_mtd(mtd)
        request = self._get_mtd_resource(mtd).request()
        start_time = None
        try:
            yield request
            start_time = env.now + self._proceed_time

            if self.logging:
                logging.info('MTD: %s deployed in the network at %.1fs.' % (mtd.get_name(), start_time))

            self._emit('mtd_deployed', mtd_name=mtd.get_name(), resource_type=mtd.get_resource_type())
            self._in_flight_deployments[mtd.get_resource_type()] = mtd

            yield env.timeout(exponential_variates(mtd.get_execution_time_mean(),
                                                   mtd.get_execution_time_std()))

            # if network is already compromised while executing mtd:
            if self.network.is_compromised(compromised_hosts=self.attack_operation.get_adversary().get_compromised_hosts()):
                # Emit a terminal event so the replay-log linter still sees a
                # matching pair for every mtd_deployed.
                self._emit('mtd_aborted', mtd_name=mtd.get_name(),
                           resource_type=mtd.get_resource_type(),
                           reason='network_compromised')
                self._in_flight_deployments.pop(mtd.get_resource_type(), None)
                return

            # execute mtd
            mtd.mtd_operation(self.attack_operation.get_adversary())

            finish_time = env.now + self._proceed_time
            duration = finish_time - start_time

            budget = mtd.get_execution_time_mean() * self._MTD_EXECUTION_BUDGET_MULTIPLIER
            assert duration <= budget, (
                f"MTD {mtd.get_name()} ran {duration:.1f}s (>{budget:.1f}s budget); "
                f"likely a stuck synchronous mtd_operation()"
            )

            if self.logging:
                logging.info('MTD: %s finished in %.1fs at %.1fs.' % (mtd.get_name(), duration, finish_time))

            self._emit('mtd_completed', mtd_name=mtd.get_name(), resource_type=mtd.get_resource_type(), duration=duration)
            self._in_flight_deployments.pop(mtd.get_resource_type(), None)

            # append execution records
            self.network.get_mtd_stats().append_mtd_operation_record(mtd, start_time, finish_time, duration)
            # interrupt adversary
            self._interrupt_adversary(env, mtd)
        finally:
            # always release the resource and clear the unfinished-mtd marker
            if request in self._get_mtd_resource(mtd).users:
                self._get_mtd_resource(mtd).release(request)
            self.network.get_unfinished_mtd().pop(mtd.get_resource_type(), None)
            self._emit_alloc_state('release', mtd)

    def _get_mtd_resource(self, mtd):
        """Get the resource to be occupied by the mtd"""
        if mtd.get_resource_type() == 'network':
            return self.network_layer_resource
        elif mtd.get_resource_type() == 'application':
            return self.application_layer_resource
        return self.reserve_resource

    def _interrupt_adversary(self, env, mtd):
        """
        interrupt the attack process of the adversary
        """
        attack_process = self.attack_operation.get_attack_process()
        if attack_process is not None and attack_process.is_alive:
            if mtd.get_resource_type() == 'network':
                self.attack_operation.set_interrupted_mtd(mtd)
                self.attack_operation.get_attack_process().interrupt()
                
                if self.logging:
                    logging.info(
                    'MTD: Interrupted %s at %.1fs!' % (self.attack_operation.get_adversary().get_curr_process(),
                                                       env.now + self._proceed_time))
                self.network.get_mtd_stats().add_total_attack_interrupted()
            elif mtd.get_resource_type() == 'application' and \
                    self.attack_operation.get_adversary().get_curr_process() not in [
                'SCAN_HOST',
                'ENUM_HOST',
                'SCAN_NEIGHBOR']:
                self.attack_operation.set_interrupted_mtd(mtd)
                self.attack_operation.get_attack_process().interrupt()

                if self.logging:
                    logging.info(
                    'MTD: Interrupted %s at %.1fs!' % (self.attack_operation.get_adversary().get_curr_process(),
                                                       env.now + self._proceed_time))
                    
                self.network.get_mtd_stats().add_total_attack_interrupted()

    def drain_in_flight(self, reason: str = "sim_terminated") -> int:
        """Emit ``mtd_aborted`` for every still-in-flight MTD deployment.

        Called from the runner after ``env.run`` returns. When the sim ends
        via the AnyOf terminator, processes parked between ``mtd_deployed``
        and their normal close event are abandoned mid-stride — their
        try/finally never runs, so without this drain the trace would have
        orphan deploys. Returns the number of events emitted (useful for
        regression assertions).
        """
        drained = list(self._in_flight_deployments.items())
        for resource_type, mtd in drained:
            self._emit('mtd_aborted', mtd_name=mtd.get_name(),
                       resource_type=resource_type, reason=reason)
        self._in_flight_deployments.clear()
        return len(drained)

    def get_proceed_time(self):
        return self._proceed_time

    def get_application_resource(self):
        return self.application_layer_resource

    def get_network_resource(self):
        return self.network_layer_resource

    def get_reserve_resource(self):
        return self.reserve_resource

    def get_mtd_scheme(self):
        return self._mtd_scheme
