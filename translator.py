import hashlib
import json
import random
import tkinter as tk
import requests
from PIL import ImageGrab
from io import BytesIO
import base64

with open(r'temp\API.json', "r", encoding="utf-8") as file:
    tokens = json.load(file)

def get_access_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={tokens['api_key']}&client_secret={tokens['secret_key']}"
    
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    token = json.loads(response.text)['access_token']
    return token

access_token = get_access_token()

def OCR():
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + access_token

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    # 将剪贴板图像 base64 编码
    bytesIO = BytesIO()                    # 初始化
    ImageGrab.grabclipboard().save(bytesIO, format="png")
    img = base64.b64encode(bytesIO.getvalue())

    params = {"image":img, "language_type": from_entry.get()}
    response = requests.request("POST", url, headers=headers, data=params)
    responseDict = json.loads(response.text)
    OCRText = '\n'.join(i['words'] for i in responseDict['words_result'])
    OCR_text.delete(1.0, tk.END)
    OCR_text.insert(tk.END, OCRText)

def translate():
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    q = OCR_text.get('1.0', tk.END)
    salt = str(random.randint(0,100))
    signText = tokens["appid"] + q + salt + tokens["key"]
    sign = hashlib.md5(signText.encode()).hexdigest()            # 计算字符串的 md5 值

    params = {'q':q, 'from':'auto', 'to':to_entry.get(), 'appid':tokens["appid"], 'salt': salt, 'sign': sign}
    
    response = requests.request("POST", url, headers=headers, data=params)
    responseDict = json.loads(response.text)
    translateText = '\n'.join(i['dst'] for i in responseDict['trans_result'])

    translation_text.delete(1.0, tk.END)
    translation_text.insert(tk.END, translateText)

# 创建一个窗口对象
root = tk.Tk()
# 设置窗口标题
root.title("OCR 翻译")
# 设置窗口大小
root.geometry("400x600") # 在屏幕左上角往右 250px，往下 350px 打开窗口
root.attributes('-topmost', 1) # 窗口置顶
root.resizable(width=False, height=False)

font = ('微软雅黑', 10)

OCR_text = tk.Text(root, font=font)
OCR_text.place(anchor="center", x=200, y=100, width=400, height=200)

translation_text = tk.Text(root, font=font)
translation_text.place(anchor="center", x=200, y=300, width=400, height=200)

entry_frame = tk.Frame(root)
entry_frame.place(anchor="center", x=200, y=425, width=400, height=50)
from_lable = tk.Label(entry_frame, text="源语言", font=font)
from_lable.grid(row=0, column=0)
from_entry = tk.Entry(entry_frame)
from_entry.grid(row=0, column=1)
from_entry.insert(tk.END, "auto_detect")
to_lable = tk.Label(entry_frame, text="目标语言", font=font)
to_lable.grid(row=0, column=2)
to_entry = tk.Entry(entry_frame)
to_entry.grid(row=0, column=3)
to_entry.insert(tk.END, "zh")
# to_entry.insert(tk.END, "cht")

OCR_button = tk.Button(text="OCR", fg="black", command=OCR)
OCR_button.place(anchor="center", x=100, y=525, width=200, height=150)

translation_button = tk.Button(text="翻译", fg="black", command=translate)
translation_button.place(anchor="center", x=300, y=525, width=200, height=150)

# 进入主循环
root.mainloop()