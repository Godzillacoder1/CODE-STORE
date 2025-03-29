import pygame
import random
import time

#START YOUR ENGINES
pygame.init()

#size of thingy
WIDTH, HEIGHT = 300, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Farm")

# couleurs
GREEN = (34, 177, 76)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
SILVER = (192, 192, 192)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)

#
crop_types = {"wheat": GREEN, "carrot": YELLOW, "tomato": RED}
current_crop = "wheat"
crop_rect = pygame.Rect(120, 200, 60, 60) 
upgrade_button = pygame.Rect(50, 420, 200, 50)  
watering_can = pygame.Rect(20, 300, 40, 40) 

#x
crop_grow_time = 5  #gorwrth speed for crop
last_planted = time.time()
crop_ready = False
coins = 0
upgrades = {"growth_speed": 0.5, "harvest_bonus": 1}
watering = False  # Track if watering can is being dragged
water_drops = []  

# Day-Night
day_length = 30  # Seconds for a full cycle
start_time = time.time()


def get_sky_color():
    elapsed = (time.time() - start_time) % day_length
    factor = abs((elapsed / (day_length / 2)) - 1)  
    return (
        int(135 - 110 * factor),  
        int(206 - 181 * factor),  
        int(250 - 138 * factor) 
    )



font = pygame.font.Font(None, 36)

running = True
while running:
    screen.fill(get_sky_color())  # Dynamic sky background
    pygame.draw.rect(screen, BROWN, (0, 350, WIDTH, 150))  # Ground

    
    if not crop_ready and time.time() - last_planted >= crop_grow_time / upgrades["growth_speed"]:
        crop_ready = True
        
    if crop_ready:
        pygame.draw.rect(screen, crop_types[current_crop], crop_rect)  # Fully grown crop
    else:
        pygame.draw.rect(screen, (0, 100, 0), crop_rect)  # Growing crop

    #moolahhhhhhhhhh
    coin_text = font.render(f"Coins: {coins}", True, WHITE)
    screen.blit(coin_text, (10, 10))

    #button
    pygame.draw.rect(screen, BLUE, upgrade_button)
    upgrade_text = font.render("Upgrade (10)", True, BLUE)
    screen.blit(upgrade_text, (60, 430))

    #upgrsdes meter
    pygame.draw.rect(screen, GRAY, (50, 380, 200, 20))  # Background bar
    pygame.draw.rect(screen, GREEN, (50, 380, min(200, upgrades["growth_speed"] * 20), 20))  # Upgrade progress
    upgrade_level_text = font.render(f"Lvl: {upgrades['growth_speed']}", True, WHITE)
    screen.blit(upgrade_level_text, (120, 380))

    # can du wuter
    pygame.draw.rect(screen, SILVER, watering_can)

    #wuter
    for drop in water_drops:
        pygame.draw.circle(screen, LIGHT_BLUE, (drop[0], drop[1]), 5)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if crop_ready and crop_rect.collidepoint(event.pos):
                coins += random.randint(1, 5) * upgrades["harvest_bonus"] 
                crop_ready = False
                last_planted = time.time()  
                current_crop = random.choice(list(crop_types.keys()))  
            elif upgrade_button.collidepoint(event.pos) and coins >= 10:  
                coins -= 10
                upgrades["growth_speed"] += 0.5
            elif watering_can.collidepoint(event.pos): 
                watering = True
        elif event.type == pygame.MOUSEBUTTONUP:
            watering = False
        elif event.type == pygame.MOUSEMOTION and watering:
            watering_can.x = event.pos[0] - 20  
            watering_can.y = event.pos[1] - 20

           
            if crop_rect.colliderect(watering_can):
                last_planted -= 0.1  

                water_drops.append([watering_can.x + 20, watering_can.y + 40])

    #wuter agian
    for drop in water_drops:
        drop[1] += 5 

    #GET OUTTTT
    water_drops = [drop for drop in water_drops if drop[1] < HEIGHT]

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
