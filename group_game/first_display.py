import pygame
import sys
import subprocess

# Pygameの初期化
pygame.init()
pygame.mixer.init()  # 音楽機能の初期化

# 画面設定
WIDTH, HEIGHT = 1024,1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Start Screen")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# フォント設定（太字や角ばったフォントを使用）
font = pygame.font.Font(None, 74)
title_font = pygame.font.Font(None, 150)  # タイトル用フォント（サイズを大きく）

# 背景画像をロード
background_image = pygame.image.load("first_background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # 画面サイズに調整

# ボタンの描画
def draw_button(screen, text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

# タイトル描画（影とアウトラインを追加）
def draw_title(screen, text):
    # 影の描画
    shadow_surf = title_font.render(text, True, BLACK)
    shadow_rect = shadow_surf.get_rect(center=(WIDTH // 2 + 5, HEIGHT // 4 + 5))  # 少しずらして描画
    screen.blit(shadow_surf, shadow_rect)

    # アウトラインを付ける（黄色）
    outline_surf = title_font.render(text, True, YELLOW)
    outline_rect = outline_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # 画面の中央上あたり
    screen.blit(outline_surf, outline_rect)

# メインループ
# メインループ
def main():
    # BGMの再生
    pygame.mixer.music.load("first_bgm.flac")  # BGMファイルを読み込み
    pygame.mixer.music.set_volume(0.5)  # 音量の設定（0.0〜1.0）
    pygame.mixer.music.play(-1, 0.0)  # BGMをループ再生（-1は無限ループ）

    while True:
        # 背景画像を描画
        screen.blit(background_image, (0, 0))

        # タイトルを描画（影とアウトラインあり）
        draw_title(screen, "LAST WAR")

        # ボタンの位置を中央に配置
        button_x = (WIDTH - 200) // 2  # 画面の中央にボタンを配置（200はボタンの幅）
        button_y = (HEIGHT - 100) // 2  # 画面の中央にボタンを配置（100はボタンの高さ）
        button_w, button_h = 200, 100  # ボタンの幅と高さ

        # ボタンを描画
        draw_button(screen, "START", button_x, button_y, button_w, button_h, BLUE)

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ボタンがクリックされたら
                if button_x <= event.pos[0] <= button_x + button_w and button_y <= event.pos[1] <= button_y + button_h:
                    pygame.mixer.music.stop()  # BGMを停止
                    # game.pyを実行する
                    subprocess.run(["python", "game.py"])  # Windowsの場合は "python" に変更
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()
