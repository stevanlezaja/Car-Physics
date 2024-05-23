import pygame as pg
import numpy as np

TIMESTEP = 1/30
class Engine:
    def __init__(self):
        self.torque_curve = {
            800: 300, 
            1000: 340, 
            1500: 400, 
            2000: 420, 
            2500: 440, 
            3000: 420, 
            3500: 400, 
            4000: 380, 
            4500: 350
        }
        self.power_curve = {
            800: 25, 
            1000: 35, 
            1500: 60, 
            2000: 88, 
            2500: 115, 
            3000: 126, 
            3500: 140, 
            4000: 140, 
            4500: 125
        }
        self.rpm = 800
        self.throttle_position = 0 # 0-100
        self.inertia = 0.01  # kg m²
        self.friction = 0.01  # Nm
        self.load = 0  # Nm

    def set_throttle(self, throttle_position):
        self.throttle_position = np.clip(throttle_position, 0, 100)

    def get_power(self):
        power = np.interp(self.rpm, list(self.power_curve.keys()), list(self.power_curve.values()))
        return power * (self.throttle_position / 100)  # Adjust power based on throttle position
    
    def get_torque(self):
        # Interpolate torque from the torque curve
        torque = np.interp(self.rpm, list(self.torque_curve.keys()), list(self.torque_curve.values()))
        return torque * (self.throttle_position / 100)  # Adjust torque based on throttle position
    

    def update_rpm(self, time_step=TIMESTEP):
        torque = self.get_torque()
        # Calculate friction torque
        friction_torque = self.friction * self.rpm
        # Calculate net torque (torque - friction torque - load torque)
        net_torque = torque - friction_torque - self.load
        # Simplified RPM update considering inertia
        rpm_change = net_torque / self.inertia * time_step
        self.rpm += rpm_change
        self.rpm = max(min(self.torque_curve.keys()), min(self.rpm, max(self.torque_curve.keys())))  # Limit RPM to the range of the power curve

    def update(self):
        self.set_throttle(self.throttle_position)
        self.update_rpm()
        power = self.get_power()
        torque = self.get_torque()
        return power, torque
    
def draw_rpm_bar(screen, rpm, max_rpm, position, size):
    # Calculate the height of the filled part of the bar
    bar_height = int((rpm / max_rpm) * size[1])
    bar_color = (0, 255, 0)  # Green color for the RPM bar
    
    # Draw the outline of the bar (optional)
    pg.draw.rect(screen, (255, 255, 255), (*position, *size), 2)  # White border
    
    # Draw the filled part of the bar
    filled_rect = pg.Rect(position[0], position[1] + size[1] - bar_height, size[0], bar_height)
    pg.draw.rect(screen, bar_color, filled_rect)

def draw_throttle_body(screen, throttle_position, position, size):
    # Calculate the height of the filled part of the bar
    bar_height = int((throttle_position / 100) * size[1])
    bar_color = (200, 200, 200)
    
    # Draw the outline of the bar (optional)
    pg.draw.rect(screen, (255, 255, 255), (*position, *size), 2)  # White border
    
    # Draw the filled part of the bar
    filled_rect = pg.Rect(position[0], position[1] + size[1] - bar_height, size[0], bar_height)
    pg.draw.rect(screen, bar_color, filled_rect)

def draw_net_torque(screen, net_torque, max_torque, position, size):
    # Calculate the height of the filled part of the bar
    bar_height = int((net_torque / max_torque) * size[1])
    bar_color = (200, 200, 200)
    
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
        elif keys[pg.K_UP] and engine.throttle_position == 100:
            engine.throttle_position = engine.throttle_position
        elif engine.throttle_position > 0:
            engine.throttle_position -= 10
        engine.update()
        screen.fill((0, 0, 0))  # Clear the screen
        draw_rpm_bar(screen, engine.rpm, max(engine.torque_curve.keys()), (50, 50), (50, 300))
        draw_throttle_body(screen, engine.throttle_position, (150, 50), (50, 300))
        draw_net_torque(screen, engine.get_torque(), max(engine.torque_curve.values()), (250, 50), (50, 300))
        pg.display.flip()  # Update the screen
        clock.tick(1/TIMESTEP)

    pg.quit()