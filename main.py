"""
Snail Hop - a simple jumping game made with pygame.

How to play:
- Press SPACE to jump over the snail.
- Touching the snail ends the game. Press R to restart.
- Jump to collect coins. Your coin total is saved between runs.
- Your score goes up by 1 every time you get past the snail.
"""

import os
import random
import sys
import pygame

# ---------- Paths ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def asset(*parts):
    return os.path.join(BASE_DIR, *parts)


# ---------- Settings ----------
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
FPS = 60
GROUND_Y = 300  # y-coordinate of the top of the ground strip
GROUND_TILE_SIZE = 100

CHAR_X = 100
CHAR_WIDTH, CHAR_HEIGHT = 90, 90
CHAR_ANIMATION_SPEED = 6  # the frame changes every N ticks (lower = faster)

GRAVITY = 1.2
JUMP_STRENGTH = -18

SNAIL_WIDTH, SNAIL_HEIGHT = 70, 50
SNAIL_SPEED = 6
SNAIL_ANIMATION_SPEED = 6

COIN_SIZE = 40
COIN_SPEED = 6
COIN_GAP = 90  # space between coins in one batch so they don't overlap
COIN_ANIMATION_SPEED = 6

BLACK = (0, 0, 0)

HIGHSCORE_FILE = asset("highscore.txt")
COINWALLET_FILE = asset("coinwallet.txt")


# ---------- Loading helpers ----------
class SilentSound:
    """Stand-in used when a sound can't be loaded, so the game still runs."""

    def play(self, *args, **kwargs):
        pass

    def stop(self):
        pass


def load_sound(filename, volume):
    try:
        sound = pygame.mixer.Sound(asset("Sound", filename))
        sound.set_volume(volume)
        return sound
    except (pygame.error, FileNotFoundError):
        print(f"Could not load sound: {filename}")
        return SilentSound()


def load_image(parts, size):
    """Load an image from the game folder and scale it to the given size."""
    image = pygame.image.load(asset(*parts)).convert_alpha()
    return pygame.transform.scale(image, size)


def load_number(path):
    """Read a whole number from a text file. Returns 0 if there is no valid number."""
    try:
        with open(path, "r") as f:
            text = f.read().strip()
        return int(text) if text.isdigit() else 0
    except OSError:
        return 0


def save_number(path, value):
    try:
        with open(path, "w") as f:
            f.write(str(value))
    except OSError:
        pass  # saving is optional, so don't crash if the folder is read-only


# ---------- Game helpers ----------
def spawn_coin_batch():
    """Return a new group of 1 to 3 coins, placed off-screen on the right."""
    count = random.randint(1, 3)
    start_x = SCREEN_WIDTH + random.randint(200, 600)  # random delay before they appear
    return [
        {
            "x": start_x + i * COIN_GAP,
            "y": GROUND_Y - CHAR_HEIGHT - random.randint(40, 100),
            "frame_index": 0,
            "anim_counter": 0,
        }
        for i in range(count)
    ]


def new_snail_x():
    """Return a start position just off-screen on the right, with a random delay."""
    return SCREEN_WIDTH + random.randint(0, 300)


# ---------- Main game ----------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snail Hop")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 28)

    # Sounds
    coin_sound = load_sound("bonus.wav", 0.2)
    game_over_sound = load_sound("game_over.wav", 0.21)
    jump_sound = load_sound("jump.wav", 0.35)
    game_music = load_sound("Game sound.wav", 0.15)

    # Images
    sky_img = load_image(("Graphics", "sky1.png"), (SCREEN_WIDTH, GROUND_Y))
    ground_img = load_image(("Graphics", "ground.png"), (GROUND_TILE_SIZE, GROUND_TILE_SIZE))
    character_frames = [
        load_image(("Graphics", "Main characters", f"walk_left_{i}.png"), (CHAR_WIDTH, CHAR_HEIGHT))
        for i in range(1, 4)
    ]
    snail_frames = [
        load_image(("Graphics", "Enimies", f"snail{i}.png"), (SNAIL_WIDTH, SNAIL_HEIGHT))
        for i in range(1, 4)
    ]
    coin_frames = [
        load_image(("Graphics", "bonus", f"coin_0{i}.png"), (COIN_SIZE, COIN_SIZE))
        for i in range(1, 9)
    ]

    # Character
    ground_level = GROUND_Y - CHAR_HEIGHT  # character's y when standing
    character_y = ground_level
    character_frame_index = 0
    character_anim_counter = 0
    is_jumping = False
    jump_velocity = 0

    # Snail
    snail_x = SCREEN_WIDTH + 50
    snail_y = GROUND_Y - SNAIL_HEIGHT
    snail_frame_index = 0
    snail_anim_counter = 0

    # Coins
    coins = spawn_coin_batch()

    # Score
    score = 0
    high_score = load_number(HIGHSCORE_FILE)
    coins_collected = load_number(COINWALLET_FILE)
    game_over = False

    game_music.play(loops=-1)
    running = True
    while running:
        clock.tick(FPS)  # 60 fps keeps the speed the same on every computer

        # ---- Input ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                    is_jumping = True
                    jump_velocity = JUMP_STRENGTH
                    jump_sound.play()
                elif event.key == pygame.K_r and game_over:
                    # Restart
                    game_over_sound.stop()
                    game_music.play(loops=-1)
                    game_over = False
                    score = 0
                    character_y = ground_level
                    is_jumping = False
                    jump_velocity = 0
                    snail_x = new_snail_x()
                    coins = spawn_coin_batch()

        # ---- Update ----
        if not game_over:
            # Jump: velocity changes a little every frame because of gravity
            if is_jumping:
                character_y += jump_velocity
                jump_velocity += GRAVITY
                if character_y >= ground_level:
                    character_y = ground_level  # landed
                    is_jumping = False
                    jump_velocity = 0

            # Character animation
            character_anim_counter += 1
            if character_anim_counter >= CHAR_ANIMATION_SPEED:
                character_anim_counter = 0
                character_frame_index = (character_frame_index + 1) % len(character_frames)

            # Snail moves right to left. A full pass gives 1 point.
            snail_x -= SNAIL_SPEED
            if snail_x < -SNAIL_WIDTH:
                snail_x = new_snail_x()
                score += 1

            # Snail animation
            snail_anim_counter += 1
            if snail_anim_counter >= SNAIL_ANIMATION_SPEED:
                snail_anim_counter = 0
                snail_frame_index = (snail_frame_index + 1) % len(snail_frames)

            # Coins move and animate
            for coin in coins:
                coin["x"] -= COIN_SPEED
                coin["anim_counter"] += 1
                if coin["anim_counter"] >= COIN_ANIMATION_SPEED:
                    coin["anim_counter"] = 0
                    coin["frame_index"] = (coin["frame_index"] + 1) % len(coin_frames)

            # Remove coins that left the screen
            coins = [c for c in coins if c["x"] > -COIN_SIZE]

            # Pick up any coin the character touches
            character_rect = pygame.Rect(CHAR_X, character_y, CHAR_WIDTH, CHAR_HEIGHT)
            remaining_coins = []
            for coin in coins:
                coin_rect = pygame.Rect(coin["x"], coin["y"], COIN_SIZE, COIN_SIZE)
                if character_rect.colliderect(coin_rect):
                    coins_collected += 1
                    coin_sound.play()
                else:
                    remaining_coins.append(coin)
            coins = remaining_coins

            # Send a new batch once the old one is gone
            if not coins:
                coins = spawn_coin_batch()

            # Snail collision. The hitboxes are a bit smaller than the pictures
            # so near-misses don't feel unfair.
            snail_rect = pygame.Rect(snail_x, snail_y, SNAIL_WIDTH, SNAIL_HEIGHT)
            if character_rect.inflate(-20, -20).colliderect(snail_rect.inflate(-20, -20)):
                game_over = True
                game_music.stop()
                game_over_sound.play(maxtime=2000)
                if score > high_score:
                    high_score = score
                    save_number(HIGHSCORE_FILE, high_score)
                save_number(COINWALLET_FILE, coins_collected)

        # ---- Draw ----
        screen.blit(sky_img, (0, 0))
        for x in range(0, SCREEN_WIDTH, GROUND_TILE_SIZE):
            screen.blit(ground_img, (x, GROUND_Y))
        screen.blit(character_frames[character_frame_index], (CHAR_X, character_y))
        screen.blit(snail_frames[snail_frame_index], (snail_x, snail_y))
        for coin in coins:
            screen.blit(coin_frames[coin["frame_index"]], (coin["x"], coin["y"]))

        score_text = font.render(
            f"Score: {score}  High Score: {high_score}  Coins: {coins_collected}", True, BLACK
        )
        screen.blit(score_text, (20, 20))

        if game_over:
            over_text = font.render("Game Over - press R to restart", True, BLACK)
            screen.blit(over_text, over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        pygame.display.update()

    save_number(COINWALLET_FILE, coins_collected)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
