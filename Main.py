import pygame
import random
import math
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Particle System with UI and Wind")
clock = pygame.time.Clock()

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DUST_COLOR = WHITE  # 초기 입자 색상

# 중력 및 바람 설정
GRAVITY = 0.005
WIND_FORCE = -1.0  # 위쪽 방향 바람 힘


center_x, center_y = WIDTH // 2, HEIGHT // 2

# 시계방향 회전 바람 상태
rotate_wind_active = False



# 입자 클래스
class Particle:
    def __init__(self, x, y, color=DUST_COLOR):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.radius = 2
        self.color = color

    def apply_gravity(self):
        self.vy += GRAVITY

    def apply_wind(self):
        self.vy += WIND_FORCE

    def apply_curl_rotate_wind(self):

            # 시계방향 회전 바람 적용
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            dx = self.x - center_x
            dy = self.y - center_y

            # 회전 각도 계산 (현재 위치에서의 각도)
            angle = math.atan2(dy, dx)

            # 회전 속도 (값이 작을수록 천천히 회전)
            rotate_speed = 0.02

            # 새로운 각도 적용 (시계방향 회전)
            new_angle = angle + rotate_speed

            # 원래 중심으로부터의 거리 유지
            distance = math.hypot(dx, dy)
            self.x = center_x + distance * math.cos(new_angle)
            self.y = center_y + distance * math.sin(new_angle)

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # 화면 경계 처리 (파티클이 경계에 닿으면 속도를 0으로 설정)
        if self.x < 0:
            self.x = 0
            self.vx = 0
        if self.x > WIDTH:
            self.x = WIDTH
            self.vx = 0
        if self.y < 0:
            self.y = 0
            self.vy = 0
        if self.y > HEIGHT:
            self.y = HEIGHT
            self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# 입자 초기화 함수
def create_particles(num_particles=300, color=DUST_COLOR):
    return [Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), color) for _ in range(num_particles)]




# 초기 입자 생성
particles = create_particles()

# UI 버튼 설정
reset_button = pygame.Rect(20, 20, 100, 30)  # 왼쪽 상단의 "다시 시작" 버튼
rotate_button = pygame.Rect(WIDTH // 2 - 15, 20, 30, 30)  # 가운데 상단의 동그라미 버튼
color_buttons = [
    {"color": RED, "rect": pygame.Rect(WIDTH - 100, 20, 20, 20)},
    {"color": WHITE, "rect": pygame.Rect(WIDTH - 70, 20, 20, 20)},
    {"color": BLUE, "rect": pygame.Rect(WIDTH - 40, 20, 20, 20)},
]

# UI 영역 설정
UI_AREA_HEIGHT = 60  # UI가 위치한 영역 높이

# 메인 루프
running = True
while running:
    mouse_pressed = pygame.mouse.get_pressed()  # 마우스 버튼 상태 확인
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 마우스 클릭 이벤트
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # UI 영역 클릭 처리
            if mouse_y <= UI_AREA_HEIGHT:
                # 다시 시작 버튼 클릭
                if reset_button.collidepoint(event.pos):
                    particles = create_particles()
                # 색상 버튼 클릭 (입자 색상만 변경)
                for button in color_buttons:
                    if button["rect"].collidepoint(event.pos):
                        for particle in particles:
                            particle.color = button["color"]
                # 회전 바람 버튼 클릭
                if rotate_button.collidepoint(event.pos):
                    rotate_wind_active = not rotate_wind_active
            else:
                # UI 영역 밖에서 클릭 시 위 방향 바람 적용
                for particle in particles:
                    if math.hypot(particle.x - mouse_x, particle.y - mouse_y) < 100:
                        particle.apply_wind()

        # 스페이스바 폭발 효과
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                center_x, center_y = WIDTH // 2, HEIGHT // 2
                for particle in particles:
                    dx = particle.x - center_x
                    dy = particle.y - center_y
                    distance = math.hypot(dx, dy)
                    if distance > 0:
                        force = 5 / distance
                        particle.apply_force(dx * force, dy * force)

    # 마우스를 누르고 있는 동안 바람 적용 (UI 영역 제외)
    if mouse_pressed[0] and mouse_y > UI_AREA_HEIGHT:
        for particle in particles:
            if math.hypot(particle.x - mouse_x, particle.y - mouse_y) < 100:
                particle.apply_wind()

    # 회전 바람 적용
    if rotate_wind_active:
        for particle in particles:
            particle.apply_curl_rotate_wind()

    # 화면 업데이트
    screen.fill(BLACK)

    # 입자 업데이트 및 그리기
    for particle in particles:
        particle.apply_gravity()
        particle.update()
        particle.draw(screen)

    # 다시 시작 버튼 그리기
    pygame.draw.rect(screen, WHITE, reset_button)
    font = pygame.font.Font(None, 24)
    text = font.render("다시 시작", True, BLACK)
    screen.blit(text, (reset_button.x + 10, reset_button.y + 5))

    # 회전 바람 버튼 그리기 (동그라미)
    pygame.draw.ellipse(screen, WHITE, rotate_button, 2)
    rotate_text = font.render("⟳", True, WHITE)
    screen.blit(rotate_text, (rotate_button.x + 7, rotate_button.y + 5))

    # 색상 버튼 그리기
    for button in color_buttons:
        pygame.draw.rect(screen, button["color"], button["rect"])
        pygame.draw.rect(screen, WHITE, button["rect"], 2)  # 테두리

    # 화면 갱신
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()






