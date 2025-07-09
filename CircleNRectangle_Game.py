# Inisiasi game dan dunia
import pygame
import random
import time

pygame.init()
panjangWindow = 750
lebarWindow = 750
window = pygame.display.set_mode((panjangWindow, lebarWindow))
pygame.display.set_caption("Game Bola")

# Pendefinisian warna
putih = (255, 255, 255)
biru = (0, 0, 255)
hitam = (0, 0, 0)

# Objek jam untuk FPS
clock = pygame.time.Clock()  # FPS

# Setup game
level = 1
uji = True
k = 0
p = 600
daftar_rintangan = []
daftar_koordinat = []

# Rintangan
def rintangan():
    global uji, k, p, level, daftar_koordinat

    if uji:
        daftar_koordinat.clear()
        for _ in range(level):
            x1 = random.randint(0, panjangWindow)
            x2 = random.randint(0, panjangWindow)
            y1 = random.randint(0, lebarWindow)
            y2 = random.randint(0, lebarWindow)

            # simpan jenis dan posisi
            daftar_koordinat.append(["vertikal", x1])  # dari atas ke bawah
            daftar_koordinat.append(["vertikal", x2])  # dari bawah ke atas
            daftar_koordinat.append(["horizontal", y1])  # dari kiri ke kanan
            daftar_koordinat.append(["horizontal", y2])  # dari kanan ke kiri

        uji = False

    daftar_rintangan.clear()
    for jenis, nilai in daftar_koordinat:
        if jenis == "vertikal":
            if nilai < panjangWindow // 2:
                haluan = pygame.draw.rect(window, hitam, (nilai, k, 40, 40))  # atas
            else:
                haluan = pygame.draw.rect(window, hitam, (nilai, p, 40, 40))  # bawah
        elif jenis == "horizontal":
            if nilai < lebarWindow // 2:
                haluan = pygame.draw.rect(window, hitam, (k, nilai, 40, 40))  # kiri
            else:
                haluan = pygame.draw.rect(window, hitam, (p, nilai, 40, 40))  # kanan
        daftar_rintangan.append(haluan)

    k += 5
    p -= 5
    if k > panjangWindow:
        uji = True
        k = 0
        p = panjangWindow

    return daftar_rintangan

# Tabrakan
def tabrakkan(pelaku, korban):
    return pelaku.colliderect(korban)


# Text
def tulis(text, font="times new roman", Uk=20, warna=hitam, x=0, y=0):
    font = pygame.font.SysFont(font, Uk)
    Text = font.render(text, True, warna)
    window.blit(Text, (x, y))


# Start screen
def start_screen():
    running = True
    while running:
        window.fill(putih)
        title_font = pygame.font.SysFont("times new roman", 50)
        instruction_font = pygame.font.SysFont("times new roman", 30)

        title_text = title_font.render("A Floating Ball", True, hitam)
        instruction_text = instruction_font.render("Press SPACE to start", True, hitam)

        window.blit(title_text, (panjangWindow // 2 - title_text.get_width() // 2, lebarWindow // 3))
        window.blit(instruction_text, (panjangWindow // 2 - instruction_text.get_width() // 2, lebarWindow // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

        pygame.display.flip()
        clock.tick(30)


# Fungsi Countdown
def countdown():
    for i in range(3, 0, -1):
        window.fill(putih)
        font = pygame.font.SysFont("times new roman", 80)
        count_text = font.render(str(i), True, hitam)
        window.blit(count_text,
                    (panjangWindow // 2 - count_text.get_width() // 2, lebarWindow // 2 - count_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

# Fungsi End screen
def end_screen():
    global level
    while True:
        window.fill(putih)

        title_font = pygame.font.SysFont("times new roman", 60)
        text = title_font.render("YOU DEAD", True, (200, 0, 0))
        window.blit(text, (panjangWindow // 2 - text.get_width() // 2, lebarWindow // 3))

        option_font = pygame.font.SysFont("times new roman", 30)
        play_again_text = option_font.render("Press R to Play Again", True, hitam)
        quit_text = option_font.render("Press Q to Quit", True, hitam)

        window.blit(play_again_text, (panjangWindow // 2 - play_again_text.get_width() // 2, lebarWindow // 2))
        window.blit(quit_text, (panjangWindow // 2 - quit_text.get_width() // 2, lebarWindow // 2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    level = 1
                    main()  # Restart game
                    return


# Looping Utama Game
def main():
    countdown()
    # Variable global dan khusus f main
    global k, p, uji, level
    objekX, objekY = 300, 300
    speed = 10
    acuan = time.time() + 10
    k = 0
    p = 600
    uji = True

    while True:
        window.fill(putih)
        player = pygame.draw.circle(window, biru, (objekX, objekY), 20)  # Player

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Keypad
        button = pygame.key.get_pressed()
        if button[pygame.K_LEFT] and objekX > 20:
            objekX -= speed
        if button[pygame.K_RIGHT] and objekX < panjangWindow - 20:
            objekX += speed
        if button[pygame.K_UP] and objekY > 20:
            objekY -= speed
        if button[pygame.K_DOWN] and objekY < lebarWindow - 20:
            objekY += speed
        if button[pygame.K_a] and objekX > 20:
            objekX -= speed
        if button[pygame.K_d] and objekX < panjangWindow - 20:
            objekX += speed
        if button[pygame.K_w] and objekY > 20:
            objekY -= speed
        if button[pygame.K_s] and objekY < lebarWindow - 20:
            objekY += speed

        musuh = rintangan()

        for i in musuh:
            if tabrakkan(player, i):
                end_screen()
                return

        # Otomatis naik level saat bertahan 10 detik
        waktuMulai = time.time()
        if waktuMulai >= acuan:
            level += 1
            acuan = waktuMulai + 10

        tulis(f"level: {level}")
        pygame.display.flip()
        clock.tick(60)  # Looping 60x per detik / FPS


# Panggil start screen
start_screen()
main()
