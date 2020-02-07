import pygame, random, threading, pygame.freetype, time, datetime

def main():

    #Iniciar o pygame
    pygame.init()

    res = (1275, 720)
    screen = pygame.display.set_mode(res)
    my_font = pygame.freetype.Font("D:/python/trabalho final python/NotoSans-Regular.ttf", 38)


    while(True):
        exit_menu = False
        y = 0
        cycle = 0
        opt_moused = 0
        dific_moused = 0
        y2 = 0
        opt_selected = False
        screen.fill((0,0,20))
        pygame.display.flip()

        #Ciclo do primeiro menu que ocorre até uma opção ser selecionada
        while(opt_selected == False):

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exit()

                #Desenha o menu de inicio de jogo e coloca as posições das opções e a última posição branca em variáveis
                menu_pos, opt_moused = begining(screen,y, cycle, opt_moused)

                #Recebe o eixo y da posição do rato para detetar se o cursor se encontra por cima de alguma opção alterando a cor da opção para branco (quando desenhada na função acima)
                y = next_menu(screen, menu_pos)

                #Se o utilizador clicar numa das opções o ciclo quebra, prosseguindo para um novo ciclo onde se escolhe a dificuldade
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if y != 0:
                        #Se a opção escolhida for EXIT o programa termina
                        if y >= 520:
                            exit()

                        #Caso a opção não seja exit o ambiente fica preto e prossegue para o menu dificuldade
                        screen.fill(pygame.Color("black"))
                        opt_selected = True
                        break

                cycle = 1

        opt_selected = False
        cycle = 0

        #Ciclo do menu da dificuldade que ocorre até uma opção ser selecionada
        while(opt_selected == False):

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exit()

                #Desenha o menu de dificuldade e coloca as posições das opções e a última posição branca em variáveis
                second_menu_pos, dific_moused = dificulty_mode(screen, y2, cycle, dific_moused)

                #Recebe o eixo y da posição do rato para detetar se o cursor se encontra por cima de alguma opção alterando a cor da opção para branco (quando desenhada na função acima)
                y2 = start_game(screen, second_menu_pos)

                #Se o utilizador clicar numa das opções o ciclo quebra, prosseguindo para um novo ciclo onde se randomizam as imagens nas posições escolhidas no primeiro menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if y2 != 0:
                        opt_selected = True
                        #Se a opção escolhida for EXIT volta ao menu anterior
                        if y2 >= 530:
                            exit_menu = True
                            screen.fill((0,0,20))
                            break

                        #Caso a opção não seja exit o ambiente fica azul e prossegue para o jogo
                        screen.fill(pygame.Color("blue"))
                        break
                cycle = 1

        #setpos é um set que recebe as posições das cartas para serem desenhadas
        setpos = start_board(screen, y)

        #Randomiza o conteúdo das cartas
        click_pos, click_form, click_color, click_fill = randomizer(setpos)

        cycle = 0
        mouse_on_card = 0
        already_used = []
        k = 0
        exit_selected = 0
        card_selected = 0
        score = 0
        penalização = 0

        #Ciclo de jogo que ocorre até a opção exit ser selecionada
        while(exit_menu == False):

            EXIT = False

            for event in pygame.event.get():

                #Desenha o exterior das cartas e o exit
                E,X,I,T, white_card, exit_selected, card_selected = mouse_card(screen, setpos, cycle, mouse_on_card, exit_selected, card_selected)

                #Desenha o score
                pontuação(screen, cycle, score, penalização)

                #Desenha o conteúdo das cartas
                draw_format(screen, click_pos, click_form, click_color, click_fill)

                m_x, m_y = pygame.mouse.get_pos()
                cycle = 1
                coord = 0
                pair_not_chosen = True

                if (event.type == pygame.QUIT):
                    exit()

                #Grava o conteúdo da variável white_card na mouse_card
                if (white_card != 0):
                    mouse_on_card = white_card

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Se exit for selecionada volta para o primeiro menu
                    if (m_x >= E and m_x <= I and m_y >= X and m_y <= T):
                        EXIT = True
                        break

                    #Verifica se alguma das cartas foi selecionada e se sim retorna coord (variável que afirma se o clique foi numa carta), e as características da carta
                    coord, first_pos, pair_form, pair_color, pair_fill = first_click(screen, click_pos, click_form, click_color, click_fill, already_used)

                    #Se a carta selecionada já tiver sido parte de um par resolvido coord volta a ser 0
                    if (first_pos in already_used):
                        coord = 0
                    #Caso contrário vira-se a carta
                    elif (coord != 0):
                        pygame.display.update(first_pos)

                if coord != 0:
                    mouse_on_card = 0

                    #Timer que dependendo da dificuldade dá um limite de tempo para o jogador selecionar o par
                    startime = time.time()

                    while(pair_not_chosen):

                        endtime = time.time()
                        estime = endtime - startime

                        times_out = time_to_choose(screen, first_pos, estime, y2)
                        if (times_out == 1):
                            if score > 0:
                                cycle = 0
                                score = pontuação(screen, cycle, score, penalização)
                                penalização += 1
                                cycle = 1
                            break

                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                coord2, pair_pos = pair_click(screen, click_pos, first_pos, pair_form, pair_color, pair_fill, click_form, click_color, click_fill, already_used)

                                if (pair_pos in already_used):
                                    coord2 = 0
                                elif (coord2 != 0):
                                    pygame.display.update(pair_pos)

                                if coord2 == 0:
                                    continue

                                elif coord2 != "pair":
                                    pair_not_chosen = False
                                    if score > 0:
                                        cycle = 0
                                        score = pontuação(screen, cycle, score, penalização)
                                        penalização += 1
                                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                                    time_to_memorise(screen, first_pos, y2)
                                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

                                    timed_out(screen, first_pos)
                                    timed_out (screen, pair_pos)

                                else:

                                    if ((pair_pos in already_used) or (pair_pos == first_pos)):
                                        continue
                                    else:
                                        already_used.append(first_pos)
                                        already_used.append(pair_pos)
                                        pair_not_chosen = False
                                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                                        time_to_memorise(screen, first_pos, y2)
                                        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                                        penalização = 0
                                        score += 100
                                        cycle = 0
                                        pontuação(screen, cycle, score, penalização)

                                        #Remove as posições dos sets
                                        if first_pos in setpos:
                                            setpos.remove(first_pos)
                                        if pair_pos in setpos:
                                            setpos.remove(pair_pos)

                                        if bool(setpos) == False:
                                            screen.fill((0,0,20))
                                            my_font.render_to(screen, (490,310), "Congratulations!", (255, 255, 255))
                                            pygame.display.flip()
                                            exit_selected = 1
                                            my_font.render_to(screen, (40, 40), ('Score: ' + str(score)), (255, 255, 0))
                                            pygame.display.update((30, 30, 200, 100))
                                            cycle = 1
                                            break

                                        right_ans(screen, first_pos)
                                        right_ans(screen, pair_pos)
                                        k += 2

                                cycle = 1

            if EXIT == True:
                break



def begining(screen,y1, cycle, opt_moused):

    #Procura as imagens e fonte
    image = pygame.image.load("D:/python/trabalho final python/shuffle.png")
    my_font = pygame.freetype.Font("D:/python/trabalho final python/NotoSans-Regular.ttf", 24)

    #Posições onde se desenham os retângulos das opções do menu, array com a escrita dentro dos rectângulos e variável que determina qual elemento do array se coloca dentro de cada rectângulo
    menu_pos = [(547.5, 285, 180, 33),(547.5, 330, 180, 33), (547.5, 375, 180, 33), (547.5, 420, 180, 33), (547.5, 465, 180, 33), (547.5, 520, 180, 33)]
    escrita = ["4x3","4x4","5x4","6x5","6x6","Exit"]
    k = 0
    #Criei uma segunda variável uma vez que se corria o risco de mudar a variável antes de atualizar a carta anterior que se tornou branca
    opt_moused2 = opt_moused

    #Para cada posição desenha o retângulo e escreve a opção
    for i in menu_pos:

        x,y2,l,a = i
        a = y2 + a/4

        #Fiz com que apenas desenhá-se na primeira vez para reduzir o número de sobreposições de imagem
        if (cycle == 0):
            pygame.draw.rect(screen, pygame.Color("yellow"), i, 4)
            my_font.render_to(screen, (617.5, a), escrita[k], (255, 255, 0))

        #Verifica se o utilizador tem o rato por cima de uma opção e se sim torna a opção branca
        elif (y1 == y2):
            screen.fill((0,0,20))
            pygame.draw.rect(screen, pygame.Color("white"), i, 4)
            my_font.render_to(screen, (617.5, a), escrita[k], (255, 255, 255))
            pygame.display.update(i)
            opt_moused2 = i

        #Caso contrário se a cor atual for branco desenha a amarelo
        elif (opt_moused == i and y1 != y2):
            screen.fill((0,0,20))
            pygame.draw.rect(screen, pygame.Color("yellow"), i, 4)
            my_font.render_to(screen, (617.5, a), escrita[k], (255, 255, 0))
            pygame.display.update(i)

        k += 1

    if cycle == 0:
        screen.blit(image, (237.5, 25))
        pygame.display.flip()

    return menu_pos, opt_moused2

def next_menu(screen, menu_pos):

    #Coordenadas do rato
    m_x, m_y = pygame.mouse.get_pos()

    #Deteta se o rato está por cima de alguma opção do menu e se sim retorna y
    for i in menu_pos:
        x,y,l,a = i
        l += x
        a += y
        if (m_x >= x and m_x <= l and m_y >= y and m_y <= a):
            return y
    return 0

def dificulty_mode(screen, y2, cycle, dific_moused):

    #Procura a fonte
    my_font = pygame.freetype.Font("D:/python/trabalho final python/NotoSans-Regular.ttf", 24)

    #Posições onde se desenham os retângulos das opções do menu, array com a escrita dentro dos rectângulos e variável que determina qual elemento do array se coloca dentro de cada rectângulo
    second_menu_pos = [(537.5, 380, 200, 33), (537.5, 530, 200, 33),  (537.5, 250, 200, 35), (537.5, 445, 200, 33), (537.5, 315, 200, 35)]

    #Ordeneios por ordem de tamanho para depois os poder definir baseado em k
    escrita = ["Pro", "Exit","Noob","Expert", "Intermediate"]
    k = 0
    #Criei uma segunda variável uma vez que se corria o risco de mudar a variável antes de atualizar a carta anterior que se tornou branca
    dific_moused2 = dific_moused

    #Para cada posição desenha o retângulo e escreve a opção
    for i in second_menu_pos:

        x,y,l,a = i
        a = y + a/4
        #Para não ter de fazê-las uma a uma e tendo em conta que o tamanho das palavras varia, defini as suas coordenadas baseados em k
        if k == 3:
            x = 602
        elif k == 1 or k == 2:
            x = 624.5 - k*8
        else:
            x = 619.5 - k*13.5

        #Fiz com que apenas desenhá-se na primeira vez para reduzir o número de sobreposições de imagem
        if (cycle == 0):
            pygame.draw.rect(screen, pygame.Color("yellow"), i, 4)
            my_font.render_to(screen, (x, a), escrita[k], (255, 255, 0))

        #Verifica se o utilizador tem o rato por cima de uma opção e se sim torna a opção branca
        elif (y == y2):
            screen.fill(pygame.Color("black"))
            pygame.draw.rect(screen, pygame.Color("white"), i, 4)
            my_font.render_to(screen, (x, a), escrita[k], (255, 255, 255))
            dific_moused2 = i
            pygame.display.update(i)

        #Caso contrário se a cor atual for branco desenha a amarelo
        elif (dific_moused == i and y != y2):
            screen.fill(pygame.Color("black"))
            pygame.draw.rect(screen, pygame.Color("yellow"), i, 4)
            my_font.render_to(screen, (x, a), escrita[k], (255, 255, 0))
            pygame.display.update(i)

        my_font.render_to(screen, (100, 80), "A dificuldade determina o tempo disponível para escolher as opções e memorizar os padrões", (255, 255, 0))
        k += 1

    if cycle == 0:
        pygame.display.flip()

    return second_menu_pos, dific_moused2

def start_game(screen, menu_pos):

    #Coordenadas do rato
    m_x, m_y = pygame.mouse.get_pos()

    #Deteta se o rato está por cima de alguma opção do menu e se sim retorna y
    for i in menu_pos:
        x,y,l,a = i
        l += x
        a += y
        if (m_x >= x and m_x <= l and m_y >= y and m_y <= a):
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

    #Funções que calculam os próximos X e Y das cartas após adicionar um espaço aberto (o intervalo 10) entre elas
    next_x = lambda previous_x, lar : previous_x + lar + 10
    next_y = lambda previous_y, alt : previous_y + alt + 10

    #Cria variável previous_y que indica o y do rectângulo prévio (já no set) e tem como valor inicial start_y retirando a altura e o espaço adicional entre cartas
    #Retira-se isto para anular a primeira função next() que iria passar para o próximo rectângulo antes de adicionar o primeiro
    previous_y = start_y - (alt + 10)

    #Ciclo for que move Y para a próxima linha de cartas a ser adicionada
    for i in range(0, vert):

        #Move Y para a próxima posição após todas as cartas da linha serem adicionadas (excepto na primeira vez)
        previous_y = next_y(previous_y, alt)

        #Reverte x para a posição inicial quando se terminam de adicionar as cartas da linha
        previous_x = start_x

        #Ciclo for que adiciona as cartas e move X ao longo da linha
        for i in range(0,hor):

            #Adiciona as medidas e coordenadas do rectângulo ao set
            setpos.add((previous_x,previous_y, lar, alt))

            #Move X para a próxima posição
            previous_x = next_x(previous_x, lar)

    return setpos

#Tentei fazer a função o mais aleatória possível para haver uma grande variedade de alterações sempre que se começa um novo jogo
def randomizer( old_setpos):


    #Listas ás quais serão adicionadas posição, forma, cor e preenchimento das cartas respectivamente
    click_pos = list()
    click_form = list()
    click_color = list()
    click_fill = list()

    #Sets com a cor,forma e preenchimento das cartas
    setcolor = {(0,0,0), (0, 255, 0, 255), (0, 229, 238, 255), (139, 90, 0, 255), (178, 34, 34, 255)}
    setform = {"rect", "circle", "triangle"}
    tupfill = (0,7)

    #Cria um set no_rep (no repetition)
    no_rep = set()
    #Transforma o set recebido numa lista ordenada
    setpos = list(old_setpos)

    while (setpos):
        for i in setpos:
            while (True):

                #Variáveis com o elemento random escolhido para cada set
                randcolor = random.choice(tuple(setcolor))
                randform = random.choice(tuple(setform))
                randpos = random.choice(tuple(setpos))
                randfill = random.choice(tupfill)

                #Verifica se alguma combinação (de forma, cor e preenchimento) já foi utilizada e se sim repete a randomização (evita que a mesma combinação seja usada em mais do que duas cartas)
                if ((randcolor, randform, randfill) in no_rep):
                    continue
                else:
                    break

            #Se a posição aleatória escolhida for a mesma do par (posição i em setpos) ele repete a randomização
            while(randpos == i):
                randpos = random.choice(tuple(setpos))

            #Adiciona os elementos ás listas
            click_pos.append(i)
            click_pos.append(randpos)
            click_form.append(randform)
            click_form.append(randform)
            click_color.append(randcolor)
            click_color.append(randcolor)
            click_fill.append(randfill)
            click_fill.append(randfill)

            #Grava as combinações já feitas no arrays no_rep
            no_rep.add((randcolor, randform, randfill))
            #Remove as posições utilizadas da lista para que não sejam sobrescritas
            setpos.remove(i)
            setpos.remove(randpos)

    #Retorna as listas que têm os pares de cartas e os seus formatos (por ordem)
    return click_pos, click_form, click_color, click_fill

def mouse_card(screen, setpos,cycle, mouse_on_card, exit_selected, card_selected):

    my_font = pygame.freetype.Font("D:/python/trabalho final python/NotoSans-Regular.ttf", 24)
    m_x, m_y = pygame.mouse.get_pos()

    E,X,I,T = 10, 680, 100, 30
    a = X + T/4
    I += E
    T += X

    #Fiz com que apenas desenhá-se na primeira vez para reduzir o número de sobreposições de imagem
    if (cycle == 0):
        pygame.draw.rect(screen, pygame.Color("yellow"), (10, 680, 100, 30),4)
        my_font.render_to(screen, (39, a), ('Exit'), (255, 255, 0))

    #Se a opção exit tiver tido o rato em cima anteriormente ele volta a ficar amarelo
    elif (exit_selected == 1 and (m_x >= E and m_x <= I and m_y >= X and m_y <= T) == False):
        pygame.draw.rect(screen, pygame.Color("yellow"), (10, 680, 100, 30),4)
        my_font.render_to(screen, (39, a), ('Exit'), (255, 255, 0))
        pygame.display.update((10, 680, 100, 30))
        exit_selected = 0

    #Se a opção exit tiver o rate em cima ela desenha exit a branco
    elif (m_x >= E and m_x <= I and m_y >= X and m_y <= T and (exit_selected != 1)):
        pygame.draw.rect(screen, pygame.Color("white"), (10, 680, 100, 30), 4)
        my_font.render_to(screen, (39, a), ('Exit'), (255, 255, 255))
        pygame.display.update((10, 680, 100, 30))
        exit_selected = 1

    #Se já alguma carta ficou a branco e se essa carta já não tem o cursor por cima, desenha essa carta a amarelo
    if (mouse_on_card != 0 and card_selected != 0):
        x,y,l,a = mouse_on_card
        l += x
        a += y
        if ((m_x >= x and m_x <= l and m_y >= y and m_y <= a) == False):
            pygame.draw.rect(screen, pygame.Color("yellow"), mouse_on_card, 0)
            pygame.display.update(mouse_on_card)
            card_selected = 0


    for i in setpos:
        x,y,l,a = i
        l += x
        a += y

        #Desenha todas as cartas na primeira vez
        if (cycle == 0):
            pygame.draw.rect(screen, pygame.Color("yellow"),i, 0)
            pygame.display.flip()

        #Se uma carta tem o cursor por cima e ainda não está a branco então é desenhada
        elif (m_x >= x and m_x <= l and m_y >= y and m_y <= a and card_selected != 1):
            pygame.draw.rect(screen, pygame.Color("white"), i, 0)
            pygame.display.update(i)
            card_selected = 1
            return E,X,I,T, i, exit_selected, card_selected


    return E,X,I,T, 0, exit_selected, card_selected

def draw_format(screen, click_pos, click_form, click_color, click_fill):

    k = 0

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

            #Mesmo que com o quadrado mas agora com a formula do circulo

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

def first_click(screen, click_pos, click_form, click_color, click_fill, already_used):

    m_x, m_y = pygame.mouse.get_pos()
    k = 0

    for i in click_pos:
        x,y,l,a = i
        l += x
        a += y

        #Se uma carta for selecionada retorna os seus elementos (detalhes)
        if (m_x >= x and m_x <= l and m_y >= y and m_y <= a):
            pair_form = click_form[k]
            pair_color = click_color[k]
            pair_fill = click_fill[k]
            return 1, i, pair_form, pair_color, pair_fill

        k += 1
    return 0,0, 0, 0, 0

def pair_click(screen, click_pos, first_pos, pair_form, pair_color, pair_fill, click_form, click_color, click_fill, already_used):

    m_x, m_y = pygame.mouse.get_pos()
    k = 0

    for i in click_pos:
        x,y,l,a = i
        l += x
        a += y

        if (m_x >= x and m_x <= l and m_y >= y and m_y <= a):

            #Se a carta selecionada não for par retorna 1
            if pair_form != click_form[k] or pair_color != click_color[k] or pair_fill != click_fill[k]:
                return 1, i

            #Caso contrário retorna "pair"
            else:
                return "pair", i

        k += 1
    return 0, 0

def pontuação(screen, cycle, score, penalização):

    my_font = pygame.freetype.Font("D:/python/trabalho final python/NotoSans-Regular.ttf", 32)

    if (penalização != 0):
        score -= 20 * (2 ** (penalização - 1))

    if (score < 0):
        score = 0

    #Fiz com que apenas desenhá-se na primeira vez para reduzir o número de sobreposições de imagem
    if (cycle == 0):
        pygame.draw.rect(screen, pygame.Color("blue"), (30, 30, 200, 100), 0)
        my_font.render_to(screen, (40, 40), ('Score: ' + str(score)), (255, 255, 0))
        pygame.display.update((30, 30, 200, 100))


    return score

def time_to_choose(screen, rect_coord, estime, y2):

    if y2 == 250:
        return 0

    elif y2 == 315:
        if estime > 2.0:
            timed_out(screen, rect_coord)
            return 1


    elif y2 == 380:
        if estime > 1.0:
            timed_out(screen, rect_coord)
            return 1

    else:
        if estime > 0.6:
            timed_out(screen, rect_coord)
            return 1

    return 0

def time_to_memorise(screen, rect_coord,  y2):

    if y2 == 250:
        time.sleep(1)

    elif y2 == 315:
        time.sleep(0.7)

    elif y2 == 380:
        time.sleep(0.5)

    else:
        time.sleep(0.3)

    return 0


def timed_out(screen, rect_coord):

    pygame.draw.rect(screen, pygame.Color("yellow"), rect_coord, 0)
    pygame.display.update(rect_coord)

def right_ans(screen, rect_coord):

    pygame.draw.rect(screen, pygame.Color("blue"), rect_coord, 0)
    pygame.display.update(rect_coord)


main()