# coding=utf-8
import os
import ipywidgets as widgets  # 控件库
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
        print ('数据集目录:' + data_dir + '不存在')
        return
    adv_ckbox = widgets.Checkbox(
        value=False,
        description='高级选项',
        disabled=False,
        indent=False
    )
    batch_size_tx = widgets.IntText(value=4, description='批尺寸')
    epochs_tx = widgets.IntText(value=15, description='训练轮数')
    train_btn = widgets.Button(description='训练模型')
    display(widgets.VBox([adv_ckbox, train_btn]))

    def on_adv_ckbox_change(b):
        clear_output()
        if adv_ckbox.value:
            display(widgets.VBox([adv_ckbox, batch_size_tx, epochs_tx, train_btn]))
        else:
            display(widgets.VBox([adv_ckbox, train_btn]))

    adv_ckbox.observe(on_adv_ckbox_change)

    def on_train_btn_click(b):
        global model, label_names
        on_adv_ckbox_change(adv_ckbox)
        batch_size = 4
        epochs = 15
        if batch_size_tx.value > 0:
            batch_size = batch_size_tx.value
        if epochs_tx.value > 0:
            epochs = epochs_tx.value
        train_generator, val_generator, classes, label_names = load_data(data_dir=dataset_path,
                                                                         batch_size=batch_size)

        print('开始模型训练。。。')
        model = train_model(classes, train_generator, val_generator, epochs)

    train_btn.on_click(on_train_btn_click)
