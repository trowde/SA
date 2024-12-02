import pygame
import random
import sys
import math

# 初期設定
pygame.init()

# 画面サイズと色
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (50, 150, 200)
PLAYER_COLOR = (255, 255, 255)
OBJECT_COLOR = (200, 200, 200)
OBJECT_BORDER_COLOR = (0, 0, 0)
BULLET_COLOR = (255, 0, 0)
FONT_COLOR = (0, 0, 0)

# ゲーム画面とフォント
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("キャッチゲーム")
font = pygame.font.SysFont(None, 24)
large_font = pygame.font.SysFont(None, 36)

# FPS制御
clock = pygame.time.Clock()
FPS = 60

# プレイヤー設定
player_radius = 20
player_x = (SCREEN_WIDTH - player_radius) // 2
player_y = SCREEN_HEIGHT - 50
player_speed = 7
players = [{"x": player_x, "y": player_y}]  # プレイヤーリスト

# オブジェクト設定
object_width = SCREEN_WIDTH // 2  # 画面の半分
object_height = 30
object_speed = 2  # 固定速度
objects = [
    {"x": 0, "y": -object_height, "score": random.randint(1, 3)},
    {"x": SCREEN_WIDTH // 2, "y": -object_height, "score": random.randint(1, 3)}
]

# 弾設定
bullet_width = 5
bullet_height = 10
bullet_speed = 5
bullets = []
bullet_timer = 0  # 自動発射用タイマー
bullet_interval = 60  # 弾発射間隔を調整

# スコア
score = 0
score_increment = 1  # 得点増加量

def display_text(text, x, y, font):
    """テキストを画面に表示する"""
    img = font.render(text, True, FONT_COLOR)
    screen.blit(img, (x, y))

def reset_object(obj):
    """オブジェクトをリセットする"""
    obj["y"] = -object_height
    obj["score"] = random.randint(1, 3)

def update_players(score):
    """スコアに応じてプレイヤー数と得点増加量を更新"""
    global score_increment
    factorials = [10**i for i in range(1, 8)]  # 10, 100, 1000, ...
    if score in factorials:
        players.append({"x": player_x, "y": player_y})
    if score % 10 == 0:
        score_increment += 1
    if score % math.factorial(len(players)) == 0:
        players.clear()
        players.append({"x": player_x, "y": player_y})
        score_increment = 1

# ゲームループ
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        for player in players:
            if player["x"] - player_radius > 0:
                player["x"] -= player_speed
    if keys[pygame.K_RIGHT]:
        for player in players:
            if player["x"] + player_radius < SCREEN_WIDTH:
                player["x"] += player_speed

    # 弾の自動発射
    bullet_timer += 1
    if bullet_timer >= bullet_interval:  # 発射間隔を調整
        for player in players:
            bullets.append({"x": player["x"], "y": player["y"]})
        bullet_timer = 0

    # オブジェクトの移動とリセット
    for obj in objects:
        obj["y"] += object_speed
        if obj["y"] > SCREEN_HEIGHT:
            reset_object(obj)

        # オブジェクトを描画
        pygame.draw.rect(screen, OBJECT_COLOR, (obj["x"], obj["y"], object_width, object_height))
        pygame.draw.rect(screen, OBJECT_BORDER_COLOR, (obj["x"], obj["y"], object_width, object_height), 2)  # 枠線
        text = f"{obj['score']}"
        display_text(text, obj["x"] + object_width // 2 - 10, obj["y"] + 5, font)

    # 弾の移動と衝突判定
    for bullet in bullets[:]:
        bullet["y"] -= bullet_speed
        if bullet["y"] < 0:
            bullets.remove(bullet)  # 画面外に出た弾を削除
            continue

        # 弾がオブジェクトに当たった場合
        for obj in objects:
            if (
                bullet["x"] > obj["x"] and
                bullet["x"] < obj["x"] + object_width and
                bullet["y"] < obj["y"] + object_height and
                bullet["y"] + bullet_height > obj["y"]
            ):
                obj["score"] += score_increment  # 得点増加
                bullets.remove(bullet)
                break  # 1つの弾で1つのオブジェクトしか当たれない

        # 弾を描画
        pygame.draw.rect(screen, BULLET_COLOR, (bullet["x"], bullet["y"], bullet_width, bullet_height))

    # オブジェクトとプレイヤーの衝突判定
    for obj in objects:
        for player in players:
            if (
                player["x"] - player_radius < obj["x"] + object_width and
                player["x"] + player_radius > obj["x"] and
                player["y"] - player_radius < obj["y"] + object_height and
                player["y"] + player_radius > obj["y"]
            ):
                score += obj["score"]  # オブジェクトのスコアをプレイヤーのスコアに加算
                reset_object(obj)
                update_players(score)

    # プレイヤーを描画
    for player in players:
        pygame.draw.circle(screen, PLAYER_COLOR, (player["x"], player["y"]), player_radius)

    # スコアを表示
    display_text(f"スコア: {score}", 10, 10, large_font)

    # 画面更新
    pygame.display.flip()

    # フレームレート制御
    clock.tick(FPS)

# ゲーム終了
pygame.quit()
sys.exit()
