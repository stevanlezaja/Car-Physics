import pygame as pg

from const import *
from engine import Engine

class Car:
    def __init__(self):
        # Car properties
        self.length = 60
        self.width = 30
        self.color = (0, 255, 0)
        self.mass = 1500 # car mass (kg)
        self.engine = Engine()
        self.drag_coefficient = 0.3
        self.frontal_area = 2.2  # m²
        self.wheel_radius = 0.3  # m
        self.rolling_resistance_coefficient = 0.015
        self.moment_of_inertia = 1  # Placeholder value for the moment of inertia
        # # Car position
        # self.x = 300
        # self.y = 300
        # self.angle = 0
        # Car dynamics
        # self.vx = 0
        # self.vy = 0
        # self.ax = 0
        # self.ay = 0
        self.speed = 0
        self.acceleration = 0
        self.force = 0
        # self.wheel_angle = 0

    def get_speed(self):
        return pg.math.Vector2(self.vx, self.vy).length()
    
    def get_revs(self):
        return self.engine.get_revs()
    
    def calculate_load_torque(self):
        air_density = 1.225  # kg/m³ at sea level
        g = 9.81  # m/s²



    def update(self, keys):
        if keys[pg.K_UP] and self.engine.throttle_position < 100:
            self.engine.throttle_position += 10
        elif self.engine.throttle_position > 0:
            self.engine.throttle_position -= 10
        self.engine.update(load_torque=self.calculate_load_torque(), moment_of_inertia=self.moment_of_inertia)
        self.physics()

    def calculate_load_torque(self):
        air_density = 1.225  # kg/m³ at sea level
        g = 9.81  # m/s²

        # Aerodynamic drag
        F_aero = 0.5 * air_density * self.drag_coefficient * self.frontal_area * (pg.math.Vector2(self.vx, self.vy).length() ** 2)
        T_aero = F_aero * self.wheel_radius

        # Rolling resistance
        F_rolling = self.rolling_resistance_coefficient * self.mass * g
        T_rolling = F_rolling * self.wheel_radius

        # Inertia
        F_inertia = self.mass * pg.math.Vector2(self.ax, self.ay).length()
        T_inertia = F_inertia * self.wheel_radius

        # Gradient resistance (assuming no incline for simplicity)
        T_gradient = 0

        T_load = T_aero + T_rolling + T_inertia + T_gradient
        return T_load

    def physics(self):
        # Calculate drag forces
        air_density = 1.225  # kg/m³ at sea level
        g = 9.81  # m/s²

        # Aerodynamic drag
        F_aero = 0.5 * air_density * self.drag_coefficient * self.frontal_area * (self.vx**2 + self.vy**2)

        # Rolling resistance
        F_rolling = self.rolling_resistance_coefficient * self.mass * g

        # Total resisting force
        resisting_force = F_aero + F_rolling

        # Calculate acceleration
        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            resisting_force_direction = pg.math.Vector2(-self.vx, -self.vy).normalize()
        else:
            resisting_force_direction = pg.math.Vector2(0, 0)

        self.force = self.engine.get_torque_from_curve() / self.wheel_radius

        net_force_x = self.force * pg.math.Vector2(pg.math.Vector2(1, 0).rotate(self.angle)).x - resisting_force * resisting_force_direction.x
        net_force_y = self.force * pg.math.Vector2(pg.math.Vector2(1, 0).rotate(self.angle)).y - resisting_force * resisting_force_direction.y

        self.ax = net_force_x / self.mass
        self.ay = net_force_y / self.mass

        # Update velocity
        self.vx += self.ax
        self.vy += self.ay

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Apply friction to slow down car gradually
        if abs(self.vx) > 0.01 or abs(self.vy) > 0.01:
            friction_force_direction = pg.math.Vector2(-self.vx, -self.vy).normalize()
            friction_force = 10 * g  # Adjust the friction coefficient as needed
            self.vx += friction_force * friction_force_direction.x / self.mass
            self.vy += friction_force * friction_force_direction.y / self.mass
        else:
            self.vx = 0
            self.vy = 0
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.length, self.width))


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
        
        keys = pg.key.get_pressed()
        car.update(keys)
        
        screen.fill((0, 0, 0))
        
        # Render the text
        text_surface = font.render(f'{car.get_speed()}', True, WHITE)

        # Blit the text to the screen
        screen.blit(text_surface, (400, 400))  # Adjust (20, 20) to change text position

        draw_rpm_bar(screen, car.get_revs(), 2500, (10, 10), (20, 100))
        pg.display.flip()
        clock.tick(60)

    pg.quit()