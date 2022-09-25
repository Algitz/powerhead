import pygame, random

pygame.init()

displayw = 1440
displayh = 900

gameDisplay = pygame.display.set_mode((displayw, displayh))
pygame.display.set_caption('Power Head')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False

pi = 3.14159265359


class player:
    x = 0
    y = 0
    dx = 0
    dy = 0
    d2x = 0
    d2y = 0
    speed = 6.5
    w = 150
    h = 120
    hearts = 3
    isJumping = False
    isDoubleJumping = False
    immunityDuration = 140
    immunityTimer = 0
    immunityFlashPeriod = 25

    class jump:
        h = 300
        time = 42
        cooldown = 30
        cooldownTimer = 0


class images:
    player = pygame.image.load('assets/player.png')
    bullet = pygame.image.load('assets/bullet.png')
    powerup = pygame.image.load('assets/power_up.png')
    heart = pygame.image.load('assets/heart.png')
    background = pygame.image.load('assets/bg.png')
    player_translucent = pygame.image.load('assets/player_translucent.png')
    platform = pygame.image.load('assets/platform.png')
    # ground = pygame.image.load('assets/ground.png')
    # favicon = pygame.image.load('icon.png')


class powerup:
    duration = 0
    durationTimer = 0
    type = ''
    spawnTime = 0

    slownessDuration = 300
    slownessMultiplier = 0.5
    slowEnemiesDuration = 300
    slowEnemiesMultiplier = 0.3
    doubleJumpDuration = 600
    blindnessDuration = 600
    blindnessRadius = 220
    blindnessColor = (10, 10, 10)
    bulletRedirectDuration = 140
    bulletRedirectSpeed = 1.25


ground_level = 780  # the top of the ground

t = 0  # game time
pb = 0  # best time

keyA = False
keyD = False
keySpace = False

screen = 'mainMenu'  # mainMenu, game, credits
mouseDown = False
mouseCursor = 'arrow'  # none, arrow, hand

platforms = []  # x, y, width, height
bullets = []  # x, y, width, height, rot, speed, dθ
powerups = []  # x, y, width, height, type (regen, doubleJump, slowEnemies, slowness, blindness, bulletRedirect)

mainMenuButtons = [['POWER HEAD', displayw / 2, 200, 60, black, 'center', '', False],
                   ['Start', displayw / 2, 360, 35, black, 'center', 'start', False],
                   ['Credits', displayw / 2, 435, 35, black, 'center', 'credits', False],
                   ['Quit Game', displayw / 2, 510, 35, black, 'center', 'leave',
                    False]]  # text, x, y, size, color, align, function (start, leave, credits), hover
pauseButtons = [['Game Paused', displayw / 2, 200, 60, black, 'center', '', False],
                ['Continue', displayw / 2, 360, 32, black, 'center', 'continue', False],
                ['Leave', displayw / 2, 435, 32, black, 'center', 'leave',
                 False]]  # text, x, y, size, color, align, function (resume, leave), hover
lostButtons = [['You Lost', displayw / 2, 200, 60, black, 'center', '', False],
               ['Restart', displayw / 2, 440, 32, black, 'center', 'restart', False],
               ['Leave', displayw / 2, 515, 32, black, 'center', 'leave',
                False]]  # text, x, y, size, color, align, function (resume, leave), hover
creditsButtons = [['Credits', displayw / 2, 200, 60, black, 'center'],
                  ['Navanatee Yampunranai', displayw / 2, 340, 24, black, 'center'],
                  ['Pannawich Siripakornchai', displayw / 2, 405, 24, black, 'center'],
                  ['Supacheep Sahakitrungruang', displayw / 2, 470, 24, black, 'center'],
                  ['© 2022 All Rights Reserved', displayw / 2, ground_level - 30, 18, black,
                   'center']]  # text, x, y, size, color, align


def check_collision_side(vertex, pltvt):  # platform vertices
    return pltvt[0] < vertex[0] < pltvt[0] + pltvt[2] and pltvt[1] < vertex[1] < pltvt[1] + pltvt[3]


def side_collide(objarr, sid, plyrarr=None):
    if plyrarr is None:
        plyrarr = [player.x, player.y, player.w, player.h]
    temp0 = 0
    if sid == 0:
        temp0 = int(check_collision_side([player.x, player.y + player.h], objarr))
        temp0 += int(check_collision_side([player.x + player.w, player.y + player.h], objarr))
        temp0 += int(check_collision_side([objarr[0], objarr[1]], plyrarr))
        temp0 += int(check_collision_side([objarr[0] + objarr[2], objarr[1]], plyrarr))
    elif sid == 1:
        temp0 = int(check_collision_side([player.x, player.y], objarr))
        temp0 += int(check_collision_side([player.x, player.y + player.h], objarr))
        temp0 += int(check_collision_side([objarr[0] + objarr[2], objarr[1]], plyrarr))
        temp0 += int(check_collision_side([objarr[0] + objarr[2], objarr[1] + objarr[3]], plyrarr))
    elif sid == 2:
        temp0 = int(check_collision_side([player.x, player.y], objarr))
        temp0 += int(check_collision_side([player.x + player.w, player.y], objarr))
        temp0 += int(check_collision_side([objarr[0], objarr[1] + objarr[3]], plyrarr))
        temp0 += int(check_collision_side([objarr[0] + objarr[2], objarr[1] + objarr[3]], plyrarr))
    elif sid == 3:
        temp0 = int(check_collision_side([player.x + player.w, player.y], objarr))
        temp0 += int(check_collision_side([player.x + player.w, player.y + player.h], objarr))
        temp0 += int(check_collision_side([objarr[0], objarr[1]], plyrarr))
        temp0 += int(check_collision_side([objarr[0], objarr[1] + objarr[3]], plyrarr))
    return temp0 > 1


def sin(n):  # n in degrees
    if not -180 < n <= 180:
        n = ((n + 180) % 360) - 180
    if n > 90:
        n = 180 - n
    elif n < -90:
        n = - 180 - n
    n *= pi / 180
    return n * (1 - n ** 2 / 6 + n ** 4 / 120 - n ** 6 / 5040)


def gafrar(rise, run):  # get angle from rise and run
    n = run / rise
    nRec = rise / run
    if -1 <= n <= 1:
        return n * (5.56047951745 * (n ** 4) - 17.8562590305 * (n ** 2) + n * 180 / pi)
    elif n > 1:
        return 90 - nRec * (5.56047951745 * (nRec ** 4) - 17.8562590305 * (nRec ** 2) + nRec * 180 / pi)
    else:
        return - 90 - nRec * (5.56047951745 * (nRec ** 4) - 17.8562590305 * (nRec ** 2) + nRec * 180 / pi)


def drawText(txt, n1, n2, sze, clr, algn):
    temp6 = pygame.font.SysFont('Comic Sans MS', sze).render(txt, True, clr)
    if algn == 'center':
        gameDisplay.blit(temp6, temp6.get_rect(center=(n1, n2)))
    elif algn == 'left':
        gameDisplay.blit(temp6, temp6.get_rect())
    elif algn == 'right':
        gameDisplay.blit(temp6, temp6.get_rect(topright=(n1, n2)))


def resetGame():
    global screen, mouseCursor, keyA, keyD, keySpace, mouseDown, platforms, bullets, powerups, pb, t

    screen = 'game'
    mouseCursor = 'none'

    player.x = displayw / 2 - player.w / 2
    player.y = ground_level - player.h
    player.dx = 0
    player.dy = 0
    player.d2x = 0
    player.d2y = 0
    player.hearts = 3
    player.isJumping = False
    player.isDoubleJumping = False
    keyA = False
    keyD = False
    keySpace = False
    mouseDown = False
    platforms = []
    bullets = []
    powerups = []
    if t > pb: pb = t
    t = 0
    player.immunityTimer = 0

    powerup.duration = 0
    powerup.durationTimer = 0
    powerup.type = ''
    powerup.spawnTime = 0


def spawnPowerup(chance):
    temp15 = ''
    temp16 = random.randint(1, 3)
    if random.randint(1, 100) <= chance:
        if temp16 == 1: temp15 = 'regen'
        elif temp16 == 2: temp15 = 'doubleJump'
        elif temp16 == 3: temp15 = 'slowEnemies'
    else:
        if temp16 == 1: temp15 = 'slowness'
        elif temp16 == 2: temp15 = 'blindness'
        elif temp16 == 3: temp15 = 'bulletRedirect'

    powerups.append([random.randint(10, displayw - 19 - 10),
                     random.randint(ground_level - 300, ground_level - 80), 50, 50, temp15])


def spawnBullet():
    temp17 = random.randint(1, 16)
    if temp17 == 1:
        bullets.append([random.randint(-600, -200), random.randint(300, ground_level - 19 - 10), 19, 66, 90, 4, 0])
    elif temp17 == 2:
        bullets.append([random.randint(displayw + 200, displayw + 600), random.randint(300, ground_level - 19 - 10), 19, 66, -90, 4,0])
    else:
        bullets.append([random.randint(10, displayw - 19 - 10), random.randint(-600, -200), 19, 66, 0, 4, 0])


# setup
player.x = displayw / 2 - player.w / 2
player.y = ground_level - player.h
# pygame.display.set_icon()

while not crashed:
    if mouseCursor == 'none':
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
        if mouseCursor == 'arrow':
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif mouseCursor == 'hand':
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    mouseX, mouseY = pygame.mouse.get_pos()
    mouseDown = False

    if screen == 'mainMenu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = 'mainMenu'

        gameDisplay.fill(white)
        gameDisplay.blit(pygame.transform.scale(images.background, (displayw, displayh)), (0, 0))
        # gameDisplay.blit(pygame.transform.scale(images.ground, (displayw, 120)), (0, ground_level))
        pygame.draw.rect(gameDisplay, (77, 58, 45), pygame.Rect(0, ground_level, displayw, displayh - ground_level))

        mouseCursor = 'arrow'
        for i in mainMenuButtons:
            if i[6] != '' and i[5] == 'center':
                temp7 = pygame.font.SysFont('Comic Sans MS', i[3]).render(i[0], True, i[4]).get_rect(
                    center=(i[1], i[2]))
                i[7] = temp7.collidepoint(mouseX, mouseY)
                if i[7]:
                    mouseCursor = 'hand'

            drawText(i[0], i[1], i[2] - (3 * i[7]), i[3], i[4], i[5])

            if i[7] and mouseDown:
                i[7] = False
                if i[6] == 'start':
                    resetGame()

                elif i[6] == 'credits':
                    screen = 'credits'
                    mouseCursor = 'arrow'
                elif i[6] == 'leave':
                    crashed = True

    elif screen == 'credits':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = 'mainMenu'

        gameDisplay.fill(white)
        gameDisplay.blit(pygame.transform.scale(images.background, (displayw, displayh)), (0, 0))
        # gameDisplay.blit(pygame.transform.scale(images.ground, (displayw, 120)), (0, ground_level))
        pygame.draw.rect(gameDisplay, (77, 58, 45), pygame.Rect(0, ground_level, displayw, displayh - ground_level))

        mouseCursor = 'arrow'
        for i in creditsButtons:
            drawText(i[0], i[1], i[2], i[3], i[4], i[5])

    elif screen == 'game' or screen == 'pause' or screen == 'lost':
        if screen == 'game':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        keyA = True
                    elif event.key == pygame.K_d:
                        keyD = True
                    elif event.key == pygame.K_SPACE:
                        keySpace = True
                    elif event.key == pygame.K_ESCAPE:
                        screen = 'pause'

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        keyA = False
                    elif event.key == pygame.K_d:
                        keyD = False
                    elif event.key == pygame.K_SPACE:
                        keySpace = False

            if player.hearts <= 0:
                screen = 'lost'

            t += 1
            # spawn enemies
            if t < 120: # stage 0
                ""
            elif t < 600:
                if len(bullets) < 2:
                    bullets.append([random.randint(10, displayw - 19 - 10), -200, 19, 66, 0, 4, 0])
            elif t < 1200:
                if len(bullets) < 4:
                    bullets.append([random.randint(10, displayw - 19 - 10), random.randint(-600, -200), 19, 66, 0, 4, 0])
            elif t < 1800:
                if len(bullets) < 6:
                    bullets.append([random.randint(10, displayw - 19 - 10), random.randint(-600, -200), 19, 66, 0, 4, 0])
                powerup.spawnTime = random.randint(1900, 3500)
            elif t < 3600: # stage 1
                if len(bullets) < 8:
                    bullets.append([random.randint(10, displayw - 19 - 10), random.randint(-600, -200), 19, 66, 0, 4, 0])
                if t == powerup.spawnTime:
                    spawnPowerup(100)
                    powerup.spawnTime = random.randint(3700, 5300)
            elif t < 5400: # stage 2
                if len(bullets) < 10:
                    spawnBullet()
                if t == powerup.spawnTime:
                    spawnPowerup(95)
                    powerup.spawnTime = random.randint(5500, 7400)
                if t == 3601:
                    platforms = [[random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40]]
            elif t < 7500: # stage 3
                if len(bullets) < 12:
                    spawnBullet()
                if t == powerup.spawnTime:
                    spawnPowerup(92)
                    powerup.spawnTime = random.randint(7600, 9500)
                if t == 5401:
                    platforms = [[random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40]]
            elif t < 9600: # stage 4
                if len(bullets) < 14:
                    spawnBullet()
                if t == powerup.spawnTime:
                    spawnPowerup(90)
                    powerup.spawnTime = random.randint(9700, 11900)
                if t == 7501:
                    platforms = [[random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40]]
                    platforms.append([random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40])
            elif t < 12000: # stage 5
                if len(bullets) < 16:
                    spawnBullet()
                if t == powerup.spawnTime:
                    spawnPowerup(87)
                    powerup.spawnTime = random.randint(12100, 14300)
                if t == 9601:
                    platforms = [[random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40]]
                    platforms.append([random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40])
            elif t < 14400: # stage 6
                if len(bullets) < 18:
                    spawnBullet()
                if t == powerup.spawnTime:
                    spawnPowerup(85)
                    powerup.spawnTime = random.randint(14500, 17900)
                if t == 12001:
                    platforms = [[random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40]]
                    platforms.append([random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40])
            elif t < 18000: # stage 7
                if len(bullets) < 14:
                    spawnBullet()
                if t == powerup.spawnTime:
                    spawnPowerup(85)
                    powerup.spawnTime = random.randint(19000, 20600)
                if t == 14401:
                    platforms = [[random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40]]
                    platforms.append([random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40])
                    platforms.append([random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40])
            else: # stage 7
                if len(bullets) < 24:
                    spawnBullet()
                if t == powerup.spawnTime:
                    spawnPowerup(80)
                    powerup.spawnTime = random.randint(t + 1200, t + 2400)
                if t % 3600 == 0:
                    platforms = [[random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40]]
                    platforms.append([random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40])
                    platforms.append([random.randint(10, displayw - 200 - 10), random.randint(400, ground_level - 200), 200, 40])


            if powerup.duration > 0 and powerup.durationTimer < powerup.duration:
                powerup.durationTimer += 1
            elif powerup.durationTimer >= powerup.duration:
                powerup.duration = 0
                powerup.durationTimer = 0
                powerup.type = ''

            if 0 < player.immunityTimer < player.immunityDuration:
                player.immunityTimer += 1
            elif player.immunityTimer >= player.immunityDuration:
                player.immunityTimer = 0

            if keyA == keyD:
                if player.isJumping:
                    player.dx *= 0.98
                elif not -0.1 < player.dx < 0.1:
                    player.dx *= 0.69
                else:
                    player.dx = 0
            elif keyA:
                if powerup.durationTimer > 0 and powerup.type == 'slowness':
                    player.dx = -player.speed * powerup.slownessMultiplier
                else:
                    player.dx = -player.speed
            elif keyD:
                if powerup.durationTimer > 0 and powerup.type == 'slowness':
                    player.dx = player.speed * powerup.slownessMultiplier
                else:
                    player.dx = player.speed

            if keySpace and not player.isJumping and player.jump.cooldownTimer == 0:
                player.isJumping = True
                player.jump.cooldownTimer = 1
                player.d2y = 8 * player.jump.h / player.jump.time ** 2
                player.dy = - 4 * player.jump.h / player.jump.time
            elif keySpace and player.isJumping and player.dy > 0 and not player.isDoubleJumping and powerup.durationTimer > 0 and powerup.type == 'doubleJump':
                player.isDoubleJumping = True
                player.d2y = 8 * player.jump.h / player.jump.time ** 2
                player.dy = - 4 * player.jump.h / player.jump.time

            if player.jump.cooldownTimer > 0:
                player.jump.cooldownTimer += 1
            if not player.isJumping and player.jump.cooldownTimer > player.jump.cooldown:
                player.jump.cooldownTimer = 0

            for i in platforms:
                if (player.x < i[0] - player.w or player.x > i[0] + i[2]) and player.y == i[1] - player.h and not player.isJumping:
                    player.isJumping = True
                    player.d2y = 8 * player.jump.h / player.jump.time ** 2

            player.dx += player.d2x
            player.x += player.dx
            player.dy += player.d2y
            player.y += player.dy

            for i in bullets:
                # i[4] += 1
                i[4] = ((i[4] + 180) % 360) - 180
                if powerup.durationTimer > 0 and powerup.type == 'bulletRedirect':
                    temp5 = gafrar(player.y + player.w / 2 - i[1], player.x + player.h / 2 - i[0])
                    if (player.y < i[1] and not -90 < temp5 < 90) or (player.x < i[0] and -180 < temp5 < 180):
                        if temp5 < 0:
                            temp5 += 180
                        else:
                            temp5 -= 180
                    if -10 < temp5 - i[4] < 10:
                        i[6] = 0
                    elif (temp5 - i[4]) % 360 < (i[4] - temp5) % 360:
                        i[6] = powerup.bulletRedirectSpeed
                    else:
                        i[6] = - powerup.bulletRedirectSpeed
                else:
                    i[6] = 0

                i[4] += i[6]

                if powerup.durationTimer > 0 and powerup.type == 'slowEnemies':
                    i[0] += i[5] * sin(i[4]) * powerup.slowEnemiesMultiplier
                    i[1] += i[5] * sin(90 - i[4]) * powerup.slowEnemiesMultiplier
                else:
                    i[0] += i[5] * sin(i[4])
                    i[1] += i[5] * sin(90 - i[4])

            # collisions
            if player.x < 0:
                player.x = 0
            if player.x > displayw - player.w:
                player.x = displayw - player.w
            if player.y > ground_level - player.h and player.isJumping:
                player.y = ground_level - player.h
                player.isJumping = False
                player.isDoubleJumping = False
                player.d2y = 0
                player.dy = 0

            for i in platforms:
                if side_collide(i, 2):
                    player.y = i[1] + i[3]
                    player.dy *= -1
                elif side_collide(i, 0) and player.dy > 0:
                    player.isJumping = False
                    player.isDoubleJumping = False
                    player.y = i[1] - player.h
                    player.dy = 0
                    player.d2y = 0
                elif side_collide(i, 1):
                    player.x = i[0] + i[2]
                elif side_collide(i, 3):
                    player.x = i[0] - player.w

                for j in bullets:
                    temp3 = [[j[0], j[1]], [j[0] + j[2] * sin(90 - j[4]), j[1] - j[2] * sin(j[4])],
                             [j[0] + j[3] * sin(j[4]), j[1] + j[3] * sin(90 - j[4])],
                             [j[0] + j[3] * sin(j[4]) + j[2] * sin(90 - j[4]),
                              j[1] + j[3] * sin(90 - j[4]) - j[2] * sin(j[4])]]
                    temp4 = False
                    for k in temp3:
                        if i[0] < k[0] < i[0] + i[2] and i[1] < k[1] < i[1] + i[3]:
                            temp4 = True
                    if temp4:
                        bullets.remove(j)

            for i in bullets:
                if -90 < i[4] < 90 and (
                        i[1] + i[3] * sin(90 - i[4]) > ground_level or i[1] + i[3] * sin(90 - i[4]) - i[2] * sin(
                    i[4]) > ground_level):
                    bullets.remove(i)
                elif (i[4] == 90 and i[0] > displayw) or (i[4] == -90 and i[0] < -i[3]):
                    bullets.remove(i)
                elif not -90 < i[4] < 90 and (
                        i[1] - i[3] * sin(90 - i[4]) < 0 or i[1] - i[3] * sin(90 - i[4]) - i[2] * sin(i[4]) < 0):
                    bullets.remove(i)
                elif ((side_collide(i, 0) and player.dy < 0) or side_collide(i, 1) or side_collide(i,
                                                                                                   2) or side_collide(i,
                                                                                                                      3)) and player.immunityTimer == 0:
                    bullets.remove(i)
                    player.hearts -= 1
                    player.immunityTimer = 1
                elif side_collide(i, 0) and player.dy >= 0:
                    bullets.remove(i)
                    player.dy *= -1

            for i in powerups:
                if side_collide(i, 0) or side_collide(i, 1) or side_collide(i, 2) or side_collide(i, 3):
                    if i[4] == 'regen':
                        player.hearts += 1
                    elif i[4] == 'doubleJump':
                        powerup.duration = powerup.doubleJumpDuration
                        powerup.type = 'doubleJump'
                    elif i[4] == 'slowEnemies':
                        powerup.duration = powerup.slowEnemiesDuration
                        powerup.type = 'slowEnemies'
                    elif i[4] == 'slowness':
                        powerup.duration = powerup.slownessDuration
                        powerup.type = 'slowness'
                    elif i[4] == 'blindness':
                        powerup.duration = powerup.blindnessDuration
                        powerup.type = 'blindness'
                    elif i[4] == 'bulletRedirect':
                        powerup.duration = powerup.bulletRedirectDuration
                        powerup.type = 'bulletRedirect'

                    powerups.remove(i)

        gameDisplay.fill(white)
        gameDisplay.blit(pygame.transform.scale(images.background, (displayw, displayh)), (0, 0))
        # gameDisplay.blit(pygame.font.SysFont('Comic Sans MS', 30).render(str(powerup.durationTimer), True, (0, 0, 0)), (0, 50))
        for i in bullets:
            newrect = pygame.transform.rotate(images.bullet, i[4]).get_rect(center=(
                (i[0] * 2 + i[3] * sin(i[4]) + i[2] * sin(90 - i[4])) / 2,
                (i[1] * 2 + i[3] * sin(90 - i[4]) - i[2] * sin(i[4])) / 2))
            gameDisplay.blit(pygame.transform.rotate(images.bullet, i[4]), newrect)
        for i in platforms:
            gameDisplay.blit(images.platform, (i[0], i[1]))
        for i in powerups:
            gameDisplay.blit(images.powerup, (i[0], i[1]))

        if player.immunityTimer > 0 and 0 <= player.immunityTimer % player.immunityFlashPeriod <= player.immunityFlashPeriod / 2:
            gameDisplay.blit(images.player_translucent, (player.x, player.y))
        else:
            gameDisplay.blit(images.player, (player.x, player.y))

        # gameDisplay.blit(pygame.transform.scale(images.ground, (displayw, 120)), (0, ground_level))
        pygame.draw.rect(gameDisplay, (77, 58, 45), pygame.Rect(0, ground_level, displayw, displayh - ground_level))

        if powerup.durationTimer > 0 and powerup.type == 'blindness':
            temp1 = [(player.x + player.w / 2, 0), (displayw, 0), (displayw, displayh), (0, displayh), (0, 0),
                     (player.x + player.w / 2, 0)]
            temp2 = 18
            for i in range(temp2):
                temp1.append((player.x + player.w / 2 - powerup.blindnessRadius * sin(i * 360 / temp2),
                              player.y + player.h / 2 - powerup.blindnessRadius * sin(90 - i * 360 / temp2)))

            temp1.append(temp1[6])
            pygame.draw.polygon(gameDisplay, powerup.blindnessColor, temp1)
            pygame.draw.circle(gameDisplay, powerup.blindnessColor, (player.x + player.w / 2, player.y + player.h / 2),
                               powerup.blindnessRadius + 5, 10)

        # ui
        for i in range(player.hearts):
            gameDisplay.blit(images.heart, (50 * i, 0))
        temp9 = str(t // 3600)  # mins
        temp10 = (t // 60) % 60  # secs
        temp10 = '0' + str(temp10) if 0 <= temp10 <= 9 else str(temp10)

        drawText(temp9 + ':' + temp10, displayw - 10, 5, 24, white if powerup.durationTimer > 0 and powerup.type == 'blindness' else black, 'right')

        if screen == 'pause':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseDown = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen = 'game'

            temp8 = pygame.Surface((displayw, displayh), pygame.SRCALPHA)
            temp8.fill((96, 96, 96, 128))
            gameDisplay.blit(temp8, (0, 0))

            mouseCursor = 'arrow'
            for i in pauseButtons:
                if i[6] != '' and i[5] == 'center':
                    temp7 = pygame.font.SysFont('Comic Sans MS', i[3]).render(i[0], True, i[4]).get_rect(
                        center=(i[1], i[2]))
                    i[7] = temp7.collidepoint(mouseX, mouseY)
                    if i[7]:
                        mouseCursor = 'hand'

                drawText(i[0], i[1], i[2] - (3 * i[7]), i[3], i[4], i[5])

                if i[7] and mouseDown:
                    i[7] = False
                    if i[6] == 'continue':
                        screen = 'game'
                        mouseCursor = 'none'
                    elif i[6] == 'leave':
                        screen = 'mainMenu'
                        mouseCursor = 'arrow'
        elif screen == 'lost':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseDown = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen = 'mainMenu'
                        mouseCursor = 'hand'

            temp8 = pygame.Surface((displayw, displayh), pygame.SRCALPHA)
            temp8.fill((96, 96, 96, 128))
            gameDisplay.blit(temp8, (0, 0))

            mouseCursor = 'arrow'

            if t // 60 > pb // 60:
                temp11 = str(t // 3600)  # mins
                temp12 = (t // 60) % 60  # secs
                temp12 = '0' + str(temp12) if 0 <= temp12 <= 9 else str(temp12)
                drawText('Time Survived ' + temp11 + ':' + temp12 + ' | New Personal Best!', displayw / 2, 340, 32,
                         black,
                         'center')
            else:
                temp11 = str(t // 3600)  # mins
                temp12 = (t // 60) % 60  # secs
                temp12 = '0' + str(temp12) if 0 <= temp12 <= 9 else str(temp12)
                temp13 = str(pb // 3600)  # mins
                temp14 = (pb // 60) % 60  # secs
                temp14 = '0' + str(temp14) if 0 <= temp14 <= 9 else str(temp14)
                drawText('Time Survived ' + temp11 + ':' + temp12 + ' | Personal Best ' + temp13 + ':' + temp14,
                         displayw / 2, 340, 32, black, 'center')

            for i in lostButtons:
                if i[6] != '' and i[5] == 'center':
                    temp7 = pygame.font.SysFont('Comic Sans MS', i[3]).render(i[0], True, i[4]).get_rect(
                        center=(i[1], i[2]))
                    i[7] = temp7.collidepoint(mouseX, mouseY)
                    if i[7]:
                        mouseCursor = 'hand'

                drawText(i[0], i[1], i[2] - (3 * i[7]), i[3], i[4], i[5])

                if i[7] and mouseDown:
                    i[7] = False
                    if i[6] == 'restart':
                        resetGame()
                    elif i[6] == 'leave':
                        screen = 'mainMenu'
                        mouseCursor = 'arrow'

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
