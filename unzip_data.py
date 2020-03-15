import os
from zipfile import ZipFile
import ipywidgets as widgets  # 控件库
from IPython.display import display  # 显示控件的方法

extract_dir = ''


def unzip_data(zipfile, to_path):
    if not os.path.exists(to_path):
        os.makedirs(to_path)
        # print('make dir:'+ to_path)
    if os.path.exists(zipfile):
        zf = ZipFile(zipfile, 'r')
        zf.extractall(to_path)
        zf.close()
        print('已将 ' + zipfile + ' 解压到 ' + os.path.split(to_path)[-1]+'目录')
        return to_path
    else:
        print('Error:' + zipfile + ' not found')
    return None


def get_zip_file_list():
    files = os.listdir()
    zip_files = []
    for file in files:
        if file.lower().endswith('.zip'):
            zip_files.append(file)
    return zip_files


def do_unzip(down_file):
    # text = widgets.Text(value=zipfile)
    zip_files=get_zip_file_list()
    zip_file_chooser = widgets.Dropdown(
        options=zip_files,
        description='zip文件:',
        value=zip_files[0],
        disabled=False,
    )
    if down_file in zip_files:
        zip_file_chooser.value = down_file
    print('请选择要解压的zip文件，点击“解压”按键将zip文件解压，点击“刷新”按键更新zip文件列表')
    unzip_btn = widgets.Button(description='解压')
    if len(zip_files) == 0:
        unzip_btn.disabled = True

    def unzip_btn_click(sender):
        global extract_dir
        filename = zip_file_chooser.value
        extract_dir = 'data/' + os.path.splitext(filename)[0]

        unzip_data(filename, extract_dir)

    unzip_btn.on_click(unzip_btn_click)
    refresh_btn = widgets.Button(description='刷新')

    def refresh_btn_click(sender):
        zip_files = get_zip_file_list()
        zip_file_chooser.options = zip_files
        zip_file_chooser.value = zip_files[0]
        if down_file in zip_files:
            zip_file_chooser.value = down_file
        if len(zip_files) == 0:
            unzip_btn.disabled = True
        else:
            unzip_btn.disabled = False
    refresh_btn.on_click(refresh_btn_click)
    box = widgets.Box([zip_file_chooser, unzip_btn, refresh_btn])
    display(box)
