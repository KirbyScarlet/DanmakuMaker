import pygame
import traceback
import dmklib.constants

class Game(object):
    """
    >>> game = Game()
    >>> game.window_size = 1366, 768
    >>> game.scope_size = 600,500
    >>> game.run()
    """

    __window_size = dmklib.constants.DEFAULT_WINDOW_SIZE
    __scope_size = dmklib.constants.DEFAULT_SCOPE_SIZE
    __scope_position = 0, 0
    __window_caption = "danmaku maker"
    __state_code = None
    
    running = True

    @property
    def window_size(self):
        return self.__window_size
    @window_size.setter
    def window_size(self, width, height):
        if not isinstance(width, int) and not isinstance(width, int):
            raise TypeError("please specify main window size correctly!")
        self.__window_size = width, height

    @property
    def scope_size(self):
        return self.__scope_size
    @scope_size.setter
    def scope_size(self, width, height):
        if not isinstance(width, int) and not isinstance(width, int):
            raise TypeError("please specify battle field size correctly!")
        if width > self.__window_size[0] or height > self.__window_size[1]:
            raise ValueError(
                "scope size must be smaller than window size.\n\
                window size: {}".format(self.__window_size)
                )
        self.__scope_size = width, height

    @property
    def scope_position(self):
        return self.__scope_position
    @scope_position.setter
    def scope_position(self, x, y):
        self.__scope_position = x, y

    @property
    def window_caption(self):
        return self.__window_caption
    @window_caption.setter
    def window_caption(self, title):
        self.__window_caption = str(title)

    def cleanup(self):
        pass

    def _run(self):
        pass

    def run(self):
        pygame.init()

        try:
            window = pygame.display.set_mode(self.__window_size)
            pygame.display.set_caption(self.__window_caption)
            scope = pygame.surface.Surface(self.__scope_size)
            window.fill((255,255,255))
            pygame.display.update()

            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                self._run()
                
        except SystemExit:
            pass
        except:
            traceback.print_exc()

        self.cleanup()
        pygame.quit()


    

            