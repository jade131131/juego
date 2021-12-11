#se importam las librerias que se utilizan 

import pygame
import os

pygame.font.init() #nos sirve para introducer texto y luego dibujarlo 
pygame.mixer.init() #esto es para poder cargar los efecto de sonido 


WIDTH, HEIGHT = 900, 500 #tamaño de la pamtalla del juego    
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #se crea la pantalla del juego, se da altura y ancho
pygame.display.set_caption("mi primer juego") #titulo del juego 
#variales que son los colores(formato rgb)
WHITE = (255, 255 , 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#aqui e crea la variable que es el borde para que las naves no se choquen 
# primero se pone el ancho dividio a la mitad para que este justo en el medio 
#la anchura son 10 pixeles y la altura es la misma que la pantalla
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.wav') #sonido de las balas al salir
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Shot.wav')#sonido de las balas al colicionar contra una nave
#este es el tipo de texto con el que se va a poner las vidas (tipografia)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
#tipo de texto para el ganador (tipografia)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#Fotogramas por segundo
FPS = 60
#la velocidad que se mueven las naves espaciales 
VEL = 5
#velocidad de las balas
BULLET_VEL = 7
#maximo de balas 
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 90, 70   
#aqui se crean dos eventos uno para cada nave sea golpeada 
#el mas uno y el mas dos es para diferenciar los eventos 
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
 
#se cargan las imagenes de lo cohetes 
# pygame.transform.rotate es para rotar la imagenes 
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

#se carga la imagen de fondo   con pygame. image. load 
#se usa os. path. join que es de la libreria OS 
# se pone el nombre de la carpeta donde esta y el nombre del archibo 
#pygame.transform.scale sirve para cambiar el tamaño de la imagen 
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


#Esta función sirve para dibujar lo que necesitemos en la pantalla
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #El orden en el que dibujamos las cosas importa
    #Si dibujas el cohete antes que el fondo, el cohete 
    #no se verá
    WIN.blit(SPACE, (0, 0)) #blit es la funcion en la que se dibuja 
    # en este casose da la imagen que quieres poner (el fondo)
    #y su ubicacion 
    pygame.draw.rect(WIN, BLACK, BORDER) #AQUI se dibuja el borde negroque hace que las naves no se choquen 
    #aqui es donde se introducen las vidas 
    #el tipo de letra que se utiliza y el colr que se quiere que tengan 
    red_health_text = HEALTH_FONT.render("vidas: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("vidas: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) #se dibuja el texto y su posicion 
    WIN.blit(yellow_health_text, (10, 10))   
    #esta es la posision de las naves
    #las imagenes se mueven donde el rectangulo va 
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    #se dibuja  la posicion de las balas 
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    #Actualiza la pantalla
    pygame.display.update()
 #aqui se dan ls movimientos de la nave amarilla 
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #izquierda
        yellow.x -= VEL    
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #derecha
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #arriba
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #abajo
        yellow.y += VEL
# aqui estan los movimientos de las nave roja
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #izquierda
        red.x -= VEL    
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #derecha
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #arriba
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #abajo
        red.y += VEL

#Esta función se encarga del movimiento de las balas, de la colisión de éstas
#y de eliminarlas cuando se salen de la pantalla
#se cargan los perimetros que son las dos listas que guardan las balas y lols dos rectangulos 
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets: #se recorre las listas de las balas
        bullet.x += BULLET_VEL #de donde sale se le suma la distancia que recorre por seg osea 7 pix
        if red.colliderect(bullet):#esta funcion sirve para saber si dos rectangulos chocaron
            pygame.event.post(pygame.event.Event(RED_HIT))#se llama al evento cuando las balas chocan
            yellow_bullets.remove(bullet) #aqui se eliminan si colicionan 

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)#aqui se eliminan se se pasa del limite
        
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #aqui en vez de sumar se resta para ir al lado correcto 
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        
        elif bullet.x < 0:
            red_bullets.remove(bullet)
#aqui se pasa el texto del ganador , el color que se quiere que sea yla ubicacion  
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE) 
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 
                        2, HEIGHT/2 - draw_text.get_height()/2))
    #se muestra todo el texto en la pantalla 
    pygame.display.update()
    #esto es lo que tarda el juego en volver a empezar
    pygame.time.delay(5000)

#Función principal
def main():
    #Estos rectángulos representan las navesespaciales
    #primero se la las posiciones imiciales  
    #y luegoe pasa el tamaño del rectangulo que es el mismo de las naves espaciales 
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
#estas listas van a guardar las balas que esten actualmente en el mapa 
#se crean cuando se disparan y entran en la lista
#  y cuando salen del mapa o cuando
#colicionen con el enemigo salen de la lista 
    red_bullets = []
    yellow_bullets = []
#aqui se declara cuanta vida va a tener cada nave en este caso 10 
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    #se inicialicia la variable booleana llamada run 
    run = True

    while run:
        #Se encarga de que este bucle se repita 60 veces por segundo
        clock.tick(FPS)

        #pygame.event.get() es una lista con todos los eventos
        #de pygame. Con el bucle for la recorremos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #se comprueva de todos los eventos que son que aqui 
                #si se toca la X salga el juego asi o sino este no se cerrara  
                run = False
                #esta funcian es la encargada de cerrar la pantalla 
                pygame.quit()
        #con este if se comprueva si se apreto alguna tecla 
            if event.type == pygame.KEYDOWN:
                #si se pulsa la tecla control del costado izquierdo se dispara la bala
                #de la nave amarilla
                #aparete se comprueba de que solo se disparen tres balas 
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: 
                    #este es el rectngulo creado para las balas 
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 + 5, 10, 5)
                    yellow_bullets.append(bullet) #se guarda la bala en la lista
                    #aqui se reproduce el sonido de la bala 
                    BULLET_FIRE_SOUND.play()
                #si se pulsa la tecla control del costado derecho se dispara la bala 
                #de la nave roja 
                #Se utilizan dos // en la división para que el resultado sea un número entero
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 + 5, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            #aqui se le resta una vida si la bala coliciona con una de las naves 
            if event.type == RED_HIT:
                red_health -= 1
                #se reproduce el sonido del choque 
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        #aqui se verifica que la vida no sea menor que 0
        #y en caso de que sea 0 se muestra quien gano 
        winner_text = ""
        if red_health <= 0:
            winner_text = "el amarillo gano!!"

        if yellow_health <= 0:
            winner_text = "el rojo gano!!"
        # esto verifica si "winner text" no es un str vacio, asi escribe quien gano 
        if winner_text != "": 
            draw_winner(winner_text)
            break
  
        
        #Devuelve una lista con las teclas presionadas
        keys_pressed = pygame.key.get_pressed()
        #se llama a la funcion de las naves 
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        #se llama a la funcion de las balas 
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        #se llama a la funcion que dibuja todo
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

#se llama de nuevo  a la funcion para que si uno gana pueda seguir jugando
    main() 
     

#Este if comprueba si el fichero se llama main
if __name__ == "__main__":
    main()