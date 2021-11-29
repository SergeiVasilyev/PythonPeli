import pygame

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
        self.kuva_pieni = pygame.transform.rotozoom(self.kuva_iso, -45, 0.25) # image rotation and size
        self.kulma = 0
        self.sijainti = (400, 300)
        self.nappi_pohjassa = False
 
    def tapahtuma(self, event):
        if event.type == pygame.QUIT:
            self.ajossa = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.nappi_pohjassa = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.nappi_pohjassa = False
            # self.sijainti = pygame.mouse.get_pos() # расположение картинки по положению мышки
 
    def pelilogiikka(self):
        if self.nappi_pohjassa:
            self.sijainti = pygame.mouse.get_pos() # расположение картинки по положению мышки
        # self.kulma -= ((360/60)/6)
        self.kulma = (self.kulma - 3) % 360
        self.kulma = 0
 
    def renderointi(self):
        self.naytto.fill(TAUSTAVARI) # заливка экрана RGB
        kuva = pygame.transform.rotozoom(self.kuva_pieni, self.kulma, 1)
        # keskipiste = self.kuva_pieni.get_rect(topleft=(0, 0)).center # make center picture
        # laatikko = kuva.get_rect(center=keskipiste)
        laatikko = kuva.get_rect(center=self.sijainti) 
        self.naytto.blit(kuva, laatikko.topleft) # image coordinates
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