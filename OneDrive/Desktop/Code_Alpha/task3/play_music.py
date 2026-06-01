import pygame
import time

pygame.init()

pygame.mixer.music.load("generated_music.mid")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Playback finished..")