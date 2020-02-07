import pygame
import gamebox
import random

# the basics of the game work with no known glitches besides the fireballs being bigger objects than they appear
# we are still working on adding more "power-ups"/special items and images for some items
# the goal is ascending into space and collecting stars
# fireballs hurt you, dynamite hurts a little but shoots you up, more to come...
width = 400
height = 500
camera = gamebox.Camera(width, height)

character = gamebox.from_color(100, 200, 'white', 15, 15)
ground = gamebox.from_color(200, 300, 'brown', width, 20)
blocks = [gamebox.from_color(200, 300, 'darkgray', 1, 1)]
start = gamebox.from_text(width/2, 350, "Start Here", 40, 'white')
cannon = gamebox.from_image(width/2, 300, 'bounce.png')
bg = gamebox.from_image(width/2, 4500, "bg.png")
cannon.scale_by(.25)

camera.clear('white')

coins = []
enemies = []
dynamite = []

healthnum = 100
scorenum = 0
currenth = character.y

def off_the_screen(object):
    return (abs(object.x - camera.x) > width/2+200) or (abs(object.y - camera.y) > height/2+200)

def tick(keys):
    global scorenum, enemies, currenth, healthnum
    # remove objects off screen
    for obj in coins:
        if off_the_screen(obj):
            coins.remove(obj)
    for obj in blocks:
        if off_the_screen(obj):
            blocks.remove(obj)
    for obj in enemies:
        if off_the_screen(obj):
            enemies.remove(obj)
    for obj in dynamite:
        if off_the_screen(obj):
            dynamite.remove(obj)
    # scrolling level, working on making a gradient or using a background image, idea is ascending into space
    if camera.y >= -3000:
        camera.clear('blue')
    if camera.y < -3000 and camera.y >= -6000:
        camera.clear('darkblue')
    if camera.y < -6000 and camera.y >= -9000:
        camera.clear('darkgray')
    if camera.y < -9000:
        camera.clear('black')
    # controls
    if pygame.K_LEFT in keys:
        character.x -= 5       # move left
    if pygame.K_RIGHT in keys:
        character.x += 5       # move right
    # start
    if character.bottom_touches(cannon):
            character.speedy = -16
    # gravity
    character.speedy += .3
    character.move_speed()
    # bounce and don't go thru blocks
    for block in blocks:
        character.move_to_stop_overlapping(block)
        if character.bottom_touches(block):
            character.speedy = -16
    # draw items
    items_on_screen = blocks + coins
    for item in items_on_screen:
        camera.draw(item)
    # collecting coins
    for coin in coins:
        if coin.touches(character):
            coins.remove(coin)
            scorenum += 1
    # moving enemies that reduce health when hit
    for enemy in enemies:
        if character.touches(enemy):
            healthnum -= 25
        camera.draw(enemy)
        if enemy.touches(character):
            enemies.remove(enemy)
        if enemy.xspeed == 0:
            enemy.xspeed = 4
        if abs(enemy.x - camera.x) >= width/2:
            enemy.xspeed = -enemy.xspeed
        enemy.x += enemy.xspeed
    # score and health text display
    score = gamebox.from_text(camera.x+140, camera.y-200, 'Score:'+str(scorenum), 30, 'white')
    camera.draw(score)
    health = gamebox.from_text(camera.x - 140, camera.y - 200, 'HP:'+str(healthnum)+'/100', 30, 'white')
    camera.draw(health)
    # adding new items to screen as old ones get deleted, chance for
    if character.y < currenth:
        currenth = character.y
    if len(blocks)<2:
        chance = random.randint(1,10)

        new_block = gamebox.from_image(random.randint(50,width-50),currenth-200,'block.png')
        new_block.scale_by(.25)
        blocks.append(new_block)

        new_coin = gamebox.from_image(random.randint(100, 200), currenth-300, 'coin.png')
        new_coin.scale_by(.05)
        coins.append(new_coin)

        if chance < 5:
            new_enemy = gamebox.from_image(random.randint(100, 200), currenth-300, 'enemy.png')
            new_enemy.scale_by(.1)
            enemies.append(new_enemy)

        if chance == 5:
            dynamite.append(gamebox.from_color(random.randint(50,width-50), currenth-random.randint(220,320), 'red', 20, 20))
    # dynamite item, shoots you up but hurts you
    for dyno in dynamite:
        for coin in coins:
            dyno.move_to_stop_overlapping(coin)
        camera.draw(dyno)
        if dyno.touches(character):
            dynamite.remove(dyno)
            healthnum -= 5
            character.speedy -= 20
    # draw main items, keep camera centered
    character.move_to_stop_overlapping(ground)
    camera.draw(ground)
    camera.draw(character)
    camera.draw(start)
    camera.draw(cannon)
    camera.center = [cannon.x,character.y]
    # end game
    if healthnum <= 0 or character.y >= height:
        game_over = gamebox.from_text(camera.x, camera.y - 50, "Game Over", 75, 'white')
        end = gamebox.from_text(camera.x, camera.y, "Score: " + str(scorenum), 50, 'white')
        end_board = gamebox.from_color(camera.x, camera.y - 25, 'black', 300, 150)
        camera.draw(end_board)
        camera.draw(end)
        camera.draw(game_over)
        gamebox.pause()

    camera.display()

gamebox.timer_loop(30, tick)