import os
import pygame
from .bird import Bird
from .pipe import Pipe

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)

class GameEngine:
    DIFFICULTIES = {
        pygame.K_e: {"name": "Easy", "speed": 3, "gap": 180},
        pygame.K_m: {"name": "Medium", "speed": 4, "gap": 150},
        pygame.K_h: {"name": "Hard", "speed": 6, "gap": 120},
    }
    SOUND_FILES = {
        "flap": "flap.wav",
        "score": "score.wav",
        "die": "die.wav",
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.message_font = pygame.font.SysFont("Arial", 26)
        self.sounds = self.load_sounds()
        self.reset()

    def load_sounds(self):
        sounds = {name: None for name in self.SOUND_FILES}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            return sounds

        sounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds")
        for name, filename in self.SOUND_FILES.items():
            path = os.path.join(sounds_dir, filename)
            try:
                sounds[name] = pygame.mixer.Sound(path)
            except (FileNotFoundError, pygame.error):
                sounds[name] = None

        return sounds

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is None:
            return

        try:
            sound.play()
        except pygame.error:
            pass

    def end_game(self):
        if not self.game_over:
            self.game_over = True
            self.play_sound("die")

    def reset(self, difficulty=None):
        if difficulty is None:
            difficulty = self.DIFFICULTIES[pygame.K_m]

        self.difficulty_name = difficulty["name"]
        self.pipe_speed = difficulty["speed"]
        self.pipe_gap = difficulty["gap"]
        self.pipe_interval = 90  # frames between pipe spawns
        self._spawn_timer = 0

        self.bird = Bird(self.width // 4, self.height // 2)
        self.pipes = [Pipe(self.width + 100, self.height, gap=self.pipe_gap, speed=self.pipe_speed)]
        self.score = 0
        self.game_over = False
        self.started = False

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return "quit"
                if event.key in self.DIFFICULTIES:
                    self.reset(self.DIFFICULTIES[event.key])
            return None

        # Flap is edge-triggered (KEYDOWN / MOUSEBUTTONDOWN), not held.
        should_flap = (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        ) or event.type == pygame.MOUSEBUTTONDOWN

        if should_flap:
            self.started = True
            self.bird.flap()
            self.play_sound("flap")

    def handle_input(self):
        # Reserved for continuously-held-key input; flapping is handled
        # in handle_event instead, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        if not self.started:
            return

        self.bird.update()

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= self.height:
            self.end_game()
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(Pipe(self.width, self.height, gap=self.pipe_gap, speed=self.pipe_speed))

        for pipe in self.pipes:
            pipe.move()

            bird_rect = self.bird.rect()
            if bird_rect.colliderect(pipe.top_rect()) or bird_rect.colliderect(pipe.bottom_rect()):
                self.end_game()

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.play_sound("score")

        self.pipes = [p for p in self.pipes if not p.off_screen()]

    def render(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(screen, WHITE, (int(self.bird.x), int(self.bird.y)), self.bird.radius)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            self.render_game_over(screen)

    def render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        title_text = self.title_font.render("Game Over", True, WHITE)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        replay_text = self.message_font.render("E: Easy    M: Medium    H: Hard", True, WHITE)
        quit_text = self.message_font.render("Q or Esc: Quit", True, WHITE)

        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 90))
        score_rect = final_score_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        replay_rect = replay_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
        quit_rect = quit_text.get_rect(center=(self.width // 2, self.height // 2 + 80))

        screen.blit(title_text, title_rect)
        screen.blit(final_score_text, score_rect)
        screen.blit(replay_text, replay_rect)
        screen.blit(quit_text, quit_rect)
