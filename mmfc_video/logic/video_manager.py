"""
视频管理模块 - 负责视频文件扫描、播放记录管理等业务逻辑
"""

import random
from typing import List, Set
from PySide6.QtCore import QThread, Signal

from ..utils.file_utils import scan_video_files
from .. import VIDEO_FORMATS

class VideoScanner(QThread):
    """视频文件扫描线程"""
    videos_found = Signal(list)
    progress_update = Signal(str)
    
    def __init__(self, folder_path: str):
        super().__init__()
        self.folder_path = folder_path
        
    def run(self):
        """执行视频文件扫描"""
        self.progress_update.emit("正在扫描视频文件...")
        video_files = scan_video_files(self.folder_path, VIDEO_FORMATS)
        self.videos_found.emit(video_files)

class VideoManager:
    """视频播放管理器"""
    
    def __init__(self):
        self.video_list: List[str] = []
        self.played_videos: Set[str] = set()
        self.current_video_path: str = ""
        self.current_folder: str = ""
        
    def set_video_list(self, video_list: List[str]):
        """设置视频列表"""
        self.video_list = video_list
        self.played_videos.clear()
        
    def get_random_unplayed_video(self) -> str:
        """获取一个随机的未播放视频"""
        unplayed_videos = [v for v in self.video_list if v not in self.played_videos]
        if not unplayed_videos:
            return ""
        
        video_path = random.choice(unplayed_videos)
        self.played_videos.add(video_path)
        self.current_video_path = video_path
        return video_path
        
    def mark_as_played(self, video_path: str):
        """标记视频为已播放"""
        self.played_videos.add(video_path)
        self.current_video_path = video_path
        
    def reset_played_videos(self):
        """重置播放记录"""
        self.played_videos.clear()
        
    def get_stats(self) -> dict:
        """获取播放统计信息"""
        total = len(self.video_list)
        played = len(self.played_videos)
        remaining = total - played
        
        return {
            'total': total,
            'played': played,
            'remaining': remaining
        }
        
    def has_unplayed_videos(self) -> bool:
        """检查是否还有未播放的视频"""
        return len(self.played_videos) < len(self.video_list) 