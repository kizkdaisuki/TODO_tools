"""语音播报模块"""
import os
import platform
import subprocess

def func_say(text: str):
    """语音播报
    
    使用系统命令进行语音播报，支持中文
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # 使用中文语音播报
        subprocess.run(['say', '-v', 'Ting-Ting', text])
    elif system == "Linux":
        # 使用 espeak 进行播报，可以指定中文
        subprocess.run(['espeak', '-v', 'zh', text])
    elif system == "Windows":
        # Windows 下使用 PowerShell 命令
        ps_script = f'Add-Type -AssemblyName System.Speech;$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;$speak.Speak("{text}")'
        subprocess.run(['powershell', '-Command', ps_script]) 