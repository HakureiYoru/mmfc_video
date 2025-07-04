# MMFC-VIDEO v2.0

基于 PySide6 (Qt6) 开发的现代化视频播放器，采用模块化架构设计，专注于随机播放视频片段。具有极简黑白透明风格的现代化界面和完善的项目结构。

## ✨ 新功能特性

### 🚀 技术升级
- **PySide6/Qt6** - 使用最新的Qt6框架，性能更强，界面更美观
- **原生视频播放** - 使用QMediaPlayer提供更好的视频播放体验
- **多线程处理** - 视频扫描使用独立线程，界面响应更流畅
- **现代化UI设计** - 渐变背景、圆角按钮、动画效果

### 🎮 功能增强
- **扩展格式支持** - 支持 `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.m4v`
- **视频列表管理** - 显示所有视频文件，支持双击播放
- **播放状态可视化** - 已播放视频带有✓标记和不同颜色
- **实时统计信息** - 显示总数、已播放、剩余视频数量
- **状态栏提示** - 实时显示当前操作状态
- **进度条和时间显示** - 更精确的播放进度控制

### 🎨 界面改进
- **深蓝紫色梦幻风格** - 仿游戏UI的渐变配色和发光效果
- **紧凑按钮设计** - 45x45px圆形按钮，最大化视频显示区域
- **半透明磨砂效果** - 所有组件都有透明质感，可透出背景
- **响应式布局** - 控制面板占比优化，视频区域最大化
- **发光进度条** - 多色渐变进度条，视觉效果炫酷
- **可折叠列表** - 视频列表默认收起，点击展开节省空间

## 📋 系统要求

- **操作系统**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python版本**: Python 3.8+
- **内存**: 建议 4GB 以上
- **显卡**: 支持硬件视频解码（推荐）

## 🗂️ 项目结构

```
mmfc_video/
├── assets/                # 静态资源
│   ├── bg.png             # 背景图片
│   └── myicon.ico         # 应用图标
├── mmfc_video/            # 主程序包
│   ├── __init__.py        # 包初始化
│   ├── main.py            # 程序入口
│   ├── ui/                # UI模块
│   │   ├── __init__.py
│   │   ├── player_window.py   # 主窗口
│   │   └── styles.py          # 样式定义
│   ├── logic/             # 业务逻辑模块
│   │   ├── __init__.py
│   │   └── video_manager.py   # 视频管理
│   └── utils/             # 工具模块
│       ├── __init__.py
│       ├── file_utils.py      # 文件工具
│       └── ui_utils.py        # UI工具
├── tests/                 # 测试模块
│   └── test_basic.py
├── run_mmfc_video.py      # 快速启动脚本
├── setup_and_run.py       # 自动安装和启动
├── mmfc_video.spec        # PyInstaller配置
└── requirements_modern.txt
```

## 🛠️ 安装和运行

### 方法一：自动安装和启动
```bash
python setup_and_run.py
```

### 方法二：手动安装
1. **安装依赖**
```bash
pip install -r requirements_modern.txt
```

2. **运行程序**
```bash
python run_mmfc_video.py
```

### 方法三：Windows快速启动
```cmd
run_modern_player.bat
```

### 方法四：打包为可执行文件
```bash
pip install pyinstaller
pyinstaller mmfc_video.spec
```

生成的可执行文件位于 `dist/MMFC-VIDEO.exe`

## 🎯 使用指南

### 基本操作流程

1. **📁 选择文件夹** - 点击"选择视频文件夹"按钮
2. **⏳ 等待扫描** - 程序会自动扫描文件夹中的所有视频文件
3. **🎲 随机播放** - 点击"随机播放片段"开始观看
4. **✅ 显示答案** - 勾选"显示答案"查看当前视频文件名
5. **🔄 重置记录** - 需要时点击"重置播放记录"

### 高级功能

- **📝 视频列表** - 双击列表中的任意视频直接播放
- **⏹️ 播放控制** - 随时停止或重新播放当前片段
- **📊 统计信息** - 实时查看播放进度和剩余视频数量

## 🔧 技术架构

### 模块化设计
- **ui** - 用户界面模块
  - `player_window.py` - 主窗口和所有UI组件
  - `styles.py` - CSS样式定义
- **logic** - 业务逻辑模块
  - `video_manager.py` - 视频扫描、播放管理
- **utils** - 工具函数模块
  - `file_utils.py` - 文件操作和资源管理
  - `ui_utils.py` - UI相关工具函数

### 核心组件
- **QMainWindow** - 主窗口框架
- **QMediaPlayer** - 原生视频播放引擎
- **QVideoWidget** - 硬件加速视频显示
- **QThread** - 异步文件扫描
- **VideoManager** - 播放记录和状态管理

### 设计模式
- **模块化架构** - 清晰的职责分离
- **观察者模式** - Qt信号槽机制
- **单例模式** - 视频管理器
- **工厂模式** - 组件创建

## 🚀 v2.0 重构亮点

### 📂 项目结构优化
- **模块化设计** - 代码按功能分离到不同模块，职责清晰
- **包管理** - 使用Python包结构，便于维护和扩展
- **资源统一** - assets目录集中管理静态资源
- **测试完善** - 独立的测试模块保证代码质量

### 💻 代码质量提升
- **类型注解** - 完整的类型提示提高代码可读性
- **文档完善** - 详细的docstring和注释
- **错误处理** - 更完善的异常捕获和用户提示
- **性能优化** - 异步文件扫描，UI响应更流畅

### 🎨 UI/UX 升级
- **极简设计** - 黑白透明风格，突出视频内容
- **紧凑布局** - 按钮最小化，视频区域最大化
- **智能交互** - 可折叠列表，工具提示等
- **响应式** - 自适应窗口大小调整

## 🆚 与原版本对比

| 特性 | 原版本 (Tkinter) | 现代版本 (PySide6) |
|------|------------------|-------------------|
| 界面框架 | Tkinter | PySide6/Qt6 |
| 视频播放 | OpenCV + PIL | QMediaPlayer |
| 界面美观度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 性能表现 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 功能丰富度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 跨平台支持 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 代码可维护性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🔮 未来规划

- [ ] **全屏播放模式** - 支持全屏观看
- [ ] **播放列表管理** - 创建和管理自定义播放列表
- [ ] **音量控制** - 添加音量调节功能
- [ ] **快捷键支持** - 键盘快捷键操作
- [ ] **主题切换** - 多种界面主题选择
- [ ] **云端同步** - 播放记录云端同步
- [ ] **AI推荐** - 基于观看历史的智能推荐

## 🐛 问题排查

### 常见问题

1. **模块导入错误**
   - 确保在项目根目录运行脚本
   - 检查Python路径设置
   - 使用 `python run_mmfc_video.py` 启动

2. **视频无法播放**
   - 确认视频格式被支持（现支持8种格式）
   - 检查文件路径是否包含特殊字符
   - 尝试更新系统的视频解码器

3. **界面显示异常**
   - 确认PySide6版本>=6.4.0
   - 检查系统字体设置
   - 尝试调整系统显示缩放

4. **扫描速度慢**
   - 大文件夹扫描使用独立线程，不会卡界面
   - 扫描进度会在状态栏显示
   - 考虑将视频文件分类到不同文件夹

### 测试和调试
```bash
# 运行基本测试
python tests/test_basic.py

# 自动安装依赖并启动
python setup_and_run.py
```

## 📄 许可证

本项目使用 MIT 许可证，详见 LICENSE 文件。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

---

**享受观看！** 🎬✨ 