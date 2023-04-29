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

# Долгота и широта:
toponym_longitude, toponym_lattitude = coodrinates
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": f'{toponym_longitude},{toponym_lattitude}',
    "z": z,
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
if not response:
    print("Ошибка выполнения запроса:")
    print(response.url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
with open('map.png', "wb") as file:
    file.write(response.content)
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
            if event.key == pygame.K_RIGHT:
                ind += 1
            if event.key == pygame.K_LEFT:
                ind -= 1
    screen.blit(img, (0, 0))

    pygame.display.flip()
pygame.quit()
