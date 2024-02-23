import random
import sys
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QGridLayout, QVBoxLayout, QLabel, QLCDNumber, QPushButton, QLineEdit

class Snake_game(QWidget):

    def __init__(self):
        super().__init__()
        self.variable()
        self.ui()
        self.preset() # 開啟時預設
        self.link() # connect設置

    def variable(self):
        self.cell = dict() # 遊戲網格座標(row, col)對應的QLabel
        self.cells = list() # 全部座標的list，方便食物生成計算，也可用cell.keys()代替
        self.snake = [(random.randint(0, 30), random.randint(0, 30))] # 蛇的list，存(row, col)，預先設置頭隨機位置
        self.fruit = tuple() # 方便計算
        self.direction = (0, 0) # 方向
        self.lock = 0  # 防止連續輸入

    def preset(self):
        self.Randomgeneration()
        self.timer = QTimer()
        self.edit_speed.setText("500")

    def ui(self):
        self.setWindowTitle("Snake")
        self.setFixedSize(500, 500)
        self.move(0, 0)
        # self.grabKeyboard()

        ########### 狀態表 ##########
        self.state = QWidget()
        self.grid_layout_1 = QGridLayout()

        self.lcd_score = QLCDNumber()
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_reset = QPushButton("Reset")
        self.label_speed = QLabel("speed: ")
        self.edit_speed = QLineEdit()

        self.grid_layout_1.addWidget(self.lcd_score, 0, 0, 1, 2)
        self.grid_layout_1.addWidget(self.btn_start, 0, 2)
        self.grid_layout_1.addWidget(self.btn_stop, 0, 3)
        self.grid_layout_1.addWidget(self.btn_reset, 0, 4)

        self.grid_layout_1.addWidget(self.label_speed, 0, 5)
        self.edit_speed.setValidator(QIntValidator())
        self.grid_layout_1.addWidget(self.edit_speed, 0, 6)

        self.state.setLayout(self.grid_layout_1)
        ########### 狀態表 ##########

        ########### 遊戲介面 ##########
        self.interface = QWidget()
        self.grid_layout_2 = QGridLayout()
        for row in range(30):
            for col in range(30):
                self.cell[(row, col)] = QLabel()
                self.cell[(row, col)].setStyleSheet("background-color:white; border:1px solid darkslategray;")
                self.cell[(row, col)].setFixedSize(10, 10)
                self.grid_layout_2.addWidget(self.cell[(row, col)], row, col)

                self.cells.append((row, col))
        # grid_layout_2.setSpacing(2) # 看起來怪怪的

        self.interface.setLayout(self.grid_layout_2)
        ########### 遊戲介面 ##########

        ########### 整體布局 ##########
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.state)
        vertical_layout.addWidget(self.interface)
        self.setLayout(vertical_layout)
        ########### 整體布局 ##########

    def Randomgeneration(self):
        ########## test ##########
        # self.random.choice(list(self.cell.values())).setStyleSheet("background-color:red; border:1px solid darkslategray;")
        ########## test ##########
        tempdict = self.cells.copy()
        for cell in self.snake:
            tempdict.remove(cell)
        self.fruit = random.choice(tempdict)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if self.direction != (0, 1) and self.lock == 0:
                self.direction = (0, -1)
        if event.key() == Qt.Key_Right:
            if self.direction != (0, -1) and self.lock == 0:
                self.direction = (0, 1)
        if event.key() == Qt.Key_Up:
            if self.direction != (1, 0) and self.lock == 0:
                self.direction = (-1, 0)
        if event.key() == Qt.Key_Down:
            if self.direction != (-1, 0) and self.lock == 0:
                self.direction = (1, 0)
        self.lock = 1 # 防止連續輸入

    def start(self):
        if self.edit_speed.text() == "":
            self.edit_speed.setText("500")
        self.interface.grabKeyboard()
        self.timer.start(int(self.edit_speed.text()))

    def stop(self):
        self.timer.stop()
        self.interface.releaseKeyboard()

    def reset(self):  # 重置
        self.timer.stop()
        self.interface.releaseKeyboard()
        self.snake = [(random.randint(0, 30), random.randint(0, 30))]  # 蛇
        self.fruit = tuple()
        self.direction = (0, 0)
        self.lock = 0
        self.Randomgeneration()
        for cell in self.cell.values():
            cell.setStyleSheet("background-color:white; border:1px solid darkslategray;")

    def refresh(self):
        self.cell[self.fruit].setStyleSheet("background-color:red; border:1px solid darkslategray;")
        head = self.snake[0]
        head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.lock = 0 # 鍵盤鎖，每個Qtimer迴圈只能輸入一次方向鍵
        self.snake.insert(0, head)

        if head == self.fruit:  # 吃到食物，再次生成
            self.Randomgeneration()
        else:  # 沒吃到食物，刪除蛇尾
            tail = self.snake.pop()
            self.cell[tail].setStyleSheet("background-color:white; border:1px solid darkslategray;")

        temp = self.snake.copy() # 除了蛇頭的蛇身
        temp.remove(head)
        if head in temp:  # 咬到自己
            self.timer.stop()
            QMessageBox.warning(self, '信息', 'GAME OVER!', QMessageBox.Ok)
            self.reset()
        elif (-1 in head) or (30 in head):  # 出界
            self.timer.stop()
            QMessageBox.warning(self, '信息', 'GAME OVER!', QMessageBox.Ok)
            self.reset()
        else:  # 計分
            self.cell[head].setStyleSheet("background-color:green; border:1px solid darkslategray;")
            self.lcd_score.display(len(self.snake) - 1)  # 分數


    def link(self):
        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_reset.clicked.connect(self.reset)
        self.timer.timeout.connect(self.refresh)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    App = Snake_game()
    App.show()
    sys.exit(app.exec_())