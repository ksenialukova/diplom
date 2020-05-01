class Entity:
    def __init__(self, code, x_coord, y_coord):
        self.code = code
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.days_for_fulling = []
        self.current_days = 0
        self.percent = 0.0

    def add_new_fulling(self, number_of_days):
        self.days_for_fulling.append(number_of_days)
