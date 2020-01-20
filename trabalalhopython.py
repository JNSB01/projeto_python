import pygame
import pygame.freetype

def main():

    pygame.init()

    res = (1275, 720)
    screen = pygame.display.set_mode(res)
    while(True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
        
        screen.fill((0,0,20))
        a = begining(screen)
    

def begining(screen):
    
    menu_pos = {(547.5, 285, 180, 33),(547.5, 330, 180, 33), (547.5, 375, 180, 33), (547.5, 420, 180, 33), (547.5, 465, 180, 33), (547.5, 520, 180, 33)}
    image = pygame.image.load("shuffle.png")
    my_font = pygame.freetype.Font("NotoSans-Regular.ttf", 24)

    for i in menu_pos:
        pygame.draw.rect(screen, pygame.Color("yellow"), i, 4)
        
    my_font.render_to(screen, (617.5, 290), "4x3", (255, 255, 0))
    my_font.render_to(screen, (617.5, 335), "4x4", (255, 255, 0))
    my_font.render_to(screen, (617.5, 380), "5x4", (255, 255, 0))
    my_font.render_to(screen, (617.5, 425), "6x5", (255, 255, 0))
    my_font.render_to(screen, (617.5, 470), "6x6", (255, 255, 0))
    my_font.render_to(screen, (617.5, 525), "Exit", (255, 255, 0))
    screen.blit(image, (237.5, 25))
    pygame.display.flip()

    return menu_pos

main()


def randomizer(screen, setpos):

    clickvars = []
    arraycolor = {sq1, sq2, }
    arrayform = {rect, circle, triangle}

    k = 0
    for i in setpos:
        randcolor = random number 0-len(number colors)
        randform = random number 0-len(number forms)
        randpos = random number 1-len(number pos)
        
        pygame.draw.rect(screen, pygame.Color("black"),setpos[randpos], 0)
        pygame.draw.rect(screen, pygame.Color("black"),setpos[i], 0)

        clickvars.append(chr(97 + k))
        clickvars.append(98 + k)
        a1,b1,c1,d1 = setpos[i] 
        a2,b2,c2,d2 = setpos[randpos]
        if (randform == rect):
            a1 += 25 
            a2 += 25
            b1 += 30
            b2 += 25
            c1 -= 50
            c2 -= 25
            d1 -= 40
            d2 -= 50
        clickvars[k] = setpos[i] 
        clickvars[k+1] =  setpos[randpos]
        k += 2
       
        

        pygame.draw.polygon(screen, )
        setpos[i].remove()
        setpos[randpos].remove()

main()
