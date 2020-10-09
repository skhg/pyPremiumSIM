#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DataVolume:

    def __init__(self, tariff_total_data, consumed_data, remaining_percentage):
        self.tariff_total_data = tariff_total_data
        self.consumed_data = consumed_data
        self.remaining_percentage = remaining_percentage
