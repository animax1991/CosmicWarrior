import math


class Player:
    def __init__(self):
        self.target = None
        self.nearest_distance = 0
        self.action_list = []

    def action(self, spaceship, asteroid_ls, bullet_ls, fuel, score):
        thrust = True
        bullet = False
        left = False
        right = False

        self.nearest_distance = 950

        # Find the nearest object
        for asteroid in asteroid_ls:
            distance = math.sqrt(math.pow(spaceship.x - asteroid.x, 2) + (math.pow(spaceship.y - asteroid.y, 2)))
            if distance < self.nearest_distance:
                self.nearest_distance = distance
                self.target = asteroid

        # Target angle Calculate with 4 case for each quadrant
        delta_y = self.target.y - spaceship.y
        delta_x = self.target.x - spaceship.x
        if delta_x > 0 and delta_y < 0:
            target_angle = math.degrees(abs(math.atan(delta_y / delta_x)))
        if delta_x < 0 and delta_y < 0:
            target_angle = 180 - math.degrees(abs(math.atan(delta_y / delta_x)))
        if delta_x < 0 and delta_y > 0:
            target_angle = 180 + math.degrees(abs(math.atan(delta_y / delta_x)))
        if delta_x > 0 and delta_y > 0:
            target_angle = 360 - math.degrees(abs(math.atan(delta_y / delta_x)))


        # Redirect angle to the nearest target
        if spaceship.angle < target_angle:
            left = True
            right = False
        else:
            left = False
            right = True

        # Not turn when the target is in angle range 5
        if abs(spaceship.angle - target_angle) < 5:
            right = False
            left = False

        # check if distance < 100, shoot
        if self.nearest_distance < 100:
            # check the angle again before shoot , the different below 15
            if abs(spaceship.angle - abs(target_angle)) < 15:
                bullet = True
            else:
                bullet = False

        # check if distance < 50, your spaceship is in danger, find the good angle which is < 90 and shoot !!!
        if self.nearest_distance < 50:
            if abs(spaceship.angle - abs(target_angle)) < 90:
                bullet = True

        return (thrust, left, right, bullet)


    # You can add additional methods if required
