import pygame
import sys
import random

# KHỞI TẠO PYGAME
pygame.init()

# THIẾT LẬP MÀN HÌNH
WIDTH, HEIGHT = 500,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# MÀU SẮC
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 204, 153)
# BIẾN CỦA GAME
gravity = 2
bird_jump = -17
pipe_gap = 200
pipe_width = 70
pipe_speed = 5

# CÀI ĐẶT HÌNH ẢNH
bird_img = pygame.image.load("fireball.png").convert_alpha()  # THÊM HÌNH CHÚ CHIM
bird_img = pygame.transform.scale(bird_img, (40, 40))

background_img = pygame.image.load("background-night.png").convert_alpha()  # BACKGROUND
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pipe_img= pygame.image.load("green-pipe.png").convert_alpha()
pipe_img= pygame.transform.scale(pipe_img,(pipe_width,HEIGHT))
flipped_pipe_img = pygame.transform.flip(pipe_img, False, True)
# THÔNG SỐ GAME
bird_x, bird_y = 100, HEIGHT // 2
bird_speed = 0
score = 0
font = pygame.font.Font("04B_19.ttf", 28)


# Tạo ống
pipes = []
pipe_timer = 0
# HÀM TẠO ống
def create_pipe():
    pipe_top = random.randint(50, HEIGHT - pipe_gap - 50)
    pipe_bottom = pipe_top + pipe_gap
    pipes.append((WIDTH, pipe_top, pipe_bottom))\
    

# MÀN HÌNH BẮT ĐẦU
def start_screen():
    screen.blit(background_img, (0, 0))
    title_text = font.render("Flappy Bird", True, BLACK)
    instruction_text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# MÀN HÌNH KẾT THÚC
def game_over_screen(final_score):
   while True:
    screen.blit(background_img, (0, 0))
    game_over_text = font.render("GAME OVER", True, BLACK)
    score_text = font.render(f"Score: {final_score}", True, BLACK)
    restart_text = font.render("Press ENTER to Restart", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 3 // 4))
    pygame.display.flip()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Phím Enter
                return  # Thoát khỏi hàm và quay lại màn hình bắt đầu

# VÒNG LẶP CHÍNH CỦA GAME
def game_loop():
    global bird_y, bird_speed, score, pipes, pipe_timer, bird_path, pipe_speed
    # Reset các biến khi bắt đầu lại game
    bird_y = HEIGHT // 2
    bird_speed = 0
    score = 0
    pipes = []
    pipe_timer = 0
    pipe_speed =5
    running = True
    while running:
        # VẼ BACKGROUND
        screen.blit(background_img, (0, 0))
        
        # SỰ KIỆN TRONG GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_speed = bird_jump  # Chim nhảy lên
    
        # VẼ CHIM
        
        bird_speed += gravity
        bird_y += bird_speed * 0.5 *gravity
        screen.blit(bird_img, (bird_x, bird_y))

        # TẠO ỐNG MỚI
        pipe_timer += 0.9
        if pipe_timer > random.randrange(50, 90, 10 ):
            create_pipe()
            pipe_timer = 0
        
        
        # DI CHUYỂN VÀ VẼ ỐNG
        for pipe in pipes[:]:
            pipe_x, pipe_top, pipe_bottom = pipe
            pipe_x -= pipe_speed
            if pipe_x < -pipe_width:
                pipes.remove(pipe)
            else:
                # Vẽ ống
                screen.blit(flipped_pipe_img, (pipe_x, pipe_top - pipe_img.get_height()))  # Ống trên
                screen.blit(pipe_img, (pipe_x, pipe_bottom))  # Ống dưới
                pipes[pipes.index(pipe)] = (pipe_x, pipe_top, pipe_bottom)

            # Kiểm tra va chạm
            if bird_x + 40 > pipe_x and bird_x < pipe_x + pipe_width:
                if bird_y < pipe_top or bird_y + 30 > pipe_bottom:
                    pygame.time.wait(1000)
                    game_over_screen(score)  # Hiển thị màn hình kết thúc
                    return  # Kết thúc vòng lặp game

            # Tăng điểm khi chim vượt qua ống
            if (pipe_x+pipe_width)//2 == bird_x:
                score += 1
               
   
        # Kiểm tra va chạm với màn hình
        if bird_y < 0  or bird_y >HEIGHT:  
            pygame.time.wait(1000)       
            game_over_screen(score)
            pygame.display.flip()
            return

        # VẼ ĐIỂM
        score_text = font.render(f"Score: {int(score)}", True, RED)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# MÀN HÌNH BẮT ĐẦU
def start_game():
    while True:  # Vòng lặp liên tục cho phép chơi lại
        start_screen()
        pygame.display.flip() 
        
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False  # Thoát vòng lặp chờ nhấn phím
                    game_loop()  # Gọi lại game loop khi nhấn SPACE
# Chạy game
start_game()