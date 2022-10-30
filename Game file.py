import pygame, random


class StartScrn:
    def __init__(self):
        self.fontti = pygame.font.SysFont("Arial", 22)
        self.eteenpain = True
        self.silmukka()
    
    def silmukka(self):
        while self.eteenpain:
            self.tutki_tapahtumat()
            self.piirra_naytto()


    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                self.eteenpain = False
            if tapahtuma.type == pygame.QUIT:
                exit()

    def piirra_naytto(self):
        naytto.fill((0, 0, 255),(0, 0, 640, 480))
        #robotti
        naytto.blit(robo, (640/2 - (robo.get_width()/2), 480-robo.get_height()))
        #ruudun pohja mustaksi, pisteet, uusi peli yms.
        naytto.fill((0,0,0), (0, 481, 640, 530 ))
        #ohjeteksti
        teksti = self.fontti.render("Kerää kolikoita ja väistä hirviöitä! Press any key to cont.", True, (255, 0, 0))
        naytto.blit(teksti, (25, 485))
        
        pygame.display.flip()
 
        kello.tick(60)

class Rahasade:
    def __init__(self):
        
        self.robotti = pygame.Rect(640/2 - (robo.get_width()/2),480-robo.get_height(), robo.get_width(), robo.get_height())
        self.rahat = []
        self.monsut = []
        self.pisteet = 0
        self.peli_kaynnissa = True
        self.fontti = pygame.font.SysFont("Arial", 22)
        self.oikealle=False
        self.vasemmalle=False
        #Ei mitään käsitystä monta kolikkoa tai hirviötä olisi hyvä niin laitoin 20 + 5.
        for i in range(20):
            self.rahat.append(pygame.Rect(random.randint(0, 640-kolikko.get_width()), random.randint(-600, 0-kolikko.get_height()), kolikko.get_width(), kolikko.get_height()))
        for i in range(5):
            self.monsut.append(pygame.Rect(random.randint(0, 640-hirvio.get_width()), random.randint(-600, 0-hirvio.get_height()), hirvio.get_width(), hirvio.get_height()))
 
        self.silmukka()   
 
    def uusi_peli(self):
        for r in self.rahat:
            r.top = random.randint(-600, 0-kolikko.get_height())
            r.left = random.randint(0, 640-kolikko.get_width())
        for h in self.monsut:
            h.top = random.randint(-600, 0-hirvio.get_height())
            h.left = random.randint(0, (640-hirvio.get_width()))
        self.robotti.left = 640/2 - (robo.get_width()/2)
        self.robotti.top = 480-robo.get_height()
        self.pisteet = 0
        self.peli_kaynnissa = True
 
    def peli_ohi(self):
        self.peli_kaynnissa = False
 
    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
 
    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            #jatkuva liike keydownilla jne.
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
 
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
 
 
            if tapahtuma.type == pygame.QUIT:
                exit()
        if self.peli_kaynnissa:    
            #robo liikkuu suuntiin
            if self.oikealle:
                pygame.Rect.move_ip(self.robotti, 2, 0)
            if self.vasemmalle:
                pygame.Rect.move_ip(self.robotti, -2, 0)
            
            #change to colliderect()?
            for r in self.rahat:
                pygame.Rect.move_ip(r, 0, 2)
                if pygame.Rect.colliderect(r, self.robotti):
                    r.top = random.randint(-600, 0-kolikko.get_height())
                    r.left = random.randint(0, 640-kolikko.get_width())
                    self.pisteet+=1
                if r.top >= 480-kolikko.get_height():
                    r.top = random.randint(-600, 0-kolikko.get_height())
                    r.left = random.randint(0, 640-kolikko.get_width())

            for h in self.monsut:
                pygame.Rect.move_ip(h, 0, 3)
                if pygame.Rect.colliderect(h, self.robotti):
                    self.peli_ohi()
                if h.top >= 480:
                    h.top = random.randint(-600, 0-hirvio.get_height())
                    h.left = random.randint(0, (640-hirvio.get_width()))

    def piirra_naytto(self):
        naytto.fill((0, 0, 255),(0, 0, 640, 480))
        #tulostus loopit
        for r in self.rahat:
            naytto.blit(kolikko, (r.left, r.top))
        for h in self.monsut:
            naytto.blit(hirvio, (h.left, h.top))
        #robotti
        naytto.blit(robo, (self.robotti.left, self.robotti.top))
        #ruudun pohja mustaksi, pisteet, uusi peli yms.
        naytto.fill((0,0,0), (0, 481, 640, 530 ))
        teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (255, 0, 0))
        naytto.blit(teksti, (25, 485))
        teksti = self.fontti.render("F2 = uusi peli", True, (255, 0, 0))
        naytto.blit(teksti, (300, 485))
        pygame.display.flip()
 
        kello.tick(60)
 

if __name__ == "__main__":

    #load pics
    robo = pygame.image.load("robo.png")
    kolikko = pygame.image.load("kolikko.png")
    hirvio = pygame.image.load("hirvio.png")



    #pygame setup
    pygame.init()
    kello = pygame.time.Clock()
    naytto = pygame.display.set_mode((640, 530))
    pygame.display.set_caption("Rahasade")

    StartScrn()
    Rahasade()
