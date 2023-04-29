import os
import sys

import pygame
import requests as requests


def load_image(name):
    fullname = os.path.join('.', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


coodrinates = input('Введите координаты без пробелов с запятой (например 37.677751,55.757718): ').split(',')
flag = True
z = 1
while flag:
    z = input('Введите масштаб целое число (0-17): ')
    try:
        if 17 >= int(z) >= 0:
            flag = False
    except BaseException:
        pass


def create_map(sc):
    toponym_longitude, toponym_lattitude = coodrinates
    map_params = {
        "ll": f'{toponym_longitude},{toponym_lattitude}',
        "z": sc,
        "l": "map"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open('map.png', "wb") as file:
        file.write(response.content)


create_map(z)
pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True

fps = 10
clock = pygame.time.Clock()

img = load_image('map.png')

screen.blit(img, (0, 0))
ind = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == 1073741921:
                if int(z) < 17:
                    z = str(int(z) + 1)
            if event.key == 1073741915:
                if int(z) > 0:
                    z = str(int(z) - 1)
            create_map(z)
            img = load_image('map.png')
    screen.blit(img, (0, 0))
    clock.tick(fps)
    pygame.display.flip()
os.remove('map.png')
pygame.quit()
