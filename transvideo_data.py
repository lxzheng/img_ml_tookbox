import os
import ffmpeg
import numpy
import ipywidgets as widgets  # 控件库
import piexif

data_base_dir='./data/'

#from IPython.display import display, clear_output
#  获取视频的指定时间画面
def read_time_as_jpeg(file_name, time):
    out, err = (
        ffmpeg.input(file_name, ss=time)
              .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
              .run(capture_stdout=True)
    )
    return out
#获取视频的总帧数
def get_video_info(file_name):
    try:
        probe = ffmpeg.probe(file_name)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('找不到视频', file=sys.stderr)
            sys.exit(1)
        return int(video_stream['nb_frames'])
    except ffmpeg.Error as err:
        print(str(err.stderr, encoding='utf8'))
        sys.exit(1)
    return   int(video_stream['nb_frames'])

def trans_video_to_jpeg(dataset_name, file_name, label_name, interval):#视频文件名,帧数间隔
    total_jpeg = int(float(ffmpeg.probe(file_name)['format']['duration'])/interval)
    data_dir = data_base_dir + dataset_name
    try:
        os.makedirs(data_dir)#创建文件夹
    except:
        print('该数据集文件夹已经创建')  
    data_dir = data_base_dir + dataset_name + '/' + label_name
    try:
        os.makedirs(data_dir)#创建文件夹
    except:
        print('该标签文件夹已经创建')  
    for i in range(1,total_jpeg):
        out=read_time_as_jpeg(file_name,i*interval)
        file = open(data_dir+'/'+str(i)+'.jpg','wb')
        file.write(out)
        file.close()
        print('当前进度'+str(i)+'/'+str(total_jpeg))
def get_video_file_list():
    files = os.listdir()
    video_files = []
    for file in files:
        if file.lower().endswith('.mp4'):
            video_files.append(file)
    return video_files
def get_Video(data_dir='data'):
      # text = widgets.Text(value=videofile)
    video_files=get_video_file_list()
    video_file_chooser = widgets.Combobox(
        options=video_files,
        description='视频文件:',
        placeholder='选择一个当前目录下的视频文件或输入路径名',
        value='',
        disabled=False,
    )


    print('请输入数据集名称、要保存的标签名、选择需转换成图像的视频文件和转换间隔，点击“转换”按键将把视频转换成数据集')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    dataset_dirs = [f for f in os.listdir(data_dir) if not f.startswith('.') and os.path.isdir(data_dir + '/' + f)]


    dataset_name=widgets.Combobox(
          value='',
          placeholder='选择一个已有数据集或输入新数据集名称',
          options=dataset_dirs,
          description='数据集名称:',
          ensure_option=False,
          disabled=False
    )
    label_name_txt = widgets.Text(description='类别',value='')
    interval_txt= widgets.IntText( description='间隔时间(秒)',value=1)
    btn = widgets.Button(description='转换')
    if len(video_files) > 0:
        video_file_chooser.value = video_files[0]


    def btn_click(sender):
        if label_name_txt.value =='' :
            print('请在文本框中输入标签名')
        elif  interval_txt.value is None :
            print('请在文本框中输入抽取图像时间间隔')
        else:
            try:
                trans_video_to_jpeg(str(dataset_name.value),str(video_file_chooser.value),str(label_name_txt.value),interval_txt.value)
                print('视频转换完成') 
            except Exception as result:
                print(result)
    btn.on_click(btn_click)
    box = widgets.VBox([dataset_name,label_name_txt,video_file_chooser,interval_txt,btn])
    display(box)

    

    