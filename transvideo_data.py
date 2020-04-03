import os
import ffmpeg
import numpy
import ipywidgets as widgets  # 控件库
import piexif
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

def trans_video_to_jpeg(date_name,file_name,label_name,interval):#视频文件名,帧数间隔
    total_jpeg = int(float(ffmpeg.probe(file_name)['format']['duration'])/interval)
    date_dir = './data/'+date_name
    try:
        os.makedirs(date_dir)#创建文件夹
    except:
        print('该数据集文件夹已经创建')  
    date_dir = './data/'+date_name+'/'+label_name
    try:
        os.makedirs(date_dir)#创建文件夹
    except:
        print('该标签文件夹已经创建')  
    for i in range(1,total_jpeg):
        out=read_time_as_jpeg(file_name,i*interval)
        file = open(date_dir+'/'+str(i)+'.jpg','wb')
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
def get_Video():
      # text = widgets.Text(value=videofile)
    video_files=get_video_file_list()
    video_file_chooser = widgets.Dropdown(
        options=video_files,
        description='选择本地文件:',
        value=video_files[0],
        disabled=False,
    )

    print('请输入本地视频地址、要保存的标签名和间隔，点击“传输”按键将把视频转换成数据集')
    file_name_txt = widgets.Text(description='视频位置',value='')
    date_name_txt = widgets.Text(description='数据集名称',value='')
    label_name_txt = widgets.Text(description='类别',value='')
    interval_txt= widgets.IntText( description='间隔时间(秒)',value=1)
    btn = widgets.Button(description='转换')
    file_name_txt.value=video_file_chooser.value
    def video_file_chooser_change(b):
        file_name_txt.value=video_file_chooser.value
    video_file_chooser.observe(video_file_chooser_change)
    def btn_click(sender):
        if file_name_txt.value  =='' :
            print('请在文本框中输入视频的地址')
        elif date_name_txt.value  =='' :
            print('请在文本框中输入要创建数据集名称')
        elif label_name_txt.value =='' :
            print('请在文本框中输入标签名')
        elif  interval_txt.value is None :
            print('请在文本框中输入间隔')
        else:
            try:
                trans_video_to_jpeg(str(date_name_txt.value),str(file_name_txt.value),str(label_name_txt.value),interval_txt.value)
                print('视频转换完成') 
            except Exception as result:
                print(result)
    btn.on_click(btn_click)
    box = widgets.VBox([file_name_txt,video_file_chooser,date_name_txt,label_name_txt, interval_txt,btn])
    display(box)

    

    