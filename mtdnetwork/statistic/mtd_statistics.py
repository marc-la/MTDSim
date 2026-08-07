import pandas as pd
import os


class MTDStatistics:
    def __init__(self):
        self._mtd_operation_record = []
        self._total_suspended = 0
        self._total_triggered = 0
        self._total_executed = 0
        self._total_attack_interrupted = 0
        self._switch_mtd_interval_at = {}
        self._switch_mtd_strategy_at = {}
        # Mutations that have begun executing but not yet finished, keyed by the
        # strategy's priority (one instance per strategy class per run, so the
        # key is unique among concurrently-running mutations). Needed because a
        # record is only appended at *finish*, and a downtime reading taken
        # mid-execution would otherwise report a quiet network while the
        # network is in fact down.
        self._in_flight = {}

    def mark_mtd_started(self, mtd_strategy, start_time):
        """Note that a mutation has begun executing.

        Bookkeeping only: no RNG is drawn and no behaviour depends on it.
        """
        self._in_flight[mtd_strategy.get_priority()] = start_time

    def append_mtd_operation_record(self, mtd_strategy, start_time, finish_time, duration):
        self._in_flight.pop(mtd_strategy.get_priority(), None)
        self._mtd_operation_record.append({
            'name': mtd_strategy.get_name(),
            'start_time': start_time,
            'finish_time': finish_time,
            'duration': duration,
            'executed_at': mtd_strategy.get_resource_type()
        })
        self._total_executed += 1

    def downtime_ratio(self, now, window):
        """Cumulative availability loss over the trailing `window` seconds.

        Tay's §4.1.2 names "Downtime / Operational Impact for Node Replacement"
        as a time-series input to the agent and nothing in the inherited code
        implements it, in any form; it is the availability half of the
        when-to-move question, and the only quantity that could make the
        do-nothing action rational. This is the project's own definition of it,
        since the paper supplies none.

        The measure is

            downtime_ratio(w) = sum over mutations overlapping [now - w, now]
                                of (overlap duration) / w

        computed over the execution records the substrate already writes, plus
        any mutation currently in flight (charged up to `now`). Two properties
        earn it over the alternatives. It composes with the resource seizure the
        substrate already models -- a suspended mutation costs nothing until it
        actually runs, and two mutations running concurrently on different
        resource layers both count -- so the concurrency structure is preserved
        rather than thrown away, which a per-mechanism weighted count would do.
        And it is bounded in [0, number of resource layers] rather than growing
        with the horizon, which matters for the conditioning of a state vector
        whose other entries are ratios.

        A per-host measure would be closer to Tay's wording ("downtime necessary
        for replacing each node") but the execution records carry no per-host
        attribution, and inventing one would be a substrate change rather than a
        derived metric.

        The per-mechanism durations this reads are `MTD_DURATION`, badged
        faithful against Zhang 2023 Table 3 in provenance.md. They are inputs
        here, never tuned.
        """
        if window <= 0:
            return 0.0
        lower = now - window
        total = 0.0
        for record in self._mtd_operation_record:
            overlap = min(record['finish_time'], now) - max(record['start_time'], lower)
            if overlap > 0:
                total += overlap
        for start_time in self._in_flight.values():
            overlap = now - max(start_time, lower)
            if overlap > 0:
                total += overlap
        return total / window

    def append_mtd_interval_record(self, timestamp, mtd_interval):
        self._switch_mtd_interval_at[timestamp] = mtd_interval

    def append_mtd_strategy_record(self, timestamp, mtd_strategy):
        self._switch_mtd_strategy_at[timestamp] = mtd_strategy

    def dict(self):
        return {
            'Total suspended MTD': self._total_suspended,
            'Total executed MTD': self._total_executed,
            'Total attack interrupted': self._total_attack_interrupted,
            'Switch MTD interval at': self._switch_mtd_interval_at,
            'Switch MTD strategy at': self._switch_mtd_strategy_at
        }

    def add_total_attack_interrupted(self):
        self._total_attack_interrupted += 1

    def add_total_suspended(self):
        self._total_suspended += 1

    def add_total_triggered(self):
        self._total_triggered += 1

    def get_record(self):
        return pd.DataFrame(self._mtd_operation_record)

    def save_record(self, sim_time, scheme):
        current_directory = os.getcwd()
        if not os.path.exists(current_directory + '/experimental_data/mtd_records'):
            os.makedirs(current_directory + '/experimental_data/mtd_records')
        pd.DataFrame(self._mtd_operation_record).to_csv('experimental_data/mtd_records/mtd_operation_record_' +
                                                        str(sim_time) + '_' + scheme + '.csv', index=False)

    def get_total_attack_interrupted(self):
        return self._total_attack_interrupted
