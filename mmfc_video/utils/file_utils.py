"""
文件操作工具函数
"""

import os
from pathlib import Path
from typing import List

def get_asset_path(filename: str) -> str:
    """
    获取静态资源文件的完整路径
    
    Args:
        filename: 资源文件名
        
    Returns:
        完整的文件路径
    """
    # 获取项目根目录
    current_dir = Path(__file__).parent.parent.parent
    asset_path = current_dir / "assets" / filename
    return str(asset_path)

def scan_video_files(folder_path: str, video_formats: set) -> List[str]:
    """
    扫描指定文件夹中的所有视频文件
    
    Args:
        folder_path: 要扫描的文件夹路径
        video_formats: 支持的视频格式集合
        
    Returns:
        视频文件路径列表
    """
    video_files = []
    
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if Path(file).suffix.lower() in video_formats:
                    video_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"扫描文件夹时出错: {e}")
        
    return video_files 