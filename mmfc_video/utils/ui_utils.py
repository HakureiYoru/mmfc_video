"""
UI相关工具函数
"""

def format_time(ms: int) -> str:
    """
    格式化时间显示（毫秒转为分:秒格式）
    
    Args:
        ms: 毫秒数
        
    Returns:
        格式化的时间字符串 (MM:SS)
    """
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}" 