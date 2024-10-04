import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class TransparentCharacterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # ウィンドウの設定
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # キャラクターの画像を読み込む
        self.character = QtGui.QPixmap("character.png")  # キャラクター画像ファイルを指定
        self.setFixedSize(self.character.size())
        
        # タイマー設定 (キャラクターの移動)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move_character)
        self.timer.start(50)  # 50ミリ秒ごとに動かす

        # 移動方向
        self.dx = 2
        self.dy = 2

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.character)

    def move_character(self):
        # ウィンドウの位置を取得して更新
        current_pos = self.pos()
        new_x = current_pos.x() + self.dx
        new_y = current_pos.y() + self.dy

        # 画面サイズを取得
        screen_rect = QtWidgets.QApplication.desktop().screenGeometry()

        # 画面の端に到達したら方向を反転
        if new_x <= 0 or new_x + self.width() >= screen_rect.width():
            self.dx = -self.dx
        if new_y <= 0 or new_y + self.height() >= screen_rect.height():
            self.dy = -self.dy

        # 新しい位置に移動
        self.move(new_x, new_y)

    def mousePressEvent(self, event):
        # ウィンドウをドラッグできるようにする
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # 左クリックを押しながら動かすとキャラクターを移動
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentCharacterWindow()
    window.show()
    sys.exit(app.exec_())