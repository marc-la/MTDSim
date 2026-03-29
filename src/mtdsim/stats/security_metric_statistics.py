import pandas as pd
import os
import logging

class SecurityMetricStatistics:
    def __init__(self):
        self._metric_record = {
            'CompleteTopologyShuffle': 0,
            'IPShuffle':0,
            'OSDiversity':0,
            'ServiceDiversity':0
        }
        self._security_metric_time_series_record = []

    def increment_metric(self, field_name):
        if field_name in self._metric_record:
            self._metric_record[field_name] += 1
        else:
            logging.warning("%s is not a valid field in the metric record.", field_name)
    def append_security_metric_record(self, state_array, timeseries_array, time):
        # Safely retrieve values from the arrays, falling back to None if not available
        def safe_get(array, index):
            return array[index] if index < len(array) else None

        self._security_metric_time_series_record.append({
            'host_compromise_ratio': safe_get(state_array, 0),
            'total_number_of_ports': safe_get(state_array, 1),
            'attack_path_exposure': safe_get(state_array, 2),
            'overall_asr_avg': safe_get(state_array, 3),
            'roa': safe_get(state_array, 4),
            'shortest_path_variability': safe_get(state_array, 5),
            'risk': safe_get(state_array, 6),
            'mtd_frequency': safe_get(timeseries_array, 0),
            'overall_mtcc_avg': safe_get(timeseries_array, 1),
            'time_since_last_mtd': safe_get(timeseries_array, 2),
            'times': time
        })

    def get_record(self):
        if self._security_metric_time_series_record:
            df = pd.DataFrame(self._security_metric_time_series_record)
            if 'times' in df.columns:
                df = df.drop_duplicates(subset=['times'], keep='last')
            return df

        # Backward-compatible fallback for counter-style usage.
        return pd.DataFrame([self._metric_record])
