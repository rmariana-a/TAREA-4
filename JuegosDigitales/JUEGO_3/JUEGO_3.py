import pygame
import random
import time

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Disparos 🎯")
clock = pygame.time.Clock()

# Ruta fija de imágenes
IMAGES_PATH = r"C:\Users\LENOVO\Desktop\JuegosDigitales\JUEGO_3\imagenes - copia 2"

# Cargar imágenes
player_img = pygame.image.load(f"{IMAGES_PATH}\\gato.png")   # jugador → gato
enemy_img = pygame.image.load(f"{IMAGES_PATH}\\escoba.png")  # enemigo → escoba
bg_img = pygame.image.load(f"{IMAGES_PATH}\\fondo.jpg")      # fondo

# Redimensionar
player_img = pygame.transform.scale(player_img, (60, 60))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bg_img = pygame.transform.scale(bg_img, (800, 600))

# Balas
bullets = []
bullet_speed = 8

# Jugador
player_rect = player_img.get_rect()
player_rect.centerx = 400
player_rect.bottom = 580
player_speed = 6

# Enemigos
enemies = []
enemy_speed = 3

# Puntuación y niveles
score = 0
level = 1
lives = 5  # total de escobas que puede tocar el jugador

# Meta por nivel (puntos necesarios para pasar al siguiente)
level_goal = {1: 10, 2: 25, 3: 50, 4: 80}

# Variables de aviso de nivel o daño
message = ""
message_time = 0

# Función para dibujar texto
def draw_text(text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", size, True)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Bucle principal
running = True
game_over = False
while running:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_rect.centerx - 2, player_rect.top])

    if not game_over:
        # Movimiento jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < 800:
            player_rect.x += player_speed

        # Generar enemigos
        if random.randint(1, 25 - level * 2) == 1:
            enemies.append(enemy_img.get_rect(topleft=(random.randint(0, 750), 0)))

        # Mover enemigos
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            screen.blit(enemy_img, enemy)

            # Colisión jugador-enemigo → perder 1 vida
            if player_rect.colliderect(enemy):
                enemies.remove(enemy)
                lives -= 1
                message = f"💥 Tocaron tu gato! Vidas restantes: {lives} 💥"
                message_time = time.time()
                if lives <= 0:
                    game_over = True

        # Mover balas
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
            else:
                pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], 5, 10))

        # Detectar colisiones bala-enemigo
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if enemy.colliderect(pygame.Rect(bullet[0], bullet[1], 5, 10)):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                        score += 1

        # Verificar meta para subir de nivel
        if level < 4 and score >= level_goal[level]:
            level += 1
            enemy_speed += 1  # enemigos más rápidos
            message = f"✨ Subiste a Nivel {level} ✨"
            message_time = time.time()

        # Dibujar jugador
        screen.blit(player_img, player_rect)

        # Interfaz
        draw_text(f"Puntos: {score}", 30, 10, 10)
        draw_text(f"Nivel: {level}", 30, 10, 50)
        draw_text(f"Meta: {level_goal[level]}", 30, 10, 90)
        draw_text(f"Vidas: {lives}", 30, 10, 130, (255, 0, 0))

        # Mostrar mensaje de nivel o daño 3 segundos
        if message and time.time() - message_time < 3:
            draw_text(message, 30, 150, 280, (255, 215, 0))
        elif message and time.time() - message_time >= 3:
            message = ""

    else:
        # Pantalla de Game Over
        draw_text("😿 GAME OVER 😿", 50, 250, 200, (255, 0, 0))
        draw_text(f"Puntos: {score}", 40, 300, 270)
        draw_text(f"Nivel alcanzado: {level}", 40, 300, 320)
        draw_text("Presiona R para reiniciar", 30, 250, 400, (255, 255, 0))
        draw_text("Presiona Q para salir", 30, 280, 440, (255, 255, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reiniciar juego
            score = 0
            level = 1
            lives = 5
            enemies.clear()
            bullets.clear()
            enemy_speed = 3
            player_rect.centerx = 400
            game_over = False
        if keys[pygame.K_q]:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
