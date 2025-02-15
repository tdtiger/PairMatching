import pyxel

WINDOW_WIDTH = 276
WINDOW_HEIGHT = 150

COL = 13
LINE = 4

class Card:
    def __init__(self, col, num):
        self.color = col
        self.num = num
        self.isSelected = False
        self.isExist = True
        self.pos = [0, 0]

class Field:
    def __init__(self):
        self.grid = self.gen_grid()

    def gen_grid(self):
        tmp = [[0] * COL for _ in range(LINE)]
        for y in range(LINE):
            for x in range(COL):
                tmp[y][x] = Card(y, x + 1)

        grid = [[0] * COL for _ in range(LINE)]
        # 一度整列した状態のカード群を作り，そこからランダムに並び変えていく
        for y in range(LINE):
            for x in range(COL):
                l = pyxel.rndi(0, len(tmp) - 1)
                c = pyxel.rndi(0, len(tmp[l]) - 1)
                grid[y][x] = tmp[l][c]
                grid[y][x].pos = [y, x]

                del tmp[l][c]
                if len(tmp[l]) == 0:
                    del tmp[l]

        return grid

class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title = "PairMatching")
        pyxel.load("resource_pairmatching.pyxres")
        self.mode = "title"
        self.skin = 0
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.mode == "title":
            self.update_title()
        elif self.mode == "game":
            self.update_game()
        elif self.mode == "clear":
            self.update_gameclear()

    def update_title(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # ゲーム開始ボタンがクリックされた時
            if pyxel.width // 2 - 55 <= pyxel.mouse_x <= pyxel.width // 2 + 50 and pyxel.height // 2 + 18 <= pyxel.mouse_y <= pyxel.height // 2 + 27:
                self.mode = "game"
                self.start_game()
            # TODO:スキン変更ボタンがクリックされた時

    def update_game(self):
        if not self.wait_start == None:
            if pyxel.frame_count - self.wait_start >= self.wait_time:
                self.check_pair()
                self.wait_start = None
                self.watching = False
            return

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(0, 0, loop = False)
            for l in range(LINE):
                for c in range(COL):
                    if 10 + c * 20 <= pyxel.mouse_x <= 25 + c * 20 and 20 + 30 * l <= pyxel.mouse_y <= 43 + l * 30:
                        if self.field.grid[l][c].isExist:
                            self.field.grid[l][c].isSelected = True
                            self.selected.append(self.field.grid[l][c])

        # カードが二枚選択されたら，クリック操作を受け付けなくする(冒頭のif文)
        if len(self.selected) == 2 and self.watching == False:
            self.watching = True
            self.wait_start = pyxel.frame_count

    def update_gameclear(self):
        if self.fanf:
            self.time = pyxel.frame_count // 30
            self.fanf = False
            pyxel.playm(0, 0 ,loop = False)

        # TODO:ゲーム終了ではなく，初期化してタイトルに戻るようにする
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.quit()

    def start_game(self):
        self.field = Field()
        self.score = 0
        self.ren = 0
        self.remaining = 52
        self.time = 0
        self.bonus = pyxel.rndi(0, 3)
        self.selected = []
        self.watching = False
        self.wait_time = 30
        self.wait_start = None
        self.fanf = True

    def draw(self):
        if self.mode == "title":
            self.draw_title()
        elif self.mode == "game":
            self.draw_game()
        elif self.mode == "clear":
            self.draw_gameclear()

    def draw_title(self):
        pyxel.cls(0)
        pyxel.text(pyxel.width // 2 - 35, pyxel.height // 4, "Pair Matching", pyxel.frame_count % 16)
        if 0 <= pyxel.frame_count % 40 <= 25:
            col = 7
        else:
            col = 0
        pyxel.rectb(pyxel.width // 2 - 55, pyxel.height // 2 + 18, 105, 9, col)
        pyxel.text(pyxel.width // 2 - 50, pyxel.height // 2 + 20, "Click here to start game", col)

    def draw_game(self):
        pyxel.cls(0)
        pyxel.text(10, 3, f"score:{self.score}", 7)
        pyxel.text(60, 3, f"remaining:{self.remaining}", 7)
        pyxel.text(120, 3, f"combo:{self.ren}", 7)
        pyxel.text(160, 3, f"time:{pyxel.frame_count // 30}", 7)
        tmp = ["red", "blue", "green", "yellow"][self.bonus]
        pyxel.text(200, 3, f"bonus:{tmp}", 7)

        if self.remaining == 0:
            self.mode = "clear"
            return

        for l in range(LINE):
            for c in range(COL):
                if self.field.grid[l][c].isExist:
                    if self.field.grid[l][c].isSelected == True:
                        pyxel.blt(10 + 20 * c, 20 + 30 * l, 1, (self.field.grid[l][c].num - 1) * 16, self.field.grid[l][c].color * 24, 16, 24)
                    else:
                        pyxel.blt(10 + 20 * c, 20 + 30 * l, 0, self.skin, 0, 16, 24)
                else:
                    pass

    def draw_gameclear(self):
        pyxel.cls(0)
        pyxel.text(WINDOW_WIDTH / 2 - 30, WINDOW_HEIGHT / 2 - 5, "GAME CLEAR!!", pyxel.frame_count % 16)
        pyxel.text(WINDOW_WIDTH / 2 - 40, WINDOW_HEIGHT / 2 + 5, f"score:{self.score}", 7)
        pyxel.text(WINDOW_WIDTH / 2 - 40, WINDOW_HEIGHT / 2 + 15, f"time :{self.time}", 7)
        pyxel.text(WINDOW_WIDTH / 2 - 40, WINDOW_HEIGHT / 2 + 35, f"click to exit", 7)

    def check_pair(self):
        # 同じカードが二回選択された時は何もせずに元に戻す
        if self.selected[0] == self.selected[1]:
            self.field.grid[self.selected[0].pos[0]][self.selected[0].pos[1]].isSelected = False
            self.selected = []
            return

        if self.selected[0].num ==  self.selected[1].num:
            pyxel.play(1, 1, loop = False)
            self.score += 100 + 50 * self.ren
            self.ren += 1
            self.check_bonus()
            self.field.grid[self.selected[0].pos[0]][self.selected[0].pos[1]].isExist = False
            self.field.grid[self.selected[1].pos[0]][self.selected[1].pos[1]].isExist = False
            self.remaining -= 2
        else:
            pyxel.play(1, 2, loop = False)
            self.ren = 0
            self.field.grid[self.selected[0].pos[0]][self.selected[0].pos[1]].isSelected = False
            self.field.grid[self.selected[1].pos[0]][self.selected[1].pos[1]].isSelected = False

        self.selected = []

    def check_bonus(self):
        if self.selected[0].color == self.bonus or self.selected[1].color == self.bonus:
            self.score += 50
        # ペアがそろうたびにボーナスが変化
        self.bonus = pyxel.rndi(0, 3)
App()