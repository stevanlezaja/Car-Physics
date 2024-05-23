import pygame as pg

class Engine:
    def __init__(self):
        self.torque_curve = {500: 1200, 1000: 2400, 1500: 2400, 2000: 2200, 2500: 1500}
        self.power_curve = {500: 70, 1000: 150, 1500: 270, 2000: 315, 2500: 250}
        self.rpm = 500
        self.throttle_position = 0
        self.gear = 1
        self.gear_ratios = {1: 3.5, 2: 2.5, 3: 1.8, 4: 1.4, 5: 1.0}

    def update(self, load_torque=100, moment_of_inertia=1):
        self.rpm = self.calculate_rpm_change(load_torque, moment_of_inertia)

    def get_revs(self):
        return self.rpm
    
    def get_torque_from_curve(self):
        # Interpolate torque from the curve based on current RPM
        rpms = sorted(self.torque_curve.keys())
        if self.rpm <= rpms[0]:
            return self.torque_curve[rpms[0]] * (self.throttle_position / 100.0)
        elif self.rpm >= rpms[-1]:
            return self.torque_curve[rpms[-1]] * (self.throttle_position / 100.0)
        for i in range(len(rpms) - 1):
            if rpms[i] <= self.rpm < rpms[i + 1]:
                # Linear interpolation
                t1 = self.torque_curve[rpms[i]]
                t2 = self.torque_curve[rpms[i + 1]]
                rpm1 = rpms[i]
                rpm2 = rpms[i + 1]
                torque = t1 + (t2 - t1) * ((self.rpm - rpm1) / (rpm2 - rpm1))
                return torque * (self.throttle_position / 100.0)
        return 0
    
    def calculate_rpm_change(self, load_torque, moment_of_inertia):
        desired_torque = self.get_torque_from_curve()
        net_torque = desired_torque - load_torque
        K = self.gear_ratios[self.gear]
        delta_rpm = (net_torque * K) / moment_of_inertia
        new_rpm = self.rpm + delta_rpm
        new_rpm = max(500, min(2500, new_rpm))
        return new_rpm
    
def draw_rpm_bar(screen, rpm, max_rpm, position, size):
    # Calculate the height of the filled part of the bar
    bar_height = int((rpm / max_rpm) * size[1])
    bar_color = (0, 255, 0)  # Green color for the RPM bar
    
    # Draw the outline of the bar (optional)
    pg.draw.rect(screen, (255, 255, 255), (*position, *size), 2)  # White border
    
    # Draw the filled part of the bar
    filled_rect = pg.Rect(position[0], position[1] + size[1] - bar_height, size[0], bar_height)
    pg.draw.rect(screen, bar_color, filled_rect)
    
if __name__ == "__main__":
    engine = Engine()
    pg.init()
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and engine.throttle_position < 100:
            engine.throttle_position += 10
        elif engine.throttle_position > 0:
            engine.throttle_position -= 10
        engine.update()
        print(f"Current revs: {engine.get_revs()}, current throttle position: {engine.throttle_position}")
        screen.fill((0, 0, 0))  # Clear the screen
        draw_rpm_bar(screen, engine.get_revs(), 2500, (50, 50), (50, 300))
        pg.display.flip()  # Update the screen
        clock.tick(60)

    pg.quit()