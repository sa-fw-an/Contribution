import pygame
import subprocess
import random
from datetime import datetime, timedelta
import os
import threading

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PRIMARY = (30, 136, 229)
SECONDARY = (255, 87, 34)
BACKGROUND = (38, 50, 56)
SURFACE = (55, 71, 79)
FONT = pygame.font.Font(None, 24)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GitHub Contribution Generator")

# Animation variables
spinner_angle = 0
loading = False

# UI Elements
buttons = [
    {"text": "Generate Contributions", "rect": pygame.Rect(100, 500, 250, 50)},
    {"text": "Clear", "rect": pygame.Rect(100, 570, 250, 50)},
]

input_fields = [
    {"label": "Start Date (YYYY-MM-DD)", "rect": pygame.Rect(100, 100, 250, 40), "value": "", "active": False},
    {"label": "End Date (YYYY-MM-DD)", "rect": pygame.Rect(100, 180, 250, 40), "value": "", "active": False},
    {"label": "Max Contributions/Day", "rect": pygame.Rect(100, 260, 250, 40), "value": "", "active": False},
    {"label": "Min Contributions/Day", "rect": pygame.Rect(100, 340, 250, 40), "value": "", "active": False},
]

def draw_spinner():
    global spinner_angle
    center = (WIDTH//2, HEIGHT//2)
    radius = 30
    pygame.draw.arc(screen, PRIMARY, (center[0]-radius, center[1]-radius, radius*2, radius*2), 
                   spinner_angle/57.3, (spinner_angle+270)/57.3, 5)
    spinner_angle = (spinner_angle + 5) % 360

def generate_fake_contributions(start_date, end_date, max_contributions, min_contributions):
    global loading
    try:
        repo_path = "."
        os.chdir(repo_path)

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        random_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        for commit_date in random_dates:
            commits_per_day = random.randint(min_contributions, max_contributions)
            
            for _ in range(commits_per_day):
                random_time = commit_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
                formatted_date = random_time.strftime('%Y-%m-%dT%H:%M:%S')
                
                with open("contribution.txt", "a") as file:
                    file.write(f"Commit for {formatted_date}\n")
                
                subprocess.run(["git", "add", "contribution.txt"])
                subprocess.run(["git", "commit", "-m", f"Contribution for {formatted_date}", "--date", formatted_date])
        
        subprocess.run(["git", "push", "origin", "main"])
        with open("contribution.txt", "w") as file:
            file.write("")
        subprocess.run(["git", "add", "contribution.txt"])
        subprocess.run(["git", "commit", "-m", "Reset contribution file"])
        subprocess.run(["git", "push", "origin", "main"])
        
        loading = False
    except Exception as e:
        loading = False
        print(f"Error: {str(e)}")

running = True
while running:
    screen.fill(BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button["rect"].collidepoint(mouse_x, mouse_y):
                    if button["text"] == "Generate Contributions" and not loading:
                        try:
                            start_date = input_fields[0]["value"]
                            end_date = input_fields[1]["value"]
                            max_contributions = int(input_fields[2]["value"])
                            min_contributions = int(input_fields[3]["value"])
                            loading = True
                            threading.Thread(target=generate_fake_contributions, 
                                           args=(start_date, end_date, max_contributions, min_contributions)).start()
                        except ValueError:
                            loading = False
                    elif button["text"] == "Clear":
                        for field in input_fields:
                            field["value"] = ""
            
            for field in input_fields:
                if field["rect"].collidepoint(mouse_x, mouse_y):
                    field["active"] = True
                else:
                    field["active"] = False
        
        elif event.type == pygame.KEYDOWN:
            for field in input_fields:
                if field["active"]:
                    if event.key == pygame.K_BACKSPACE:
                        field["value"] = field["value"][:-1]
                    else:
                        field["value"] += event.unicode

    # Draw input fields
    for field in input_fields:
        color = SURFACE if not field["active"] else PRIMARY
        pygame.draw.rect(screen, color, field["rect"], border_radius=5)
        label = FONT.render(field["label"], True, WHITE)
        screen.blit(label, (field["rect"].x, field["rect"].y - 30))
        text = FONT.render(field["value"], True, WHITE)
        screen.blit(text, (field["rect"].x + 10, field["rect"].y + 10))

    # Draw buttons
    for button in buttons:
        color = PRIMARY if button["rect"].collidepoint(mouse_x, mouse_y) else SURFACE
        pygame.draw.rect(screen, color, button["rect"], border_radius=10)
        text = FONT.render(button["text"], True, WHITE)
        screen.blit(text, (button["rect"].x + 20, button["rect"].y + 15))
    
    # Draw loading animation
    if loading:
        draw_spinner()
    
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()