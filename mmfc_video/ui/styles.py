"""
UI样式定义 - 极简黑白透明风格
"""

def get_app_stylesheet() -> str:
    """获取应用程序的完整样式表 - 磨砂玻璃 + 浅白色透明风格"""
    return """
    QMainWindow {
        background: transparent;
    }
    
    /* 控制面板框架 - 磨砂玻璃效果 */
    #controlFrame {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        backdrop-filter: blur(25px);
    }
    
    /* 进度条框架 */
    #progressFrame {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        backdrop-filter: blur(25px);
    }
    
    /* 图标按钮样式 */
    #iconButton {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(200, 200, 200, 0.6);
        border-radius: 8px;
        color: rgba(0, 0, 0, 0.8);
        font-weight: 600;
        font-size: 16px;
    }
    
    #iconButton:hover {
        background: rgba(173, 216, 230, 0.8);
        border: 1px solid rgba(135, 206, 235, 0.8);
        color: rgba(0, 0, 0, 0.9);
    }
    
    #iconButton:pressed {
        background: rgba(135, 206, 235, 0.9);
        border: 1px solid rgba(100, 149, 237, 0.9);
    }
    
    #iconButton:disabled {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(200, 200, 200, 0.3);
        color: rgba(0, 0, 0, 0.4);
    }
    
    /* 播放按钮特殊样式 */
    #playButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(100, 149, 237, 0.8),
            stop:1 rgba(135, 206, 235, 0.9));
        border: 1px solid rgba(70, 130, 180, 0.8);
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        font-size: 18px;
    }
    
    #playButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(70, 130, 180, 0.9),
            stop:1 rgba(100, 149, 237, 1.0));
    }
    
    #playButton:disabled {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(200, 200, 200, 0.3);
        color: rgba(0, 0, 0, 0.4);
    }
    
    /* 通用框架样式 */
    QFrame {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        backdrop-filter: blur(20px);
    }
    
    /* 标签样式 */
    QLabel {
        color: rgba(0, 0, 0, 0.8);
        font-weight: 500;
    }
    
    #infoLabel {
        color: rgba(0, 0, 0, 0.75);
        font-size: 12px;
        padding: 4px 8px;
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 6px;
    }
    
    #answerLabel {
        color: rgba(0, 0, 0, 0.9);
        font-weight: 600;
        font-size: 13px;
        padding: 6px 10px;
        background: rgba(173, 216, 230, 0.6);
        border: 1px solid rgba(135, 206, 235, 0.7);
        border-radius: 8px;
    }
    
    #statsLabel {
        color: rgba(0, 0, 0, 0.8);
        font-size: 11px;
        font-weight: 600;
        padding: 4px 8px;
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 6px;
    }
    
    /* 复选框样式 */
    #modernCheckBox {
        font-size: 12px;
        color: rgba(0, 0, 0, 0.8);
        font-weight: 500;
        spacing: 8px;
    }
    
    #modernCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 1px solid rgba(135, 206, 235, 0.7);
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.8);
    }
    
    #modernCheckBox::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(100, 149, 237, 0.9),
            stop:1 rgba(135, 206, 235, 0.9));
        border: 1px solid rgba(70, 130, 180, 0.9);
    }
    
    /* 进度条样式 */
    #progressBar {
        border: 1px solid rgba(135, 206, 235, 0.7);
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.6);
        height: 14px;
    }
    
    #progressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(100, 149, 237, 0.9),
            stop:0.5 rgba(135, 206, 235, 1.0),
            stop:1 rgba(173, 216, 230, 0.9));
        border-radius: 5px;
        border: none;
    }
    
    #timeLabel {
        color: rgba(0, 0, 0, 0.8);
        font-weight: 600;
        font-size: 11px;
        padding: 2px 4px;
    }
    
    /* 视频列表标题栏样式 */
    #listHeader {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(135, 206, 235, 0.6);
        border-radius: 8px 8px 0 0;
        backdrop-filter: blur(20px);
    }
    
    #listTitle {
        color: rgba(0, 0, 0, 0.9);
        font-weight: 600;
        font-size: 13px;
    }
    
    /* 折叠按钮样式 */
    #collapseButton {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(135, 206, 235, 0.7);
        border-radius: 4px;
        color: rgba(0, 0, 0, 0.8);
        font-weight: bold;
        font-size: 12px;
    }
    
    #collapseButton:hover {
        background: rgba(173, 216, 230, 0.8);
        border: 1px solid rgba(100, 149, 237, 0.8);
        color: rgba(0, 0, 0, 0.9);
    }
    
    #collapseButton:pressed {
        background: rgba(135, 206, 235, 0.9);
        border: 1px solid rgba(70, 130, 180, 0.9);
    }
    
    /* 视频列表样式 */
    #videoList {
        border: 1px solid rgba(135, 206, 235, 0.5);
        border-radius: 0 0 8px 8px;
        border-top: none;
        background: rgba(255, 255, 255, 0.6);
        color: rgba(0, 0, 0, 0.8);
        font-size: 12px;
        backdrop-filter: blur(15px);
    }
    
    #videoList::item {
        padding: 6px 8px;
        border-bottom: 1px solid rgba(135, 206, 235, 0.2);
        border-radius: 4px;
        margin: 1px;
    }
    
    #videoList::item:selected {
        background: rgba(135, 206, 235, 0.5);
        color: rgba(0, 0, 0, 0.9);
        border: 1px solid rgba(100, 149, 237, 0.7);
    }
    
    #videoList::item:hover {
        background: rgba(173, 216, 230, 0.4);
    }
    
    /* 视频播放器样式 */
    QVideoWidget {
        background-color: rgba(0, 0, 0, 0.95);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
    }
    
    /* 状态栏样式 */
    QStatusBar {
        background: rgba(255, 255, 255, 0.3);
        color: rgba(0, 0, 0, 0.8);
        font-weight: 500;
        border-top: 1px solid rgba(255, 255, 255, 0.4);
    }
    """ 