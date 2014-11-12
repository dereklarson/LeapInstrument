import sys, os, pygame, time


class InstrDisplay(object):

    def __init__(self, size, font, font_size):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.bg_color = [10, 10, 10]
        self.size = size
        self.bar1 = {'pos': [self.size[0]/4, self.size[1]/4],
                    'size': [self.size[0]/6, self.size[1]/2]}
        self.bar2 = {'pos': [2*self.size[0]/3, self.size[1]/4],
                    'size': [self.size[0]/6, self.size[1]/2]}
        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont(font, font_size)
        self.draw_all(0.3, 200., 1.)
        pygame.display.flip()

    def clean(self):
        pygame.display.quit()

    def draw_all(self, vol, pitch, w1):
        self.screen.fill(self.bg_color)
        pygame.draw.rect(self.screen, [140, 140, 140],
                self.bar1['pos'] + self.bar1['size'], 2)
        pygame.draw.rect(self.screen, [140, 140, 140],
                self.bar2['pos'] + self.bar2['size'], 2)
        self.draw_volume(vol)
        self.draw_pitch(pitch, w1)
        pygame.display.flip()

    def write(self, text, color=(0, 0, 255), centered=True, pos=(0,0)):
        label = self.font.render(text, 4, color)
        if centered:
            pos = label.get_rect(centerx=self.size[0]/2, centery=self.size[1]/2)
        self.redraw()
        self.screen.blit(label, pos)
        pygame.display.flip()

    def draw_volume(self, vol):
        pos = [self.bar1['pos'][0], self.bar1['pos'][1] + 
                                int((1 - vol) * self.bar1['size'][1])]
        box = pos + [self.bar2['size'][0], 15]
        color = [50 + int(vol * 200)] * 3
        pygame.draw.rect(self.screen, color, box)

    def draw_pitch(self, pitch, w1):
        pitch = max(0, min(1, pitch/400.))
        pos = [self.bar2['pos'][0], self.bar2['pos'][1] + 
                                int((1 - pitch) * self.bar2['size'][1])]
        box = pos + [self.bar2['size'][0], 15]
        color = [50, 50 + int(w1 * pitch * 200), 50 + int((1 - w1) * pitch * 200)]
        pygame.draw.rect(self.screen, color, box)
