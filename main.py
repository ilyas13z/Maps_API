import os
import sys

import pygame
import requests as requests

pygame.init()
toponym_coodrinates = input('Введите координаты без пробелов с запятой (например 37.677751,55.757718): ').split(',')
zennet = float(input('Введите масштаб: (в формате spn): '))
dct_resp, lst_resp = {}, []
toponym_longitude, toponym_lattitude = toponym_coodrinates
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ','.join([str(zennet), str(zennet)]),
    "l": "map"
}
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
running = True
couns = zennet
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
os.remove(map_file)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if 0 <= couns / 1.5 <= 90.0:
                    couns /= 1.5
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "spn": ','.join([str(couns), str(couns)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    if not response:
                        print("Это край, дальше нельзя!")
                    else:
                        with open('map.png', "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        pygame.display.flip()
                        os.remove(map_file)
            if event.key == pygame.K_PAGEDOWN:
                if 0 <= couns * 1.5 <= 90.0:
                    couns *= 1.5
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "spn": ','.join([str(couns), str(couns)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
                    if not response:
                        print("Это край, дальше нельзя!")
                    else:
                        with open('map.png', "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        pygame.display.flip()
                        os.remove(map_file)
            if event.key == pygame.K_DOWN:
                if 80 >= float(toponym_lattitude) - couns * 2 >= -80:
                    if float(toponym_lattitude) - couns * 2 <= 80:
                        toponym_lattitude = str(float(toponym_lattitude) - couns * 2)
                    else:
                        toponym_lattitude = 90
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "spn": ','.join([str(couns), str(couns)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    if not response:
                        print("Это край, дальше нельзя! K_DOWN")
                    else:
                        with open('map.png', "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        pygame.display.flip()
                        os.remove(map_file)
                else:
                    toponym_lattitude = '-80'
            if event.key == pygame.K_UP:
                if 80 >= float(toponym_lattitude) + couns * 2 >= -80:
                    toponym_lattitude = str(float(toponym_lattitude) + couns * 2)
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "spn": ','.join([str(couns), str(couns)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    if not response:
                        print("Это край, дальше нельзя! K_UP")
                    else:
                        with open('map.png', "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        pygame.display.flip()
                        os.remove(map_file)
                else:
                    toponym_lattitude = '80'
            if event.key == pygame.K_LEFT:
                if 180 >= float(toponym_longitude) - couns * 2 >= -180:
                    toponym_longitude = str(float(toponym_longitude) - couns * 2)
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "spn": ','.join([str(couns), str(couns)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    if not response:
                        print("Это край, дальше нельзя! K_LEFT")
                    else:
                        with open('map.png', "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        pygame.display.flip()
                        os.remove(map_file)
                else:
                    toponym_longitude = '-179'
            if event.key == pygame.K_RIGHT:
                if 180 >= float(toponym_longitude) + couns * 2 >= -180:
                    toponym_longitude = str(float(toponym_longitude) + couns * 2)
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "spn": ','.join([str(couns), str(couns)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    if not response:
                        print("Это край, дальше нельзя! K_RIGHT")
                    else:
                        with open('map.png', "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        pygame.display.flip()
                        os.remove(map_file)
                else:
                    toponym_longitude = '179'
sys.exit()
