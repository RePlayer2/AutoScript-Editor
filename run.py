#!/usr/bin/env python3
"""步骤编辑器 - 主入口文件"""
import tkinter as tk
import pyautogui
import sys
import os

# 添加父目录到路径，以便导入同级模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_window import StepEditorApp


def main():
    """主函数 - 启动步骤编辑器"""
    # 配置 pyautogui
    pyautogui.FAILSAFE = True  # 启用安全模式，移动鼠标到左上角可中断执行
    pyautogui.PAUSE = 0.1  # 每次操作后的暂停时间

    # 创建主窗口
    root = tk.Tk()
    app = StepEditorApp(root)

    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    main()