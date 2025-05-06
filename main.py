import pygame
import sys
import random
import time

# Inicializando o Pygame
pygame.init()

# Definindo dimensões da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aventura")

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Cor para as moedas

# Definindo o clock
clock = pygame.time.Clock()
FPS = 60

# Definindo fontes
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 20)

# Variáveis do jogo
player_pos = [400, 300]
player_speed = 5
player_size = 50
player_health = 5
player_traps = []

# Variáveis dos inimigos
enemy_size = 50
enemy_traps = []
enemies = [{"pos": [100, 100], "speed": 2, "health": 3, "trap_time": time.time(), 
            "direction": random.choice(["up", "down", "left", "right"]), "change_dir_time": time.time()}, 
           {"pos": [700, 500], "speed": 2, "health": 3, "trap_time": time.time(), 
            "direction": random.choice(["up", "down", "left", "right"]), "change_dir_time": time.time()}]

# Variáveis das moedas
coin_size = 20
coins = [{"pos": [random.randint(0, WIDTH-coin_size), random.randint(0, HEIGHT-coin_size)]} for _ in range(10)]

# Inicializando o mixer
pygame.mixer.init()

# Sons
coin_sound = pygame.mixer.Sound("C:/Users/Pc/Desktop/Jogo/sons/moeda.mp3") #LEMBRE DE ALTERAR O CAMINNHO
attack_sound = pygame.mixer.Sound("C:/Users/Pc/Desktop/Jogo/sons/ataque.mp3") #LEMBRE DE ALTERAR O CAMINNHO 
trap_sound = pygame.mixer.Sound("C:/Users/Pc/Desktop/Jogo/sons/armadilha.mp3") #LEMBRE DE ALTERAR O CAMINNHO 
victory_sound = pygame.mixer.Sound("C:/Users/Pc/Desktop/Jogo/sons/vitoria.mp3") #LEMBRE DE ALTERAR O CAMINNHO 
gameover_sound = pygame.mixer.Sound("C:/Users/Pc/Desktop/Jogo/sons/derrota.mp3") #LEMBRE DE ALTERAR O CAMINNHO 

# Música de fundo
pygame.mixer.music.load("C:/Users/Pc/Desktop/Jogo/sons/background.mp3") #LEMBRE DE ALTERAR O CAMINNHO
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop infinito

sound_enabled = True

def play_sound(sound):
    if sound_enabled:
        sound.play()

# Função para desenhar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Função para desenhar moedas
def draw_coins():
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (int(coin["pos"][0] + coin_size // 2), int(coin["pos"][1] + coin_size // 2)), coin_size // 2)

# Função para checar colisão com moedas
def check_coin_collision():
    global coins
    for coin in coins[:]:
        if (abs(player_pos[0] - coin["pos"][0]) < player_size) and (abs(player_pos[1] - coin["pos"][1]) < player_size):
            coins.remove(coin)
            play_sound(coin_sound)

            print("Moeda coletada!")

# Função para desenhar o jogador
def draw_player():
    pygame.draw.rect(screen, BLACK, (*player_pos, player_size, player_size))

# Função de movimentação do jogador
def move_player(keys_pressed):
    if keys_pressed[pygame.K_w]:  # Para cima
        player_pos[1] -= player_speed
    if keys_pressed[pygame.K_s]:  # Para baixo
        player_pos[1] += player_speed
    if keys_pressed[pygame.K_a]:  # Para a esquerda
        player_pos[0] -= player_speed
    if keys_pressed[pygame.K_d]:  # Para a direita
        player_pos[0] += player_speed

# Função para mover os inimigos suavemente
def move_enemies():
    current_time = time.time()
    for enemy in enemies:
        # Muda a direção a cada 2-4 segundos
        if current_time - enemy["change_dir_time"] > random.randint(2, 4):
            enemy["direction"] = random.choice(["up", "down", "left", "right"])
            enemy["change_dir_time"] = current_time
        
        # Movimentando os inimigos na direção atual
        if enemy["direction"] == "up":
            enemy["pos"][1] -= enemy["speed"]
        elif enemy["direction"] == "down":
            enemy["pos"][1] += enemy["speed"]
        elif enemy["direction"] == "left":
            enemy["pos"][0] -= enemy["speed"]
        elif enemy["direction"] == "right":
            enemy["pos"][0] += enemy["speed"]

        # Garantindo que os inimigos fiquem dentro da tela
        enemy["pos"][0] = max(0, min(WIDTH - enemy_size, enemy["pos"][0]))
        enemy["pos"][1] = max(0, min(HEIGHT - enemy_size, enemy["pos"][1]))

# Função para desenhar os inimigos e suas vidas
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (*enemy["pos"], enemy_size, enemy_size))
        draw_text(f"{enemy['health']}", small_font, BLACK, screen, enemy["pos"][0] + enemy_size // 2, enemy["pos"][1] - 10)

# Função para atacar
def attack():
    global enemies
    for enemy in enemies:
        if (abs(player_pos[0] - enemy["pos"][0]) < player_size) and (abs(player_pos[1] - enemy["pos"][1]) < player_size):
            enemy["health"] -= 1
            print(f"Inimigo atingido! Vidas restantes: {enemy['health']}")
            play_sound(attack_sound)
            if enemy["health"] <= 0:
                enemies.remove(enemy)
                print("Inimigo derrotado!")

# Função para inimigos colocarem armadilhas a cada 5 segundos
def enemy_place_traps():
    for enemy in enemies:
        if time.time() - enemy["trap_time"] > 5:  # A cada 5 segundos
            enemy_traps.append(enemy["pos"].copy())
            enemy["trap_time"] = time.time()
            play_sound(trap_sound)
            print("Inimigo colocou uma armadilha!")

# Função para desenhar armadilhas
def draw_traps():
    for trap in enemy_traps:
        pygame.draw.circle(screen, GREEN, (int(trap[0]), int(trap[1])), 20)  # Ajustar o hitbox para a armadilha

# Função para checar colisão com armadilhas
def check_trap_collision():
    global player_health
    # Checando se o jogador passa por uma armadilha
    for trap in enemy_traps:
        if (abs(player_pos[0] - trap[0]) < player_size // 2) and (abs(player_pos[1] - trap[1]) < player_size // 2):
            player_health -= 1
            enemy_traps.remove(trap)  # Remove a armadilha após o dano
            play_sound(trap_sound)
            print(f"Você foi atingido por uma armadilha! Vidas restantes: {player_health}")

    # Checando se o inimigo passa por uma armadilha
    for enemy in enemies:
        for trap in player_traps:
            if (abs(enemy["pos"][0] - trap[0]) < enemy_size // 2) and (abs(enemy["pos"][1] - trap[1]) < enemy_size // 2):
                enemy["health"] -= 1
                player_traps.remove(trap)  # Remove a armadilha após o dano
                print(f"Inimigo atingido por uma armadilha! Vidas restantes: {enemy['health']}")
                if enemy["health"] <= 0:
                    enemies.remove(enemy)
                    print("Inimigo derrotado!")

# Função para verificar se o jogador venceu
def check_victory():
    if len(enemies) == 0 and len(coins) == 0:
        # Desenha mensagem de vitória
        play_sound(victory_sound)
        draw_text("Você venceu!", font, BLUE, screen, WIDTH // 2, HEIGHT // 2 - 50)  # Mensagem de vitória
        
        # Desenha instruções para jogar novamente ou voltar ao menu
        draw_text("Aperte R para jogar novamente", small_font, GREEN, screen, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text("Aperte M para voltar ao Menu principal", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)
        
        pygame.display.update()

        # Pausar o jogo e dar a opção de voltar ao menu ou reiniciar
        victory = True
        while victory:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # Voltar ao menu principal
                        victory = False
                        main_menu()
                    if event.key == pygame.K_r:  # Reiniciar o jogo
                        victory = False
                        game_loop()
        return True
    return False

# Função para pausar o jogo
def pause_game():
    paused = True
    while paused:
        screen.fill(WHITE)
        draw_text("Jogo Pausado", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        draw_text("Aperte R para reiniciar", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("Aperte M para voltar ao Menu principal", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 20)
        draw_text("Aperte P para continuar", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar o jogo
                    paused = False
                    game_loop()
                if event.key == pygame.K_m:  # Voltar ao menu principal
                    paused = False
                    main_menu()
                if event.key == pygame.K_p:  # Continuar o jogo
                    paused = False

# Função de tela de Game Over
def game_over_screen():
    game_over = True
    while game_over:
        screen.fill(WHITE)
        draw_text("Você perdeu todas as suas vidas!", font, RED, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Aperte R para reiniciar", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text("Aperte M para voltar ao Menu principal", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar o jogo
                    game_over = False
                    game_loop()
                if event.key == pygame.K_m:  # Voltar ao menu principal
                    game_over = False
                    main_menu()

# Função principal do jogo
def game_loop():
    global player_health, enemies, player_traps, enemy_traps, coins
    player_health = 5
    enemies = [{"pos": [100, 100], "speed": 2, "health": 3, "trap_time": time.time(), 
                "direction": random.choice(["up", "down", "left", "right"]), "change_dir_time": time.time()}, 
               {"pos": [700, 500], "speed": 2, "health": 3, "trap_time": time.time(), 
                "direction": random.choice(["up", "down", "left", "right"]), "change_dir_time": time.time()}]
    player_traps = []
    enemy_traps = []
    coins = [{"pos": [random.randint(0, WIDTH-coin_size), random.randint(0, HEIGHT-coin_size)]} for _ in range(10)]

    running = True
    game_over = False
    while running:
        screen.fill(WHITE)
        
        # Movimentação do jogador
        keys_pressed = pygame.key.get_pressed()
        move_player(keys_pressed)

        if not game_over:
            # Movimentação dos inimigos
            move_enemies()

            # Desenha o jogador
            draw_player()
            draw_text(f"Vidas: {player_health}", font, BLUE, screen, WIDTH // 2, 50)

            # Desenha inimigos, armadilhas e moedas
            draw_enemies()
            draw_traps()
            draw_coins()

            # Checando colisão com armadilhas e moedas
            check_trap_collision()
            check_coin_collision()

            # Checando condição de vitória
            if check_victory():
                game_over = True

            # Verifica se o jogador ainda tem vidas
            if player_health <= 0:
                play_sound(gameover_sound)
                screen.fill(WHITE)
                draw_text("Você perdeu todas as suas vidas!", font, RED, screen, WIDTH // 2, HEIGHT // 2 - 50)
                draw_text("Aperte R para reiniciar", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 10)
                draw_text("Aperte M para voltar ao Menu principal", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)
                pygame.display.update()
                game_over_screen()
                running = False

            # Inimigos colocando armadilhas
            enemy_place_traps()

        # Checando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Ataque
                    attack()
                if event.key == pygame.K_p:  # Pausar o jogo
                    pause_game()

        pygame.display.update()
        clock.tick(FPS)
        
# Função para mostrar informações ao pressionar J
def show_info():
    global sound_enabled

    showing_info = True
    while showing_info:
        screen.fill(WHITE)
        
        # Informações gerais
        draw_text("Informações do Jogo", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        
        # Controles básicos
        draw_text("Movimentação: W A S D", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 80)
        draw_text("Ataque: Espaço", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        
        # Informações do sistema de vida e armadilhas
        draw_text("Você começa com 5 vidas", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text("Cuidado! Inimigos colocam armadilhas a cada 5 segundos.", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("Se passar em uma armadilha inimiga, você perde 1 vida.", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 70)
        
        # Objetivo do jogo
        draw_text("Objetivo: Colete todas as moedas e derrote todos os inimigos para vencer!", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 130)

        # Instruções adicionais
        draw_text("M para voltar ao menu", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 160)
        
        # Verifica eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    showing_info = False
                elif event.key == pygame.K_s:
                    sound_enabled = not sound_enabled
                    if sound_enabled:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

        pygame.display.update()


# Função para o menu principal
def main_menu():
    global sound_enabled

    while True:
        screen.fill(WHITE)
        draw_text("Bem-vindo à Aventura!", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        draw_text("Aperte ENTER para começar", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("Aperte J para ver informações do jogo", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 20)
        draw_text(f"Aperte S para {'Desligar ou Ligar'} Som", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                elif event.key == pygame.K_j:
                    show_info()
                elif event.key == pygame.K_s:
                    sound_enabled = not sound_enabled
                    if sound_enabled:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()


# Iniciando o jogo com o menu principal
main_menu()
