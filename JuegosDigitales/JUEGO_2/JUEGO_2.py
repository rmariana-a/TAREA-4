import pygame
import random
import time

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego del Gato y las Escobas 🐱🧹")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Ruta fija de imágenes

IMAGES_PATH = r"C:\Users\LENOVO\Desktop\JuegosDigitales\JUEGO_2\imagenes - copia"

# Cargar imágenes
player_img = pygame.image.load(f"{IMAGES_PATH}\\gato.png")
item_img = pygame.image.load(f"{IMAGES_PATH}\\escoba.png")
bg_img = pygame.image.load(f"{IMAGES_PATH}\\fondo.jpg")

# Redimensionar imágenes
player_img = pygame.transform.scale(player_img, (70, 70))
item_img = pygame.transform.scale(item_img, (50, 50))
bg_img = pygame.transform.scale(bg_img, (800, 600))

# Configuración fija de niveles
level_time = {1: 20, 2: 12, 3: 8, 4: 6}          # tiempo en segundos
items_required = {1: 15, 2: 20, 3: 25, 4: 25}    # escobas mínimas

# Función para mostrar texto
def draw_text(text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", size, True)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def game_loop():
    # Jugador
    player_rect = player_img.get_rect()
    player_rect.centerx = 400
    player_rect.bottom = 580
    player_speed = 7

    # Objetos
    items = []

    # Puntuación y nivel
    score = 0
    level = 1
    collected = 0
    running = True
    game_over = False

    level_start_time = pygame.time.get_ticks()

    # Variables para aviso de nivel
    level_up_message = ""
    level_up_time = 0

    while running:
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Movimiento jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < 800:
                player_rect.x += player_speed
            if keys[pygame.K_UP] and player_rect.top > 0:
                player_rect.y -= player_speed
            if keys[pygame.K_DOWN] and player_rect.bottom < 600:
                player_rect.y += player_speed

            # Generar escobas (más rápidas en niveles altos)
            if random.randint(1, 25 - level * 4) == 1:
                items.append(item_img.get_rect(topleft=(random.randint(0, 750), random.randint(0, 550))))

            # Dibujar y detectar colisiones
            for item in items[:]:
                screen.blit(item_img, item)
                if player_rect.colliderect(item):
                    items.remove(item)
                    score += 1
                    collected += 1

            # Tiempo restante
            elapsed_time = (pygame.time.get_ticks() - level_start_time) // 1000
            remaining_time = max(level_time[level] - elapsed_time, 0)

            # Verificar si se acabó el tiempo
            if remaining_time <= 0:
                if collected >= items_required[level]:
                    # Subir de nivel
                    level += 1
                    if level > 4:  # Ganó el juego
                        game_over = True
                    else:
                        collected = 0
                        items.clear()
                        level_start_time = pygame.time.get_ticks()

                        # Aviso de nivel
                        level_up_message = f"✨ Subiste a Nivel {level} ✨"
                        level_up_time = time.time()
                else:
                    game_over = True

            # Dibujar jugador
            screen.blit(player_img, player_rect)

            # Interfaz
            draw_text(f"Puntos: {score}", 30, 10, 10)
            draw_text(f"Nivel: {level}", 30, 10, 50)
            draw_text(f"Escobas: {collected}/{items_required[level]}", 30, 10, 90)
            draw_text(f"Tiempo: {remaining_time}", 30, 10, 130, (255, 255, 0))

            # Aviso en pantalla de nivel
            if level_up_message and time.time() - level_up_time < 3:
                draw_text(level_up_message, 40, 200, 280, (255, 215, 0))
            elif level_up_message and time.time() - level_up_time >= 3:
                level_up_message = ""

        else:
            # Pantalla final
            if level > 4:
                draw_text("🎉 ¡GANASTE EL JUEGO! 🎉", 50, 180, 200, (0, 255, 0))
            else:
                draw_text("😿 GAME OVER 😿", 50, 250, 200, (255, 0, 0))

            draw_text(f"Puntos: {score}", 40, 300, 270)
            draw_text(f"Nivel alcanzado: {level}", 40, 250, 320)
            draw_text("Presiona R para reiniciar", 30, 250, 400, (255, 255, 0))
            draw_text("Presiona Q para salir", 30, 280, 440, (255, 255, 0))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return True
            if keys[pygame.K_q]:
                running = False

        pygame.display.update()
        clock.tick(60)

    return False

# Bucle principal
restart = True
while restart:
    restart = game_loop()

pygame.quit()
