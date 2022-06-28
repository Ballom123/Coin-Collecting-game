import pygame, random
 
class Rahasade:
    def __init__(self):
        pygame.init()
        self.robotti = Robo()
        self.rahat = []
        self.monsut = []
        self.pisteet = 0
        self.peli_kaynnissa = True
        self.fontti = pygame.font.SysFont("Arial", 22)
        self.oikealle=False
        self.vasemmalle=False
        #Ei mitään hajua monta kolikkoa tai hirviötä olisi hyvä :D ni laitoin vaan 20 + 5.
        for i in range(20):
            self.rahat.append(Kultaraha())
        for i in range(5):
            self.monsut.append(Hirvio())
 
        self.kello = pygame.time.Clock()
        self.naytto = pygame.display.set_mode((640, 530))
 
        pygame.display.set_caption("Rahasade")
 
        self.silmukka()   
 
    def uusi_peli(self):
        for raha in self.rahat:
            raha.resetoi_kolikko()
        for monsu in self.monsut:
            monsu.resetoi_hirvio()
        self.robotti.alkuun()
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
                self.robotti.liiku_oikea()
            if self.vasemmalle:
                self.robotti.liiku_vasen()
            
            #rahasade ja mörkö loopit, varmaan voisi rangella iskeä kummatkin samaan looppiin jotenkin.
            #kolikoiden keräily ja mörköjen törmäys tarkistus
            for raha in self.rahat:
                raha.raha_falling_check()
                if self.robotti.robo_y <= raha.kulta_y+raha.kolikko.get_height() <= self.robotti.robo_y+self.robotti.robo.get_height():
                    if self.robotti.robo_x <= raha.kulta_x <= self.robotti.robo_x+self.robotti.robo.get_width() or self.robotti.robo_x <= raha.kulta_x+raha.kolikko.get_width() <= self.robotti.robo_x+self.robotti.robo.get_width():
                        raha.resetoi_kolikko()
                        self.pisteet+=1
            for monsu in self.monsut:
                monsu.hirvio_falling_check()
                if self.robotti.robo_y <= monsu.hirvio_y+monsu.hirvio.get_height() <= self.robotti.robo_y+self.robotti.robo.get_height():
                    if self.robotti.robo_x <= monsu.hirvio_x <= self.robotti.robo_x+self.robotti.robo.get_width() or self.robotti.robo_x <= monsu.hirvio_x+monsu.hirvio.get_width() <= self.robotti.robo_x+self.robotti.robo.get_width():
                        self.peli_ohi()
 
        
 
 
    def piirra_naytto(self):
        self.naytto.fill((0, 0, 255),(0, 0, 640, 480))
        #tulostus loopit
        for raha in self.rahat:
            self.naytto.blit(raha.kolikko, (raha.kulta_x, raha.kulta_y))
        for monsu in self.monsut:
            self.naytto.blit(monsu.hirvio, (monsu.hirvio_x, monsu.hirvio_y))
        #robotti
        self.naytto.blit(self.robotti.robo, (self.robotti.robo_x, self.robotti.robo_y))
        #ruudun pohja mustaksi, pisteet, uusi peli yms.
        self.naytto.fill((0,0,0), (0, 481, 640, 530 ))
        teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (25, 485))
        teksti = self.fontti.render("F2 = uusi peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (300, 485))
        pygame.display.flip()
 
        self.kello.tick(60)
 
 
#oliot robotille, kolikoille, hirviölle en tiiä onko tehokkainta :D
class Robo:
    #yleinen robokuva luokkamuuttujaksi, varmaan parmempiakin paikkoja tälle
    robo = pygame.image.load("robo.png")
    #aloittaa keskeltä
    def __init__(self):
        self.robo_x= 640/2 - (self.robo.get_width()/2)
        self.robo_y= 480-self.robo.get_height()
 
    #resetoi olion
    def alkuun(self):
        self.robo_x= 640/2 - (self.robo.get_width()/2)
        self.robo_y= 480-self.robo.get_height()
    
    #liike metodit tarkistaa samalla seinät
    def liiku_oikea(self):
        if self.robo_x >= 640-self.robo.get_width():
            return
        self.robo_x+=2
    def liiku_vasen(self):
        if self.robo_x <= 0:
            return
        self.robo_x-=2
 
class Kultaraha:
    kolikko = pygame.image.load("kolikko.png")
    #satunnainen spawnikohde kolikoille, ei myöskään hajua kuinka korkealla kolikoita kannattaa asettaa maksimissaan.
    def __init__(self):
        self.kulta_x = random.randint(0, 640-self.kolikko.get_width())
        self.kulta_y = random.randint(-600, 0-self.kolikko.get_height())
 
    #heittää takasin taivaaseen.
    def resetoi_kolikko(self):
        self.kulta_x = random.randint(0, (640-self.kolikko.get_width()))
        self.kulta_y = random.randint(-600, 0-self.kolikko.get_height())
            
    def raha_falling_check(self):
        self.kulta_y+=2
        if self.kulta_y >= 480-self.kolikko.get_height():
            self.resetoi_kolikko()
    
class Hirvio:
    #kopio Kultaraha luokasta, lisätään vaan eri toiminnallisuus
    hirvio = pygame.image.load("hirvio.png")
    #satunnainen spawnikohde möröille jne.
    def __init__(self):
        self.hirvio_x = random.randint(0, 640-self.hirvio.get_width())
        self.hirvio_y = random.randint(-600, 0-self.hirvio.get_height())
 
    #heittää takasin taivaaseen.
    def resetoi_hirvio(self):
        self.hirvio_x = random.randint(0, (640-self.hirvio.get_width()))
        self.hirvio_y = random.randint(-600, 0-self.hirvio.get_height())
            
    def hirvio_falling_check(self):
        #vähän nopeampi kuin kolikko
        self.hirvio_y+=3
        if self.hirvio_y >= 480-self.hirvio.get_height():
            self.resetoi_hirvio()
 
 
if __name__ == "__main__":
    Rahasade()
