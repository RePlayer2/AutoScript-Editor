"""步骤模块类 - 定义各种自动化步骤类型"""
from typing import Dict, Any
import pyautogui
import time

# 模块类型常量
MODULE_TYPE_KEYBOARD_TYPE = "keyboard_type"
MODULE_TYPE_KEYBOARD_PRESS = "keyboard_press"
MODULE_TYPE_MOUSE_CLICK = "mouse_click"
MODULE_TYPE_MOUSE_MOVE = "mouse_move"
MODULE_TYPE_DELAY = "delay"
MODULE_TYPE_TEXT = "text_display"


class StepModule:
    """步骤模块类 - 表示一个自动化步骤"""
    
    def __init__(self, module_type: str, params: Dict[str, Any], description: str = ""):
        self.module_type = module_type
        self.params = params
        self.description = description or self._generate_description()
    
    def _generate_description(self) -> str:
        """生成模块描述"""
        if self.module_type == MODULE_TYPE_KEYBOARD_TYPE:
            return f"键盘输入: {self.params.get('text', '')}"
        elif self.module_type == MODULE_TYPE_KEYBOARD_PRESS:
            return f"按键: {self.params.get('key', '')}"
        elif self.module_type == MODULE_TYPE_MOUSE_CLICK:
            x = self.params.get('x', 0)
            y = self.params.get('y', 0)
            button = self.params.get('button', 'left')
            clicks = self.params.get('clicks', 1)
            return f"鼠标点击: ({x}, {y}) [{button}] x{clicks}"
        elif self.module_type == MODULE_TYPE_MOUSE_MOVE:
            x = self.params.get('x', 0)
            y = self.params.get('y', 0)
            return f"鼠标移动: ({x}, {y})"
        elif self.module_type == MODULE_TYPE_DELAY:
            return f"等待: {self.params.get('seconds', 0)}秒"
        elif self.module_type == MODULE_TYPE_TEXT:
            return f"显示文本: {self.params.get('text', '')}"
        return "未知模块"
    
    def to_dict(self) -> Dict:
        """转换为字典 - 用于序列化"""
        return {
            "module_type": self.module_type,
            "params": self.params,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StepModule':
        """从字典创建对象 - 用于反序列化"""
        return cls(
            module_type=data.get("module_type", ""),
            params=data.get("params", {}),
            description=data.get("description", "")
        )
    
    def execute(self):
        """执行步骤 - 根据类型执行不同操作"""
        module_type = self.module_type
        params = self.params
        
        if module_type == MODULE_TYPE_KEYBOARD_TYPE:
            pyautogui.typewrite(params.get('text', ''))
        
        elif module_type == MODULE_TYPE_KEYBOARD_PRESS:
            pyautogui.press(params.get('key', ''))
        
        elif module_type == MODULE_TYPE_MOUSE_CLICK:
            x = params.get('x', 0)
            y = params.get('y', 0)
            button = params.get('button', 'left')
            clicks = params.get('clicks', 1)
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
        
        elif module_type == MODULE_TYPE_MOUSE_MOVE:
            x = params.get('x', 0)
            y = params.get('y', 0)
            duration = params.get('duration', 0)
            if duration > 0:
                pyautogui.moveTo(x, y, duration=duration)
            else:
                pyautogui.moveTo(x, y)
        
        elif module_type == MODULE_TYPE_DELAY:
            time.sleep(params.get('seconds', 1))
        
        elif module_type == MODULE_TYPE_TEXT:
            pass  # 仅显示文本，不执行操作