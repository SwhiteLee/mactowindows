# path_converter.py
import re

def mac_to_windows(path):
    # 转换示例：/Users/Alice/Documents → C:\Users\Alice\Documents
    if path.startswith("/Users/"):
        path = "C:" + path.replace("/", "\\")
    return path

def windows_to_mac(path):
    # 转换示例：C:\Users\Alice\Documents → /Users/Alice/Documents
    if re.match(r"^[A-Z]:\\", path, re.IGNORECASE):
        path = path[2:].replace("\\", "/")
        if path.startswith("Users/"):
            path = "/" + path
    return path

if __name__ == "__main__":
    # 读取输入文件
    with open("input.txt", "r") as f:
        input_path = f.read().strip()

    # 判断输入类型并转换
    if input_path.startswith("/"):
        output = mac_to_windows(input_path)
    elif ":" in input_path:
        output = windows_to_mac(input_path)
    else:
        output = "Invalid path format"

    # 写入输出文件
    with open("output.txt", "w") as f:
        f.write(output)
