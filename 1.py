import pygame
import random

# Inicialización de Pygame
pygame.init()

# Colores
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Dimensiones de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Configuración de la ventana
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Clase para los Agentes
class Agent(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def move_towards(self, target_x, target_y):
        # Mueve el agente hacia la posición objetivo
        if self.rect.x < target_x:
            self.rect.x += 1
        elif self.rect.x > target_x:
            self.rect.x -= 1
        if self.rect.y < target_y:
            self.rect.y += 1
        elif self.rect.y > target_y:
            self.rect.y -= 1

# Clase para la Suciedad
class Dirt(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 20)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 20)

# Clase para el Agente Coordinador
class Coordinator:
    def __init__(self):
        self.dirt_positions = []

    def update_dirt_positions(self, dirt_list):
        self.dirt_positions = [(dirt.rect.x, dirt.rect.y) for dirt in dirt_list]

    def assign_dirt(self, agent):
        if not self.dirt_positions:
            return None
        closest_dirt = min(self.dirt_positions, key=lambda pos: self.distance(agent.rect.x, agent.rect.y, pos[0], pos[1]))
        return closest_dirt

    @staticmethod
    def distance(x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# Grupos de sprites
all_sprites_list = pygame.sprite.Group()
dirt_list = pygame.sprite.Group()

# Creación de agentes
for i in range(2):
    agent = Agent(BLUE, 20, 20)
    agent.rect.x = random.randint(0, SCREEN_WIDTH - 20)
    agent.rect.y = random.randint(0, SCREEN_HEIGHT - 20)
    all_sprites_list.add(agent)

# Creación de suciedad
for i in range(20):
    dirt = Dirt()
    dirt_list.add(dirt)
    all_sprites_list.add(dirt)

# Instancia del coordinador
coordinator = Coordinator()

clock = pygame.time.Clock()
done = False

# Bucle principal
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Actualizar posiciones de suciedad en el coordinador
    coordinator.update_dirt_positions(dirt_list)

    # Lógica para mover agentes hacia la suciedad asignada
    for agent in all_sprites_list:
        if isinstance(agent, Agent):
            target_dirt = coordinator.assign_dirt(agent)
            if target_dirt:
                agent.move_towards(*target_dirt)

            # Limpieza de la suciedad al tocarla
            dirt_hit_list = pygame.sprite.spritecollide(agent, dirt_list, True)
            for hit in dirt_hit_list:
                coordinator.dirt_positions.remove((hit.rect.x, hit.rect.y))
    
    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
