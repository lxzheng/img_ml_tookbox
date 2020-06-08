import os
from zipfile import ZipFile
import tarfile
import ipywidgets as widgets  # 控件库
from IPython.display import display  # 显示控件的方法

down_file=['']
extract_dir = ''
data_base_dir='./data/'
zip_file_chooser = widgets.Dropdown()
unzip_btn = widgets.Button(description='解压')


def unzip_data(zipfile, to_path):
    dataset_name=os.path.split(to_path)[-1]
    if not os.path.exists(to_path):
        os.makedirs(to_path)
        # print('make dir:'+ to_path)
    if os.path.exists(zipfile):
        if zipfile.lower().endswith('.zip'):
            zf = ZipFile(zipfile, 'r')
            name_list=zf.namelist()
            if name_list and dataset_name in name_list[0]:
                to_path=data_base_dir
            zf.extractall(to_path)
            zf.close()
        if zipfile.lower().endswith('.tgz') or zipfile.lower().endswith('.tar.gz'):
            tar = tarfile.open(zipfile)
            name_list=tar.getnames()
            if name_list and dataset_name in name_list[0]:
                to_path = data_base_dir
            tar.extractall(path=to_path)
            tar.close()
        print('已将 ' + zipfile + ' 解压到 ' + os.path.split(extract_dir)[-1]+'目录')
        return to_path
    else:
        print('Error:' + zipfile + ' not found')
    return None


def get_zip_file_list():
    files = os.listdir()
    zip_files = []
    for file in files:
        if file.lower().endswith('.zip') or file.lower().endswith('.tgz') or file.lower().endswith('.tar.gz'):
            zip_files.append(file)
    return zip_files


def refresh_btn_click(sender):
    zip_files = get_zip_file_list()
    if len(zip_files):
        zip_file_chooser.options = zip_files
        zip_file_chooser.value = zip_files[0]
        unzip_btn.disabled = False
        if down_file[0] in zip_files:
            zip_file_chooser.value = down_file[0]
    else:
        unzip_btn.disabled = True


def do_unzip(zip_file_name):
    global down_file
    down_file=zip_file_name
    zip_files=get_zip_file_list()

    if len(zip_files):
        zip_file_chooser.options=zip_files
        zip_file_chooser.description='压缩文件:'
        zip_file_chooser.value=zip_files[0]
        zip_file_chooser.disabled=False
        
    if zip_file_name[0] in zip_files:
        zip_file_chooser.value = zip_file_name[0]
    print('请选择要解压的数据集文件，点击“解压”按键将压缩文件解压，点击“刷新”按键更新文件列表')

    if len(zip_files) == 0:
        unzip_btn.disabled = True

    def unzip_btn_click(sender):
        global extract_dir
        filename = zip_file_chooser.value
        extract_dir = data_base_dir + os.path.splitext(filename)[0]

        unzip_data(filename, extract_dir)

    unzip_btn.on_click(unzip_btn_click)

    refresh_btn = widgets.Button(description='刷新')
    refresh_btn.on_click(refresh_btn_click)

    box = widgets.Box([zip_file_chooser, unzip_btn, refresh_btn])
    display(box)
