import base64
from PIL import Image
from io import BytesIO

# base64转图片
def down_base64(path,base64_str):
    img_data = base64.b64decode(base64_str)    # 解码时只要内容部分
    image = Image.open(BytesIO(img_data))
    image.save(path)

# 图片转base64
def get_base64(path, fmt='png'):
    image = Image.open(path)
    output_buffer = BytesIO() # 创建缓冲区
    image.save(output_buffer, format=fmt) # 保存图片到缓冲区
    byte_data = output_buffer.getvalue() # 获取缓冲区内容
    base64_str = base64.b64encode(byte_data).decode('utf-8') # 编码并转换为字符串
    return base64_str

# 写入txt文本
def write_txt(path,content):
    with open(path,'w') as f:
        f.write(str(content))

# 读取txt文本
def read_txt(path):
    with open(path,'r') as f:
        return str(f.read())