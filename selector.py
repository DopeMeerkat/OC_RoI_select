import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF

from PIL import Image



Image.MAX_IMAGE_PIXELS = 200000000
imgHeight = 1200 
imgWidth = 1200  



class MovingObject(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 1200, 1000)

        self.backgrounfImage = None
        self.graphicsPixmapItem = None

        self.moveObject = MovingObject(50, 50, 300, 300)
        # self.moveObject2 = MovingObject(100, 100, 100)
        # self.scene.addItem(self.moveObject)
        # self.scene.addItem(self.moveObject2)

class ImageLoader(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QGridLayout(self)

        # self.label = QtWidgets.QLabel()
        self.label = GraphicView()
        layout.addWidget(self.label, 1, 1, 1, 1)
        # self.label.setMinimumSize(imgWidth, imgHeight)
        
        self.setWindowTitle('RoI selection')

        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.loadImageButton = QtWidgets.QPushButton('Load image')
        layout.addWidget(self.loadImageButton, 0, 0, 1, 1)

        self.newPatchButton = QtWidgets.QPushButton('New Patch')
        layout.addWidget(self.newPatchButton, 0, 1, 1, 1)

        self.savePatchButton = QtWidgets.QPushButton('Save Patch')
        layout.addWidget(self.savePatchButton, 0, 2, 1, 1)

        self.nextImageButton = QtWidgets.QPushButton('>')
        layout.addWidget(self.nextImageButton, 1, 3)
        self.nextImageButton.setMinimumSize(20,imgHeight)


        self.loadImageButton.clicked.connect(self.loadImage)
        self.nextImageButton.clicked.connect(self.nextImage)
        self.newPatchButton.clicked.connect(self.nextImage)
        self.savePatchButton.clicked.connect(self.nextImage)
        

        self.filename = ''
        self.cropState = 0 # 0 = inactive, 1 = left, 2 = right
        self.x = 0
        self.dirIterator = None
        self.fileList = []
        self.fullFileList = []
        self.pixmap = QtGui.QPixmap()

    def loadImage(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        if self.filename:
            self.setWindowTitle(self.filename)
            self.pixmap = QtGui.QPixmap(self.filename).scaled(self.label.size(), 
                QtCore.Qt.KeepAspectRatio)
            if self.pixmap.isNull():
                return
            # self.label.setPixmap(self.pixmap)
            self.label.graphicsPixmapItem = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(self.pixmap))
            self.label.scene.addItem(self.label.graphicsPixmapItem)
            self.label.scene.addItem(self.label.moveObject)

            dirpath = os.path.dirname(self.filename)
            self.fileList = []
            for f in os.listdir(dirpath):
                fpath = os.path.join(dirpath, f)
                if os.path.isfile(fpath) and f.endswith(('.png', '.jpg', '.jpeg')):
                    self.fileList.append(fpath)



            self.fileList.sort()
            self.fullFileList.sort()
            self.dirIterator = iter(self.fileList)
          
            while True:
                # cycle through the iterator until the current file is found
                if next(self.dirIterator) == self.filename:
                    break

        

    def nextImage(self):
        # ensure that the file list has not been cleared due to missing files
        # del self.painter
        if self.fileList:
            try:
                self.filename = next(self.dirIterator)
                self.setWindowTitle(self.filename)
                self.pixmap = QtGui.QPixmap(self.filename).scaled(self.label.size(), 
                    QtCore.Qt.KeepAspectRatio)
                if self.pixmap.isNull():
                    # the file is not a valid image, remove it from the list
                    # and try to load the next one
                    self.fileList.remove(self.filename)
                    self.nextImage()
                else:
                    self.label.setPixmap(self.pixmap)
            except:
                # the iterator has finished, restart it
                self.dirIterator = iter(self.fileList)
                self.nextImage()
        else:
            # no file list found, load an image
            self.loadImage()

        



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    imageLoader = ImageLoader()
    imageLoader.show()
    sys.exit(app.exec_())