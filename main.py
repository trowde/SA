import pygame
import random
import math

# 初期化
pygame.init()

# ウィンドウの設定
WIDTH, HEIGHT = 300, 600  # 画面の横幅を縮める
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("二レーン 数式シューティングゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# フレームレート
clock = pygame.time.Clock()
FPS = 60

# プレイヤークラス（味方）
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)  # プレイヤーのサイズを大きくする
        pygame.draw.circle(self.image, GREEN, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 3  # 移動速度を遅くする
        self.friends = 1  # 味方の初期値を1に設定
        self.lane = 0  # 0 = 左レーン, 1 = 右レーン

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:  # 左レーンに移動
            self.rect.x -= self.speed
            self.lane = 0  # 左レーン
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:  # 右レーンに移動
            self.rect.x += self.speed
            self.lane = 1  # 右レーン

    def get_lane(self):
        return self.lane

# 数式クラス
class Formula(pygame.sprite.Sprite):
    def __init__(self, x, y, operator, value, lane, speed):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.operator = operator  # 演算子
        self.value = value  # 数式の値
        self.lane = lane  # 0 = 左レーン, 1 = 右レーン
        self.speed = speed  # 落ちる速度

        font = pygame.font.SysFont(None, 36)
        text = font.render(f"{operator}{value}", True, BLACK)
        self.image.blit(text, (10, 10))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()  # 画面外に出たら削除

# 数式の速度をユーザー入力で設定（今回は固定）
def get_speed():
    return 2.5  # 落下速度を固定

# 初期化
player = Player()
all_sprites = pygame.sprite.Group()
formulas = pygame.sprite.Group()
all_sprites.add(player)

# 味方の数の表示
font = pygame.font.SysFont(None, 36)

# 数式生成の間隔（秒単位）
generate_interval = 5  # 5秒ごとに生成
last_generated_time = pygame.time.get_ticks()

# メインループ
running = True
score = 0

# 数式ペアを管理するリスト
formula_pairs = []

while running:
    clock.tick(FPS)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 現在の時刻を取得
    current_time = pygame.time.get_ticks()

    # 数式を生成するタイミング
    if current_time - last_generated_time >= generate_interval * 1000:  # 5秒ごとに生成
        # 左レーン
        operator_left = random.choices(['+', '-','×', '÷'], weights=[3, 1])[0]
        value_left = random.randint(1, 10)
        
        # 右レーン
        operator_right = random.choices(['+', '-','×', '÷'], weights=[3, 1])[0]
        value_right = random.randint(1, 10)
        
        # 左右の数式を同時に生成し、垂直位置を合わせる
        y_position = random.randint(-200, -40)
        formula_left = Formula(WIDTH // 4, y_position, operator_left, value_left, 0, get_speed())
        formula_right = Formula(WIDTH * 3 // 4, y_position, operator_right, value_right, 1, get_speed())
        
        all_sprites.add(formula_left, formula_right)
        formulas.add(formula_left, formula_right)

        # 数式ペアをリストに追加
        formula_pairs.append((formula_left, formula_right))

        # 最後に数式を生成した時間を更新
        last_generated_time = current_time

    # 更新処理
    all_sprites.update()

    # 数式と味方の衝突判定
    hits = pygame.sprite.spritecollide(player, formulas, True, pygame.sprite.collide_circle)
    for hit in hits:
        # 数式ペアの管理
        for pair in formula_pairs:
            if hit in pair:
                # 演算子に応じた処理
                if player.get_lane() == hit.lane:  # プレイヤーが数式と同じレーンにいるとき
                    if hit.operator == '+':
                        player.friends += hit.value
                    elif hit.operator == '×':
                        player.friends *= hit.value
                    elif hit.operator == '-':
                        player.friends -= hit.value
                    elif hit.operator == '÷' and player.friends != 0:
                        player.friends //= hit.value  # ゼロ除算防止
                
                # ペアのもう一方の数式を削除
                if hit == pair[0]:
                    pair[1].kill()
                else:
                    pair[0].kill()
                formula_pairs.remove(pair)
                break

    # 描画処理
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # 味方の数だけプレイヤーキャラクターを同心円状に描画（味方のオブジェクトサイズは小さいまま）
    friend_image = pygame.Surface((10, 10), pygame.SRCALPHA)  # 味方のオブジェクトサイズ
    pygame.draw.circle(friend_image, GREEN, (5, 5), 5)

    friends_to_display = player.friends

    radius_increment = 20  # 各円周の半径の増加量
    friends_per_ring_base = 10  # 最初の円周に配置する味方の数
    ring = 1
    displayed_friends = 0

    while friends_to_display > 0:
        friends_per_ring = friends_per_ring_base * ring  # 現在のリングに配置する味方の数
        friends_on_this_ring = min(friends_to_display, friends_per_ring)  # 残りの味方数またはリングに配置できる最大数

        for i in range(friends_on_this_ring):
            angle = 2 * math.pi * i / friends_on_this_ring
            offset_x = int(radius_increment * ring * math.cos(angle))
            offset_y = int(radius_increment * ring * math.sin(angle))
            friend_rect = friend_image.get_rect()
            friend_rect.center = (player.rect.centerx + offset_x, player.rect.centery + offset_y)
            screen.blit(friend_image, friend_rect.topleft)

        friends_to_display -= friends_on_this_ring
        ring += 1

    # 味方の数を画面に表示
    score_text = font.render(f"味方の数: {player.friends}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
