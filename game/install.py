import sys
import subprocess
import tkinter

def INSTALL():
    if "PIL" not in sys.modules:
        print("PIL module not installed. Installing now.")
        p = subprocess.run(('pip3', 'install', 'pillow'))
        print(p.returncode)    

        print("Success.")
    
    if "LLPixel3" not in tkinter.font.families():
        print("Font not installed. Installing now.")
        import platform
        system = platform.system()
        if system == "Windows":
            import ctypes
            ctypes.windll.gdi32.AddFontResourceExA("assets/LLPixel3.ttf")    
        elif system == "Linux":
            subprocess.run(('cp', 'assets/LLPixel3.ttf', '/home/.fonts/'))
        elif system == "Darwin": # MacOS
            subprocess.run(('cp', 'assets/LLPixel3.ttf', '/Library/Fonts/'))
        
        if "LLPixel3" not in tkinter.font.families():
            print("Could not install assets/LLPixel3.ttf font automatically. Please install manually.")
            exit()
        
        print("Success.")