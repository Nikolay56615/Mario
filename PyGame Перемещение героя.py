import pygame
import sys
import os

FPS = 50
size = WIDTH, HEIGHT = 500, 500
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, direction, level):
        for i in range(len(level)):
            if '@' in level[i]:
                pos_x = i
                pos_y = level[i].index('@')
        if direction == "right":
            if level[pos_x][pos_y + 1] != '#':
                try:
                    level[pos_x] = level[pos_x][:pos_y] + '.' + level[pos_x][pos_y + 1:]
                    level[pos_x] = level[pos_x][:pos_y + 1] + '@' + level[pos_x][pos_y + 2:]
                except:
                    pass
        elif direction == 'left':
            if level[pos_x][pos_y - 1] != '#':
                try:
                    level[pos_x] = level[pos_x][:pos_y] + '.' + level[pos_x][pos_y + 1:]
                    level[pos_x] = level[pos_x][:pos_y - 1] + '@' + level[pos_x][pos_y:]
                except:
                    pass
        elif direction == 'up':
            if level[pos_x - 1][pos_y] != '#':
                try:
                    level[pos_x] = level[pos_x][:pos_y] + '.' + level[pos_x][pos_y + 1:]
                    level[pos_x - 1] = level[pos_x - 1][:pos_y] + '@' + level[pos_x - 1][pos_y + 1:]
                except:
                    pass
        elif direction == 'down':
            if level[pos_x + 1][pos_y] != '#':
                try:
                    level[pos_x] = level[pos_x][:pos_y] + '.' + level[pos_x][pos_y + 1:]
                    level[pos_x + 1] = level[pos_x + 1][:pos_y] + '@' + level[pos_x + 1][pos_y + 1:]
                except:
                    pass


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
start_screen()
try:
    filename0 = input()
    level = load_level(filename0)
except FileNotFoundError as e:
    print('FileNotFoundError', e)
player, level_x, level_y = generate_level(level)
running = True
while running:
    player, level_x, level_y = generate_level(level)
    clock.tick(120)
    all_sprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.unicode == 'a':
            player.move('left', level)
        if event.type == pygame.KEYDOWN and event.unicode == 'd':
            player.move('right', level)
        if event.type == pygame.KEYDOWN and event.unicode == 'w':
            player.move('up', level)
        if event.type == pygame.KEYDOWN and event.unicode == 's':
            player.move('down', level)

    screen.fill(pygame.Color("Black"))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
