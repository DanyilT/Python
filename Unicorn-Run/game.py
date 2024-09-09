import os
import json
import random
import pygame
from pygame.constants import QUIT, MOUSEBUTTONDOWN, K_RETURN, KEYDOWN, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_s, K_w, K_d, K_a

# Start the Game
class MainMenu:
    def __init__(self, display, paused=False):
        self.display = display
        self.WIDTH, self.HEIGHT = display.get_width(), display.get_height()
        self.sorted_scores = sorted(GameData().load_player_data()['players'].values(), key=lambda x: x['score'], reverse=True)[:5]
        self.player_name = ''
        self.paused = paused
        self.show()

    # Display main menu
    def show(self):
        self.ui()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = event.w, event.h
                    self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                    self.show()
                if event.type == MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        if self.paused:
                            waiting = False
                        else:
                            Game(self.display, self.player_name)
                    if self.exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if self.paused:
                            waiting = False
                        else:
                            Game(self.display, self.player_name)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        self.player_name += event.unicode

                    # Update input field
                    self.display_input_field()

            pygame.display.flip()

    # Display user interface (labels, buttons, etc.)
    def ui(self):
        # Fill background
        self.display.fill((210, 200, 210))

        # Display tip label
        tip_font = pygame.font.SysFont('Arial', 24)
        tip_text = tip_font.render('Press Play to Start', True, (0, 0, 0))
        tip_text_pos = (self.WIDTH//2 - tip_text.get_width()//2, self.HEIGHT//2 - 100)
        self.display.blit(tip_text, tip_text_pos)

        # Display title label
        title_font = pygame.font.SysFont('Arial', 48)
        title_text = title_font.render('Welcome to the Game', True, (48, 25, 52))
        title_text_pos = (self.WIDTH//2 - title_text.get_width()//2, tip_text_pos[1] - title_text.get_height() - 10)
        self.display.blit(title_text, title_text_pos)

        # Display play button
        self.play_button = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('Play.png', 'images/icons')), (96, 96))
        self.play_button_rect = self.play_button.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        self.display.blit(self.play_button, self.play_button_rect)

        # Display exit button
        self.exit_button = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('Exit.png', 'images/icons')), (48, 48))
        self.exit_button_rect = self.exit_button.get_rect(topleft=(20, 20))
        self.display.blit(self.exit_button, self.exit_button_rect)

        # Label for input field
        input_label_font = pygame.font.SysFont('Arial', 18)
        input_label = input_label_font.render('Who are You?', True, (0, 0, 0))
        input_label_pos = (self.WIDTH - 220, self.HEIGHT - 80)
        self.display.blit(input_label, input_label_pos)
        self.display_input_field()

        # Display top 5 scores
        self.display_top_scores()

    # Display input field
    def display_input_field(self):
        input_font = pygame.font.SysFont('Arial', 21)
        input_rect = pygame.Rect(self.WIDTH - 220, self.HEIGHT - 50, 200, 30)
        pygame.draw.rect(self.display, (133, 96, 136), input_rect)
        input_text = input_font.render(self.player_name, True, (0, 0, 0))
        self.display.blit(input_text, (input_rect.x + 10, input_rect.y + 1))

    # Display top 5 scores
    def display_top_scores(self):
        for i, player in enumerate(self.sorted_scores):
            score_font = pygame.font.SysFont('Arial', 16)
            score_text = score_font.render(f"{player['name']}: {player['score']}", True, (0, 0, 0))
            score_text_pos = (self.WIDTH - score_text.get_width() - 20, 20 + i * 20)
            self.display.blit(score_text, score_text_pos)
            if player['score'] == self.sorted_scores[0]['score']:
                star_icon = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('player.png', 'images')), (24, 24))
                self.display.blit(star_icon, (score_text_pos[0] - 30, score_text_pos[1] - 5))

# Play the Game
class Game:
    def __init__(self, display,  player_name):
        self.display = display
        self.WIDTH, self.HEIGHT = display.get_width(), display.get_height()
        self.FPS = pygame.time.Clock()

        self.player_name = player_name if player_name else 'Guest'

        self.score = 0 if player_name != 'qwerty' else 999999999

        self.sorted_scores = sorted(GameData().load_player_data()['players'].values(), key=lambda x: x['score'], reverse=True)[:5]

        self.background = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('background.png', 'images')), (self.WIDTH, self.HEIGHT))
        self.background_1 = 0
        self.background_2 = self.background.get_width()
        self.background_move = 3

        self.player, self.player_rect, self.player_move = self.create_player()

        self.CREATE_ENEMY = pygame.USEREVENT + 1
        self.CREATE_BONUS = pygame.USEREVENT + 2

        pygame.time.set_timer(self.CREATE_ENEMY, max(600, int(600 * (self.WIDTH / 1200))))
        pygame.time.set_timer(self.CREATE_BONUS, max(1800, int(1800 * (self.WIDTH / 1200))))

        self.enemies = []
        self.bonuses = []

        self.run()

    # Main game loop
    def run(self):
        playing = True
        while playing:
            self.FPS.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    playing = False
                if event.type == KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.pause()
                if event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = event.w, event.h
                    self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                    self.background = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('background.png', 'images')), (self.WIDTH, self.HEIGHT))
                    self.background_1 = 0
                    self.background_2 = self.background.get_width()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_rect.collidepoint(event.pos):
                        self.pause()
                if event.type == self.CREATE_ENEMY:
                    self.enemies.append(self.create_enemy())
                if event.type == self.CREATE_BONUS:
                    self.bonuses.append(self.create_bonus())

            self.background_1 -= self.background_move
            self.background_2 -= self.background_move
            if self.background_1 < -self.background.get_width():
                self.background_1 = self.background.get_width()
            if self.background_2 < -self.background.get_width():
                self.background_2 = self.background.get_width()

            self.display.blit(self.background, (self.background_1, 0))
            self.display.blit(self.background, (self.background_2, 0))

            # Display user interface
            self.ui()

            # Player moves
            self.display.blit(self.player, self.update_player(self.player_rect))

            # Update enemies and bonuses
            for enemy in self.enemies:
                enemy[1] = enemy[1].move(enemy[2])
                self.display.blit(enemy[0], enemy[1])
                if self.player_rect.colliderect(enemy[1]):
                    playing = False
                    self.save_score()
                    self.game_over()
            for bonus in self.bonuses:
                bonus[1] = bonus[1].move(bonus[2])
                self.display.blit(bonus[0], bonus[1])
                if self.player_rect.colliderect(bonus[1]):
                    self.bonuses.pop(self.bonuses.index(bonus))
                    self.score += 1

            # Destroy enemies and bonuses that are out of the screen
            for enemy in self.enemies:
                if enemy[1].left < 0:
                    self.enemies.pop(self.enemies.index(enemy))
            for bonus in self.bonuses:
                if bonus[1].bottom > self.HEIGHT:
                    self.bonuses.pop(self.bonuses.index(bonus))

            # Update display
            pygame.display.flip()

        self.save_score()

    # Display user interface (labels, buttons, etc.)
    def ui(self):
        # Display pause button
        self.pause_button = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('Pause.png', 'images/icons')), (48, 48))
        self.pause_button_rect = self.pause_button.get_rect(topright=(self.WIDTH - 20, 20))
        self.display.blit(self.pause_button, self.pause_button_rect)

        # Show score
        score_font = pygame.font.SysFont('Arial', 24)
        score_text = score_font.render(str(self.score), True, (0, 0, 0))
        score_text_pos = (20, 20)
        self.display.blit(score_text, score_text_pos)

        # Show player name (bottom right)
        player_name_font = pygame.font.SysFont('Arial', 18)
        player_name_text = player_name_font.render(self.player_name, True, (0, 0, 0))
        player_name_text_pos = (self.WIDTH - player_name_text.get_width() - 20, self.HEIGHT - player_name_text.get_height() - 20)
        self.display.blit(player_name_text, player_name_text_pos)

    # Update player position
    def update_player(self, player_rect):
        # wasd or arrow keys
        keys = pygame.key.get_pressed()
        if (keys[K_UP] or keys[K_w]) and player_rect.top > 0:
            player_rect.move_ip(self.player_move[0][0], -self.player_move[0][1])
        if (keys[K_LEFT] or keys[K_a]) and player_rect.left > 0:
            player_rect.move_ip(-self.player_move[1][0], self.player_move[1][1])
        if (keys[K_DOWN] or keys[K_s]) and player_rect.bottom < self.HEIGHT:
            player_rect.move_ip(*self.player_move[0])
        if (keys[K_RIGHT] or keys[K_d]) and player_rect.right < self.WIDTH:
            player_rect.move_ip(*self.player_move[1])
        return player_rect

    # Spawn player
    def create_player(self):
        player = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('player.png', 'images')).convert_alpha(), (64, 64))
        player_rect = pygame.Rect(self.WIDTH/10, self.HEIGHT/2, 64, 64)
        player_move_vertical_and_horizontal = [[0, 10], [10, 0]]
        return player, player_rect, player_move_vertical_and_horizontal

    # Create enemy
    def create_enemy(self):
        enemy = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('enemy.png', 'images')).convert_alpha(), (72, 72))
        enemy_rect = pygame.Rect(self.WIDTH, random.randint(0, self.HEIGHT), 72, 72)
        enemy_move = [random.randint(-15, -5), 0]
        return [enemy, enemy_rect, enemy_move]

    # Create bonus
    def create_bonus(self):
        bonus = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('bonus.png', 'images')).convert_alpha(), (64, 64))
        bonus_rect = pygame.Rect(random.randint(0, self.WIDTH), 0, 64, 64)
        bonus_move = [0, random.randint(5, 10)]
        return [bonus, bonus_rect, bonus_move]

    # Save player score to file
    def save_score(self):
        player_data = GameData().load_player_data()

        player_id = None
        for id, player in player_data['players'].items():
            if player['name'] == self.player_name:
                player_id = id
                break

        if player_id and self.score > player_data['players'][player_id]['score']:
            player_data['players'][player_id]['score'] = self.score
        elif not player_id and self.player_name != 'Guest':
            player_data['players'][str(len(player_data['players']))] = {'name': self.player_name, 'score': self.score}

        GameData().save_player_data(player_data)

    # Pause the game
    def pause(self):
        paused = True
        modal_width, modal_height = 480, 360
        modal_x = (self.WIDTH - modal_width) // 2
        modal_y = (self.HEIGHT - modal_height) // 2

        while paused:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        MainMenu(self.display, paused=True)
                    if event.key == K_RETURN:
                        paused = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                if event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = event.w, event.h
                    self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                    self.background = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('background.png', 'images')), (self.WIDTH, self.HEIGHT))
                    modal_x = (self.WIDTH - modal_width) // 2
                    modal_y = (self.HEIGHT - modal_height) // 2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_rect.collidepoint(event.pos):
                        paused = False
                    if close_button_rect.collidepoint(event.pos):
                        paused = False
                    if exit_button_rect.collidepoint(event.pos):
                        MainMenu(self.display, paused=True)

            # Redraw background
            self.display.blit(self.background, (self.background_1, 0))
            self.display.blit(self.background, (self.background_2, 0))

            # Redraw player
            self.display.blit(self.player, self.player_rect)

            # Redraw enemies
            for enemy in self.enemies:
                self.display.blit(enemy[0], enemy[1])

            # Redraw bonuses
            for bonus in self.bonuses:
                self.display.blit(bonus[0], bonus[1])

            # Display pause modal
            pause_modal_surface = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
            pygame.draw.rect(pause_modal_surface, (50, 50, 50, 180), pause_modal_surface.get_rect(), border_radius=20)
            self.display.blit(pause_modal_surface, (modal_x, modal_y))

            # Display pause title label
            title_font = pygame.font.SysFont('Arial', 32)
            title_text = title_font.render('Pause', True, (255, 255, 255))
            title_text_pos = (modal_x + (modal_width - title_text.get_width()) // 2, modal_y + 20)
            self.display.blit(title_text, title_text_pos)

            # Display player name
            player_name_font = pygame.font.SysFont('Arial', 24)
            player_name_text = player_name_font.render(self.player_name, True, (255, 255, 255))
            player_name_text_pos = (modal_x + modal_width / 2 - player_name_text.get_width(), modal_y + modal_height / 2)
            self.display.blit(player_name_text, player_name_text_pos)

            # Display score
            score_font = pygame.font.SysFont('Arial', 18)
            score_text = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
            score_text_pos = (player_name_text_pos[0], player_name_text_pos[1] + 30)
            self.display.blit(score_text, score_text_pos)

            # Display close (unpause) button
            close_button = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('Back.png', 'images/icons')), (32, 32))
            close_button_rect = close_button.get_rect(topright=(modal_x + modal_width - 10, modal_y + 10))
            self.display.blit(close_button, close_button_rect)

            # Display exit button
            exit_button = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('Exit.png', 'images/icons')), (32, 32))
            exit_button_rect = exit_button.get_rect(topleft=(modal_x + 10, modal_y + 10))
            self.display.blit(exit_button, exit_button_rect)

            # Display top 5 scores
            for i, player in enumerate(self.sorted_scores):
                score_font = pygame.font.SysFont('Arial', 16)
                score_text = score_font.render(f"{player['name']}: {player['score']}", True, (0, 0, 0))
                score_text_pos = (self.WIDTH - score_text.get_width() - 20, 20 + i * 20)
                self.display.blit(score_text, score_text_pos)
                if player['score'] == self.sorted_scores[0]['score']:
                    star_icon = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('player.png', 'images')), (24, 24))
                    self.display.blit(star_icon, (score_text_pos[0] - 30, score_text_pos[1] - 5))

            pygame.display.flip()

    def game_over(self):
        modal_width, modal_height = 720, 480
        modal_x = (self.WIDTH - modal_width) // 2
        modal_y = (self.HEIGHT - modal_height) // 2

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == K_RETURN:
                        game_over = False
                        MainMenu(self.display)
                    if event.key == pygame.K_r:
                        game_over = False
                        self.__init__(self.display, self.player_name)
                if event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = event.w, event.h
                    self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                    self.background = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('background.png', 'images')), (self.WIDTH, self.HEIGHT))
                    modal_x = (self.WIDTH - modal_width) // 2
                    modal_y = (self.HEIGHT - modal_height) // 2
                if event.type == MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        game_over = False
                        self.__init__(self.display, self.player_name)
                    if exit_button_rect.collidepoint(event.pos):
                        game_over = False
                        MainMenu(self.display)

            # Redraw background
            self.display.blit(self.background, (self.background_1, 0))
            self.display.blit(self.background, (self.background_2, 0))

            # Redraw player
            self.display.blit(self.player, self.player_rect)

            # Redraw enemies
            for enemy in self.enemies:
                self.display.blit(enemy[0], enemy[1])

            # Redraw bonuses
            for bonus in self.bonuses:
                self.display.blit(bonus[0], bonus[1])

            # Display game over modal
            game_over_modal_surface = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
            pygame.draw.rect(game_over_modal_surface, (50, 50, 50, 180), game_over_modal_surface.get_rect(), border_radius=20)
            self.display.blit(game_over_modal_surface, (modal_x, modal_y))

            # Display game over title label
            title_font = pygame.font.SysFont('Arial', 32)
            title_text = title_font.render('Game Over', True, (255, 255, 255))
            title_text_pos = (modal_x + (modal_width - title_text.get_width()) // 2, modal_y + 20)
            self.display.blit(title_text, title_text_pos)

            # Display player name
            player_name_font = pygame.font.SysFont('Arial', 24)
            player_name_text = player_name_font.render(self.player_name, True, (255, 255, 255))
            player_name_text_pos = (modal_x + (modal_width - player_name_text.get_width()) // 2, modal_y + 80)
            self.display.blit(player_name_text, player_name_text_pos)

            # Display score
            score_font = pygame.font.SysFont('Arial', 18)
            score_text = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
            score_text_pos = (modal_x + (modal_width - score_text.get_width()) // 2, modal_y + 120)
            self.display.blit(score_text, score_text_pos)

            # Display restart button
            restart_button = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('Restart.png', 'images/icons')), (48, 48))
            restart_button_rect = restart_button.get_rect(topright=(modal_x + modal_width - 10, modal_y + 10))
            self.display.blit(restart_button, restart_button_rect)

            # Display exit button
            exit_button = pygame.transform.scale(pygame.image.load(GameData().get_relative_path('Exit.png', 'images/icons')), (48, 48))
            exit_button_rect = exit_button.get_rect(topleft=(modal_x + 10, modal_y + 10))
            self.display.blit(exit_button, exit_button_rect)

            # Display top 5 scores
            for i, player in enumerate(self.sorted_scores):
                score_font = pygame.font.SysFont('Arial', 16)
                score_text = score_font.render(f"{player['name']}: {player['score']}", True, (255, 255, 255))
                score_text_pos = (modal_x + (modal_width - score_text.get_width()) // 2, modal_height + i * 20)
                self.display.blit(score_text, score_text_pos)

            pygame.display.flip()

# Operations on player data
class GameData:
    def __init__(self):
        self.filename = self.get_relative_path('data.json', 'data')

    # Load player data from file
    def load_player_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                json.dump({'players': {}}, file)
                return self.load_player_data()

    # Save player data to file
    def save_player_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    # Get relative path of a file in the images directory
    def get_relative_path(self, filename, directory):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, directory, filename)

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    pygame.display.set_icon(pygame.image.load(GameData().get_relative_path('logo.png', 'images')))
    pygame.display.set_caption('Unicorn Run')

    main_menu = MainMenu(display)
    pygame.quit()
    exit()
