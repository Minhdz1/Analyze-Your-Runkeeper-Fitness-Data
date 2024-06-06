import pygame
import sys
import time
import random

# Khởi tạo pygame
pygame.init()

# Thiết lập màn hình toàn màn hình
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Chạy bộ")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load hình ảnh người chạy bộ (thay thế bằng hình ảnh của bạn)
player_img = pygame.image.load("player.png")

# Giảm kích thước của người chơi xuống 1/10
player_width, player_height = player_img.get_size()
scaled_width = player_width // 10
scaled_height = player_height // 10
player_img = pygame.transform.scale(player_img, (scaled_width, scaled_height))

# Load hình ảnh viên đá (thay thế bằng hình ảnh của bạn)
rock_img = pygame.image.load("rock.png")
rock_width, rock_height = rock_img.get_size()
scaled_rock_width = rock_width // 10
scaled_rock_height = rock_height // 10
rock_img = pygame.transform.scale(rock_img, (scaled_rock_width, scaled_rock_height))

# Vị trí và tốc độ của người chạy bộ
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Thông số nhảy
is_jumping = False
jump_height = 150
jump_speed = 10
initial_y = player_y

# Điểm số
score = 0
font = pygame.font.Font(None, 74)

# Thời gian giới hạn
start_time = time.time()
time_limit = 30  # Thời gian giới hạn là 30 giây

# Viên đá rơi
rocks = []
rock_spawn_time = 1
last_rock_spawn = time.time()
rock_speed = 5


# Hàm vẽ người chạy bộ
def draw_player(screen, x, y):
    screen.blit(player_img, (x, y))


# Hàm vẽ điểm số
def draw_score(screen, score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


# Hàm vẽ thời gian
def draw_time(screen, time_left):
    time_text = font.render(f"Time: {time_left}", True, BLACK)
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))


# Hàm vẽ thông báo chiến thắng
def draw_win(screen):
    win_text = font.render("You Win!", True, BLACK)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))


# Hàm vẽ thông báo thua cuộc
def draw_lose(screen):
    lose_text = font.render("You Lose!", True, BLACK)
    screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - lose_text.get_height() // 2))


# Vòng lặp chính
running = True
while running:
    screen.fill(WHITE)

    # Kiểm tra thời gian
    elapsed_time = time.time() - start_time
    time_left = max(0, time_limit - int(elapsed_time))

    if time_left == 0:
        draw_win(screen)
        pygame.display.update()
        pygame.time.wait(3000)  # Hiển thị màn hình "You Win" trong 3 giây
        running = False
        continue

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping:
            is_jumping = True
            score += 1  # Cộng điểm khi nhảy

    # Di chuyển người chạy bộ bằng các phím mũi tên
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Xử lý nhảy
    if is_jumping:
        player_y -= jump_speed
        if player_y <= initial_y - jump_height:
            is_jumping = False
    else:
        if player_y < initial_y:
            player_y += jump_speed
        if player_y > initial_y:
            player_y = initial_y

    # Tạo viên đá rơi khi đạt 100 điểm
    if score >= 100 and time.time() - last_rock_spawn >= rock_spawn_time:
        rock_x = player_x + random.randint(-WIDTH // 2, WIDTH // 2)
        rock_y = player_y - HEIGHT // 2
        rocks.append([rock_x, rock_y])
        last_rock_spawn = time.time()

    # Di chuyển và vẽ viên đá
    for rock in rocks[:]:
        rock[1] += rock_speed
        screen.blit(rock_img, (rock[0] - player_x + WIDTH // 2, rock[1] - player_y + HEIGHT // 2))

        # Kiểm tra va chạm
        if player_x < rock[0] + scaled_rock_width and player_x + scaled_width > rock[0] and player_y < rock[
            1] + scaled_rock_height and player_y + scaled_height > rock[1]:
            draw_lose(screen)
            pygame.display.update()
            pygame.time.wait(3000)  # Hiển thị màn hình "You Lose" trong 3 giây
            running = False
            continue

        # Loại bỏ viên đá nếu ra khỏi màn hình
        if rock[1] - player_y + HEIGHT // 2 > HEIGHT:
            rocks.remove(rock)

    # Vẽ người chạy bộ, điểm số và thời gian lên màn hình
    draw_player(screen, WIDTH // 2 - scaled_width // 2, HEIGHT // 2 - scaled_height // 2)
    draw_score(screen, score)
    draw_time(screen, time_left)

    # Cập nhật màn hình
    pygame.display.update()

    # Điều chỉnh tốc độ khung hình
    pygame.time.Clock().tick(60)

# Kết thúc chương trình
pygame.quit()
sys.exit()
