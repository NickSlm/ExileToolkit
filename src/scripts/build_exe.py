import subprocess
import os

root_dir= os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
main_path = os.path.join(root_dir, "main.py")

pyinstaller_cmd = [
    "python", "-m", "PyInstaller",
    "--distpath", os.path.join(root_dir, "dist"),
    "--workpath", os.path.join(root_dir, "build"),
    "--specpath", os.path.join(root_dir, "specs"),
    "--add-data", os.path.join(root_dir, "config") + ":config",
    "--add-data", os.path.join(root_dir, "data") + ":data",
    "--add-data", os.path.join(root_dir, "assets") + ":assets",
    "--add-data", r"C:\Program Files\Tesseract-OCR\tessdata;tessdata",
    "--add-binary", r"C:\Program Files\Tesseract-OCR\tesseract.exe;.",
    "--noconfirm",
    "--windowed",
    main_path
]

subprocess.run(pyinstaller_cmd, shell=True)