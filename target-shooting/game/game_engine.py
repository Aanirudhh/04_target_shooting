"""
GameEngine: owns the targets and handles player clicks.

Targets move continuously at one of two speed tiers and bounce off the
play area's edges. Hits build a combo multiplier that raises how many
points each hit is worth; a miss resets the combo. Each round lasts
30 seconds; once time runs out, clicks are ignored until the player
restarts.
"""

import math
import random

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28

# Two distinct speed tiers (pixels/second) targets are randomly assigned.
SPEED_TIERS = [80, 170]

POINTS_PER_HIT = 10
MAX_COMBO = 5
ROUND_DURATION = 30.0


class GameEngine:
    def __init__(self):
        self._reset_state()

    def _reset_state(self):
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 1
        self.time_remaining = ROUND_DURATION
        self.game_over = False

    def restart(self):
        self._reset_state()

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)

        speed = random.choice(SPEED_TIERS)
        angle = random.uniform(0, 2 * math.pi)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)

        return Target(x, y, radius=TARGET_RADIUS, vx=vx, vy=vy)

    def handle_click(self, pos):
        if self.game_over:
            return

        target = check_hit(self.targets, pos)
        if target is not None:
            self.hits += 1
            self.score += POINTS_PER_HIT * self.combo
            self.combo = min(self.combo + 1, MAX_COMBO)
            self.targets.remove(target)
            self.targets.append(self._random_target())
        else:
            self.misses += 1
            self.combo = 1

    def update(self, dt):
        if self.game_over:
            return

        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.game_over = True
            return

        for target in self.targets:
            target.update(dt, WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.targets)
        renderer.draw_text(
            surface, font,
            f"Score: {self.score}  Combo: x{self.combo}  "
            f"Hits: {self.hits}  Misses: {self.misses}",
            (10, 10),
        )
        renderer.draw_text(
            surface, font,
            f"Time: {int(math.ceil(self.time_remaining))}",
            (10, 40),
        )

        if self.game_over:
            renderer.draw_banner(
                surface, font,
                f"Time's up! Final score: {self.score}  "
                "(press R to play again)",
            )
