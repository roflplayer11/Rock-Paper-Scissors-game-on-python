import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
FPS = 240
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BACKGROUND = pygame.image.load("background1.png")
score = 0

font = pygame.font.Font(None, 32)
title_font = pygame.font.Font(None, 48)

CHOICES = {
    "rock": "Rock",
    "paper": "Paper",
    "scissors": "Scissors"
}

WIN_RULES = {
    ("Rock", "Scissors"): "You win!",
    ("Scissors", "Paper"): "You win!",
    ("Paper", "Rock"): "You win!",
    ("Scissors", "Rock"): "Computer win!",
    ("Paper", "Scissors"): "Computer win!",
    ("Rock", "Paper"): "Computer win!",
}

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, surface, enabled=True):
        current_color = self.color if enabled else DARK_GRAY
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

pygame.display.set_caption("Rock, Paper, Scissors")
clock = pygame.time.Clock()

button_width = 250
button_height = 55
spacing = 50
total_width = 3 * button_width + 2 * spacing
start_x = (1920 - total_width) // 2

buttons = {
    "rock": Button(start_x, 400, button_width, button_height, "Rock"),
    "paper": Button(start_x + button_width + spacing, 400, button_width, button_height, "Paper"),
    "scissors": Button(start_x + 2*(button_width + spacing), 400, button_width, button_height, "Scissors"),
    "retry": Button(650, 550, 200, 40, "Play again", GREEN),
    "quit": Button(1050, 550, 200, 40, "Exit", RED)
}

def draw_game(user_choice, pc_choice, result, choices_enabled):

    screen.blit(BACKGROUND, (0, 0))
    
    title = title_font.render("Rock, Paper, Scissors!", True, BLACK)
    title_rect = title.get_rect(center=(screen.get_width()//2, 50))
    screen.blit(title, title_rect)
    
    user_text = font.render(f"Your choice: {user_choice}", True, BLACK)
    screen.blit(user_text, (50, 200))
    
    pc_text = font.render(f"Computer choice: {pc_choice}", True, BLACK)
    screen.blit(pc_text, (50, 250))

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (1750, 200))
    
    if result:
        result_color = GREEN if "You" in result else RED if "Computer" in result else BLACK
        result_text = font.render(result, True, result_color)
        result_rect = result_text.get_rect(center=(screen.get_width()//2, 300))
        screen.blit(result_text, result_rect)
    
    for keys, btn in buttons.items():
        if keys in ["rock", "paper", "scissors"]:
            btn.draw(screen, enabled=choices_enabled)
        else:
            btn.draw(screen)
    
    pygame.display.flip()

def main():
    global score
    user_choice = ""
    pc_choice = ""
    result = ""
    choices_enabled = True
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                for key, btn in buttons.items():
                    if btn.is_clicked(pos):
                        if key == "quit":
                            running = False
                            pygame.quit()
                            sys.exit()
                        elif key == "retry":
                            user_choice = ""
                            pc_choice = ""
                            result = ""
                            choices_enabled = True
                        elif key in ["rock", "paper", "scissors"]:
                            if choices_enabled:
                                user_choice = CHOICES[key]
                                pc_choice = CHOICES[random.choice(list(CHOICES.keys()))]
                            
                            if user_choice == pc_choice:
                                result = "Draw!"
                            else:
                                result = WIN_RULES.get((user_choice, pc_choice), "Error") 

                                if result == "You win!":
                                    score += 1
                            
                            choices_enabled = False
        
        draw_game(user_choice, pc_choice, result, choices_enabled)

if __name__ == "__main__":
    main()
    pygame.quit()