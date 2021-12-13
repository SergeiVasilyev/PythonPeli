import math
import pygame
from pygame.constants import K_LEFT, K_RIGHT

TAUSTAVARI = (180, 180, 240)  # (Red, Green, Blue), 0...255

 
def main():
    peli = Peli()
    peli.aja()
 
 
class Peli:
    def __init__(self):
        self.ajossa = True
        self.naytto = None
        self.leveys = 800
        self.korkeus = 600
        self.nayton_koko = (self.leveys, self.korkeus)
        # self.nayton_koko = (self.weight, self.height) = (800, 600)

 
    def aja(self):
        self.alustus()
        while self.ajossa:
            for event in pygame.event.get():
                self.tapahtuma(event)
            self.pelilogiikka()
            self.renderointi()
        self.lopetus()
 
    def alustus(self):
        pygame.init()
        self.kello = pygame.time.Clock()
        self.naytto = pygame.display.set_mode(
            self.nayton_koko, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # self.kuva_iso = pygame.image.load("rocket_640r2.png")
        self.kuva_iso = pygame.image.load("man.gif")
        # self.kuva = pygame.transform.scale(self.kuva, (512, 512)) # image size
        self.kuva_pieni = pygame.transform.rotozoom(self.kuva_iso, 0, 0.5) # image rotation and size
        self.kulma = 0
        self.pyorimisvauhti = 0
        self.voima = 0
        self.sijainti = (400, 300)
        self.vauhti = 0
        self.hiiren_nappi_pohjassa = False
        self.voimanlisays = False
        self.laukaisu = False
 
    def tapahtuma(self, event):
        if event.type == pygame.QUIT:
            self.ajossa = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.hiiren_nappi_pohjassa = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.hiiren_nappi_pohjassa = False
            # self.sijainti = pygame.mouse.get_pos() # расположение картинки по положению мышки

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.pyorimisvauhti = 3
            elif event.key == pygame.K_RIGHT:
                self.pyorimisvauhti = -3
            elif event.key == pygame.K_SPACE:
                self.voimanlisays = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.pyorimisvauhti = 0
            elif event.key == pygame.K_SPACE:
                self.voimanlisays = False
                self.laukaisu = True

 
    def pelilogiikka(self):
        if self.hiiren_nappi_pohjassa:
            self.sijainti = pygame.mouse.get_pos() # расположение картинки по положению мышки
        if self.pyorimisvauhti != 0:
            self.kulma = (self.kulma + self.pyorimisvauhti) % 360

        if self.voimanlisays:
            self.voima = min(self.voima + 2, 100)
            # print (self.voima)
        
        if self.laukaisu:
            # print (f"Pam {self.voima}")
            self.vauhti = self.voima ** 2 / 100
            self.voima = 0
            self.laukaisu = False
        
        if self.vauhti > 0.1:
            vauhti_x = -self.vauhti * math.sin(self.kulma / 180 * math.pi)
            vauhti_y = -self.vauhti * math.cos(self.kulma / 180 * math.pi)
            uusi_x = self.sijainti[0] + vauhti_x
            uusi_y = self.sijainti[1] + vauhti_y
            self.sijainti = (uusi_x, uusi_y)
            self.vauhti *= 0.99 # затухание

        # self.kulma -= ((360/60)/6)
        # self.kulma = (self.kulma - 3) % 360 # вращение картинки
        # self.kulma = 0
 
    def renderointi(self):
        self.naytto.fill(TAUSTAVARI) # заливка экрана RGB
        kuva = pygame.transform.rotozoom(self.kuva_pieni, self.kulma, 1)
        # keskipiste = self.kuva_pieni.get_rect(topleft=(0, 0)).center # make center picture
        # laatikko = kuva.get_rect(center=keskipiste)
        laatikko = kuva.get_rect(center=self.sijainti) 
        self.naytto.blit(kuva, laatikko.topleft) # image coordinates
        
        pygame.draw.rect(self.naytto, (0, 0, 0), (2, self.korkeus-19, 102, 17))
        pygame.draw.rect(self.naytto, (0, 255, 0), (3, self.korkeus-18, self.voima, 15))
        suuntapallo_x = self.leveys - 35
        suuntapallo_y = self.korkeus - 35
        vektori_x = -30 * math.sin(self.kulma / 180 * math.pi)
        vektori_y = -30 * math.cos(self.kulma / 180 * math.pi)
        suuntapallo_x = self.leveys - 30
        suuntapallo_y = self.korkeus - 30
        pygame.draw.circle(self.naytto, (0, 0, 0), (suuntapallo_x, suuntapallo_y), 30)
        pygame.draw.line(self.naytto, (255, 0, 0), (suuntapallo_x, suuntapallo_y), (suuntapallo_x + vektori_x, suuntapallo_y + vektori_y))
        pygame.display.flip()

        # print('laatikko :', laatikko)
        # print('laatikko.topleft :', laatikko.topleft)
        # print('laatikko.bottomright :', laatikko.bottomright)
        # print('laatikko.center :', laatikko.center)
        self.kello.tick(60)  # 60 fps
        # if self.kulma % 100 == 0:
        #     print(self.kello.get_fps()) # текущий fps

 
    def lopetus(self):
        pygame.quit()
 
 
if __name__ == "__main__" :
    main()