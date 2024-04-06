import pygame
import sys
import random
from pygame.locals import QUIT

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simulación de Pastoreo con IA Distribuida')

# Colores
WHITE = (255, 255, 255)
BROWN = (160, 82, 45)
GREEN = (150, 225, 150)
GREY = (200, 200, 200)

# Parámetros
NUM_SHEEP = 5
NUM_DOGS = 2
AGENT_SIZE = 20
DOG_SPEED = 3
SHEEP_SPEED = 2
CORRAL_POSITION = (600, 100)
CORRAL_SIZE = (150, 400)

# Agentes
sheep_positions = [[random.randint(0, SCREEN_WIDTH-AGENT_SIZE), random.randint(0, SCREEN_HEIGHT-AGENT_SIZE)] for _ in range(NUM_SHEEP)]
dog_positions = [[random.randint(0, SCREEN_WIDTH-AGENT_SIZE), random.randint(0, SCREEN_HEIGHT-AGENT_SIZE)] for _ in range(NUM_DOGS)]

def move_dogs():
    for dog_pos in dog_positions:
        target_sheep = min(sheep_positions, key=lambda x: (x[0] - dog_pos[0])**2 + (x[1] - dog_pos[1])**2)
        dog_pos[0] += DOG_SPEED if target_sheep[0] > dog_pos[0] else -DOG_SPEED
        dog_pos[1] += DOG_SPEED if target_sheep[1] > dog_pos[1] else -DOG_SPEED

def move_sheep():
    for i, sheep_pos in enumerate(sheep_positions):
        # Alejarse del perro más cercano
        closest_dog = min(dog_positions, key=lambda x: (x[0] - sheep_pos[0])**2 + (x[1] - sheep_pos[1])**2)
        dx = sheep_pos[0] - closest_dog[0]
        dy = sheep_pos[1] - closest_dog[1]
        distance = max((dx**2 + dy**2)**0.5, 1)  # Evitar división por cero
        move_x = (SHEEP_SPEED * dx / distance) if dx else 0
        move_y = (SHEEP_SPEED * dy / distance) if dy else 0
        
        # Mantenerse cerca del rebaño
        flock_center_x = sum([pos[0] for j, pos in enumerate(sheep_positions) if j != i]) / (len(sheep_positions) - 1)
        flock_center_y = sum([pos[1] for j, pos in enumerate(sheep_positions) if j != i]) / (len(sheep_positions) - 1)
        move_x += (flock_center_x - sheep_pos[0]) * 0.1  # Ajuste este factor para cambiar la fuerza de la tendencia a agruparse
        move_y += (flock_center_y - sheep_pos[1]) * 0.1  # Ajuste este factor para cambiar la fuerza de la tendencia a agruparse

        # Actualizar posición
        sheep_pos[0] += move_x
        sheep_pos[1] += move_y

        # Mantener dentro de los límites de la pantalla y evitar las esquinas
        sheep_pos[0] = max(0, min(SCREEN_WIDTH - AGENT_SIZE, sheep_pos[0]))
        sheep_pos[1] = max(0, min(SCREEN_HEIGHT - AGENT_SIZE, sheep_pos[1]))
# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(GREEN)
    
    # Dibujar corral
    pygame.draw.rect(screen, GREY, (*CORRAL_POSITION, *CORRAL_SIZE))
    
    # Mover y dibujar perros
    move_dogs()
    for dog_pos in dog_positions:
        pygame.draw.rect(screen, BROWN, (*dog_pos, AGENT_SIZE, AGENT_SIZE))
    
    # Mover y dibujar ovejas
    move_sheep()
    for sheep_pos in sheep_positions:
        pygame.draw.rect(screen, WHITE, (*sheep_pos, AGENT_SIZE, AGENT_SIZE))

    pygame.display.update()
    pygame.time.Clock().tick(40)
