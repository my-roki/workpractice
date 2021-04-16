import tkinter.ttk as ttk
from tkinter import * # __all__
from tkinter import filedialog


# 파일 추가
def add_file():
    files = filedialog.askopenfilenames(
        title="이미지 파일을 선택하세요", 
        filetypes=(("PNG파일", "*.png"), ("모든 파일", "*.*")),
        initialdir="C:/")  # 최초 탐색 경로

    for file in files:
        print(file)

# 파일 삭제
def delete_file():
    pass