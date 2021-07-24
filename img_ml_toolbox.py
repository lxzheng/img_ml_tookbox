import ipywidgets as widgets
from IPython.display import display, clear_output  # 显示控件的方法


import net_transfer
import unzip_data
import image_browser
import transvideo_data
import downloadimage_data
import gen_model
import classifier

current_dataset_dir=['']


def prepare_data():
    global current_dataset_dir

    get_data_option=widgets.RadioButtons(
        options=['网络下载', '搜索引擎爬取', '视频转换'],
        description='数据准备方式',
        disabled=False,
        value='网络下载'
    )
    out = widgets.Output(layout={'border': '1px solid black','height':"360px"})

    def on_get_data_option_change(b):
        with out:
            clear_output()
            display(get_data_option)
            if get_data_option.value:
                if get_data_option.value=='网络下载':
                    net_transfer.get_zip_file()
                    unzip_data.do_unzip(net_transfer.file_name)
                if get_data_option.value=='搜索引擎爬取':
                    downloadimage_data.get_image()
                if get_data_option.value =='视频转换':
                    transvideo_data.get_Video()

    get_data_option.observe(on_get_data_option_change,names='value')
    with out:
        display(get_data_option)
        net_transfer.get_zip_file()
        unzip_data.do_unzip(net_transfer.file_name)
    display(out)
    image_browser.display_images(grid_size=(2,3),img_disp_size=(150,150))

def make_model():
    gen_model.do_model_train(image_browser.current_dataset_dir)

def predict():
    classifier.do_classification(gen_model.model, gen_model.label_names)
