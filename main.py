import pygame
import time
import random

pygame.font.init()

WIDTH,HEIGHT=1000,800
# SETTING UP THE WINDOW
WIN=pygame.display.set_mode((WIDTH,HEIGHT))

# After finishing this ie tomorrow, make notes of this and also find documentation
STAR_WIDTH=10
STAR_HEIGHT=15
star_increment=2000
star_count=0
STAR_VELOCITY=4

stars=[] # that will be present on the screen
hit=False

PLAYER_WIDTH=40
PLAYER_HEIGHT=60

PLAYER_VELOCITY=5

FONT=pygame.font.SysFont("JetBrains Mono",30)

BG=pygame.image.load("bg.jpeg")
# if it doesnt fit then we can use the pygame.trasnform function to scale the image

points=0
coin_WIDTH=10
coin_HEIGHT=15
coin_increment=2500
coin_count=0
coin_VELOCITY=3
coins=[]
collected=False

lives = 3
end=False

def draw(player,elapsed_time,stars):
    # top left corner corresponds to 0,0 coordinates
    WIN.blit(BG,(0,0))

    time_text=FONT.render(f"Time: {round(elapsed_time)}s",1,"white")
    points_text= FONT.render(f"Points: {round(points)}", 1, "white")
    WIN.blit(time_text, (10,10))
    WIN.blit(points_text,(WIDTH-points_text.get_width(),10))

    pygame.draw.rect(WIN,"green",player)

    for star in stars:
        pygame.draw.rect(WIN,"white",star)
    for coin in coins:
        pygame.draw.circle(WIN, "yellow", (coin.x + coin_WIDTH // 2, coin.y + coin_HEIGHT // 2), round(coin_WIDTH/1.5) )

    pygame.display.update()


def update(path,score):
    with open(path, 'r') as file:
        scores=[int(line.strip()) for line in file.readlines()]

    scores.sort(reverse=True)
    scores = scores[:5]

    if score > min(scores):
        scores.remove(min(scores))
        scores.append(score)
        scores.sort(reverse=True)

    with open(path, 'w') as file:
        for score in scores:
            file.write(f"{score}\n")

    return scores


path = "scores.txt"




def main():
    global star_count
    global star_increment
    global hit
    global collected
    global points
    global coin_increment
    global coin_count
    global end
    global lives

    run=True
    player=pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)

    clock=pygame.time.Clock()
    start_time=time.time()
    elapsed_time=0


    while run:
        delta_time = clock.tick(80)
        star_count += delta_time
        coin_count += delta_time

        elapsed_time=time.time()-start_time
        points+=0.02
        points += elapsed_time * 0.005
        STAR_VELOCITY = 4 + (elapsed_time // 30)
        if(star_count>star_increment):
            for i in range(3):
                star_x=random.randint(0,WIDTH-STAR_WIDTH)
                star=pygame.Rect(star_x,-STAR_HEIGHT,STAR_WIDTH,STAR_HEIGHT)
                stars.append(star)

            star_increment=max(200,star_increment-50)
            star_count=0
        if coin_count > coin_increment:
            for i in range(2):
                coin_x = random.randint(0, WIDTH - coin_WIDTH)
                coin = pygame.Rect(coin_x, -coin_HEIGHT, coin_WIDTH, coin_HEIGHT)
                coins.append(coin)
            coin_increment=max(500,coin_increment-35)
            coin_count=0

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
                # this pygame.QUIT corresponds to the cross button

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x-PLAYER_VELOCITY>=0:
            player.x-=PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x+PLAYER_VELOCITY+PLAYER_WIDTH<=WIDTH:
            player.x+=PLAYER_VELOCITY

        for star in stars[:]: #working on a copy only
            star.y+=STAR_VELOCITY
            if(star.y>HEIGHT):
                stars.remove(star)
            elif star.y +STAR_HEIGHT>=player.y and star.colliderect(player):
                stars.remove(star)
                hit=True
                break

        if hit:
            lives -= 1
            hit = False

            life_text = FONT.render("One Life Down", 1, "red")
            WIN.blit(life_text, (WIDTH // 2 - life_text.get_width() // 2, 10))
            pygame.display.update()

            pygame.time.delay(1000)

            if lives <= 0:
                end = True

        if end:
            lost_text=FONT.render("Git Gud",1,"red")
            WIN.blit(lost_text,(WIDTH//2-lost_text.get_width()//2, HEIGHT//2-lost_text.get_height()//2))
            points_text = FONT.render(f"Your Score: {round(points)}", 1, "blue")
            WIN.blit(points_text, ((WIDTH // 2 - points_text.get_width() // 2)+20, (HEIGHT // 2 - points_text.get_height() // 2)+20))
            pygame.display.update()
            pygame.time.delay(2000)

            # =============================================================
            updated_scores = update(path, points)
            WIN.fill("black")
            y_offset = 50
            for i, score in enumerate(updated_scores):
                scores_text=FONT.render("Highest Scores",1,"green")
                WIN.blit(scores_text,(WIDTH // 2 - scores_text.get_width() // 2,20))
                text = FONT.render(f"{i + 1}. {round(score)}", 1, "white")
                WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 40
            pygame.display.update()
            pygame.time.delay(2000)

            break
        for coin in coins[:]: #working on a copy only
            coin.y+=coin_VELOCITY
            if coin.y>HEIGHT:
                coins.remove(coin)
            elif coin.y +coin_HEIGHT>=player.y and coin.colliderect(player):
                coins.remove(coin)
                collected=True

        if collected:
            points+=25
            collected=False
            pygame.display.update()

        draw(player,elapsed_time,stars)
    pygame.quit()

if __name__=="__main__":
    main()