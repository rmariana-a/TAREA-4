import pygame
import random
import time

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego del Gato y las Escobas 🐱🧹")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# RUTA FIJA A LAS IMÁGENES DE JUEGO_1
IMAGES_PATH = r"C:\Users\LENOVO\Desktop\JuegosDigitales\JUEGO_1\imagenes"

# Cargar imágenes
player_img = pygame.image.load(f"{IMAGES_PATH}\\gato.png")
enemy_img = pygame.image.load(f"{IMAGES_PATH}\\escoba.png")
bg_img = pygame.image.load(f"{IMAGES_PATH}\\fondo.jpg")

# Redimensionar imágenes
player_img = pygame.transform.scale(player_img, (70, 70))
enemy_img = pygame.transform.scale(enemy_img, (60, 60))
bg_img = pygame.transform.scale(bg_img, (800, 600))

# Función para dibujar texto
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

    # Enemigos
    enemies = []
    enemy_speed = 3

    # Sistema de puntuación y niveles
    score = 0
    level = 1
    running = True
    game_over = False

    # Mensaje de subida de nivel
    level_up_message = ""
    level_up_time = 0

    while running:
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < 800:
                player_rect.x += player_speed

            # Generar enemigos
            if random.randint(1, 25 - level * 2) == 1:
                enemies.append(enemy_img.get_rect(topleft=(random.randint(0, 750), 0)))

            # Mover y dibujar enemigos
            for enemy in enemies[:]:
                enemy.y += enemy_speed
                if enemy.y > 600:
                    enemies.remove(enemy)
                    score += 1
                else:
                    screen.blit(enemy_img, enemy)

                # Detectar colisiones
                if player_rect.colliderect(enemy):
                    game_over = True

            # Subir de nivel con aviso
            if score > 10 and level == 1:
                level = 2
                enemy_speed = 4
                level_up_message = "✨ Subiste a Nivel 2 ✨"
                level_up_time = time.time()
            elif score > 25 and level == 2:
                level = 3
                enemy_speed = 5
                level_up_message = "🔥 Subiste a Nivel 3 🔥"
                level_up_time = time.time()
            elif score > 50 and level == 3:
                level = 4
                enemy_speed = 6
                level_up_message = "🚀 Subiste a Nivel 4 🚀"
                level_up_time = time.time()

            # Dibujar jugador
            screen.blit(player_img, player_rect)

            # Dibujar puntuación y nivel
            draw_text(f"Puntos: {score}", 30, 10, 10)
            draw_text(f"Nivel: {level}", 30, 10, 50)

            # Mostrar mensaje de subida de nivel (3 segundos)
            if level_up_message and time.time() - level_up_time < 3:
                draw_text(level_up_message, 40, 200, 280, (255, 215, 0))
            elif level_up_message and time.time() - level_up_time >= 3:
                level_up_message = ""  # limpiar mensaje después de 3s

        else:
            # Pantalla de Game Over
            draw_text("😿 GAME OVER 😿", 50, 250, 200, (255, 0, 0))
            draw_text(f"Puntos: {score}", 40, 300, 270)
            draw_text(f"Nivel: {level}", 40, 300, 320)
            draw_text("Presiona R para reiniciar", 30, 250, 400, (255, 255, 0))
            draw_text("Presiona Q para salir", 30, 280, 440, (255, 255, 0))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return True  # Reiniciar
            if keys[pygame.K_q]:
                running = False

        pygame.display.update()
        clock.tick(60)

    return False  # Salir

# Bucle principal que permite reinicios
restart = True
while restart:
    restart = game_loop()

pygame.quit()
