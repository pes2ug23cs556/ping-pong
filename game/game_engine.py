import pygame
import os
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.small_font = pygame.font.SysFont("Arial", 25)

        # Load winning sound
        sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        try:
            self.sound_win = pygame.mixer.Sound(os.path.join(sound_path, "win.wav"))
        except:
            self.sound_win = None

        # Wait for player to choose mode
        self.best_of = self.get_best_of_choice()
        self.reset_game(self.best_of)

    def get_best_of_choice(self):
        """Show menu at game start to choose mode."""
        screen = pygame.display.get_surface()
        choosing = True

        while choosing:
            screen.fill(BLACK)
            title = self.big_font.render("Choose Game Mode", True, WHITE)
            screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 80)))

            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, opt in enumerate(options):
                text = self.small_font.render(opt, True, WHITE)
                screen.blit(text, text.get_rect(center=(self.width // 2, self.height // 2 + i * 40)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_5:
                        return 5
                    elif event.key == pygame.K_7:
                        return 7
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

    def reset_game(self, best_of):
        """Reset everything based on 'best_of' rounds."""
        # For best_of=3 → win at 2; best_of=5 → win at 3; best_of=7 → win at 4
        self.target_score = (best_of // 2) + 1
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self, screen):
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI tracking
        self.ai.auto_track(self.ball, self.height)

        # check for game over
        if self.player_score == self.target_score or self.ai_score == self.target_score:
            self.display_winner(screen)

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def display_winner(self, screen):
        """Show who won and replay options."""
        self.game_over = True
        winner = "Player Wins!" if self.player_score > self.ai_score else "AI Wins!"

        # Play winning sound
        if self.sound_win:
            self.sound_win.play()

        screen.fill(BLACK)
        text_surface = self.big_font.render(winner, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 60))
        screen.blit(text_surface, text_rect)

        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        for i, opt in enumerate(options):
            text = self.small_font.render(opt, True, WHITE)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + 40 + i * 30))
            screen.blit(text, rect)

        pygame.display.flip()
        self.wait_for_replay_choice()

    def wait_for_replay_choice(self):
        """Wait for user to select replay option."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.reset_game(3)
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.reset_game(5)
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.reset_game(7)
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
