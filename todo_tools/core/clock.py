"""番茄钟模块"""
import time
import threading
import signal
import platform
from datetime import datetime
import subprocess
from rich.live import Live
from todo_tools.utils.table_utils import generate_timer_table, console
from todo_tools.models.task import Task
from todo_tools.utils.time_utils import func_return_time_form

class TomatoClock:
    def __init__(self, task_manager):
        self.running = False
        self.task = None
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.thread = None
        self.task_manager = task_manager
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        """处理 Ctrl+C 中断"""
        if not self.running:  # 已经停止了，不需要重复处理
            return
        
        self.running = False
        console.print("\n[yellow]任务已手动结束[/yellow]")
        self._notify("任务已手动结束")
        self._finish_task()

    def _notify(self, message: str):
        """发送系统通知"""
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.run(['osascript', '-e', f'display notification "{message}" with title "TODO"'])
            elif system == "Linux":
                subprocess.run(['notify-send', "TODO", message])
            elif system == "Windows":
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast("TODO", message, duration=3, threaded=True)
        except Exception:
            pass  # 忽略通知失败

    def start(self, task: Task, seconds: int):
        """启动番茄钟"""
        self.task = task
        self.total_seconds = seconds
        self.remaining_seconds = seconds
        self.running = True
        
        # 发送开始通知
        self._notify(f"开始任务：{task.name}")
        
        # 创建并启动计时线程
        self.thread = threading.Thread(target=self._run_timer)
        self.thread.start()

    def _run_timer(self):
        """运行计时器"""
        with Live(console=console, refresh_per_second=4, transient=True) as live:
            start_time = datetime.now()
            while self.running and self.remaining_seconds > 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                self.remaining_seconds = max(0, self.total_seconds - int(elapsed))
                
                table = generate_timer_table(
                    self.task,
                    self.remaining_seconds,
                    self.total_seconds
                )
                live.update(table)
                time.sleep(0.1)
            
            if self.remaining_seconds <= 0:
                # 在退出 Live 上下文之前显示最后一次完整的进度
                final_table = generate_timer_table(
                    self.task,
                    0,  # 剩余时间为0
                    self.total_seconds
                )
                live.update(final_table)
                time.sleep(0.5)  # 稍微暂停一下让用户看到100%
                
                # 清除计时器显示
                live.stop()
                console.clear()
                
                # 显示完成信息
                self._notify("任务完成！")
                console.print("\n[green]任务完成！[/green]")
                self._finish_task()

    def _finish_task(self):
        """完成任务的后续处理"""
        if not self.task:  # 防止重复调用
            return
        
        # 更新任务状态
        self.task.end_time = datetime.now().strftime('%H:%M:%S')
        self.task.status = "completed"  # 无论如何都标记为已完成
        self.task.task_len = func_return_time_form(self.total_seconds)
        
        # 获取满意度评分
        empty_inputs = 0  # 记录空输入次数
        while True:
            satisfaction = console.input("\n请为这个任务打分 (1-5): ")
            if not satisfaction.strip():  # 空输入
                empty_inputs += 1
                if empty_inputs >= 3:  # 连续三次空输入
                    self.task.satisfaction = 3  # 默认3分
                    break
                continue
            
            try:
                score = int(satisfaction)
                if 1 <= score <= 5:
                    self.task.satisfaction = score
                    break
                else:
                    console.print("[red]请输入1-5之间的数字[/red]")
                    empty_inputs = 0  # 重置空输入计数
            except ValueError:
                console.print("[red]请输入有效的数字[/red]")
                empty_inputs = 0  # 重置空输入计数
        
        # 获取任务总结
        empty_inputs = 0  # 重置空输入计数
        while True:
            summary = console.input("\n请简单总结一下这个任务: ")
            if not summary.strip():  # 空输入
                empty_inputs += 1
                if empty_inputs >= 3:  # 连续三次空输入
                    self.task.summary = ""  # 不填写总结
                    break
                continue
            else:
                self.task.summary = summary
                break
        
        # 保存任务状态
        self.task_manager.save_task(self.task)
        self.task = None  # 清除当前任务，防止重复处理 