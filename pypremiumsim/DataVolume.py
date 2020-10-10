#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DataVolume:

    def __init__(self, tariff_total_data_gb, consumed_data_gb, used_percentage):
        self.tariff_total_data_gb = tariff_total_data_gb
        self.consumed_data_gb = consumed_data_gb
        self.used_percentage = used_percentage
