"""主应用窗口 - 步骤编辑器的主界面"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import threading
import pyautogui
from step_module import StepModule, MODULE_TYPE_KEYBOARD_TYPE, MODULE_TYPE_KEYBOARD_PRESS, \
    MODULE_TYPE_MOUSE_CLICK, MODULE_TYPE_MOUSE_MOVE, MODULE_TYPE_DELAY
from custom_widgets import DraggableListbox
from file_manager import FileManager
from recorder import Recorder


class StepEditorApp:
    """步骤编辑器主应用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("自动化步骤编辑器")
        self.root.geometry("1050x850")
        self.root.minsize(1000, 800)
        
        # 状态变量
        self.steps = []
        self.capturing_coords = False
        
        # 初始化组件
        self.recorder = Recorder()
        self.recorder.set_log_callback(self.add_log)
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        """创建主界面组件"""
        # 创建Notebook（选项卡控件）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建选项卡
        self.tab_editor = ttk.Frame(self.notebook)
        self.tab_password = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_editor, text="📝 步骤编辑器")
        self.notebook.add(self.tab_password, text="🔐 密码测试")
        
        # 初始化编辑器选项卡
        self.init_editor_tab()
        # 初始化密码测试选项卡（保留为空）
        self.init_password_tab()
    
    def init_editor_tab(self):
        """初始化步骤编辑器选项卡"""
        # 顶部工具栏
        toolbar = tk.Frame(self.tab_editor, relief=tk.RAISED, bd=2)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # 模块类型选择
        tk.Label(toolbar, text="模块类型:").pack(side=tk.LEFT, padx=5)
        self.module_type_var = tk.StringVar(value=MODULE_TYPE_KEYBOARD_TYPE)
        module_types = [
            ("键盘输入", MODULE_TYPE_KEYBOARD_TYPE),
            ("按键Press", MODULE_TYPE_KEYBOARD_PRESS),
            ("鼠标点击", MODULE_TYPE_MOUSE_CLICK),
            ("鼠标移动", MODULE_TYPE_MOUSE_MOVE),
            ("延时", MODULE_TYPE_DELAY),
        ]
        
        for text, value in module_types:
            tk.Radiobutton(toolbar, text=text, variable=self.module_type_var, value=value).pack(side=tk.LEFT, padx=5)
        
        # 点击获取坐标按钮
        tk.Button(toolbar, text="🖱️ 点击获取坐标", command=self.start_capture_coords,
                 bg="#E67E22", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        
        # 参数输入区域
        params_frame = tk.LabelFrame(self.tab_editor, text="模块参数", padx=10, pady=10)
        params_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 第一行参数
        row1 = tk.Frame(params_frame)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(row1, text="文本:").pack(side=tk.LEFT)
        self.text_param = tk.Entry(row1, width=20)
        self.text_param.pack(side=tk.LEFT, padx=5)
        self.text_param.insert(0, "Hello")
        
        tk.Label(row1, text="按键:").pack(side=tk.LEFT, padx=(20, 0))
        self.key_param = tk.Entry(row1, width=15)
        self.key_param.pack(side=tk.LEFT, padx=5)
        self.key_param.insert(0, "enter")
        
        # 第二行参数
        row2 = tk.Frame(params_frame)
        row2.pack(fill=tk.X, pady=5)
        
        tk.Label(row2, text="X坐标:").pack(side=tk.LEFT)
        self.x_param = tk.Entry(row2, width=10)
        self.x_param.pack(side=tk.LEFT, padx=5)
        self.x_param.insert(0, "0")
        
        tk.Label(row2, text="Y坐标:").pack(side=tk.LEFT, padx=(20, 0))
        self.y_param = tk.Entry(row2, width=10)
        self.y_param.pack(side=tk.LEFT, padx=5)
        self.y_param.insert(0, "0")
        
        tk.Label(row2, text="延时(秒):").pack(side=tk.LEFT, padx=(20, 0))
        self.delay_param = tk.Entry(row2, width=10)
        self.delay_param.pack(side=tk.LEFT, padx=5)
        self.delay_param.insert(0, "1")
        
        # 第三行参数（鼠标按键）
        row3 = tk.Frame(params_frame)
        row3.pack(fill=tk.X, pady=5)
        
        tk.Label(row3, text="鼠标按键:").pack(side=tk.LEFT)
        self.mouse_button_var = tk.StringVar(value="left")
        tk.Radiobutton(row3, text="左键", variable=self.mouse_button_var, value="left").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(row3, text="右键", variable=self.mouse_button_var, value="right").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(row3, text="中键", variable=self.mouse_button_var, value="middle").pack(side=tk.LEFT, padx=5)
        
        tk.Label(row3, text="点击次数:").pack(side=tk.LEFT, padx=(20, 0))
        self.clicks_param = tk.Entry(row3, width=5)
        self.clicks_param.pack(side=tk.LEFT, padx=5)
        self.clicks_param.insert(0, "1")
        
        # 添加模块按钮
        btn_frame = tk.Frame(self.tab_editor)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="➕ 添加模块", command=self.add_step, 
                 bg="#2ECC71", fg="white", width=12).pack(side=tk.LEFT, padx=3)
        self.start_recording_btn = tk.Button(btn_frame, text="🎙️ 开始录制", command=self.start_recording,
                 bg="#9B59B6", fg="white", width=12)
        self.start_recording_btn.pack(side=tk.LEFT, padx=3)
        self.stop_recording_btn = tk.Button(btn_frame, text="⏹️ 停止录制", command=self.stop_recording,
                 bg="#F39C12", fg="white", width=12, state=tk.DISABLED)
        self.stop_recording_btn.pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="▶️ 执行步骤", command=self.execute_steps,
                 bg="#3498DB", fg="white", width=12).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="💾 保存录制", command=self.save_recorded_sequence,
                 bg="#16A085", fg="white", width=12).pack(side=tk.LEFT, padx=3)
        
        # 步骤列表区域
        list_frame = tk.LabelFrame(self.tab_editor, text="步骤列表 (可拖拽排序)", padx=5, pady=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建列表框和滚动条
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.step_listbox = DraggableListbox(list_container, height=15, font=("Consolas", 10),
                                            yscrollcommand=scrollbar.set)
        self.step_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.step_listbox.yview)
        
        # 设置拖拽回调
        self.step_listbox.set_reorder_callback(self.on_step_reordered)
        
        # 步骤操作按钮
        step_btn_frame = tk.Frame(list_frame)
        step_btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(step_btn_frame, text="⬆️ 上移", command=self.move_step_up,
                 width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(step_btn_frame, text="⬇️ 下移", command=self.move_step_down,
                 width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(step_btn_frame, text="✏️ 编辑", command=self.edit_step,
                 width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(step_btn_frame, text="🗑️ 删除", command=self.delete_step,
                 width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(step_btn_frame, text="🗑️ 清空全部", command=self.clear_all_steps,
                 width=10, bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=3)
        
        # 保存加载按钮
        file_btn_frame = tk.Frame(self.tab_editor)
        file_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(file_btn_frame, text="💾 保存步骤", command=self.save_steps,
                 bg="#27AE60", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(file_btn_frame, text="📂 加载步骤", command=self.load_steps,
                 bg="#2980B9", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(file_btn_frame, text="📁 导入录制", command=self.import_recorded_sequence,
                 bg="#8E44AD", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        
        # 日志区域
        log_frame = tk.LabelFrame(self.tab_editor, text="日志", padx=5, pady=5)
        log_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=5, font=("Consolas", 9))
        self.log_text.pack(fill=tk.X)
    
    def init_password_tab(self):
        """初始化密码测试选项卡"""
        pass
    
    # ==================== 日志功能 ====================
    def add_log(self, msg):
        """添加日志信息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        print(msg)
    
    # ==================== 坐标捕获功能 ====================
    def start_capture_coords(self):
        """开始捕获屏幕坐标"""
        self.capturing_coords = True
        self.add_log("🖱️ 开始捕获坐标...")
        self.add_log("提示: 点击屏幕任意位置获取坐标，3秒后生效")
        
        # 最小化窗口
        self.root.iconify()
        
        # 启动坐标捕获线程
        threading.Thread(target=self.capture_mouse_coords, daemon=True).start()
    
    def capture_mouse_coords(self):
        """捕获鼠标坐标"""
        import time
        time.sleep(3)
        
        try:
            # 获取当前鼠标位置
            x, y = pyautogui.position()
            
            # 恢复窗口
            self.root.after(0, self.root.deiconify)
            
            # 更新坐标输入框
            self.x_param.delete(0, tk.END)
            self.x_param.insert(0, str(x))
            self.y_param.delete(0, tk.END)
            self.y_param.insert(0, str(y))
            
            # 自动选中鼠标点击模块类型
            self.module_type_var.set(MODULE_TYPE_MOUSE_CLICK)
            
            self.add_log(f"✅ 捕获坐标成功: ({x}, {y})")
            
        except Exception as e:
            self.root.after(0, self.root.deiconify)
            self.add_log(f"❌ 捕获坐标失败: {e}")
        
        self.capturing_coords = False
    
    # ==================== 步骤管理功能 ====================
    def on_step_reordered(self, original_index, final_index):
        """步骤拖拽排序回调"""
        if original_index != final_index:
            step = self.steps.pop(original_index)
            self.steps.insert(final_index, step)
            self.update_step_list()
            self.step_listbox.selection_clear(0, tk.END)
            self.step_listbox.selection_set(final_index)
            self.add_log(f"🔄 步骤 {original_index+1} 已移动到 {final_index+1}")
    
    def add_step(self):
        """添加步骤"""
        module_type = self.module_type_var.get()
        params = {}
        
        if module_type == MODULE_TYPE_KEYBOARD_TYPE:
            params = {"text": self.text_param.get()}
        elif module_type == MODULE_TYPE_KEYBOARD_PRESS:
            params = {"key": self.key_param.get()}
        elif module_type == MODULE_TYPE_MOUSE_CLICK:
            params = {
                "x": int(self.x_param.get() or 0),
                "y": int(self.y_param.get() or 0),
                "button": self.mouse_button_var.get(),
                "clicks": int(self.clicks_param.get() or 1)
            }
        elif module_type == MODULE_TYPE_MOUSE_MOVE:
            params = {
                "x": int(self.x_param.get() or 0),
                "y": int(self.y_param.get() or 0)
            }
        elif module_type == MODULE_TYPE_DELAY:
            params = {"seconds": float(self.delay_param.get() or 1)}
        
        step = StepModule(module_type, params)
        self.steps.append(step)
        self.update_step_list()
        self.add_log(f"➕ 添加步骤: {step.description}")
    
    def update_step_list(self):
        """更新步骤列表显示"""
        self.step_listbox.delete(0, tk.END)
        for i, step in enumerate(self.steps, 1):
            self.step_listbox.insert(tk.END, f"{i}. {step.description}")
    
    def move_step_up(self):
        """上移步骤"""
        selection = self.step_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要移动的步骤")
            return
        if selection[0] == 0:
            messagebox.showinfo("提示", "该步骤已在最顶端")
            return
        
        idx = selection[0]
        self.steps[idx], self.steps[idx-1] = self.steps[idx-1], self.steps[idx]
        self.update_step_list()
        self.step_listbox.selection_clear(0, tk.END)
        self.step_listbox.selection_set(idx-1)
        self.add_log(f"⬆️ 上移步骤 {idx+1} -> {idx}")
    
    def move_step_down(self):
        """下移步骤"""
        selection = self.step_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要移动的步骤")
            return
        if selection[0] >= len(self.steps) - 1:
            messagebox.showinfo("提示", "该步骤已在最底端")
            return
        
        idx = selection[0]
        self.steps[idx], self.steps[idx+1] = self.steps[idx+1], self.steps[idx]
        self.update_step_list()
        self.step_listbox.selection_clear(0, tk.END)
        self.step_listbox.selection_set(idx+1)
        self.add_log(f"⬇️ 下移步骤 {idx+1} -> {idx+2}")
    
    def edit_step(self):
        """编辑选中的步骤"""
        selection = self.step_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要编辑的步骤")
            return
        
        idx = selection[0]
        step = self.steps[idx]
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑步骤")
        edit_window.geometry("450x350")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        tk.Label(edit_window, text="模块类型:").pack(pady=5)
        type_entry = tk.Entry(edit_window, width=40)
        type_entry.insert(0, step.module_type)
        type_entry.config(state='readonly')
        type_entry.pack(pady=5)
        
        tk.Label(edit_window, text="描述:").pack(pady=5)
        desc_entry = tk.Entry(edit_window, width=40)
        desc_entry.insert(0, step.description)
        desc_entry.pack(pady=5)
        
        tk.Label(edit_window, text="参数 (JSON格式):").pack(pady=5)
        params_text = tk.Text(edit_window, height=10, width=40)
        params_text.pack(pady=5)
        params_text.insert(tk.END, json.dumps(step.params, indent=2, ensure_ascii=False))
        
        def save_edit():
            import json
            try:
                new_params = json.loads(params_text.get("1.0", tk.END))
                new_desc = desc_entry.get()
                step.params = new_params
                step.description = new_desc if new_desc else step._generate_description()
                self.update_step_list()
                edit_window.destroy()
                self.add_log(f"✏️ 已更新步骤: {step.description}")
            except json.JSONDecodeError:
                messagebox.showerror("错误", "参数格式错误，请输入有效的JSON")
        
        tk.Button(edit_window, text="💾 保存", command=save_edit,
                 bg="#27AE60", fg="white", width=15).pack(pady=10)
    
    def delete_step(self):
        """删除选中的步骤"""
        selection = self.step_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的步骤")
            return
        
        idx = selection[0]
        removed = self.steps.pop(idx)
        self.update_step_list()
        self.add_log(f"🗑️ 删除步骤: {removed.description}")
    
    def clear_all_steps(self):
        """清空所有步骤"""
        if not self.steps:
            return
        
        if messagebox.askyesno("确认", "确定要清空所有步骤吗？"):
            self.steps = []
            self.update_step_list()
            self.add_log("🗑️ 已清空所有步骤")
    
    # ==================== 录制功能 ====================
    def start_recording(self):
        """开始录制"""
        self.start_recording_btn.config(state=tk.DISABLED)
        self.stop_recording_btn.config(state=tk.NORMAL)
        self.recorder.start_recording()
    
    def stop_recording(self):
        """停止录制"""
        self.start_recording_btn.config(state=tk.NORMAL)
        self.stop_recording_btn.config(state=tk.DISABLED)
        self.recorder.stop_recording()
    
    def save_recorded_sequence(self):
        """保存录制的序列"""
        sequence = self.recorder.get_sequence()
        if not sequence:
            messagebox.showwarning("警告", "没有录制的序列可保存")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            title="保存录制序列"
        )
        
        if filepath:
            if FileManager.save_recorded_sequence(sequence, filepath):
                self.add_log(f"💾 已保存录制到: {filepath}")
                messagebox.showinfo("成功", f"录制已保存到:\n{filepath}")
            else:
                messagebox.showerror("错误", "保存失败")
    
    def import_recorded_sequence(self):
        """导入录制的序列"""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            title="导入录制序列"
        )
        
        if filepath:
            sequence = FileManager.load_recorded_sequence(filepath)
            
            # 将录制的序列转换为步骤
            for item in sequence:
                module_type = item.get("type", "")
                params = item.get("params", {})
                
                if module_type == "keyboard_type":
                    step = StepModule(MODULE_TYPE_KEYBOARD_TYPE, params)
                elif module_type == "keyboard_press":
                    step = StepModule(MODULE_TYPE_KEYBOARD_PRESS, params)
                elif module_type == "mouse_click":
                    step = StepModule(MODULE_TYPE_MOUSE_CLICK, params)
                elif module_type == "mouse_move":
                    step = StepModule(MODULE_TYPE_MOUSE_MOVE, params)
                else:
                    continue
                
                self.steps.append(step)
            
            self.update_step_list()
            self.add_log(f"📁 已导入: {filepath}")
            self.add_log(f"共导入 {len(sequence)} 个步骤")
            messagebox.showinfo("成功", f"已导入 {len(sequence)} 个步骤")
    
    # ==================== 执行功能 ====================
    def execute_steps(self):
        """执行所有步骤"""
        if not self.steps:
            messagebox.showwarning("警告", "没有可执行的步骤")
            return
        
        self.add_log("▶️ 开始执行步骤...")
        self.add_log("请在3秒内切换到目标窗口")
        
        def run():
            import time
            time.sleep(3)
            for i, step in enumerate(self.steps, 1):
                try:
                    self.add_log(f"执行 {i}/{len(self.steps)}: {step.description}")
                    step.execute()
                    time.sleep(0.3)
                except Exception as e:
                    self.add_log(f"❌ 执行错误: {e}")
            
            self.add_log("✅ 执行完成")
        
        threading.Thread(target=run, daemon=True).start()
    
    # ==================== 文件操作功能 ====================
    def save_steps(self):
        """保存步骤到文件"""
        if not self.steps:
            messagebox.showwarning("警告", "没有步骤可保存")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            title="保存步骤文件"
        )
        
        if filepath:
            if FileManager.save_steps(self.steps, filepath):
                self.add_log(f"💾 已保存到: {filepath}")
                messagebox.showinfo("成功", f"步骤已保存到:\n{filepath}")
            else:
                messagebox.showerror("错误", "保存失败")
    
    def load_steps(self):
        """从文件加载步骤"""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            title="加载步骤文件"
        )
        
        if filepath:
            self.steps = FileManager.load_steps(filepath)
            self.update_step_list()
            self.add_log(f"📂 已加载: {filepath}")
            self.add_log(f"共加载 {len(self.steps)} 个步骤")
            messagebox.showinfo("成功", f"已加载 {len(self.steps)} 个步骤")