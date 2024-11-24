import pygame
import math
import random
import asyncio

async def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    player_turn = 1
    dt = 0
    GRAVITY = 2
    windwandy = (random.random() - 0.5) *2
     
    ground_hits = []

    ball_pos = pygame.Vector2(0, 0)
    ball_speed_x = 0
    ball_speed_y = 0
    ball_visible = False

    cannon1_x = 40
    cannon2_x = 840
    cannon_angle1 = math.pi / 3
    cannon_angle2 = math.pi*2 / 3

    def cannon_draw(x, cannon_end_x, cannon_end_y):
        pygame.draw.arc(screen, "black", (x,550,60,60), 0, math.pi)
        pygame.draw.line(screen, "black", (x+30,580),(cannon_end_x, cannon_end_y), 3)

    def switch_turn(player_turn):
        if player_turn == 1:
            return  2
        else:
            return 1


    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.set_caption('Player '+str(player_turn)+' wind:'+str(windwandy))


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("blue")

        pygame.draw.rect(screen, "green", (0, 500, 1280,720))


        for pos in ground_hits:
            pygame.draw.circle(screen, "black", (pos), 7)
        

        cannon1_end_x = cannon1_x+30 + 60 * math.cos(cannon_angle1)
        cannon1_end_y = 580 + 60 * math.sin(cannon_angle1)*-1

        cannon2_end_x = cannon2_x+30 + 60 * math.cos(cannon_angle2)
        cannon2_end_y = 580 + 60 * math.sin(cannon_angle2)*-1

        cannon_draw(cannon1_x, cannon1_end_x, cannon1_end_y)
        cannon_draw(cannon2_x, cannon2_end_x, cannon2_end_y)

        if ball_visible:
            pygame.draw.circle(screen, "red", ball_pos, 3)
            ball_speed_y = ball_speed_y + GRAVITY*dt
            ball_speed_x = ball_speed_x + windwandy*dt
            ball_pos = pygame.Vector2(ball_pos.x+ball_speed_x, ball_pos.y+ball_speed_y)

            pygame.draw.rect(screen, "pink", (cannon2_x, 550, 60, 30), 3)
            pygame.draw.rect(screen, "pink", (cannon1_x, 550, 60, 30), 3)
            
            if ball_pos.x < 0 or ball_pos.x > 1280 or ball_pos.y > 600:
                player_turn = switch_turn(player_turn)
                windwandy = (random.random() - 0.5) *2
                ball_visible = False

            if ball_pos.y > 600:
                ground_hits.append(ball_pos)

            if ball_pos.y > 550 and ball_pos.x > (cannon2_x) and ball_pos.x < (cannon2_x + 60):
                screen.fill("red")

            if ball_pos.y > 550 and ball_pos.x > (cannon1_x) and ball_pos.x < (cannon1_x + 60):
                screen.fill("red")
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            ball_visible = True
            if player_turn == 1:
                ball_speed_x = 350 * math.cos(cannon_angle1) * dt
                ball_speed_y = (350 * math.sin(cannon_angle1)*-1)* dt
                ball_pos = pygame.Vector2(cannon1_end_x, cannon1_end_y)
            else:
                ball_speed_x = 350 * math.cos(cannon_angle2) * dt
                ball_speed_y = (350 * math.sin(cannon_angle2)*-1)* dt
                ball_pos = pygame.Vector2(cannon2_end_x, cannon2_end_y)

        if keys[pygame.K_a]:
            cannon_angle1 += 0.5 * dt
        if keys[pygame.K_d]:
            cannon_angle1 -= 0.5 * dt

        if keys[pygame.K_j]:
            cannon_angle2 += 0.5 * dt
        if keys[pygame.K_l]:
            cannon_angle2 -= 0.5 * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)

asyncio.run(main())

pygame.quit()

