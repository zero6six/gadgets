import wordninja
import pyperclip

# 本脚本供我将 OCR 识别出来的不带空格的英文段落还原

while True:
    try:
        line = input()
        pyperclip.copy(" ".join(wordninja.split(line)))
    except EOFError:
        break