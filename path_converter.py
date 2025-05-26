# path_converter.py
import re
from urllib.parse import unquote

# ========== SMB路径转换 ==========
def smb_to_windows_unc(smb_path):
    """SMB转Windows UNC路径（自动处理特殊字符）"""
    if not smb_path.startswith("smb://"):
        return smb_path
    
    # 提取服务器地址和共享路径
    path_parts = smb_path[6:].split("/", 1)
    server = path_parts[0]
    share_path = path_parts[1] if len(path_parts) > 1 else ""
    
    # 解码URL特殊字符（如空格自动转为%20）
    share_path = unquote(share_path).replace("/", "\\")
    
    # 处理中文和空格（Windows UNC直接支持）
    return f"\\\\{server}\\{share_path}"

def smb_to_mac_mount(smb_path, mount_root="/Volumes"):
    """SMB转Mac挂载路径（需提前挂载）"""
    if not smb_path.startswith("smb://"):
        return smb_path
    
    path_parts = smb_path[6:].split("/", 1)
    server = path_parts[0].replace(".", "-")  # 服务器地址中的.转-
    share_path = path_parts[1] if len(path_parts) > 1 else ""
    
    # 示例映射规则：smb://10.163.0.55/Share-sea → /Volumes/Share-sea
    share_name = share_path.split("/")[0] if "/" in share_path else "default"
    return f"{mount_root}/{share_name}/{unquote(share_path)}"

# ========== 反向转换 ==========
def windows_to_smb(win_path):
    """Windows路径转SMB格式"""
    if win_path.startswith("\\\\"):
        win_path = win_path.replace("\\", "/")
        return f"smb:/{win_path}"
    return win_path

def mac_to_smb(mac_path):
    """Mac路径转SMB格式"""
    if mac_path.startswith("/Volumes/"):
        path_parts = mac_path.split("/")[3:]
        server_share = "/".join(path_parts[:2])  # 假设/Volumes/[ShareName]
        return f"smb://{server_share.replace('-', '.')}/{'/'.join(path_parts[2:])}"
    return mac_path

# ========== 主逻辑 ==========
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input_path = f.read().strip()

    # 自动检测输入类型
    if input_path.startswith("smb://"):
        # 转换到目标系统（示例：Windows）
        output = smb_to_windows_unc(input_path)
    elif input_path.startswith("\\\\"):
        output = windows_to_smb(input_path)
    elif input_path.startswith("/Volumes/"):
        output = mac_to_smb(input_path)
    else:
        output = "Unsupported path format"

    with open("output.txt", "w") as f:
        f.write(output)
