from ursina import *
import random

app = Ursina()

# Player
player = Entity(model='cube', color=color.azure, scale=(1, 2, 1), position=(0, 1, 0), collider='box')

# Ground
ground = Entity(model='cube', color=color.green, scale=(10, 1, 50), position=(0, 0, 0), collider='box')

grounds = [ground]
obstacles = []
speed = 20
spawn_timer = 0.5
next_spawn = spawn_timer
is_jumping = False
jump_velocity = 0
gravity = -10.0
jump_count = 1
max_jumps = 3


def update():
    global next_spawn, is_jumping, jump_velocity, jump_count

    if not player or not grounds:
        print("Error: Player or ground missing!")
        return

    player.z += speed * time.dt  # Move forward
    next_spawn -= time.dt

    if next_spawn <= 0:
        spawn_obstacle()
        next_spawn = spawn_timer

    for obstacle in obstacles[:]:
        if obstacle and obstacle.z is not None:
            obstacle.z -= speed * time.dt
            if obstacle.z < -25:
                destroy(obstacle)
                obstacles.remove(obstacle)
            if player.intersects(obstacle).hit:
                print("Game Over! Restarting...")
                reset_game()
                return

    if held_keys['a'] and player.x > -4:
        player.x -= 5 * time.dt
    if held_keys['d'] and player.x < 4:
        player.x += 5 * time.dt

    # Jump logic with double jump
    if is_jumping:
        player.y += jump_velocity * time.dt
        jump_velocity += gravity * time.dt
        if player.y <= 1:
            player.y = 1
            is_jumping = False
            jump_velocity = 0
            jump_count = 0  # Reset jump count when player lands

    if jump_count < max_jumps and held_keys['space'] and not is_jumping:
        is_jumping = True
        jump_velocity = 5
        jump_count += 1

    # Make camera follow the player
    camera.position = (player.x, 5, player.z - 15)
    camera.look_at(player)

    # Extend ground
    if player.z > grounds[-1].z - 25:
        new_ground = duplicate(ground, position=(0, 0, grounds[-1].z + 50))
        grounds.append(new_ground)
        if len(grounds) > 5:
            destroy(grounds.pop(0))


def spawn_obstacle():
    if not player:
        return
    obstacle = Entity(
        model='cube', color=color.red, scale=(1, 2, 1),
        position=(random.choice([-3, 0, 3]), 1, player.z + 20),
        collider='box'
    )
    obstacles.append(obstacle)


def reset_game():
    global jump_count, is_jumping, jump_velocity
    player.position = (0, 1, 0)
    jump_count = 0
    is_jumping = False
    jump_velocity = 0
    for obstacle in obstacles:
        destroy(obstacle)
    obstacles.clear()
    for g in grounds:
        g.z = 0


app.run()
