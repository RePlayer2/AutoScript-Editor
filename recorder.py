"""录制管理器 - 负责键盘和鼠标操作的录制"""
import time
from typing import List, Dict
from pynput import keyboard, mouse


class Recorder:
    """录制管理器 - 监听并记录用户的键盘和鼠标操作"""
    
    def __init__(self):
        self.recording = False
        self.recorded_sequence: List[Dict] = []
        self.keyboard_listener = None
        self.mouse_listener = None
        self.log_callback = None
    
    def set_log_callback(self, callback):
        """设置日志回调函数"""
        self.log_callback = callback
    
    def add_log(self, msg):
        """添加日志"""
        if self.log_callback:
            self.log_callback(msg)
        print(msg)
    
    def start_recording(self):
        """开始录制"""
        if self.recording:
            return
        
        self.recording = True
        self.recorded_sequence = []
        
        self.add_log("🎙️ 开始录制...")
        self.add_log("提示: 按 ESC 键停止录制")
        
        # 启动键盘监听器
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=None
        )
        self.keyboard_listener.start()
        
        # 启动鼠标监听器
        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click,
            on_move=None,
            on_scroll=None
        )
        self.mouse_listener.start()
    
    def stop_recording(self):
        """停止录制"""
        if not self.recording:
            return
        
        self.recording = False
        
        # 停止监听器
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        
        self.add_log(f"⏹️ 停止录制，共录制 {len(self.recorded_sequence)} 个操作")
        
        return self.recorded_sequence
    
    def on_key_press(self, key):
        """键盘按键事件处理"""
        if key == keyboard.Key.esc:
            # ESC键停止录制
            self.stop_recording()
            return False
        
        try:
            if hasattr(key, 'char') and key.char:
                # 普通字符输入
                self.recorded_sequence.append({
                    "type": "keyboard_type",
                    "params": {"text": key.char},
                    "timestamp": time.time()
                })
                self.add_log(f"录制键盘输入: {key.char}")
            else:
                # 特殊按键
                key_name = str(key).replace('Key.', '')
                self.recorded_sequence.append({
                    "type": "keyboard_press",
                    "params": {"key": key_name},
                    "timestamp": time.time()
                })
                self.add_log(f"录制按键: {key_name}")
        except Exception as e:
            self.add_log(f"录制键盘错误: {e}")
    
    def on_mouse_click(self, x, y, button, pressed):
        """鼠标点击事件处理"""
        if pressed:  # 只记录按下事件
            button_name = str(button).replace('Button.', '')
            self.recorded_sequence.append({
                "type": "mouse_click",
                "params": {"x": x, "y": y, "button": button_name, "clicks": 1},
                "timestamp": time.time()
            })
            self.add_log(f"录制鼠标点击: ({x}, {y}) [{button_name}]")
    
    def get_sequence(self):
        """获取录制的序列"""
        return self.recorded_sequence
    
    def clear_sequence(self):
        """清空录制序列"""
        self.recorded_sequence = []