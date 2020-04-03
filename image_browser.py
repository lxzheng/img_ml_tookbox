# coding=utf-8
import os
import ipywidgets as widgets  # 控件库
from ipywidgets import GridspecLayout
from IPython.display import display, clear_output  # 显示控件的方法
from numpy import zeros
from matplotlib.pyplot import figure, imshow, subplot, imread

index, del_index, imgs_count = 0, 0, 0
imgs = []

current_dataset_dir = ''


def display_images(data_dir='data', grid_size=(2, 2), img_disp_size=(100, 100)):
    global index, del_index, imgs_count, imgs, current_dataset_dir
    n, m = grid_size[0], grid_size[1]  # 图像grid布局
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    dataset_dirs = [f for f in os.listdir(data_dir) if not f.startswith('.') and os.path.isdir(data_dir + '/' + f)]
    dir_chooser = widgets.Dropdown(
        options=dataset_dirs,
        description='数据集目录')
    if len(dataset_dirs) > 0:
        dir_chooser.value = dataset_dirs[0]
        dir_chooser.disabled = False
    else:
        dir_chooser.disabled = True
    if len(dir_chooser.value):
        current_dataset_dir = dir_chooser.value
        refresh_btn = widgets.Button(description='刷新')

    def refresh_btn_click(sender):
        global current_dataset_dir
        dataset_dirs = [f for f in os.listdir(data_dir) if
                        (not f.startswith('.')) and os.path.isdir(data_dir + '/' + f)]
        dir_chooser.options = dataset_dirs
        if len(dataset_dirs) > 0:
            dir_chooser.value = dataset_dirs[0]
            dir_chooser.disabled = False
        else:
            dir_chooser.disabled = True
        current_dataset_dir = dir_chooser.value

    refresh_btn.on_click(refresh_btn_click)
    box = widgets.Box([dir_chooser, refresh_btn])

    display(box)

    if dir_chooser.value is None:
        classes_names = []
    else:
        classes_names = [f for f in os.listdir(data_dir + '/' + dir_chooser.value) if
                         os.path.isdir(data_dir + '/' + dir_chooser.value + '/' + f)]
    classes_chooser = widgets.Dropdown(
        options=classes_names,
        description='类别:',
        disabled=False,
    )
    if len(classes_names) > 0:
        classes_chooser.value = classes_names[0]
        classes_chooser.disabled = False
    else:
        classes_chooser.disabled = True

    display(classes_chooser)

    if classes_chooser.value is None:
        imgs = []
    else:
        imgs = os.listdir(data_dir + '/' + dir_chooser.value + '/' + classes_chooser.value)
    imgs_count = len(imgs)

    grid = GridspecLayout(n, m)
    next_bt = widgets.Button(description="下一页")
    display(next_bt)
    index = 0
    del_index = 0
    images = [widgets.Image(width=img_disp_size[0], height=img_disp_size[1], ) for i in range(m * n)]
    del_ckbxs = [widgets.Checkbox() for i in range(m * n)]
    file_name_labels = [widgets.Label() for i in range(m * n)]
    # image_del_boxs = [widgets.VBox([del_ckbxs[i], images[i], file_name_labels[i]]) for i in range(m * n)]
    image_del_boxs = [widgets.VBox([del_ckbxs[i], images[i]]) for i in range(m * n)]

    out = widgets.Output(layout={'border': '1px solid black'})
    display(out)
    out.clear_output()
    del_bt = widgets.Button(description="删除选中图像")
    display(del_bt)

    def on_next_bt_clicked(b):
        global index, del_index, imgs, imgs_count
        out.clear_output()
        for i in range(m * n):
            images[i].value = bytes()
            file_name_labels[i].value = ''
            del_ckbxs[i].disabled = True
            del_ckbxs[i].value = False

        next_bt.disabled = True
        del_bt.disabled = True
        if imgs_count > 0:
            del_bt.disabled = False
        if imgs_count > m * n:
            next_bt.disabled = False
        imgs.sort()
        for i in range(n):
            for j in range(m):
                if i * m + j + index >= imgs_count:
                    break

                file_name_labels[i * m + j].value = imgs[i * m + j + index]

                img_file = data_dir + '/' + dir_chooser.value + '/' + classes_chooser.value + '/' + imgs[
                    i * m + j + index]
                if (not os.path.isdir(img_file)) and (img_file.lower().endswith(('.png', '.jpg',
                                                                                 '.jpeg', '.tiff',
                                                                                 '.bmp'))):
                    file = open(img_file, 'rb')
                    image = file.read()
                    file.close()
                    images[i * m + j].value = image
                    grid[i, j] = image_del_boxs[i * m + j]
                    del_ckbxs[i * m + j].disabled = False
            else:
                continue
            break
        with out:
            print('page:' + str(int(1 + index / (m * n))))
            display(grid)

        del_index = index
        index = index + m * n
        if index >= imgs_count:
            index = 0

    next_bt.on_click(on_next_bt_clicked)
    on_next_bt_clicked(next_bt)

    def on_del_bt_clicked(b):
        global imgs, imgs_count, index, del_index
        for i in range(m * n):
            if del_ckbxs[i].value:
                del_ckbxs[i].value = False
                os.remove(data_dir + '/' + dir_chooser.value + '/' + classes_chooser.value + '/' + imgs[del_index + i])
                images[i].value = bytes()
        imgs = os.listdir(data_dir + '/' + dir_chooser.value + '/' + classes_chooser.value)
        imgs_count = len(imgs)
        index = del_index
        on_next_bt_clicked(next_bt)

    del_bt.on_click(on_del_bt_clicked)

    def on_classes_change(change):
        global imgs, imgs_count, index
        if change['type'] == 'change' and change['name'] == 'value':
            imgs = []

            if not classes_chooser.value is None:
                img_dir = data_dir + '/' + dir_chooser.value + '/' + classes_chooser.value
                if os.path.isdir(img_dir):
                    imgs = os.listdir(img_dir)
            imgs_count = len(imgs)
            index = 0

            on_next_bt_clicked(next_bt)

    classes_chooser.observe(on_classes_change)

    def on_dir_change(change):
        global imgs, imgs_count, index, current_dataset_dir

        current_dataset_dir = dir_chooser.value
        if dir_chooser.value is None:
            classes_names = []
        else:
            classes_names = [f for f in os.listdir(data_dir + '/' + dir_chooser.value) if
                             os.path.isdir(data_dir + '/' + dir_chooser.value + '/' + f)]

        classes_chooser.options = classes_names
        if len(classes_names) > 0:
            classes_chooser.value = classes_names[0]
            classes_chooser.disabled = False
        else:
            classes_chooser.disabled = True

    dir_chooser.observe(on_dir_change)
