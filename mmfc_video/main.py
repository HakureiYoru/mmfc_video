"""
MMFC-VIDEO 主入口文件
"""

import sys
from PySide6.QtWidgets import QApplication

from .ui import ModernVideoPlayer
from . import __version__, __description__

def main():
    """主函数 - 启动应用程序"""
    app = QApplication(sys.argv)
    app.setApplicationName("MMFC_VIDEO")
    app.setApplicationVersion(__version__)
    # 不设置 setApplicationDisplayName，避免标题被拼接
    app.setStyle("Fusion")
    
    # 创建并显示主窗口
    player = ModernVideoPlayer()
    player.show()
    
    # 运行事件循环
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 