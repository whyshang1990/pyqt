import base64


def picture_to_base64(file_path):
    """
    将图片转换为base64编码字符串
    """
    with open(file_path, "rb") as p:
        # p_base64类型为bytes
        p_base64 = base64.b64encode(p.read())
    print(p_base64.decode("utf-8"))
    return p_base64.decode("utf-8")


if __name__ == '__main__':
    file_path = "../tmp/mainwindow_layout.png"
    picture_to_base64(file_path)
