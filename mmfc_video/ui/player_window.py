"""
主窗口类 - MMFC-VIDEO 现代化视频播放器
"""

import os
import random
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QCheckBox, QFileDialog,
    QFrame, QListWidget, QListWidgetItem,
    QMessageBox, QSpacerItem, QSizePolicy, QStatusBar
)
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QPixmap, QPalette, QBrush, QIcon, QColor
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

from .styles import get_app_stylesheet
from ..logic.video_manager import VideoManager, VideoScanner
from ..utils.file_utils import get_asset_path
from ..utils.ui_utils import format_time


class ModernVideoPlayer(QMainWindow):
    """现代化视频播放器主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化组件
        self.video_manager = VideoManager()
        self.is_playing = False
        self.segment_start = 0
        self.segment_duration = 7000  # 7秒，单位毫秒
        
        # 初始化UI
        self.setup_ui()
        self.setup_media_player()
        self.setup_styles()
        self.setup_background()
        
    def setup_ui(self):
        """设置用户界面 - 简洁风格"""
        self.setWindowTitle("MMFC_VIDEO")
        self.setGeometry(100, 100, 900, 650)
        self.setMinimumSize(700, 500)
        
        # 设置应用图标
        icon_path = get_asset_path("myicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)
        
        # 控制面板框架
        control_frame = QFrame()
        control_frame.setObjectName("controlFrame")
        main_layout.addWidget(control_frame)
        
        control_layout = QVBoxLayout(control_frame)
        control_layout.setContentsMargins(15, 12, 15, 12)
        control_layout.setSpacing(10)
        
        # 顶部控制按钮行
        top_controls = QHBoxLayout()
        top_controls.setSpacing(8)
        
        # 文件夹选择按钮
        self.select_folder_btn = QPushButton("📁")
        self.select_folder_btn.setObjectName("iconButton")
        self.select_folder_btn.setToolTip("选择视频文件夹")
        self.select_folder_btn.setFixedSize(40, 40)
        self.select_folder_btn.clicked.connect(self.select_folder)
        top_controls.addWidget(self.select_folder_btn)
        
        # 播放控制按钮
        self.play_random_btn = QPushButton("▶")
        self.play_random_btn.setObjectName("playButton")
        self.play_random_btn.setToolTip("随机播放")
        self.play_random_btn.setFixedSize(40, 40)
        self.play_random_btn.clicked.connect(self.play_random_video)
        self.play_random_btn.setEnabled(False)
        top_controls.addWidget(self.play_random_btn)
        
        self.replay_btn = QPushButton("↻")
        self.replay_btn.setObjectName("iconButton")
        self.replay_btn.setToolTip("重播")
        self.replay_btn.setFixedSize(40, 40)
        self.replay_btn.clicked.connect(self.replay_video)
        self.replay_btn.setEnabled(False)
        top_controls.addWidget(self.replay_btn)
        
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setObjectName("iconButton")
        self.stop_btn.setToolTip("停止")
        self.stop_btn.setFixedSize(40, 40)
        self.stop_btn.clicked.connect(self.stop_video)
        self.stop_btn.setEnabled(False)
        top_controls.addWidget(self.stop_btn)
        
        self.reset_btn = QPushButton("↺")
        self.reset_btn.setObjectName("iconButton")
        self.reset_btn.setToolTip("重置记录")
        self.reset_btn.setFixedSize(40, 40)
        self.reset_btn.clicked.connect(self.reset_played_videos)
        top_controls.addWidget(self.reset_btn)
        
        # 列表切换按钮
        self.list_toggle_btn = QPushButton("📋")
        self.list_toggle_btn.setObjectName("iconButton")
        self.list_toggle_btn.setToolTip("显示/隐藏视频列表")
        self.list_toggle_btn.setFixedSize(40, 40)
        self.list_toggle_btn.clicked.connect(self.toggle_video_list)
        top_controls.addWidget(self.list_toggle_btn)
        
        # 显示答案复选框
        self.show_answer_cb = QCheckBox("显示答案")
        self.show_answer_cb.setObjectName("modernCheckBox")
        self.show_answer_cb.stateChanged.connect(self.update_answer_display)
        top_controls.addWidget(self.show_answer_cb)
        
        top_controls.addStretch()
        
        # 统计信息
        self.stats_label = QLabel("总数: 0 | 已播: 0 | 剩余: 0")
        self.stats_label.setObjectName("statsLabel")
        top_controls.addWidget(self.stats_label)
        
        control_layout.addLayout(top_controls)
        
        # 信息显示行
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        
        # 文件夹信息
        self.folder_label = QLabel("未选择文件夹")
        self.folder_label.setObjectName("infoLabel")
        info_layout.addWidget(self.folder_label)
        
        info_layout.addStretch()
        
        # 答案显示
        self.answer_label = QLabel()
        self.answer_label.setWordWrap(True)
        self.answer_label.setObjectName("answerLabel")
        self.answer_label.hide()
        info_layout.addWidget(self.answer_label)
        
        control_layout.addLayout(info_layout)
        
        # 创建主要内容区域
        content_widget = QWidget()
        main_layout.addWidget(content_widget)
        
        # 主要内容的水平布局
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        
        # 左侧视频容器
        video_container = QWidget()
        content_layout.addWidget(video_container)
        
        video_container_layout = QVBoxLayout(video_container)
        video_container_layout.setContentsMargins(0, 0, 0, 0)
        video_container_layout.setSpacing(10)
        
        # 添加控制面板到视频容器
        video_container_layout.addWidget(control_frame)
        
        # 视频播放区域
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 360)
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_widget.setAspectRatioMode(Qt.KeepAspectRatio)
        video_container_layout.addWidget(self.video_widget)
        
        # 底部进度条区域
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        video_container_layout.addWidget(progress_frame)
        
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.setContentsMargins(15, 8, 15, 8)
        progress_layout.setSpacing(10)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        progress_layout.addWidget(self.progress_bar)
        
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setFixedWidth(80)
        progress_layout.addWidget(self.time_label)
        
        # 右侧视频列表容器
        self.list_container = QWidget()
        self.list_container.setMaximumWidth(250)
        self.list_container.hide()  # 默认隐藏
        content_layout.addWidget(self.list_container)
        
        list_container_layout = QVBoxLayout(self.list_container)
        list_container_layout.setContentsMargins(0, 0, 0, 0)
        list_container_layout.setSpacing(5)
        
        # 列表标题栏 - 包含折叠按钮
        list_header = QFrame()
        list_header.setObjectName("listHeader")
        list_header.setFixedHeight(35)
        list_container_layout.addWidget(list_header)
        
        header_layout = QHBoxLayout(list_header)
        header_layout.setContentsMargins(8, 5, 8, 5)
        header_layout.setSpacing(8)
        
        # 列表标题
        list_title = QLabel("视频列表")
        list_title.setObjectName("listTitle")
        header_layout.addWidget(list_title)
        
        header_layout.addStretch()
        
        # 折叠按钮
        self.collapse_btn = QPushButton("◀")
        self.collapse_btn.setObjectName("collapseButton")
        self.collapse_btn.setFixedSize(24, 24)
        self.collapse_btn.setToolTip("隐藏视频列表")
        self.collapse_btn.clicked.connect(self.toggle_video_list)
        header_layout.addWidget(self.collapse_btn)
        
        # 视频列表
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("videoList")
        self.list_widget.itemDoubleClicked.connect(self.play_selected_video)
        list_container_layout.addWidget(self.list_widget)
        
        # 状态栏
        self.create_status_bar()
        
    def toggle_video_list(self):
        """切换视频列表的显示/隐藏状态"""
        if self.list_container.isVisible():
            # 隐藏列表
            self.list_container.hide()
            self.collapse_btn.setText("▶")
            self.collapse_btn.setToolTip("显示视频列表")
            self.list_toggle_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.6);
                    border: 1px solid rgba(200, 200, 200, 0.5);
                }
            """)
            self.list_toggle_btn.setToolTip("显示视频列表")
        else:
            # 显示列表
            self.list_container.show()
            self.collapse_btn.setText("◀")
            self.collapse_btn.setToolTip("隐藏视频列表")
            self.list_toggle_btn.setStyleSheet("")  # 恢复默认样式
            self.list_toggle_btn.setToolTip("隐藏视频列表")
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
    def setup_media_player(self):
        """设置媒体播放器"""
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        
        # 连接信号
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.errorOccurred.connect(self.handle_error)
        
        # 播放定时器
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.check_segment_end)
        
    def setup_styles(self):
        """设置样式表"""
        self.setStyleSheet(get_app_stylesheet())
        
    def setup_background(self):
        """设置背景图片"""
        try:
            bg_image_path = get_asset_path('bg.png')
            if os.path.exists(bg_image_path):
                self.bg_pixmap = QPixmap(bg_image_path)
                # 设置窗口背景
                palette = QPalette()
                palette.setBrush(QPalette.Window, QBrush(self.bg_pixmap))
                self.setPalette(palette)
                self.setAutoFillBackground(True)
        except Exception as e:
            print(f"背景图片加载失败: {e}")
            
    def resizeEvent(self, event):
        """窗口大小改变时调整背景"""
        try:
            if hasattr(self, 'bg_pixmap'):
                scaled_pixmap = self.bg_pixmap.scaled(
                    self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                )
                palette = QPalette()
                palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
                self.setPalette(palette)
        except Exception:
            pass
        super().resizeEvent(event)
        
    # === 事件处理方法 ===
    
    def select_folder(self):
        """选择视频文件夹"""
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择视频文件夹", "", 
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder_path:
            self.video_manager.current_folder = folder_path
            self.folder_label.setText(f"文件夹: {os.path.basename(folder_path)}")
            self.status_bar.showMessage("正在扫描视频文件...")
            
            # 启动扫描线程
            self.scanner = VideoScanner(folder_path)
            self.scanner.videos_found.connect(self.on_videos_found)
            self.scanner.progress_update.connect(self.status_bar.showMessage)
            self.scanner.start()
            
    def on_videos_found(self, video_files):
        """处理扫描到的视频文件"""
        self.video_manager.set_video_list(video_files)
        
        # 更新UI
        self.update_video_list()
        self.update_stats()
        self.play_random_btn.setEnabled(len(video_files) > 0)
        
        self.status_bar.showMessage(f"找到 {len(video_files)} 个视频文件")
        
        # 自动显示视频列表
        if len(video_files) > 0:
            self.list_container.show()
            self.collapse_btn.setText("◀")
            self.collapse_btn.setToolTip("隐藏视频列表")
            self.list_toggle_btn.setStyleSheet("")  # 恢复默认样式
            self.list_toggle_btn.setToolTip("隐藏视频列表")
        
    def play_random_video(self):
        """播放随机视频"""
        if not self.video_manager.has_unplayed_videos():
            QMessageBox.information(self, "提示", "所有视频都已播放过！\n请重置播放记录或选择新的文件夹。")
            return
            
        video_path = self.video_manager.get_random_unplayed_video()
        if video_path:
            self.play_video_segment(video_path)
            self.update_video_list()
            self.update_stats()
            self.update_answer_display()
            
    def play_selected_video(self, item: QListWidgetItem):
        """播放选中的视频"""
        video_path = item.data(Qt.UserRole)
        if video_path:
            self.video_manager.mark_as_played(video_path)
            self.update_video_list()
            self.update_stats()
            self.play_video_segment(video_path)
            self.update_answer_display()
            
    def play_video_segment(self, video_path: str):
        """播放视频片段"""
        if not video_path:
            return
            
        # 停止当前播放
        self.media_player.stop()
        
        # 设置新的媒体源
        url = QUrl.fromLocalFile(video_path)
        self.media_player.setSource(url)
        
        # 等待媒体加载完成后开始播放
        self.media_player.play()
        
        # 更新UI状态
        self.is_playing = True
        self.play_random_btn.setEnabled(False)
        self.replay_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        
        self.status_bar.showMessage(f"正在播放: {os.path.basename(video_path)}")
        
    def replay_video(self):
        """重新播放当前视频"""
        if self.video_manager.current_video_path:
            self.play_video_segment(self.video_manager.current_video_path)
            
    def stop_video(self):
        """停止播放"""
        self.media_player.stop()
        self.play_timer.stop()
        self.is_playing = False
        
        # 更新UI状态
        self.play_random_btn.setEnabled(len(self.video_manager.video_list) > 0)
        self.stop_btn.setEnabled(False)
        
        self.status_bar.showMessage("播放已停止")
        
    def reset_played_videos(self):
        """重置播放记录"""
        reply = QMessageBox.question(
            self, "确认重置", 
            "确定要重置播放记录吗？这将清除所有已播放视频的标记。",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.video_manager.reset_played_videos()
            self.update_video_list()
            self.update_stats()
            self.status_bar.showMessage("播放记录已重置")
            
    def update_answer_display(self):
        """更新答案显示"""
        if self.show_answer_cb.isChecked() and self.video_manager.current_video_path:
            filename = os.path.basename(self.video_manager.current_video_path)
            self.answer_label.setText(f"答案: {filename}")
            self.answer_label.show()
        else:
            self.answer_label.hide()
            
    def update_video_list(self):
        """更新视频列表显示"""
        self.list_widget.clear()
        
        for video_path in self.video_manager.video_list:
            item = QListWidgetItem()
            filename = os.path.basename(video_path)
            
            # 标记已播放的视频
            if video_path in self.video_manager.played_videos:
                item.setText(f"✓ {filename}")
                item.setForeground(QColor("#888"))
            else:
                item.setText(f"○ {filename}")
                item.setForeground(QColor("#000"))
                
            item.setData(Qt.UserRole, video_path)
            self.list_widget.addItem(item)
            
    def update_stats(self):
        """更新统计信息"""
        stats = self.video_manager.get_stats()
        self.stats_label.setText(f"总数: {stats['total']} | 已播: {stats['played']} | 剩余: {stats['remaining']}")
        
    # === 媒体播放相关方法 ===
    
    def media_status_changed(self, status):
        """媒体状态改变处理"""
        if status == QMediaPlayer.LoadedMedia:
            # 媒体加载完成，设置随机播放位置
            duration = self.media_player.duration()
            if duration > self.segment_duration:
                max_start = duration - self.segment_duration
                self.segment_start = random.randint(0, max_start)
                self.media_player.setPosition(self.segment_start)
            else:
                self.segment_start = 0
                self.segment_duration = duration
                
            # 启动播放定时器
            self.play_timer.start(100)  # 每100ms检查一次
            
    def update_position(self, position):
        """更新播放位置"""
        if self.media_player.duration() > 0:
            progress = (position / self.media_player.duration()) * 100
            self.progress_bar.setValue(int(progress))
            
            # 更新时间显示
            current_time = format_time(position)
            total_time = format_time(self.media_player.duration())
            self.time_label.setText(f"{current_time} / {total_time}")
            
    def update_duration(self, duration):
        """更新总时长"""
        self.progress_bar.setMaximum(100)
        
    def check_segment_end(self):
        """检查片段是否播放完毕"""
        if self.is_playing and self.media_player.position() >= (self.segment_start + self.segment_duration):
            self.stop_video()
            
    def handle_error(self, error):
        """处理播放错误"""
        error_messages = {
            QMediaPlayer.NoError: "无错误",
            QMediaPlayer.ResourceError: "资源错误",
            QMediaPlayer.FormatError: "格式错误",
            QMediaPlayer.NetworkError: "网络错误",
            QMediaPlayer.AccessDeniedError: "访问被拒绝"
        }
        
        message = error_messages.get(error, "未知错误")
        QMessageBox.warning(self, "播放错误", f"播放时发生错误: {message}")
        self.stop_video()
        
    def closeEvent(self, event):
        """关闭事件处理"""
        if self.media_player:
            self.media_player.stop()
        event.accept() 