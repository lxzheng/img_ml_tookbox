# coding=utf-8
import os
import ipywidgets as widgets  # 控件库
import train
from IPython.display import display, clear_output  # 显示控件的方法
from load_data import load_data
from train import train_model
from typing import List, Any

model = None  # type: Any
label_names = []


def do_model_train(data_dir):
    global model
    clear_output()
    dataset_path = 'data/' + data_dir
    if len(data_dir) == 0 or not os.path.exists(dataset_path):
        print('数据集目录:' + data_dir + '不存在')
        return
    adv_ckbox = widgets.Checkbox(
        value=False,
        description='高级选项',
        disabled=False,
        indent=False
    )
    model_chose_tx = widgets.Dropdown(options=['mobilenetv2','inceptionv3'],description='训练模型选择')
    batch_size_tx = widgets.IntText(value=4, description='批尺寸')
    epochs_tx = widgets.IntText(value=15, description='训练轮数')

    data_aug_ckbox = widgets.Checkbox( value=False,description='数据增强',disabled=False,indent=False)
    validation_perc_tx = widgets.FloatText(value=0.10, description='验证集比例')
    rotation_range_tx = widgets.IntText(value=45, description='旋转角度范围')
    width_shift_range_tx=widgets.FloatText(value=.15, description='水平偏移幅度')
    height_shift_range_tx=widgets.FloatText(value=.15, description='竖直偏移幅度')
    horizontal_flip_tx=widgets.Checkbox( value=True,description='进行随机水平翻转')
    zoom_range_tx=widgets.FloatText(value=0.5, description='缩放幅度')

    #模型选择
    train_btn = widgets.Button(description='训练模型')
    display(widgets.VBox([adv_ckbox, train_btn]))

    def on_adv_ckbox_change(b):
        clear_output()
        if adv_ckbox.value:
            display(widgets.VBox([adv_ckbox,model_chose_tx,batch_size_tx,epochs_tx,validation_perc_tx,data_aug_ckbox]))
            if data_aug_ckbox.value:
                display(widgets.VBox([rotation_range_tx,width_shift_range_tx,height_shift_range_tx,zoom_range_tx,horizontal_flip_tx]))
            display(widgets.VBox([train_btn]))
        else:
            display(widgets.VBox([adv_ckbox, train_btn]))
    def data_aug_ckbox_change(b):
        clear_output()
        if data_aug_ckbox.value:
            display(widgets.VBox([adv_ckbox,model_chose_tx,batch_size_tx,epochs_tx,validation_perc_tx,data_aug_ckbox]))
            display(widgets.VBox([rotation_range_tx,width_shift_range_tx,height_shift_range_tx,zoom_range_tx,horizontal_flip_tx,train_btn]))
        else:
             display(widgets.VBox([adv_ckbox,model_chose_tx,batch_size_tx,epochs_tx,validation_perc_tx,data_aug_ckbox,train_btn]))
    adv_ckbox.observe(on_adv_ckbox_change)
    data_aug_ckbox.observe(data_aug_ckbox_change)

    def on_train_btn_click(b):
        global model, label_names
        on_adv_ckbox_change(adv_ckbox)
        train.model_chose='mobilenetv2'
        batch_size = 4
        epochs = 15
        validation_perc=0.1
        data_aug =False
        rotation_range=45,
        width_shift_range=.15,
        height_shift_range=.15,
        horizontal_flip=True,
        zoom_range=0.5
        horizontal_flip=horizontal_flip_tx.value
        data_aug =data_aug_ckbox.value
        #验证输入数据的正确性
        if model_chose_tx.value=='inceptionv3':
            train.model_chose='inceptionv3'
        if batch_size_tx.value > 0:
            batch_size = batch_size_tx.value
        if epochs_tx.value > 0:
            epochs = epochs_tx.value
        if  validation_perc_tx.value>0 and validation_perc_tx.value<1:
            validation_perc=validation_perc_tx.value
        if  rotation_range_tx.value>0 and rotation_range_tx.value<360:
            rotation_range=rotation_range_tx.value
        if width_shift_range_tx.value>0 :
            width_shift_range=width_shift_range_tx.value
        if height_shift_range_tx.value>0 :
            height_shift_range=height_shift_range_tx.value
        if zoom_range_tx.value>0 :
            zoom_range=zoom_range_tx.value
        train_generator, val_generator, classes, label_names = load_data(data_dir=dataset_path,
                                                                         batch_size=batch_size,
                                                                         validation_perc=validation_perc,
                                                                         data_aug=data_aug,
                                                                         rotation_range=rotation_range,
                                                                         width_shift_range=width_shift_range,
                                                                         height_shift_range=height_shift_range,
                                                                         horizontal_flip=horizontal_flip,
                                                                         zoom_range=zoom_range)

        print('开始模型训练。。。')
        model = train_model(classes, train_generator, val_generator, epochs)
        with open('label_names.dat', 'w') as f:
            for i in range(len(label_names)):
                f.write(label_names[i]+' ')
    train_btn.on_click(on_train_btn_click)
