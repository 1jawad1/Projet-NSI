import pygame 
from client import Client
from protocols import Protocols


class Game:
    def __init__(self, client):
        self.client = client
        client.start()

        self.font = None
        self.input_box = pygame.Rect(100, 100, 400, 32)
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("lightskyblue3")
        self.color = self.color_inactive

        self.text = ''
        self.done = False
        self.logged_in = False
    
    def handle_event():
        pass

    def draw(self, screen):
        screen.fill(255, 255, 255)
        if not self.logged_in and not self.client.started:
            self.draw_login(screen)
        elif not self.client.started:
            self.draw_waiting(screen)
        else:
            self.draw_game(screen)
        pygame.display.update()
    
    def draw_login(self, screen):
        prompt="Enter a nickname"
        prompt_surface = self.font.render(prompt, 1, (0,0,0))
        screen.blit(prompt_surface, (100, 50))

        pygame.draw.rect(screen, self.color, self.input_box, 2)
        txt_surface = self.font.render(self.text, 1, self.color)
        screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        self.input_box.w = max(100, txt_surface.get_width()+10)


    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        self.font = pygame.font.SkyFont('comicsans', 32)

        while not self.client.closed:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                else:
                    self.handle_event(event)
        self.draw(screen)
                

if __name__ == '__main__':
    game = Game(Client())
    game.run()