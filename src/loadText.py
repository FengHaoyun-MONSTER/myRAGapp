import mimetypes # mimetypes模块用来根据文件扩展名猜测内容类型，反之亦可，
import os
import configparser # configparser模块用来读取配置文件

def loadtext(path):
    path = path.rstrip( ) # 去除文件路径末尾空格，为了防止空格导致文件读取失败
    path = path.replace(' \n', '') # 去除文件路径中的换行符，为了防止换行符导致文件读取失败

    # 转换绝对路径 - 如果是相对路径，基于脚本所在目录解析
    if not os.path.isabs(path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, path)
    else:
        filename = path
    
    # 判断文档存在， 获取文档类型
    if not os.path.isfile(filename):
        print(f"File {filename} not found")
        return None
    
    # 读取文档内容 - 对于文本文件，直接尝试读取并解码
    try:
        # 尝试UTF-8编码
        with open(filename, 'rb') as f:
            text = f.read().decode('utf-8')
    except UnicodeDecodeError:
        # 如果UTF-8失败，尝试GBK（常见中文编码）
        try:
            with open(filename, 'rb') as f:
                text = f.read().decode('gbk')
        except UnicodeDecodeError:
            print(f"无法解码文件 {filename}，尝试使用UTF-8和GBK都失败了")
            return None
    
    return text

    # 模型配置获取
def getconfig():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return dict(config.items("main"))