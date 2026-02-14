import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arrow Shooting Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Arrow class
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 2))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += 10
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, SCREEN_WIDTH - 100)
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

# Player class
class Player:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y - 25, 20, 50))

    def move(self, direction):
        if direction == "up" and self.y > 25:
            self.y -= 5
        elif direction == "down" and self.y < SCREEN_HEIGHT - 25:
            self.y += 5

# Main game function
def main():
    player = Player()
    all_sprites = pygame.sprite.Group()
    arrows = pygame.sprite.Group()
    targets = pygame.sprite.Group()

    # Spawn initial targets
    for _ in range(3):
        target = Target()
        targets.add(target)
        all_sprites.add(target)

    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arrow = Arrow(player.x + 20, player.y)
                    arrows.add(arrow)
                    all_sprites.add(arrow)

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move("up")
        if keys[pygame.K_DOWN]:
            player.move("down")

        # Update all sprites
        all_sprites.update()

        # Check for collisions
        for arrow in arrows:
            hit_targets = pygame.sprite.spritecollide(arrow, targets, True)
            for target in hit_targets:
                score += 10
                target = Target()
                targets.add(target)
                all_sprites.add(target)
                arrow.kill()

        # Drawing everything
        screen.fill(WHITE)
        player.draw()
        all_sprites.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
