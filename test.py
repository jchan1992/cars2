#!/usr/bin/python

# load functions and classes from gamefunc
from gamefunc import *  
from classes import * 

# if __name__ == '__main__':
#     main()

#game intro screen
def gameintro(screen,clock):
    timer = 0
    time1 = pygame.time.get_ticks()
    #screen.fill(white)
    intromenu(screen)
    while timer <= 2000:
            time2 = pygame.time.get_ticks()
            timer = time2-time1
            for event in pygame.event.get():
                    print(event)
                    if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                    pygame.quit()
                                    quit()
                            if event.key == pygame.K_s:
                                    timer = 5001
            print(time1,time2,timer)

def pauseloop(screen,pause_game):
    while pause_game == True:
        print("paused")
        pausemenu(screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_u:
                    pause_game = False              

def gameloop(screen,clock):
    #game states
    end_game = False
    pause_game = False
    restart = False
    paused = False
    
    time = 0
    time1 = pygame.time.get_ticks()
    
    #set score counter
    score = 0
    
    #set speed threshold to adjust speed
    speedthresh = 1
    
    #set dodge counter
    dodged = 0
    
    #set drop speed
    speed = 3
    resume_speed = 3
    #instantiate car objects
    car11 = car1()
    car22 = car2()
    
    #instantiate coin objects
    coin11 = coin1()
    coin22 = coin2()
    
    #coin release
    coin11r = random.randint(0,1)
    coin22r = random.randint(0,1)

    while not end_game:
        #random timer
        time2 = pygame.time.get_ticks()
        time = time2-time1
        if time > 250:
            time = 0
            time1 = pygame.time.get_ticks()
            
        #speed adjustment
        if score >= speedthresh:
            speed = speed + 1
            resume_speed = speed
            speedthresh = speedthresh*5    
        
        #print(time,coin11r,coin22r,speed,speedthresh,score)

        clock.tick(60)

        #draw background
        displaygameboard(screen)
        
        #draw car
        screen.blit(car11.image,car11.loc)
        screen.blit(car22.image,car22.loc)
        
        #draw coins
        if coin11r == 1 and coin11.y <= displayh:
            screen.blit(coin11.image,coin11.loc)
            coin11.update(speed)
        elif time < 5:
            coin11r = random.randint(0,1)
            if coin11r ==1:
                coin11 = coin1()    
            
        if coin22r == 1 and coin22.y <= displayh:
            screen.blit(coin22.image,coin22.loc)
            coin22.update(speed)
        elif time < 5:
            coin22r = random.randint(0,1) 
            if coin22r == 1:
                coin22 = coin2()
        
        #update score
        #detect coin collection
        if coin11.x == car11.x and coin11.y > (car11.y-100) and coin11.y < car11.y:
            score = score + 1
            coin11.y = displayh + 1
        elif coin11.x is not car11.x and coin11.y > (car11.y-100) and coin11.y < car11.y :
            displaymissed(screen)
            end_game = True 
        if coin22.x == car22.x and coin22.y > (car22.y-100) and coin22.y < car22.y:
            score = score + 1
            coin22.y = displayh + 1
        elif coin22.x != car22.x and coin22.y > (car22.y-100) and coin22.y < car22.y:
            displaymissed(screen)
            end_game = True

        displaydodged(screen,dodged)
        displayscore(screen,score)
        displayfps(screen,clock)
        pygame.display.update()    
        
        #keyboard inputs
        for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                        end_game = True
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                                end_game = True
                        if event.key == pygame.K_p:
                                pause_game = True
                                pauseloop(screen,pause_game)
                        if event.key == pygame.K_LEFT:
                                car11.update()
                                screen.blit(car11.image,car11.loc)
                        if event.key == pygame.K_RIGHT:
                                car22.update()
                                screen.blit(car22.image,car22.loc)
                        if event.key == pygame.K_UP:
                                displaycrash(screen)
                                end_game = True


    if end_game == True:
        print("end_game = TRUE")
        while not restart:
            restartmenu(screen,score)
            for event in pygame.event.get():
                    print(event)
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                    quitgame()
                            if event.key == pygame.K_r:
                                    gameloop(screen,clock)


#main game loop
def main():
    #instantiate surface
    pygame.init()
    
    #instantiate clock
    clock = pygame.time.Clock()
    
    #set screen size
    screen = pygame.display.set_mode((displayw,displayh))
    pygame.display.set_caption("CARS")
    pygame.mixer.music.load('initiald.mid')
    pygame.mixer.music.play(-1)

    gameintro(screen,clock)
    gameloop(screen,clock)
    
    quitgame()

main()
