import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),
         pg.K_DOWN:(0,+5),
         pg.K_LEFT:(-5,0),
         pg.K_RIGHT:(+5,0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect):
    """
    引数　: こうかとん　または　爆弾のRect
    戻り値　: 真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue  画面外ならFalse
    """
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate


def game_over(screen):
    # フォント設定
    font = pg.font.Font(None, 80)
    text = font.render("GAME OVER", True, (255, 0, 0))
    
    # 泣いているこうかとん画像（8.png）を読み込む
    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    
    # 左右にこうかとんを表示する座標
    left_pos = (WIDTH // 4 - crying_kk_img.get_width() // 2, HEIGHT // 2 - crying_kk_img.get_height() // 2)
    right_pos = (3 * WIDTH // 4 - crying_kk_img.get_width() // 2, HEIGHT // 2 - crying_kk_img.get_height() // 2)
    
    # ブラックアウトのための半透明Surface
    blackout = pg.Surface((WIDTH, HEIGHT))  # 画面全体のサイズでSurface作成
    blackout.fill((0, 0, 0))  # 黒で塗りつぶす
    
    # 画面を5段階で暗くしていく
    for alpha in range(0, 256, 51):  # 透明度を徐々に上げる (0, 51, 102, 153, 204, 255)
        # 画面を黒く塗りつぶす前にこうかとんとテキストを描画
        screen.fill((0, 0, 0))  # 画面全体を黒で塗りつぶす
        screen.blit(crying_kk_img, left_pos)  # 左側のこうかとん画像
        screen.blit(crying_kk_img, right_pos)  # 右側のこうかとん画像
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 40))
        
        # ブラックアウトのエフェクト
        blackout.set_alpha(alpha)  # 透明度を設定
        screen.blit(blackout, (0, 0))  # 画面に半透明の黒を描画
        
        pg.display.update()  # 画面を更新
        time.sleep(0.5)  # 少しずつ暗くなる演出

    # 最後に5秒間完全な黒背景で停止
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  # 空のSurface
    bb_img.set_colorkey((0,0,0))
    

    pg.draw.circle(bb_img,(255,0,0),(10,10,),10)
    bb_rct = bb_img.get_rect()  # 爆弾の抽出
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)  # 爆弾の初期座標
    vx,vy = +5,+5  # 爆弾速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):  #　こうかとんと爆弾重なっていたら
            game_over(screen)
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
            #sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横
                sum_mv[1] += tpl[1]  # 縦

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx,vy)
        yoko,tate=  check_bound (bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()