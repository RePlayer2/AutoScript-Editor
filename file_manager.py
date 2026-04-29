"""文件管理器 - 负责步骤文件的保存和加载"""
import json
import time
from typing import List
from step_module import StepModule


class FileManager:
    """文件管理器 - 处理步骤文件的读写操作"""
    
    @staticmethod
    def save_steps(steps: List[StepModule], filepath: str) -> bool:
        """
        保存步骤列表到文件
        
        Args:
            steps: 步骤列表
            filepath: 文件路径
        
        Returns:
            是否保存成功
        """
        try:
            data = {
                "version": "1.0",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "steps": [step.to_dict() for step in steps]
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存步骤失败: {e}")
            return False
    
    @staticmethod
    def load_steps(filepath: str) -> List[StepModule]:
        """
        从文件加载步骤列表
        
        Args:
            filepath: 文件路径
        
        Returns:
            步骤列表，如果加载失败返回空列表
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            steps = [StepModule.from_dict(s) for s in data.get("steps", [])]
            return steps
        except Exception as e:
            print(f"加载步骤失败: {e}")
            return []
    
    @staticmethod
    def save_recorded_sequence(sequence: List[dict], filepath: str) -> bool:
        """
        保存录制的操作序列到文件
        
        Args:
            sequence: 录制的序列列表
            filepath: 文件路径
        
        Returns:
            是否保存成功
        """
        try:
            data = {
                "type": "recorded_sequence",
                "version": "1.0",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "sequence": sequence
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存录制序列失败: {e}")
            return False
    
    @staticmethod
    def load_recorded_sequence(filepath: str) -> List[dict]:
        """
        从文件加载录制的操作序列
        
        Args:
            filepath: 文件路径
        
        Returns:
            录制序列列表，如果加载失败返回空列表
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data.get("sequence", [])
        except Exception as e:
            print(f"加载录制序列失败: {e}")
            return []