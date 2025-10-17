import pygame
import os

class Ball:
    def __init__(self, x, y, speed_x, speed_y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.speed_x = float(speed_x)
        self.speed_y = float(speed_y)
        self.width = width
        self.height = height
        self.radius = 10

        # Load sound files safely
        sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        try:
            self.sound_paddle = pygame.mixer.Sound(os.path.join(sound_path, "paddle_hit.wav"))
        except:
            self.sound_paddle = None
        try:
            self.sound_wall = pygame.mixer.Sound(os.path.join(sound_path, "wall_bounce.wav"))
        except:
            self.sound_wall = None
        try:
            self.sound_score = pygame.mixer.Sound(os.path.join(sound_path, "score.wav"))
        except:
            self.sound_score = None

    def rect(self):
        """Return pygame.Rect for collision detection"""
        return pygame.Rect(int(self.x), int(self.y), self.radius * 2, self.radius * 2)

    def move(self):
        """Move the ball and handle top/bottom wall collisions"""
        self.x += self.speed_x
        self.y += self.speed_y

        # Top wall
        if self.y <= 0:
            self.y = 0
            self.speed_y *= -1
            if self.sound_wall:
                self.sound_wall.play()

        # Bottom wall
        elif self.y >= self.height - self.radius * 2:
            self.y = self.height - self.radius * 2
            self.speed_y *= -1
            if self.sound_wall:
                self.sound_wall.play()

    def check_collision(self, player, ai):
        """Check collision with paddles"""
        ball_rect = self.rect()

        # Player paddle
        if ball_rect.colliderect(player.rect()):
            if self.speed_x < 0:  # Ball moving towards player
                self.speed_x = abs(self.speed_x)
                self.x = player.rect().right + 1
                if self.sound_paddle:
                    self.sound_paddle.play()
                # Optional: increase speed for more challenge
                # self.speed_x *= 1.05
                # self.speed_y *= 1.05

        # AI paddle
        elif ball_rect.colliderect(ai.rect()):
            if self.speed_x > 0:  # Ball moving towards AI
                self.speed_x = -abs(self.speed_x)
                self.x = ai.rect().left - self.radius * 2 - 1
                if self.sound_paddle:
                    self.sound_paddle.play()
                # Optional: increase speed for more challenge
                # self.speed_x *= 1.05
                # self.speed_y *= 1.05

    def reset(self):
        """Reset ball to center and alternate serve direction"""
        self.x = self.width // 2 - self.radius
        self.y = self.height // 2 - self.radius
        self.speed_x *= -1  # Alternate serve
        self.speed_y = 7  # Reset vertical speed to default
        if self.sound_score:
            self.sound_score.play()
