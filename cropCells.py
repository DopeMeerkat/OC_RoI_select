import os
from PIL import Image, ImageDraw
import pybboxes as pbx

REFERENCE_SCALE = 5

def drawLabelBox(imagePath, labelPath, saveDir):
    refImage = Image.open(imagePath)
    if REFERENCE_SCALE != 1:
        refImage = refImage.resize((refImage.size[0] * REFERENCE_SCALE, refImage.size[1] * REFERENCE_SCALE), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(refImage)

    with open(labelPath) as file:
        for i, label in enumerate(file):
            label = label.split(' ')
            label[4] = label[4][:-2] #remove \n
            converted = pbx.convert_bbox((float(label[1]),float(label[2]),float(label[3]), float(label[4])), from_type="yolo", to_type="voc", image_size=refImage.size)
            # print(label)
            draw.rectangle([converted[0],converted[1],converted[2],converted[3]], outline="red", width=1)
            draw.text((converted[0] + 2,converted[1]), str(i + 1), fill="red")

    # refImage.save(os.path.join(saveDir, 'reference.jpg'), format = 'JPEG', dpi = refImage.info['dpi'])
    refImage.save(os.path.join(saveDir, 'reference.png'))

def cropCells(layerDir):
    dir = os.path.join(layerDir, 'cells')
    if not os.path.exists(dir):
        os.mkdir(dir)
    labelName = ''
    for file in os.listdir(layerDir):
        if file.endswith('.txt') and file != 'classes.txt':
            labelName = file
    classes = []

    with open(os.path.join(layerDir, 'classes.txt'), 'r') as file:
        for className in file:
            classes.append(className.replace('\n', ''))

    with open(os.path.join(layerDir, labelName)) as file:
        for i, label in enumerate(file):
            # print(label)
            label = label.split(' ')
            label[4] = label[4][:-2] #remove \n
            cellDir = os.path.join(dir, f'Cell-{(i + 1)}_class-{classes[int(label[0])]}')
            if not os.path.exists(cellDir):
                os.mkdir(cellDir)
            for file in os.listdir(layerDir):
                if file.endswith('A.jpg'):
                    drawLabelBox(os.path.join(layerDir, file), os.path.join(layerDir, labelName), dir)
                if file.endswith('.jpg'):
                    # file = 'patch.jpg'
                    im = Image.open(os.path.join(layerDir, file))
                    width, height = im.size
                    converted = pbx.convert_bbox((float(label[1]),float(label[2]),float(label[3]), float(label[4])),
                                                from_type="yolo", to_type="voc", image_size=(width, height))
                    im1 = im.crop((converted[0],converted[1],converted[2],converted[3]))
                    im1.save(os.path.join(cellDir, file), format = 'JPEG', dpi = im.info['dpi'])








cwd = os.getcwd()
for subdir, dirs, files in os.walk(cwd):
    # for file in files:
    #     print(file)
    for dir in dirs:
        if dir.find('RoI') != -1:
            cropCells(dir)

