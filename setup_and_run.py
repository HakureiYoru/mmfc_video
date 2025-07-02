#!/usr/bin/env python3
"""
MMFC-VIDEO 自动安装和启动脚本
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要 Python 3.8 或更高版本")
        print(f"当前版本: Python {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python版本检查通过: {sys.version.split()[0]}")

def install_package(package_name):
    """安装Python包"""
    try:
        print(f"📦 正在安装 {package_name}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True, check=True)
        print(f"✅ {package_name} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package_name} 安装失败: {e}")
        return False

def check_and_install_dependencies():
    """检查并安装依赖"""
    dependencies = [
        ("PySide6", "PySide6>=6.4.0"),
    ]
    
    missing_packages = []
    
    for package_name, pip_name in dependencies:
        try:
            spec = importlib.util.find_spec(package_name)
            if spec is None:
                missing_packages.append(pip_name)
            else:
                print(f"✅ {package_name} 已安装")
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print("\n🔧 需要安装以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        
        print("\n开始安装...")
        for package in missing_packages:
            if not install_package(package):
                print(f"❌ 无法安装 {package}，请手动安装")
                return False
    
    return True

def run_tests():
    """运行基本测试"""
    try:
        print("\n🧪 运行基本测试...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 测试通过")
        else:
            print("⚠️ 测试失败，但可以继续运行")
            
    except FileNotFoundError:
        # pytest不存在，使用unittest
        try:
            result = subprocess.run([
                sys.executable, "tests/test_basic.py"
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 基本测试通过")
        except Exception as e:
            print(f"⚠️ 测试跳过: {e}")

def run_mmfc_video():
    """运行MMFC-VIDEO"""
    try:
        print("\n🚀 启动 MMFC-VIDEO...")
        if os.path.exists("run_mmfc_video.py"):
            import subprocess
            subprocess.run([sys.executable, "run_mmfc_video.py"])
        else:
            print("❌ 找不到 run_mmfc_video.py 文件")
            return False
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🎬 MMFC-VIDEO - 自动安装和启动")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 检查并安装依赖
    if not check_and_install_dependencies():
        print("\n❌ 依赖安装失败，请手动安装后再运行")
        input("按回车键退出...")
        sys.exit(1)
    
    print("\n✅ 所有依赖已就绪!")
    
    # 运行测试
    run_tests()
    
    # 运行播放器
    if not run_mmfc_video():
        print("\n❌ 播放器启动失败")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，再见!")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")
        input("按回车键退出...") 