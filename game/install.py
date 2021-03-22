import subprocess
from tkinter import font

def INSTALL():

    # Installing PIL if not already installed.
    # PIL is an imaging library that is used here for loading of saved images.

    try:
        import PIL
    except ImportError:
        print("PIL module not installed. Installing now.")
        import sys
        subprocess.run((sys.executable, '-m', 'pip', 'install', 'pillow'))
    
        try:
            import PIL
        except:
            print("Could not install Pillow library automatically. Please install manually.")
            exit()

        print("Success.")

    # Installing font if not already installed.
    # LLPixel3 is the main font used throughout the game because of its pixelated look.
    
    if "LLPixel" not in font.families():
        print("Font not installed. Installing now.")
        import platform
        system = platform.system()
        if system == "Windows":
            subprocess.run(('copy', '/Y', 'assets/LLPixel3.ttf', '%WINDIR%/Fonts'))
        elif system == "Linux":
            subprocess.run(('cp', 'assets/LLPixel3.ttf', '/home/.fonts/'))
        elif system == "Darwin": # MacOS
            subprocess.run(('cp', 'assets/LLPixel3.ttf', '/Library/Fonts/'))
        
        if "LLPixel" not in font.families():
            print("Could not install assets/LLPixel3.ttf font automatically. Please install manually.")
            exit()
        
        print("Success.")