import datetime


class Entity:
    def __init__(self, code):
        self.code = code
        self.days_for_filling = []
        self.current_days = 0
        self.percent = 0.0
        self.last_shipment_day = datetime.date(2020, 5, 1)
        self.next_shipment_day = '2020-05-01'
        self.days_to_next_shipment = 0
        self.intensity = 0

    def add_new_fulling(self, number_of_days):
        self.days_for_filling.append(number_of_days)
