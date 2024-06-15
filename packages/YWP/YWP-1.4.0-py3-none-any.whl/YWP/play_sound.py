import pygame

def play_sound(filename="tts.mp3"):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(filename)
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)
    sound.stop()
    return "played"