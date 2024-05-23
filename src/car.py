import pygame as pg

from const import *
from engine import Engine

AIR_DENSITY = 1.225  # kg/m³
TIMESTEP = 1/30


class Car:
    def __init__(self):
        # Car parameters
        self.mass = 1500 # car mass (kg)
        self.engine = Engine()
        self.drag_coefficient = 0.3
        self.frontal_area = 2.2  # m²
        self.wheel_radius = 0.3  # m
        self.rolling_resistance_coefficient = 0.015
        self.moment_of_inertia = 1  # Placeholder value for the moment of inertia
        # Car dynamics
        self.speed = 0
        self.acceleration = 0
        self.force = 0

    def calculate_engine_load(self):
        drag_force = 0.5 * self.drag_coefficient * self.frontal_area * AIR_DENSITY * (self.speed ** 2)
        # Calculate rolling resistance
        rolling_resistance = self.rolling_resistance_coefficient * self.mass * 9.81  # N
        # Sum of forces
        total_force = drag_force + rolling_resistance
        # Convert force to load (torque) using the wheel radius (assuming wheel radius of 0.3 m)
        self.engine.load = total_force * self.wheel_radius
        return self.engine.load


    def update(self, keys):
        if keys[pg.K_UP] and self.engine.throttle_position < 100:
            self.engine.throttle_position += 10
        elif self.engine.throttle_position > 0:
            self.engine.throttle_position -= 10
        self.engine.update()

    def physics(self):
        net_torque = self.engine.get_torque() - self.calculate_engine_load()
        self.force = net_torque / self.wheel_radius

        self.acceleration = self.force / self.mass

        # Update velocity
        self.speed += self.acceleration * TIMESTEP  # 1/60 is the time step in seconds


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
    
if __name__ == "__main__":
    car = Car()
    pg.init()
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    running = True
    font = pg.font.Font(None, 36)  # None uses the default font, size 36
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                car.engine.transmission.shift_up()
                print(car.engine.transmission.current_gear)
            elif event.type == pg.KEYDOWN and event.key == pg.K_z:
                car.engine.transmission.shift_down()
                print(car.engine.transmission.current_gear)

        keys = pg.key.get_pressed()
        car.update(keys)
        car.physics()
        
        screen.fill((0, 0, 0))
        
        # Render the text
        text_speed = font.render(f'Speed: {int(car.speed)}', True, WHITE)
        text_load = font.render(f'Load: {int(car.engine.load)}', True, WHITE)
        text_torque = font.render(f'Torque: {int(car.engine.get_torque())}', True, WHITE)
        #print(car.calculate_load_torque())

        # Blit the text to the screen
        screen.blit(text_speed, (400, 400))  # Adjust (20, 20) to change text position
        screen.blit(text_load, (400, 200))  # Adjust (20, 20) to change text position
        screen.blit(text_torque, (400, 300))  # Adjust (20, 20) to change text position

        draw_rpm_bar(screen, car.engine.rpm, max(car.engine.power_curve.keys()), (10, 10), (20, 100))
        draw_throttle_body(screen, car.engine.throttle_position, (40, 10), (20, 100))
        pg.display.flip()
        clock.tick(1/TIMESTEP)

    pg.quit()