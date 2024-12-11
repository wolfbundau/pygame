import pygame
import sys
import random

# KHỞI TẠO PYGAME
pygame.init()

#Khởi tạo âm thanh
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sfx_wing.wav")
jump_sound.set_volume(0.7)
die_sound = pygame.mixer.Sound("sfx_hit.wav")
die_sound.set_volume(0.7)
point_sound = pygame.mixer.Sound("sfx_point.wav")
point_sound.set_volume(0.7)
special_sound = pygame.mixer.Sound("sfx_swooshing.wav")
special_sound.set_volume(1)
background_music = pygame.mixer.music.load("sfx_background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) 

# THIẾT LẬP MÀN HÌNH
WIDTH, HEIGHT = 500,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Ball")

# MÀU SẮC
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 10)
# BIẾN CỦA GAME
gravity = 2
ball_jump = -17
pipe_gap = 150
pipe_width = 70
pipe_speed = 5

# CÀI ĐẶT HÌNH ẢNH
powerup_img = pygame.image.load("special_ball.png").convert_alpha()  # Tải ảnh vật phẩm
powerup_img = pygame.transform.scale(powerup_img, (40, 50))  # Tùy chỉnh kích thước

ball_img = pygame.image.load("ballflap.png").convert_alpha()  # THÊM HÌNH BÓNG
ball_img = pygame.transform.scale(ball_img, (30, 30))

background_img = pygame.image.load("background2.png").convert_alpha()  # BACKGROUND
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pipe_img= pygame.image.load("pipe-green.png").convert_alpha()
pipe_img= pygame.transform.scale(pipe_img,(pipe_width,HEIGHT))

flipped_pipe_img = pygame.transform.flip(pipe_img, False, True)
# THÔNG SỐ GAME
ball_x, ball_y = 100, HEIGHT // 2
ball_speed = 0
score = 0
font = pygame.font.Font("04B_19.ttf", 28)

# Tạo ống
pipes = []
pipe_timer = 40
# HÀM TẠO ống
def create_pipe():
    pipe_top = random.randint(50, HEIGHT - pipe_gap - 50)
    pipe_bottom = pipe_top + pipe_gap
    pipes.append((WIDTH, pipe_top, pipe_bottom))\
    
# MÀN HÌNH BẮT ĐẦU
def start_screen():
    screen.blit(background_img, (0, 0))
    title_text = font.render("FLAPPY BALL", True, BLUE)
    instruction_text = font.render("Press SPACE to Start", True, RED)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# MÀN HÌNH KẾT THÚC
def game_over_screen(final_score):
   while True:
    screen.blit(background_img, (0, 0))
    game_over_text = font.render("GAME OVER", True, BLUE)
    score_text = font.render(f"Score: {final_score}", True, RED)
    restart_text = font.render("Press ENTER to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 3 // 4))
    pygame.display.flip()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Phím Enter
                return  # Thoát khỏi hàm và quay lại màn hình bắt 
                
# TRẠNG THÁI BÓNG ĐẶC BIỆT
powerup_active = False  # Vật phẩm có đang hoạt động không
powerup_x, powerup_y = 0, 0  # Tọa độ của vật phẩm
is_invincible = False  # Trạng thái "vô hình"    

# TẠO BÓNG ĐẶC BIỆT
def handle_powerup(ball_rect, pipe_speed): 
    global powerup_active, powerup_x, powerup_y, is_invincible, invincible_timer, ball_img
    # Nếu vật phẩm chưa xuất hiện, tạo ngẫu nhiên
    if not powerup_active: 
       for pipe in pipes:
         pipe_x,pipe_top,pipe_bottom = pipe
         if pipe_x + pipe_width > ball_x:
            if random.random()<0.005:
                powerup_x =pipe_x +pipe_width //2
                powerup_y = pipe_bottom - pipe_gap //2
                powerup_active = True
                break

    # Di chuyển vật phẩm và vẽ lên màn hình
    if powerup_active:
        powerup_x -= pipe_speed  # Di chuyển vật phẩm sang trái
        screen.blit(powerup_img, (powerup_x, powerup_y))

        # Nếu vật phẩm ra khỏi màn hình, đặt lại trạng thái
        if powerup_x < -30:
            powerup_active = False

        # Kiểm tra va chạm giữa bóng và vật phẩm
        powerup_rect = powerup_img.get_rect(topleft=(powerup_x, powerup_y))
        if ball_rect.colliderect(powerup_rect):
            powerup_active = False  # Vật phẩm biến mất
            is_invincible = True  # Kích hoạt trạng thái đặc biệt
            special_sound.play()
            invincible_timer = pygame.time.get_ticks()  # Ghi lại thời gian bắt đầu
            ball_img = pygame.image.load("special_ball.png").convert_alpha()  # Đổi hình ảnh
            ball_img = pygame.transform.scale(ball_img, (40, 50))  # Tùy chỉnh kích thước

    # Kiểm tra thời gian hiệu ứng đặc biệt
    if is_invincible:
        current_time = pygame.time.get_ticks()
        if current_time - invincible_timer > 5000:  # 5 giây hiệu ứng
            is_invincible = False
            ball_img = pygame.image.load("ballflap.png").convert_alpha()  # Trở lại hình ảnh ban đầu
            ball_img = pygame.transform.scale(ball_img, (30, 30))  # Tùy chỉnh kích thước
            
        time_left = 5000 - (current_time - invincible_timer)  # Thời gian còn lại
        time_percentage = time_left / 5000  # Tỷ lệ phần trăm thời gian còn lại
        bar_width = 40  # Chiều rộng của thanh thời gian
        bar_height = 5  # Chiều cao của thanh thời gian
        # Vẽ thanh nền (background) của thanh thời gian
        pygame.draw.rect(screen, (200, 200, 200), (ball_x, ball_y - 10, bar_width, bar_height))
        # Vẽ thanh thời gian (foreground)
        pygame.draw.rect(screen, (0, 255, 0), (ball_x, ball_y - 10, bar_width * time_percentage, bar_height))  # Màu xanh
        
        time_text = font.render(f"BAT TU TIME !!!!", True, RED)
        screen.blit(time_text, (150, 40 ))
    return ball_img

# VÒNG LẶP CHÍNH CỦA GAME
def game_loop():
    global ball_y, ball_speed, score, pipes, pipe_timer, ball_path, pipe_speed,time_left, powerup_active, is_invincible, invincible_timer
    # Reset các biến khi bắt đầu lại game
    ball_y = HEIGHT // 2
    ball_speed = 0
    score = 0
    pipes = []
    pipe_timer = 40
    pipe_speed =5
    running = True
    powerup_active = False  # Đặt lại vật phẩm đặc biệt
    is_invincible = False  # Đặt lại trạng thái vô hình
    invincible_timer = 0  # Đặt lại bộ đếm thời gian
    ball_img = pygame.image.load("ballflap.png").convert_alpha()  
    ball_img = pygame.transform.scale(ball_img, (30, 30))  
    time_left=0

    while running:
        # VẼ BACKGROUND
        screen.blit(background_img, (0, 0))
        # SỰ KIỆN TRONG GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump_sound.play()
                ball_speed = ball_jump  # Bóng nhảy lên


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
        
            # Tăng điểm khi bóng vượt qua ống
            if (pipe_x+pipe_width)//2 == ball_x:
                score += 1
                point_sound.play()
        
        # VẼ BÓNG
        ball_speed += gravity 
        ball_y += ball_speed * 0.5 *gravity
        screen.blit(ball_img, (ball_x, ball_y))

        ball_rect = ball_img.get_rect(topleft=(ball_x, ball_y))
        ball_img = handle_powerup(ball_rect, pipe_speed)

     

        #Kiểm tra va chạm với ống
        if not is_invincible:
            for pipe in pipes[:]:
               pipe_x, pipe_top, pipe_bottom = pipe
               pipe_rect_top = flipped_pipe_img.get_rect(topleft=(pipe_x, pipe_top - pipe_img.get_height()))
               pipe_rect_bottom = pipe_img.get_rect(topleft=(pipe_x, pipe_bottom))
               if ball_rect.colliderect(pipe_rect_top) or ball_rect.colliderect(pipe_rect_bottom):
                  die_sound.play()
                  pygame.time.wait(1000)
                  game_over_screen(score)
                  return

        # Kiểm tra va chạm với màn hình
        if ball_y < 0  or ball_y >HEIGHT: 
            die_sound.play()
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