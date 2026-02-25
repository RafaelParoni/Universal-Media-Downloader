import subprocess
with open("error.txt", "w") as f:
    subprocess.run(["d:/MyPrograms/UniversalMediaDownloader/.venv/Scripts/python.exe", "youtube_downloader.py"], stderr=f, stdout=f)
