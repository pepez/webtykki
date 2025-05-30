import pygame
import math
import random
import asyncio

async def main():
    # pygame setup
    pygame.mixer.pre_init(44100, 16, 2, 4096)
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
    cannon2_x = 1140
    cannon_angle1 = math.pi / 3
    cannon_angle2 = math.pi*2 / 3

    score1 = 0
    score2 = 0
    red_power = 100
    red_power_change = 5

    flag_wave = 0
    game_time = 60
    game_time_lock = 0 
    game_play = 0 # 0 = ajan säätö, 1 = peli, 2 = game over

    
    global font
    font=pygame.font.Font(None,50)

    cannon_sound = pygame.mixer.Sound("cannon-shot.wav")
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    ground_hit_sound = pygame.mixer.Sound("distant-explosion.wav")

    def cannon_draw(x, cannon_end_x, cannon_end_y):
        #pygame.draw.arc(screen, "black", (x,550,60,60), 0, math.pi)
        pygame.draw.line(screen, (50,50,50), (x+30,580),(cannon_end_x, cannon_end_y), 5)
        pygame.draw.circle(screen, (50,50,50), (x+30,580),30)
        pygame.draw.rect(screen, "black", (x-5, 580, 70,30))

    def switch_turn(player_turn):
        if player_turn == 1:
            return  2
        else:
            return 1

    # Turn
    def turn_triangle(tx, red_power):
        triangle_vertices = [(tx, 620),(tx-20, 640),(tx+20, 640)]
        pygame.draw.polygon(screen, (red_power, 0, 0), triangle_vertices)  


    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.set_caption('Player '+str(player_turn)+' wind:'+str(windwandy))


        # fill the screen with a color to wipe away anything from last frame
        screen.fill((22,130,250))

        pygame.draw.rect(screen, (80,200,0), (0, 500, 1280,720))


        for pos in ground_hits:
            pygame.draw.ellipse(screen, (150,80,0), (pos.x-20, pos.y, 40,18))
        
        for pos in ground_hits:
            pygame.draw.ellipse(screen, (60,40,0), (pos.x-15, pos.y+2, 30,14))

        for pos in ground_hits:
            pygame.draw.ellipse(screen, "black", (pos.x-8, pos.y+3, 16,10))
        

        cannon1_end_x = cannon1_x+30 + 60 * math.cos(cannon_angle1)
        cannon1_end_y = 580 + 60 * math.sin(cannon_angle1)*-1

        cannon2_end_x = cannon2_x+30 + 60 * math.cos(cannon_angle2)
        cannon2_end_y = 580 + 60 * math.sin(cannon_angle2)*-1

        cannon_draw(cannon1_x, cannon1_end_x, cannon1_end_y)
        cannon_draw(cannon2_x, cannon2_end_x, cannon2_end_y)

        # Wind flag
        pygame.draw.line(screen, "black", (640,590),(640, 450), 3)


        flag_wave += 0.1
        flag_edge_x = 640 + windwandy * 60
        flag_edge_y = (1 - abs(windwandy)) * 40 + math.sin(flag_wave)*5*abs(windwandy)
        flag_vertices = [(640, 450),(640, 490),(flag_edge_x + math.cos(flag_wave*2)*3, 480+flag_edge_y), (flag_edge_x + math.cos(flag_wave)*2, 460+flag_edge_y)]
        pygame.draw.polygon(screen, "yellow", flag_vertices) 



        if ball_visible:
            pygame.draw.circle(screen, "red", ball_pos, 3)
            ball_speed_y = ball_speed_y + GRAVITY*dt
            ball_speed_x = ball_speed_x + (windwandy/2)*dt
            ball_pos = pygame.Vector2(ball_pos.x+ball_speed_x, ball_pos.y+ball_speed_y)

            #pygame.draw.rect(screen, "pink", (cannon2_x, 550, 60, 30), 3)
            #pygame.draw.rect(screen, "pink", (cannon1_x, 550, 60, 30), 3)
            
            ball_hit = False

            if ball_pos.x < 0 or ball_pos.x > 1280 or ball_pos.y > 600:
                ball_hit = True

            if ball_pos.y > 600:
                ball_hit = True
                pygame.mixer.Sound.play(ground_hit_sound)
                ground_hits.append(ball_pos)

            if ball_pos.y > 550 and ball_pos.x > (cannon2_x) and ball_pos.x < (cannon2_x + 60):
                ball_hit = True
                pygame.mixer.Sound.play(explosion_sound)
                score1 = score1 + 1
                screen.fill("red")

            if ball_pos.y > 550 and ball_pos.x > (cannon1_x) and ball_pos.x < (cannon1_x + 60):
                ball_hit = True
                pygame.mixer.Sound.play(explosion_sound)
                score2 = score2 + 1
                screen.fill("red")

            if ball_hit:
                ball_visible = False
                player_turn = switch_turn(player_turn)
                windwandy = (random.random() - 0.5) *2
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and ball_visible == False and (game_play == 0 or game_play == 1):
            ball_visible = True
            
            if (game_play == 0):
                game_play = 1
            
            pygame.mixer.Sound.play(cannon_sound)

            if player_turn == 1:
                ball_speed_x = 350 * math.cos(cannon_angle1) * dt
                ball_speed_y = (350 * math.sin(cannon_angle1)*-1)* dt
                ball_pos = pygame.Vector2(cannon1_end_x, cannon1_end_y)
            else:
                ball_speed_x = 350 * math.cos(cannon_angle2) * dt
                ball_speed_y = (350 * math.sin(cannon_angle2)*-1)* dt
                ball_pos = pygame.Vector2(cannon2_end_x, cannon2_end_y)

        if keys[pygame.K_a] and cannon_angle1 < math.pi:
            cannon_angle1 += 0.5 * dt
        if keys[pygame.K_d] and cannon_angle1 > 0:
            cannon_angle1 -= 0.5 * dt
        if keys[pygame.K_j] and cannon_angle2 < math.pi:
            cannon_angle2 += 0.5 * dt
        if keys[pygame.K_l] and cannon_angle2 > 0:
            cannon_angle2 -= 0.5 * dt
        if keys[pygame.K_y] and game_time_lock <= 0:
            score1 = 0
            score2 = 0
            player_turn = 1
            ground_hits = []
            cannon_angle1 = math.pi / 3
            cannon_angle2 = math.pi*2 / 3
            windwandy = (random.random() - 0.5) *2
            ball_visible = False
            game_play = 0
            game_time = 60
            game_time_lock = 1

        if keys[pygame.K_u] and game_play == 0 and game_time > 60 and game_time_lock <= 0:
            game_time = game_time - 60
            game_time_lock = 0.2
        if keys[pygame.K_i] and game_play == 0 and game_time_lock <= 0:
            game_time = game_time + 60    
            game_time_lock = 0.2


        if (game_play == 0):
            textpos = pygame.Vector2(460, 50)
            color=(255,255,255)
            screen.blit(font.render("Next player",True,color),textpos)
        if (game_play == 1):
            # Score text
            textpos = pygame.Vector2(460, 50)
            color=(255,255,255)
            screen.blit(font.render("SCORE",True,color),textpos)
            textpos = pygame.Vector2(500, 90)
            screen.blit(font.render(str(score1)+" - "+str(score2),True,color),textpos)
        if (game_play == 2):
            # Score text
            textpos = pygame.Vector2(460, 50)
            color=(255,255,255)
            screen.blit(font.render("Game Over - SCORE",True,color),textpos)
            textpos = pygame.Vector2(500, 90)
            screen.blit(font.render(str(score1)+" - "+str(score2),True,color),textpos)

        # Time text
        if (game_play == 0 or game_play == 1):
            textpos = pygame.Vector2(800, 50)
            color=(255,255,255)
            screen.blit(font.render("Time left",True,color),textpos)
            textpos = pygame.Vector2(800, 90)
            seconds = math.floor(game_time % 60)
            minutes = math.floor(game_time / 60)
            screen.blit(font.render(str(minutes)+" : "+str(seconds),True,color),textpos)

        # Player turn marker
        red_power = red_power + red_power_change
        if (red_power > 250):
            red_power_change = -5
        if (red_power < 100):
            red_power_change = 5

        if player_turn == 1:
            turn_triangle(cannon1_x+30, red_power)
        else:
            turn_triangle(cannon2_x+30, red_power)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

        if (game_play == 1):
            game_time = game_time - dt

        if (game_time < 0):
            game_play = 2

        if (game_time_lock > 0):
            game_time_lock = game_time_lock - dt

        await asyncio.sleep(0)

asyncio.run(main())

pygame.quit()
