from PyQt5.QtWidgets import(
    QApplication, QWidget,
    QFileDialog,QLabel,QPushButton,QListWidget,
    QHBoxLayout,QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR,DETAIL,EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, SHARPEN, FIND_EDGES, SMOOTH, SMOOTH_MORE
)
app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor')
Ib_image = QLabel('Картинка')
btn_dir = QPushButton("Владик")
Iw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton(' Резкость')
btn_bw = QPushButton('Негр')


row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(Iw_files)
col2.addWidget(Ib_image,95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1,20)
row.addLayout(col2,80)
win.setLayout(row)

win.show()

workdir = ''
def filter(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamelist():
    extensions = ['.jpg','.jpeg','.png','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    Iw_files.clear()
    for filename in filenames:
        Iw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamelist)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
    def LoadImage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def niga(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    


    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path)or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def showImage(self,path):
        Ib_image.hide()
        pixmapimage = QPixmap(path)
        w , h = Ib_image.width(), Ib_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        Ib_image.setPixmap(pixmapimage)
        Ib_image.show()

workimage = ImageProcessor()

def showChosenImage():
    if Iw_files.currentRow() >=0:
        filename = Iw_files.currentItem().text()
        workimage.LoadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

Iw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.niga)#workdir
btn_left.clicked.connect(workimage.left)
btn_right.clicked.connect(workimage.right)
btn_flip.clicked.connect(workimage.flip)
btn_sharp.clicked.connect(workimage.sharp)
app.exec() 


















