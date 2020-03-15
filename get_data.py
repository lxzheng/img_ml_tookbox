import ipywidgets as widgets	# 控件库
from IPython.display import display	# 显示控件的方法

text = widgets.Text()
print('请输入数据文件下载链接，点击加载按键将数据集加载到服务器')
btn=widgets.Button(description ='加载')
box = widgets.Box([text,btn])
display(box)
