from PIL import Image
import numpy as np
import io
from typing import List, Any
import ipywidgets as widgets
from IPython.display import display, clear_output
from tensorflow.keras.models import load_model
from tensorflow_hub import KerasLayer
import cv2
img = None  # type: Any


def classification(model,image_input):
    img_size = model.get_layer(index=0).input_shape[1:3]
    image = Image.open(io.BytesIO(image_input)).convert('RGB')
    image = np.array(image.resize(img_size, Image.NEAREST)) / 255.0
    result = model.predict(image[np.newaxis, ...])
    return result


def img_upload():
    display(uploader)


def do_classification(label_names):
    try:
        model = load_model('my_model.h5',custom_objects={'KerasLayer':KerasLayer})
    except:
        print("当前没有找到用来识别的数据模型，请先进行训练")
        return
    with open('label_names.dat', 'r') as f:
        tempLabel=f.read()
        label_names=tempLabel.split(' ')
    uploader = widgets.FileUpload(accept='image/*', description='上传待识别图像')
    cls_btn = widgets.Button(description='识别图像')
    display(widgets.VBox([uploader, cls_btn]))

    def on_uploader_change(b):
        global img
        clear_output()
        display(widgets.VBox([uploader, cls_btn]))
        key = list(uploader.value.keys())[0]
        img = uploader.value[key]['content']
        image = widgets.Image(value=img,width=150,height=150)
        display(image)

    uploader.observe(on_uploader_change, names='value')

    def on_cls_btn_click(b):
        on_uploader_change(uploader)
        print('开始图像识别')
        result = classification(model,img)
        print('识别结果：' + label_names[np.argmax(result)])

    cls_btn.on_click(on_cls_btn_click)
