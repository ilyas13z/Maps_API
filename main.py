import os
import sys
import pygame_textinput
import pygame
import requests as requests


def get_coord_from_name(name):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?" \
                       f"apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={name}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        top = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        coord = top["Point"]["pos"]
        coord = coord.split()
        return coord[0], coord[1]
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")



map_type = 'map'
pygame.init()
textinput = pygame_textinput.TextInputVisualizer()
toponym_coodrinates = input('Введите координаты без пробелов с запятой (например 37.677751,55.757718): ').split(',')
zennet = float(input('Введите масштаб: (в формате spn): '))
dct_resp, lst_resp = {}, []
toponym_longitude, toponym_lattitude = toponym_coodrinates
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ','.join([str(zennet), str(zennet)]),
    "l": map_type
}
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
running = True
couns = zennet
screen = pygame.display.set_mode((600, 700))
screen.blit(pygame.image.load(map_file), (0, 0))
clock = pygame.time.Clock()
pygame.display.flip()
old_response = response.url
pt = ''
while running:
    pygame.draw.rect(screen, 'black', (0, 545, 600, 250))
    events = pygame.event.get()

    textinput.update(events)
    textinput.font_color = 'white'
    textinput.cursor_color = 'white'
    screen.blit(textinput.surface, (10, 550))
    pygame.display.update()
    pygame.display.flip()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pygame.display.flip()
            if event.key == pygame.K_RETURN:
                toponym_longitude, toponym_lattitude = get_coord_from_name(textinput.value)
                pt = ','.join([toponym_longitude, toponym_lattitude, 'pm2rdm'])
            if event.key == pygame.K_PAGEUP:
                if 0 <= couns / 1.5 <= 90.0:
                    couns /= 1.5
            if event.key == pygame.K_PAGEDOWN:
                if 0 <= couns * 1.5 <= 90.0:
                    couns *= 1.5
            if event.key == pygame.K_DOWN:
                if 80 >= float(toponym_lattitude) - couns * 2 >= -80:
                    if float(toponym_lattitude) - couns * 2 <= 80:
                        toponym_lattitude = str(float(toponym_lattitude) - couns * 2)
                    else:
                        toponym_lattitude = 90
                else:
                    toponym_lattitude = '-80'
            if event.key == pygame.K_UP:
                if 80 >= float(toponym_lattitude) + couns * 2 >= -80:
                    toponym_lattitude = str(float(toponym_lattitude) + couns * 2)
                else:
                    toponym_lattitude = '80'
            if event.key == pygame.K_LEFT:
                if 180 >= float(toponym_longitude) - couns * 2 >= -180:
                    toponym_longitude = str(float(toponym_longitude) - couns * 2)
                else:
                    toponym_longitude = '-179'
            if event.key == pygame.K_RIGHT:
                if 180 >= float(toponym_longitude) + couns * 2 >= -180:
                    toponym_longitude = str(float(toponym_longitude) + couns * 2)
                else:
                    toponym_longitude = '179'
            if event.key == pygame.K_F1:
                map_type = 'map'
            if event.key == pygame.K_F2:
                map_type = 'sat'
            if event.key == pygame.K_F3:
                map_type = 'sat,skl'
            map_params = {
                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                "spn": ','.join([str(couns), str(couns)]),
                "l": map_type,
                "pt": pt
            }
            response = requests.get(map_api_server, params=map_params)
            if not response:
                print("Это край, дальше нельзя!")
            elif response.url == old_response:
                pass
            else:
                with open('map.png', "wb") as file:
                    file.write(response.content)
                old_response = response.url
            screen.blit(pygame.image.load(map_file), (0, 0))
    font = pygame.font.Font(None, 40)
    font1 = pygame.font.Font(None, 30)
    text1 = font.render("Переключение клавишами F1 F2 F3", True, (100, 255, 100))
    text2 = font1.render("Это поисковое поле:", True, (100, 255, 100))
    text3 = font1.render("(чтобы увидеть результат нажмите enter)", True, (100, 255, 100))
    screen.blit(text1, (50, 450))
    screen.blit(text2, (0, 480))
    screen.blit(text3, (0, 515))
    pygame.display.flip()
    clock.tick(60)
sys.exit()
