import pygame
import db
from game import Game

pygame.init()
screen = pygame.display.set_mode((600,600))
font = pygame.font.SysFont(None,40)

def input_name():
    name=""
    while True:
        screen.fill((0,0,0))
        txt=font.render("Enter name: "+name,True,(255,255,255))
        screen.blit(txt,(100,300))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: return None
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:
                    return name
                elif e.key==pygame.K_BACKSPACE:
                    name=name[:-1]
                else:
                    name+=e.unicode

def show_leaderboard():
    data=db.get_top()
    while True:
        screen.fill((0,0,0))
        y=100
        for i,row in enumerate(data):
            t=font.render(f"{i+1}. {row[0]} {row[1]}",True,(255,255,255))
            screen.blit(t,(100,y))
            y+=40

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: return
            if e.type==pygame.KEYDOWN:
                return

def main():
    username=input_name()
    if not username: return

    while True:
        screen.fill((0,0,0))

        play=font.render("1 Play",True,(255,255,255))
        lb=font.render("2 Leaderboard",True,(255,255,255))
        quitb=font.render("ESC Quit",True,(255,255,255))

        screen.blit(play,(200,200))
        screen.blit(lb,(200,250))
        screen.blit(quitb,(200,300))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                return
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_1:
                    Game(username).run()
                if e.key==pygame.K_2:
                    show_leaderboard()
                if e.key==pygame.K_ESCAPE:
                    return

main()