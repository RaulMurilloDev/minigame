import pygame
import sys
import os
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Memory Harness Game")

# Colors
WHITE = (255, 255, 255)
DARK_BG = (20, 20, 30)
TEXT_COLOR = (220, 220, 220)
TIMER_COLOR = (255, 200, 100)
CORRECT_COLOR = (50, 200, 100)
INCORRECT_COLOR = (200, 50, 50)

# Font loading
def load_font(name, size):
    try:
        return pygame.font.Font(name, size)
    except:
        return pygame.font.SysFont("arial", size, bold=True)

TITLE_FONT = load_font(None, 64)
TEXT_FONT = load_font(None, 40)
TIMER_FONT = load_font(None, 50)

# Questions setup
questions = [
    {
        "prompt": "¿Qué es el terminal en el arnés?",
        "images": ["other1.PNG", "other2.PNG", "other3.PNG", "terminal.PNG"],
        "correct": "terminal.PNG",
        "sound": "OK.mp3"
    },
    {
        "prompt": "¿Cuál es el módulo del arnés?",
        "images": ["other1.PNG", "other2.PNG", "other4.PNG", "module.PNG"],
        "correct": "module.PNG",
        "sound": "success.mp3"
    }
]

# Load images
def load_image(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, size)

# Draw centered text
def draw_text(surface, text, font, color, y, center=True):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(SCREEN_WIDTH//2, y) if center else (10, y))
    surface.blit(render, rect)

# Gradient background
def draw_gradient(surface, top_color, bottom_color):
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

# Show memorization screen
def show_memorization(image_path, seconds):
    img = load_image(image_path, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    start_time = time.time()
    while time.time() - start_time < seconds:
        draw_gradient(screen, (10, 10, 20), (30, 30, 40))
        screen.blit(img, img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        remaining = seconds - int(time.time() - start_time)
        draw_text(screen, f"Tienes {remaining} segundos para memorizar el arnés!", TEXT_FONT, TIMER_COLOR, 80)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

# Show question
def ask_question(question):
    prompt = question["prompt"]
    images = question["images"]
    correct = question["correct"]
    sound = question["sound"]

    cols = 2
    img_size = (SCREEN_WIDTH//4, SCREEN_HEIGHT//4)
    padding = 50
    positions = []

    # Calculate grid starting position
    total_width = cols * img_size[0] + (cols - 1) * padding
    total_height = ((len(images) + 1) // cols) * img_size[1] + (((len(images) + 1) // cols) - 1) * padding
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = (SCREEN_HEIGHT - total_height) // 2

    # Load images and positions
    loaded_images = []
    for idx, img_name in enumerate(images):
        img = load_image(img_name, img_size)
        row = idx // cols
        col = idx % cols
        x = start_x + col * (img_size[0] + padding)
        y = start_y + row * (img_size[1] + padding)
        positions.append((x, y))
        loaded_images.append(img)

    selected = None
    running = True
    while running:
        draw_gradient(screen, (10, 10, 20), (30, 30, 40))
        draw_text(screen, prompt, TEXT_FONT, TEXT_COLOR, 80)

        for idx, img in enumerate(loaded_images):
            rect = img.get_rect(topleft=positions[idx])
            if rect.collidepoint(pygame.mouse.get_pos()):
                img_hover = pygame.transform.smoothscale(img, (int(img_size[0]*1.05), int(img_size[1]*1.05)))
                screen.blit(img_hover, img_hover.get_rect(center=rect.center))
            else:
                screen.blit(img, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for idx, img_name in enumerate(images):
                    rect = loaded_images[idx].get_rect(topleft=positions[idx])
                    if rect.collidepoint(event.pos):
                        selected = img_name
                        running = False
                        break

    if selected == correct:
        pygame.mixer.Sound(sound).play()
        return True
    else:
        return False

# Main game loop
def main():
    show_memorization("complete.PNG", 20)
    score = 0
    for q in questions:
        if ask_question(q):
            score += 1

    # Final result
    draw_gradient(screen, (10, 10, 20), (30, 30, 40))
    result_text = f"Has acertado {score} de {len(questions)} preguntas."
    draw_text(screen, result_text, TITLE_FONT, TEXT_COLOR, SCREEN_HEIGHT//2)
    pygame.display.flip()
    pygame.time.wait(4000)

if __name__ == "__main__":
    main()
    pygame.quit()
