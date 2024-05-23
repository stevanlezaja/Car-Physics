class Transmission:
    def __init__(self):
        self.gear_ratios = {0: None, 1: 3.5, 2: 2.5, 3: 1.7, 4: 1.3, 5: 1.0, 6: 0.8}
        self.current_gear = 0

    def shift_up(self):
        if self.current_gear < len(self.gear_ratios) - 1:
            self.current_gear += 1

    def shift_down(self):
        if self.current_gear > 0:
            self.current_gear -= 1

    def transfer_torque(self, torque):
        if self.current_gear == 0:
            return 0
        return torque * self.gear_ratios[self.current_gear]
    
    def transfer_power(self, power):
        return power * self.gear_ratios[self.current_gear] if self.current_gear != 0 else 0
    
    def transfer_load(self, load):
        return load / self.gear_ratios[self.current_gear] if self.current_gear != 0 else 0