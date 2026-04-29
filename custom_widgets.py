"""自定义控件 - 可拖拽的列表框"""
import tkinter as tk


class DraggableListbox(tk.Listbox):
    """可拖拽排序的列表框控件"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.drag_data = {"index": None, "y": 0, "dragging": False, "original_index": None}
        self.callback = None
    
    def set_reorder_callback(self, callback):
        """设置重新排序回调函数"""
        self.callback = callback
    
    def on_click(self, event):
        """鼠标点击事件 - 记录初始位置"""
        if not self.drag_data["dragging"]:
            self.drag_data["index"] = self.nearest(event.y)
            self.drag_data["original_index"] = self.drag_data["index"]
            self.drag_data["y"] = event.y
    
    def on_drag(self, event):
        """鼠标拖拽事件 - 实时移动列表项"""
        index = self.nearest(event.y)
        if index != self.drag_data["index"] and index >= 0:
            self.drag_data["dragging"] = True
            # 获取当前选中的文本
            selection = self.get(self.drag_data["index"])
            # 删除原位置
            self.delete(self.drag_data["index"])
            # 插入新位置
            self.insert(index, selection)
            self.drag_data["index"] = index
    
    def on_release(self, event):
        """鼠标释放事件 - 完成拖拽并调用回调"""
        self.drag_data["dragging"] = False
        if self.callback and self.drag_data["original_index"] is not None and self.drag_data["index"] is not None:
            # 获取最终位置
            final_index = self.nearest(event.y)
            if final_index < 0:
                final_index = self.drag_data["index"]
            # 选中拖拽后的项目
            self.selection_clear(0, tk.END)
            self.selection_set(final_index)
            # 调用回调通知外部
            self.callback(self.drag_data["original_index"], final_index)
        # 重置拖拽数据
        self.drag_data = {"index": None, "y": 0, "dragging": False, "original_index": None}