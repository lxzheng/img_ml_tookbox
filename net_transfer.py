import ipywidgets as widgets      # 控件库
from IPython.display import display, clear_output # 显示控件的方法
import wget

output = widgets.Output(layout={'height':"40px"})
progress=0
def bar_progress(current, total, width=80):
    global progress
    curr_progress=current/total*100
    if curr_progress>progress:
        progress=+progress+10
        with output:
            clear_output()
            print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))


file_name=['']
def get_zip_file():
    url_txt = widgets.Text(description='链接')
    print('请输入下载链接，和要保存的文件名，点击“传输”按键开始数据集下载')
    file_name_txt = widgets.Text(description='文件名',value='dataset.zip')
    btn = widgets.Button(description='传输')

    def btn_click(sender):
        global file_name
        if url_txt.value is None or str(url_txt.value).lstrip()=='':
            with output:
                clear_output()
                print('请在文本框中输入下载链接')
        else:
            try:
                wget.download(url_txt.value, out=file_name_txt.value, bar=bar_progress)
                with output:
                    clear_output()
                    print('下载完成')
                file_name[0]=file_name_txt.value
            except:
                with output:
                    clear_output()
                    print('下载出错')

    btn.on_click(btn_click)
    box = widgets.VBox([url_txt,file_name_txt, btn])
    display(box)
    display(output)
