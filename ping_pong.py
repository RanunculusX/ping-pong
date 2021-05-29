from pygame import *

'''Необходимые классы'''
#Подача
#Заново
#Окно настроек:
# Выбор колво раундов
# Выбор скорости мяча
# Выбор размера ракетки
#Музыка
mixer.init()
mixer.music.load('bgmusic.mp3')
mixer.music.play(-1)

collision_sound = mixer.Sound('hit.ogg')

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
       #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height): # добавить еще два параметра при создании и задавать размер прямоугольгника для картинки самим
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (wight, height)) # вместе 55,55 - параметры
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed


#Игровая сцена:

back = (200, 255, 255) #цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))

bgimage = image.load('bg.png')
#window.fill(back)

def bg():
    window.blit(bgimage, bgimage.get_rect())

bg()


#флаги отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 80
score1 = 0
score2 = 0
max_score = 3
P1F = False
P2F = False
feed_1 = False
feed_2 = False

#создания мяча и ракетки    
racket1 = Player('racket1.png', 30, 200, 4, 50, 150) #при созданни спрайта добавляется еще два параметра
racket2 = Player('racket2.png', 520, 200, 4, 50, 150)
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)


font.init()

font_score = font.Font('StarJediHollow-A4lL.ttf', 45)
font_win = font.Font('StarJedi-DGRW.ttf', 45)
font_message = font.SysFont('Arial', 35)

win1 = font_win.render('Player 1 win!', True, (212, 164, 13))
win2 = font_win.render('Player 2 win!', True, (212, 164, 13))
restart = font_message.render('To restart press X!', True, (180, 0, 0))
feed = font_message.render('To feed press X!', True, (180, 0, 0))
feed2 = font_message.render('To feed press <-!', True, (180, 0, 0))

def draw_score():
    score = font_score.render(str(score1) + ':' + str(score2), True, (212, 164, 13))
    window.blit(score, (280, 20))


speed_x = 3
speed_y = 3

while game:
    if FPS >= 250:
        pass
    else:
        FPS += 0.05
    if P1F == True:
        feed_1 = True
        FPS = 80
        speed_x = 0
        speed_y = 0
        ball.rect.y = racket1.rect.y + 50
        ball.rect.x = racket1.rect.x + 50
        keys = key.get_pressed()
        if keys[K_w] and ball.rect.y > 5:
            ball.rect.y -= racket1.speed
        if keys[K_s] and ball.rect.y < win_height - 80:
            ball.rect.y += racket1.speed
        if keys[K_x]:
            speed_x = 3
            speed_y = 3
            feed_1 = False
            bg()
            P1F = False
    if P2F == True:
        feed_2 = True
        FPS = 80
        speed_x = 0
        speed_y = 0
        ball.rect.y = racket2.rect.y + 50
        ball.rect.x = racket2.rect.x - 50
        keys = key.get_pressed()
        if keys[K_UP] and ball.rect.y > 5:
            ball.rect.y -= racket2.speed
        if keys[K_DOWN] and ball.rect.y < win_height - 80:
            ball.rect.y += racket2.speed
        if keys[K_LEFT]:
            speed_x = 3
            speed_y = 3
            feed_2 = False
            bg()
            P2F = False

    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == True:
        keys = key.get_pressed()
        if keys[K_x]:
            ball.rect.y = 200
            ball.rect.x = 200
            score1 = 0
            score2 = 0
            FPS = 80
            finish = False
            
    
    if finish != True:
        bg()
        draw_score()
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        feed = font_message.render('To feed press X!', True, (180, 0, 0))
        if feed_1 == True:
            window.blit(feed, (200, 400))
        if feed_2 == True:
            window.blit(feed2, (200, 400))

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
            collision_sound.play()
        
        # если мяч достигает границ экрана меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        # если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            #finish = False
            #window.blit(lose1, (200, 200))
            #game_over = False
            score2 += 1
            #ball.rect.x = racket1.rect.x + 50      
            #ball.rect.y = racket1.rect.y
            FPS = 80
            #speed_x *= -1
            #speed_y *= -1
            P1F = True
        # если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            #finish = True
            #window.blit(lose2, (200, 200))
            #game_over = False
            score1 += 1
            #ball.rect.x = racket2.rect.x - 50
            #ball.rect.y = racket2.rect.y
            FPS = 80
            #speed_x *= -1
            #speed_y *= -1
            P2F = True
        if score1 == max_score:
            bg()
            draw_score()
            finish = True
            window.blit(win1, (130, 200))
            ball.rect.y = 20000
            window.blit(restart, (200, 400))
            P1F = False
            P2F = False
        if score2 == max_score:
            bg()
            draw_score()
            finish = True
            window.blit(win2, (130, 200))
            ball.rect.y = 20000
            window.blit(restart, (200, 400))
            P1F = False
            P2F = False

        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)