import pygame, random, threading, pygame.freetype, time, datetime

def main():

    #Iniciar o pygame
    pygame.init()

    res = (1275, 720)
    screen = pygame.display.set_mode(res)

    y = 0

    while(True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()

        screen.fill((0,0,20))

        #Desenhar o menu de inicio de jogo e colocar as posições das opções numa variável
        menu_pos = begining(screen,y)

        #Recebe o eixo y da posição do rato para detetar se o cursor se encontra por cima de alguma opção alterando a cor da opção para branco (quando desenhada na função acima)
        y = start_game(screen, menu_pos)

        #Se o utilizador clicar numa das opções o ciclo quebra, prosseguindo para um novo ciclo onde se randomizam as imagens nas posições da dificuldade escolhida
        if event.type == pygame.MOUSEBUTTONDOWN:
            y = start_game(screen, menu_pos)

            if y != 0:
                #Se a opção escolhida for EXIT o programa termina
                if y >= 520:
                    exit()

                screen.fill(pygame.Color("blue"))
                break
        else:
            continue


    #setpos é um set que recebe
    setpos = start_board(screen, y)
    #
    click_pos, click_form, click_color, click_fill = randomizer(setpos)


    while(True):
        for event in pygame.event.get():

            ans = "none"

            if (event.type == pygame.QUIT):
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                draw_format(screen, click_pos, click_form, click_color, click_fill)
                coord = pair_click(screen, click_pos, ans)

                if coord != 0:

                    timer = threading.Timer(1.0, timed_out, (screen, coord))
                    timer.start()
                    startime = time.monotonic()
                    while(startime < 1.0):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            coord2 = pair_click(screen, click_pos, coord)

                            if coord2 == 0:
                                while(coord2 == 0):
                                    coord2 = pair_click(screen, click_pos, coord)

                            if coord2 != "pair":

                                while(startime < 1.0):
                                    continue
                                timed_out (screen, coord2)

                            else:
                                while(startime< 1.0):
                                    continue

                        else:
                            continue
                else:
                    continue



def begining(screen,y1):

    #Procura as imagens e fonte
    image = pygame.image.load("D:/python/trabalho final python/shuffle.png")
    my_font = pygame.freetype.Font("D:/python/trabalho final python/NotoSans-Regular.ttf", 24)

    #Posições onde se desenham os retângulos das opções do menu, array com a escrita dentro dos rectângulos e variável que determina qual elemento do array se coloca dentro de cada rectângulo
    menu_pos = [(547.5, 285, 180, 33),(547.5, 330, 180, 33), (547.5, 375, 180, 33), (547.5, 420, 180, 33), (547.5, 465, 180, 33), (547.5, 520, 180, 33)]
    escrita = ["4x3","4x4","5x4","6x5","6x6","Exit"]
    k = 0

    #Para cada posição desenha o retângulo e escreve a opção
    for i in menu_pos:

        x,y2,l,a = i
        a = y2 + a/4

        #Verifica se o utilizador tem o rato por cima de uma opção e se sim torna a opção branca
        if y2 == y1:
            pygame.draw.rect(screen, pygame.Color("white"), i, 4)
            my_font.render_to(screen, (617.5, a), escrita[k], (255, 255, 255))

        #Caso contrário desenha a amarelo
        else:
            pygame.draw.rect(screen, pygame.Color("yellow"), i, 4)
            my_font.render_to(screen, (617.5, a), escrita[k], (255, 255, 0))

        k += 1

    screen.blit(image, (237.5, 25))
    pygame.display.flip()

    return menu_pos

def start_game(screen, menu_pos):

    #Coordenadas do rato
    m_x, m_y = pygame.mouse.get_pos()

    #Deteta se o rato está por cima de alguma opção do menu e se sim retorna y
    for i in menu_pos:
        x,y,l,a = i
        l += x
        a += y
        if (m_x >= x and m_x <= l and m_y >= y and m_y <= a):
            screen.fill((0,0,20))
            return y
    return 0

def start_board(screen, y):

    #Valor base  do número de cartas em jogo horizontalmente e verticalmente
    hor = 4
    vert = 4

    #Define setpos antes de lhe adicionar elementos
    setpos = set()

    #Verifica o y recebido (que corresponde á altura da opção selecionada no menu) e altera o número das cartas de acordo com a opção escolhida
    if y < 330:
        vert = 3
    elif y >= 330 and y < 375:
        pass
    elif y >= 375 and y < 420:
        hor = 5
    elif y >= 420 and y < 465: 
        hor = 6
        vert = 5
    else:
        hor = 6
        vert = 6

    #Largura e altura das cartas 

    # A largura varia de modo a que a soma da largura de todas as cartas reunidas corresponda a um terço da largura do ecrã
    lar = 1275 / (hor * 3)
    # A altura varia de modo a que a soma da altura delas corresponda a dois terços da altura do ecrã
    alt = 720 / (vert * 1.5)

    #Coordenadas X e Y iniciais das cartas

    #Coordenada X é calculada como um terço do ecrã (a largura das cartas reunidas) menos metade dos espaços entre cartas (a outra metade fica no espaço livre á direita do ecrâ para fins de simetria)
    start_x = lar * hor - hor * 10 / 2
    #Coordenada Y é calculada como metade do terço restante de espaço (3/3- 2/3 = 1/3, 1/3/2 = 1/6 == 0.25 * 2/3) ocupado pelas cartas no ecrã (a altura das cartas reunidas) menos metade dos espaços entre cartas (a outra metade fica no espaço livre abaixo do ecrâ para fins de simetria)
    start_y = alt * (0.25 * vert) - vert * 10 / 2

    previous_y = start_y - (alt + 10) - (alt + 10)

    #Funções que calculam os próximos X e Y das cartas após adicionar um espaço aberto (o intervalo 10) entre elas
    next_x = lambda previous_x, lar : previous_x + lar + 10
    next_y = lambda previous_y, alt : previous_y + alt + 10

    for i in range(0, vert):

        previous_y = next_y(previous_y, alt)
        previous_x = start_x - (lar + 10)

        for i in range(0,hor):

            setpos.add((next_x(previous_x, lar), next_y(previous_y, alt), lar, alt))
            previous_x = next_x(previous_x, lar)

    for i in setpos:

        pygame.draw.rect(screen, pygame.Color("yellow"),i, 0)
        pygame.display.flip()

    return setpos

def randomizer( old_setpos):

    click_pos = list()
    click_form = list()
    click_color = list()
    click_fill = list()
    setcolor = {(0,0,0), (0, 255, 0, 255), (0, 229, 238, 255), (139, 90, 0, 255), (178, 34, 34, 255)}
    setform = {"rect", "circle", "triangle"}
    tupfill = (0,7)
    no_rep = set()
    setpos = list(old_setpos)
    k = 0
    while (setpos):
        for i in setpos:
            while (True):
                randcolor = random.choice(tuple(setcolor))
                randform = random.choice(tuple(setform))
                randpos = random.choice(tuple(setpos))
                randfill = random.choice(tupfill)
                if ((randcolor, randform, randfill) in no_rep):
                    continue
                else:
                    break

            while(randpos == i):
                randpos = random.choice(tuple(setpos))

            click_pos.append(chr(97 + k))
            click_pos.append(98 + k)
            click_pos[k] = i
            click_pos[k+1] =  randpos
            click_form.append(chr(97 + k))
            click_form.append(98 + k)
            click_form[k] = randform
            click_form[k+1] =  randform
            click_color.append(chr(97 + k))
            click_color.append(98 + k)
            click_color[k] = randcolor
            click_color[k+1] = randcolor
            click_fill.append(chr(97 + k))
            click_fill.append(98 + k)
            click_fill[k] = randfill
            click_fill[k+1] = randfill
            k += 2
            no_rep.add((randcolor, randform, randfill))
            setpos.remove(i)
            setpos.remove(randpos)
            
    return click_pos, click_form, click_color, click_fill

def draw_format(screen, click_pos, click_form, click_color, click_fill):

    k = 0
    f = 0

    for  i in click_pos:

        x, y, l, a = i

        pygame.draw.rect(screen, pygame.Color("white"), i, 0)

        #  Nos ciclos if seguintes são usadas variáveis de posicionamento dos pontos das formas
        #  Usando as localizações do quadrado base em que se encontram para obter uma imagem centrada

        if (click_form[k] == "rect"):

            # Uma vez que o quadrado base varia entre as localizações selecionadas, x e y vão variar entre eles
            # Atribuí 1 e 2 à frente das variáveis para distinguir quais pertencem a qual quadrado base
            # Alterei-lhes o valor para que quando desenhadas na função se posicionacem no centro

            x += l / 4
            y += a / 4
            l -=  l / 2
            a -=  a / 2

            pygame.draw.rect(screen, click_color[k],(x,y,l,a), click_fill[k])

        elif (click_form[k] == "circle"):
            x += l / 2
            y += a / 2
            l =  l / 4

            pygame.draw.circle(screen, click_color[k], (int(x), int(y)), int(l), click_fill[k])


        else:
            # Precisei de variáveis extra uma vez que são necessários 3 'x' e 2 'y' diferentes por quadrado
            # Para as distinguir e manter a distinção entre quadrados, adicionei b à frente e realizei os cálculos
            # A ordem pode parecer aleatória mas é necessária para que não se alterem as váriáveis necessárias antes de os cálculos que as involvem serem concluídos
            # x3 e y(1,2) correspondem ao x centrado do ponto no topo, os restantes aos pontos de baixo
            
            x3 = x + l / 2
            xb = x + 3 * l / 4
            x += l / 4
            yb = y + a / 4
            y += 3 * a / 4

            pygame.draw.polygon(screen, click_color[k], [(int(x), int(y)),(int(xb), int(y)), (int(x3), int(yb))], click_fill[k])

        k += 1
        f += k // 2



def pair_click(screen, click_pos, ans):

    m_x, m_y = pygame.mouse.get_pos()
    k = 0

    for i in click_pos:
        x,y,l,a = i
        l += x
        a += y

        if (m_x >= x and m_x <= l and m_y >= y and m_y <= a):

            pygame.display.update(i)

            if k % 2 == 0:
                if ans != click_pos[k+1]:
                    return i
                else:
                    return "pair"
            else:
                if ans != click_pos[k-1]:
                    return i
                else:
                    return "pair"
            k += 1
    return 0


def timed_out(screen, rect_coord):

    pygame.draw.rect(screen, pygame.Color("yellow"), rect_coord, 0)
    pygame.display.update(rect_coord)


def right_ans():

    return 0

main()