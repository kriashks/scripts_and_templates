## Description: Crawls throught inner folders to find all paths
import os
import platform
import glob
from pathlib import Path
import sys


def get_recent_files_windows():
    try:
        import win32com.client
    except ImportError:
        print("pywin32 is required on Windows. Install it using 'pip install pywin32'")
        return []

    recent_path = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Recent"
    shortcut_files = glob.glob(str(recent_path / "*.lnk"))

    shell = win32com.client.Dispatch("WScript.Shell")
    recent_files = []

    for shortcut in shortcut_files:
        try:
            shortcut_obj = shell.CreateShortCut(shortcut)
            target_path = shortcut_obj.Targetpath
            if target_path:
                recent_files.append(target_path)
        except Exception as e:
            print(f"Error processing shortcut {shortcut}: {e}")

    return recent_files


def get_recent_files_macos():
    # Placeholder for macOS recent files retrieval
    # Implement one of the approaches discussed above
    print("macOS recent files retrieval not implemented.")
    return []


def get_recent_files():
    current_os = platform.system()
    if current_os == "Windows":
        return get_recent_files_windows()
    elif current_os == "Darwin":
        return get_recent_files_macos()
    else:
        print(f"Unsupported OS: {current_os}")
        return []


if __name__ == "__main__":
    recent = get_recent_files()
    print("Recently Used Files:")
    for file in recent:
        print(file)
