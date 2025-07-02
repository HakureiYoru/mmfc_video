"""
基本功能测试
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicFunctionality(unittest.TestCase):
    """基本功能测试类"""
    
    def test_imports(self):
        """测试模块导入"""
        try:
            import mmfc_video
            from mmfc_video.ui import ModernVideoPlayer
            from mmfc_video.logic import VideoManager, VideoScanner
            from mmfc_video.utils import get_asset_path, format_time
            self.assertTrue(True, "所有模块导入成功")
        except ImportError as e:
            self.fail(f"模块导入失败: {e}")
    
    def test_video_formats(self):
        """测试视频格式定义"""
        from mmfc_video import VIDEO_FORMATS
        expected_formats = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        self.assertEqual(VIDEO_FORMATS, expected_formats, "视频格式定义正确")
    
    def test_video_manager(self):
        """测试视频管理器"""
        from mmfc_video.logic import VideoManager
        
        manager = VideoManager()
        self.assertEqual(len(manager.video_list), 0, "初始视频列表为空")
        self.assertEqual(len(manager.played_videos), 0, "初始播放记录为空")
        
        # 测试设置视频列表
        test_videos = ["test1.mp4", "test2.avi"]
        manager.set_video_list(test_videos)
        self.assertEqual(len(manager.video_list), 2, "视频列表设置成功")
    
    def test_format_time(self):
        """测试时间格式化"""
        from mmfc_video.utils import format_time
        
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(60000), "01:00")
        self.assertEqual(format_time(125000), "02:05")

def run_tests():
    """运行所有测试"""
    try:
        # 检查PySide6是否可用
        from PySide6.QtWidgets import QApplication
        print("✅ PySide6 可用")
        
        unittest.main(verbosity=2)
    except ImportError:
        print("❌ PySide6 未安装，请运行: pip install PySide6")
        return False

if __name__ == "__main__":
    run_tests() 