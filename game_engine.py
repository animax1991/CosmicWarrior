import config
from space_object import SpaceObject


class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.asteroid_ls = []
        self.bullet_ls = []
        self.upcoming_asteroid_ls = []
        self.starting_fuel = 0

        self.width = 0
        self.height = 0
        self.score = 0
        self.spaceship = None
        self.fuel = 0
        self.asteroids_count = 0
        self.bullets_count = 0
        self.upcoming_asteroids_count = 0

        # Warning flag
        self.threshold1 = True
        self.threshold2 = True
        self.threshold3 = True

        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    # Slit string to space_object as the format: <x>,<y>,<angle>,<ID>
    def split_data_format(self, string_line, object_type, line_number):
        s_data = string_line.split(' ')[1].split(',')
        if len(s_data) == 4:
            x = s_data[0]
            y = s_data[1]
            radius = config.radius[object_type]
            angle = s_data[2]
            object_type = object_type
            id = s_data[3]
            space_object = SpaceObject(x, y, radius, radius, angle, object_type, id)
            return space_object
        else:
            raise ValueError('Error: invalid data type in line ' + str(line_number))

    def import_state(self, game_state_filename):
        line_number = 0
        with open(game_state_filename) as file2:
            file2.seek(0)  # Ensure you're at the start of the file..
            first_char = file2.read(1)  # Get the first character
            if not first_char:
                raise ValueError("Error: game state incomplete")
                exit(0)
            for line in file2.readlines():
                line = line.strip()
                line_number += 1
                if line == '':
                    raise ValueError("Error: game state incomplete")
                    break
                if line_number == 1:
                    if line.split(' ')[0] == 'width':
                        self.width = int(line.split(' ')[1])
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number == 2:
                    if line.split(' ')[0] == 'height':
                        self.height = int(line.split(' ')[1])
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number == 3:
                    if line.split(' ')[0] == 'score':
                        self.score = int(line.split(' ')[1])
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number == 4:
                    if line.split(' ')[0] == 'spaceship':
                        self.spaceship = self.split_data_format(line, 'spaceship', line_number)
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number == 5:
                    if line.split(' ')[0] == 'fuel':
                        self.fuel = int(line.split(' ')[1])
                        self.starting_fuel = int(line.split(' ')[1])
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number == 6:
                    if line.split(' ')[0] == 'asteroids_count':
                        self.asteroids_count = int(line.split(' ')[1])
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number > 6 and line_number <= 6 + int(self.asteroids_count):
                    if line.split(' ')[0] == 'asteroid_large':
                        self.asteroid_ls.append(self.split_data_format(line, 'asteroid_large', line_number))
                        continue
                    elif line.split(' ')[0] == 'asteroid_small':
                        self.asteroid_ls.append(self.split_data_format(line, 'asteroid_small', line_number))
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number == 7 + int(self.asteroids_count):
                    if line.split(' ')[0] == 'bullets_count':
                        self.bullets_count = line.split(' ')[1]
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number > 7 + int(self.asteroids_count) and line_number <= 7 + int(self.asteroids_count) + int(
                        self.bullets_count):
                    if line.split(' ')[0] == 'bullet':
                        self.bullet_ls.append(self.split_data_format(line, 'bullet', line_number))
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number == 8 + int(self.asteroids_count) + int(self.bullets_count):
                    if line.split(' ')[0] == 'upcoming_asteroids_count':
                        self.upcoming_asteroids_count = line.split(' ')[1]
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                if line_number > 8 + int(self.asteroids_count) + int(self.bullets_count) and line_number <= 8 + int(
                        self.asteroids_count) + int(self.bullets_count) + int(self.upcoming_asteroids_count):
                    if line.split(' ')[0] == 'upcoming_asteroid_large':
                        self.upcoming_asteroid_ls.append(self.split_data_format(line, 'asteroid_large', line_number))
                        continue
                    elif line.split(' ')[0] == 'upcoming_asteroid_small':
                        self.upcoming_asteroid_ls.append(self.split_data_format(line, 'asteroid_small', line_number))
                        continue
                    else:
                        raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))
                elif line_number > 8 + int(self.asteroids_count) + int(self.bullets_count) + int(
                        self.upcoming_asteroids_count):
                    raise ValueError("Error: game state incomplete")
                else:
                    raise ValueError('Error: unexpected key: ' + str(line.split(' ')[0]) + ' in line ' + str(line_number))

    def export_state(self, game_state_filename):
        f = open(game_state_filename, "w")
        f.write("width " + str(self.width) + '\n')
        f.write("height " + str(self.height) + '\n')
        f.write("score " + str(self.score) + '\n')
        f.write(str(self.spaceship) + '\n')
        f.write("fuel " + str(self.fuel) + '\n')
        f.write("asteroids_count " + str(len(self.asteroid_ls)) + '\n')
        for asteroid in self.asteroid_ls:
            if asteroid.obj_type == 'asteroid_large':
                f.write(str(asteroid) + '\n')
            elif asteroid.obj_type == 'asteroid_small':
                f.write(str(asteroid) + '\n')
        f.write("bullets_count " + str(len(self.bullet_ls)) + '\n')
        for bullet in self.bullet_ls:
            f.write(str(bullet) + '\n')
        f.write("upcoming_asteroids_count " + str(len(self.upcoming_asteroid_ls)) + '\n')
        for asteroid in self.upcoming_asteroid_ls:
            if asteroid.obj_type == 'asteroid_large':
                f.write('upcoming_' + str(asteroid) + '\n')
            elif asteroid.obj_type == 'asteroid_small':
                f.write('upcoming_' + str(asteroid) + '\n')
        f.close()


    def run_game(self):
        bullet_id = 0
        while True:
            # 1. Receive player input
            current_player_action = self.player.action(self.spaceship, self.asteroid_ls, self.bullet_ls, self.fuel,
                                                        self.score)

            # 2. Process game logic
            # Rotate handle - High priority
            if current_player_action[1] == True and current_player_action[2] == True:
                pass
            elif current_player_action[1] == False and current_player_action[2] == False:
                pass
            elif current_player_action[1] == True :
                self.spaceship.turn_left()
            elif current_player_action[2] == True:
                self.spaceship.turn_right()

            # Thruster handle
            if current_player_action[0] == True:
                self.spaceship.move_forward()

            # Bullet handle
            if current_player_action[3] == True:
                if self.fuel >= config.shoot_fuel_threshold:
                    bullet = SpaceObject(self.spaceship.x, self.spaceship.y, config.radius['bullet'],
                                         config.radius['bullet'], self.spaceship.angle, 'bullet', bullet_id)
                    self.bullet_ls.append(bullet)
                    self.fuel -= config.bullet_fuel_consumption
                    bullet_id += 1
                else:
                    print('Cannot shoot due to low fuel')

            self.fuel -= config.spaceship_fuel_consumption
            # Warning Fuel Flag
            if self.fuel / self.starting_fuel <= config.fuel_warning_threshold[0] / 100 and self.threshold1 == True:
                print(str(config.fuel_warning_threshold[0]) + '% fuel warning: ' + str(self.fuel) + ' remaining')
                self.threshold1 = False
            if self.fuel / self.starting_fuel <= config.fuel_warning_threshold[1] / 100 and self.threshold2 == True:
                print(str(config.fuel_warning_threshold[1]) + '% fuel warning: ' + str(self.fuel) + ' remaining')
                self.threshold2 = False
            if self.fuel / self.starting_fuel <= config.fuel_warning_threshold[2] / 100 and self.threshold3 == True:
                print(str(config.fuel_warning_threshold[2]) + '% fuel warning: ' + str(self.fuel) + ' remaining')
                self.threshold3 = False

            # Asteroid list handle
            for asteroid in self.asteroid_ls:
                asteroid.move_forward()

            # Bullet list handle
            # print(self.bullet_ls)
            # print(str(len(self.bullet_ls)))
            for bullet in self.bullet_ls[:]:
                # Bullet live n Frames
                if bullet.life < config.bullet_move_count:
                    bullet.move_forward()
                    bullet.life += 1
                else:
                    self.bullet_ls.remove(bullet)
                    continue

            # Collide handle
            # Bullet collide Asteroid
            # Prioritize Bullet vs Asteroid first, if collide, remove both of them then we go next check step
            for asteroid in self.asteroid_ls:
                for bullet in self.bullet_ls:
                    if bullet.collide_with(asteroid):
                        if asteroid.obj_type == 'asteroid_small':
                            self.score += int(config.shoot_small_ast_score)
                        if asteroid.obj_type == 'asteroid_large':
                            self.score += int(config.shoot_large_ast_score)
                        # Remove both
                        self.bullet_ls.remove(bullet)
                        self.asteroid_ls.remove(asteroid)
                        # Check if upcomming asteroid list have item
                        if len(self.upcoming_asteroid_ls) > 0:
                            upcoming_asteroid = self.upcoming_asteroid_ls.pop(0)
                            self.asteroid_ls.append(upcoming_asteroid)
                            print('Score: ' + str(self.score) + ' \t [Bullet ' + str(bullet.id) +
                                  ' has shot asteroid ' + str(asteroid.id) + ']')
                            print('Added asteroid ' + str(upcoming_asteroid.id))
                        else:
                            # Score: <score> \t [Bullet <id> has shot asteroid
                            print('Score: ' + str(self.score) + ' \t [Bullet ' + str(bullet.id) +
                                  ' has shot asteroid ' + str(asteroid.id) + ']')
                            print('Error: no more asteroids available')
                            break
                        break

            # Asteroid collide Spaceship
            # This is the next check step, After remove Asteroid and bullet if they collided
            for asteroid in self.asteroid_ls:
                if self.spaceship.collide_with(asteroid):
                    self.score += config.collide_score
                    self.asteroid_ls.remove(asteroid)

                    # Check if upcomming asteroid list have item
                    if len(self.upcoming_asteroid_ls) > 0:
                        upcoming_asteroid = self.upcoming_asteroid_ls.pop(0)
                        self.asteroid_ls.append(upcoming_asteroid)
                        print('Added asteroid ' + str(upcoming_asteroid.id))
                    else:
                        print(
                            'Score: ' + str(self.score) + ' \t [Spaceship collided with asteroid ' + str(
                                asteroid.id) + ']')
                        print('Error: no more asteroids available')
                        break

            # 3. Draw the game state on screen using the GUI class
            self.GUI.update_frame(self.spaceship, self.asteroid_ls, self.bullet_ls, self.score, self.fuel)

            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            if self.fuel <= 0:
                self.export_state('output_data.out')
                self.GUI.finish(self.score)
                break
            # - no more asteroids are available
            if len(self.asteroid_ls) <= 0:
                self.export_state('output_data.out')
                self.GUI.finish(self.score)
                break
            if self.score < 0:
                self.export_state('output_data.out')
                self.GUI.finish(self.score)
                break

        # Display final score
        self.GUI.finish(self.score)
