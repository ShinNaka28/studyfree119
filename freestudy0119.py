# The MIT License (MIT)
#
# Copyright (c) 2024 kitao
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pyxel

SCREEN_WIDTH = 150
SCREEN_HEIGHT = 200
STONE_INTERVAL = 30
ITEM_INTERVAL = 100

# 星
class star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 2
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 0, 1, 1, pyxel.COLOR_BLACK)

# 敵
class enemy:
    def __init__(self, x, y,kind):
        self.x = x
        self.y = y
        self.count = 1
        self.kind = kind
        
    def update(self):
        if self.kind == 1:
            if self.y < SCREEN_HEIGHT:
                self.y += 0.8
                self.x += self.count
            if pyxel.frame_count % 30 == 0:
                self.count *= -1
        
        if self.kind == 2:
            if self.y < SCREEN_HEIGHT:
                self.y += 0.5
            
    def draw(self):
        if self.kind == 1:
            pyxel.blt(self.x, self.y, 0, 16, 8, 8, 8, pyxel.COLOR_BLACK)
        if self.kind == 2:
            pyxel.blt(self.x, self.y, 0, 24, 8, 8, 8, pyxel.COLOR_BLACK)

# 石
class stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 2
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, pyxel.COLOR_BLACK)

# アイテム
class item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, pyxel.COLOR_BLACK)

# 弾丸
class Bullet:
    def __init__(self, x, y,kind):
        self.x = x
        self.y = y
        self.bullet_speed = 3
        self.kind = kind

    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y -= self.bullet_speed
            self.x += self.kind
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)

# 弾丸-敵
class enemy_bullet:
    def __init__(self, x, y,kind,):
        self.x = x
        self.y = y
        self.kind = kind
        self.bullet_speed = 2

    def update(self):
            #上
            if self.kind == 1:
                self.y += self.bullet_speed
            #下
            if self.kind == 2:
                self.y -= self.bullet_speed
            #右
            if self.kind == 3:
                self.x += self.bullet_speed
            #左
            if self.kind == 4:
                self.x -= self.bullet_speed    
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, 8, 8, pyxel.COLOR_BLACK)


class App:
    def __init__(self): #設定
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="シューティングゲーム")
        pyxel.load("+.pyxres")
        self.Bullet_INTERVAL = 30
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.score = 0
        self.stars = []
        self.Bullets = []
        self.stones = []
        self.enemy_bullets = []
        self.enemys = []
        self.items = []
        self.speed_up = 0
        self.player_HP = 3
        self.is_collision = False
        self.Bullet_spped = 1
        self.bullets_special = 0
        self.special_level = 0
        self.level = 1
        self.music = 1
        if self.music == 1:
            pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        # プレイヤーの移動
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 12 or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and self.player_x < SCREEN_WIDTH - 12: 
            self.player_x += 2

        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 4 or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) and self.player_x > 4:
            self.player_x -= 2
        
        if pyxel.btn(pyxel.KEY_UP) and self.player_y > 0 or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and self.player_y > 0:
            self.player_y -= 2
            
        if pyxel.btn(pyxel.KEY_DOWN) and self.player_y < SCREEN_HEIGHT - 16 or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) and self.player_y < SCREEN_HEIGHT - 16:
            self.player_y += 2

        # 石を追加
        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(stone(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))

        # 石の落下
        for b in self.stones.copy():
            b.update()
            # 衝突
            if (self.player_x - 7 <= b.x <= self.player_x + 7 and self.player_y - 7 <= b.y <= self.player_y + 7):
                self.stones.remove(b)
                self.player_HP -= 1
                if self.player_HP == 0:
                   self.is_collision = True                    
            
            # 画面外に出た石を削除
            if b.y >= SCREEN_HEIGHT:
                self.stones.remove(b)
            
        for bullet in self.Bullets.copy():
            for stones_obj in self.stones.copy():
                if (stones_obj.x - 4 <= bullet.x <= stones_obj.x + 4 and stones_obj.y - 4 <= bullet.y <= stones_obj.y + 4):
                    self.Bullets.remove(bullet)
                    break
        
        # 敵を追加
        if pyxel.frame_count % STONE_INTERVAL * 2 == 0:
            self.enemys.append(enemy(pyxel.rndi(0, SCREEN_WIDTH - 8), 0,pyxel.rndi(1,2)))
        
        # 敵の落下
        for b in self.enemys.copy():
            b.update()
            # プレイヤーと敵の衝突判定
            if (self.player_x - 7 <= b.x <= self.player_x + 7 and self.player_y - 7 <= b.y <= self.player_y + 7):
                self.enemys.remove(b)
                self.player_HP -= 1
                if self.player_HP == 0:
                    self.is_collision = True
            #敵の弾丸を追加
            if pyxel.frame_count % 90 == 0 and b.kind == 2:
                self.enemy_bullets.append(enemy_bullet(b.x,b.y,1))
                self.enemy_bullets.append(enemy_bullet(b.x,b.y,2))
                self.enemy_bullets.append(enemy_bullet(b.x,b.y,3))
                self.enemy_bullets.append(enemy_bullet(b.x,b.y,4))
            
            # 画面外に出た敵を削除
            if b.y >= SCREEN_HEIGHT:
                self.enemys.remove(b)

        # 弾丸と敵の衝突判定を追加
        for bullet in self.Bullets.copy():
            for enemy_obj in self.enemys.copy():
                if (enemy_obj.x - 4 <= bullet.x <= enemy_obj.x + 4 and enemy_obj.y - 4 <= bullet.y <= enemy_obj.y + 4):
                    self.Bullets.remove(bullet)
                    self.enemys.remove(enemy_obj)
                    self.score += 1
                    break

        # 星を追加
        if pyxel.frame_count % 5 == 0 and pyxel.frame_count > 0:
            self.stars.append(star(pyxel.rndi(0, SCREEN_WIDTH), 0))
        
        # 星の落下
        for n in self.stars.copy():
            n.update()             
            # 画面外に出た星を削除
            if n.y >= SCREEN_HEIGHT:
                self.stars.remove(n)

        # アイテムを追加
        if pyxel.frame_count % ITEM_INTERVAL == 0 and pyxel.frame_count > 0:
            self.items.append(item(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))
        
        # アイテムの落下
        for i in self.items.copy():
            i.update()
            # 衝突
            if (self.player_x - 7 <= i.x <= self.player_x + 7 and self.player_y - 7 <= i.y <= self.player_y + 7):
                self.bullets_special += 1
                self.items.remove(i)              
            # 画面外に出たアイテムを削除
            if i.y >= SCREEN_HEIGHT:
                self.items.remove(i)

        # 弾丸を追加
        if pyxel.frame_count % self.Bullet_INTERVAL == 0:
            self.Bullets.append(Bullet(self.player_x, self.player_y,0))

        if self.bullets_special > 0 and self.special_level == 0:
            self.Bullet_INTERVAL -= 5
            self.special_level += 1

        if self.bullets_special > 2 and self.special_level == 1:
            self.Bullet_INTERVAL -= 5
            self.special_level += 1

        if self.bullets_special > 3 and self.special_level == 2:
            self.Bullet_INTERVAL -= 5
            self.special_level += 1

        if pyxel.frame_count % self.Bullet_INTERVAL == 0 and self.bullets_special > 2:
            self.Bullets.append(Bullet(self.player_x + 4, self.player_y,0.5))
            self.Bullets.append(Bullet(self.player_x - 4, self.player_y,-0.5))

        if self.bullets_special > 4 and self.special_level == 3:
            self.Bullet_INTERVAL -= 5
            self.special_level += 1

        if self.bullets_special > 5 and self.special_level == 4:
            self.Bullet_INTERVAL -= 5
            self.special_level += 1

        if pyxel.frame_count % self.Bullet_INTERVAL == 0 and self.bullets_special > 5:
            self.Bullets.append(Bullet(self.player_x + 3, self.player_y, + 0.25))
            self.Bullets.append(Bullet(self.player_x - 3, self.player_y, - 0.25))  

        if self.bullets_special > 6 and self.special_level == 12:
            self.Bullet_INTERVAL -= 5
            self.special_level += 1

        if self.bullets_special > 7 and self.special_level == 18:
            self.Bullet_INTERVAL -= 5
            self.special_level += 1          

        # 弾丸の落下
        for s in self.Bullets.copy():
            s.update()
            
            # 画面外に出た弾丸を削除
            if s.y >= SCREEN_HEIGHT:
                self.Bullets.remove(s)


        # 敵の弾丸の落下
        for s in self.enemy_bullets.copy():
            s.update()
            
            # 画面外に出た敵の弾丸を削除
            if SCREEN_HEIGHT - 3 >= s.y >= SCREEN_HEIGHT or 3 <= s.y <= 0 or SCREEN_WIDTH - 2 >= s.y >= SCREEN_WIDTH or 3 <= s.y <= 0:
                self.enemy_bullets.remove(s)

            # 衝突
            if (self.player_x - 7 <= s.x <= self.player_x + 7 and self.player_y - 7 <= s.y <= self.player_y + 7):
                self.enemy_bullets.remove(s)
                self.player_HP -= 1
                if self.player_HP == 0:
                   self.is_collision = True



    def draw(self):
        # 背景
        pyxel.cls(pyxel.COLOR_BLACK)
        
        # スコア&残機
        pyxel.text(1,1,'SCORE:' + str(self.score), pyxel.COLOR_WHITE)
        pyxel.text(1,10,'HP:' + str(self.player_HP), pyxel.COLOR_WHITE)
        
        # 弾丸
        for s in self.Bullets:
            s.draw()

        # 敵の弾丸
        for s in self.enemy_bullets:
            s.draw()
            
        # 敵
        for b in self.enemys:
            b.draw()

        # 石
        for b in self.stones:
            b.draw()

        # アイテム
        for i in self.items:
            i.draw()
 
        # 星
        for n in self.stars:
            n.draw()
        
        # プレイヤー
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 8, 8, pyxel.COLOR_BLACK)
        
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "Game Over", pyxel.COLOR_YELLOW)
            if pyxel.frame_count % 120 == 0:
                pyxel.quit()



App()

