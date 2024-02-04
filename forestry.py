import tkinter as tk
from tkinter import filedialog
from threading import Thread
from time import sleep
import queue
import pyautogui
import json

def threaded_function(log_queue):
    '''主要的逻辑代码'''
    loopCount = 1
    delay=0.1
    start = tuple(int(i) for i in bee_entry.get().split(",") if i) # if i 可以移除元组中的空元素
    points = []
    for point in points_text.get("1.0", tk.END).split("\n"):
        temp = tuple(int(i) for i in point.split(",") if i)
        if temp:
            points.append(temp)                                    # 但是 if i 移除不了空元祖 

    def my_click(point: tuple):
        '''
        传入点的元祖，移动并点击。\n
        pyautogui 的 click 方法加上坐标会造成前一步的物品拿在手上，无法使用。
        '''
        pyautogui.moveTo(point[0], point[1])
        sleep(delay)
        pyautogui.click()
        sleep(delay)

    def whether_lose(point: tuple) -> bool:
        '''传入点的元组并判定是否为“×”，传出 True 即为失败。'''
        pyautogui.moveTo(1, 1) # 鼠标复位以防止遮挡到“×”
        sleep(delay)
        pix = pyautogui.pixel(point[0], point[1])
        if pix == (255, 73, 64):
            return(True)
        else:
            return(False)
        
    while True:
        my_click(start)
        my_click(start)
        # 重复两次以重新放蜜蜂
        loseBool = False
        for i in range(len(points)):
            my_click(points[i])
            if i % 2 == 1:
                lose = whether_lose(points[i])
                if lose:
                    loseBool = True
                    break
        if loseBool:
            log_queue.put(f"第 {loopCount} 次操作 失败。\n")
        else:
            log_queue.put(f"第 {loopCount} 次操作 成功。\n")
        loopCount+=1

def save():
    saveList = [bee_entry.get(), points_text.get("1.0", tk.END)]
    file = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Text files", "*.json"), ("All files", "*.*")],
        title="Save As"
        )
    with open(file, "w", encoding='utf-8') as f:
        json.dump(saveList, f, ensure_ascii=False, indent=4)

def load():
    file_path = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Text files", "*.json"), ("All files", "*.*")],
        title="Open File"
    )

    if file_path:
        # 使用open函数打开文件并指定编码方式为UTF-8
        with open(file_path, "r", encoding="utf-8") as file:
            loadList = json.load(file)
        bee_entry.delete(0, tk.END)
        bee_entry.insert(tk.END, loadList[0])
        points_text.delete(1.0, tk.END)
        points_text.insert(tk.END, loadList[1])

def update_log(log_queue):
    try:
        while True:  # 尝试读取队列中的所有消息
            log_message = log_queue.get_nowait()  # 非阻塞读取队列
            log_text.insert(tk.END, log_message)  # 更新文本框
            log_text.see(tk.END)  # 滚动到文本框的底部
    except queue.Empty:
        pass  # 如果队列为空，什么也不做
    root.after(300, lambda: update_log(log_queue))  # 每300ms调用一次自身以检查新消息

def start_thread(log_queue):
    log_text.delete(1.0, tk.END)
    t = Thread(target=threaded_function, args=(log_queue,))
    t.daemon = True  # 设置为守护线程，确保它会在主程序退出时结束
    t.start()
    update_log(log_queue)  # 开始更新日志的循环

root = tk.Tk()
root.title("林业写字台自动化")
root.geometry("600x400")
root.attributes('-topmost', 1) # 窗口置顶
root.resizable(width=False, height=False)

def font(size):
    return(('微软雅黑', size))

log_text = tk.Text(root, font=font(10))
log_text.place(anchor="center", x=450, y=200, width=300, height=400)
log_text.insert(tk.END, "这个脚本用于林业写字台的自动化。请以管理员方式运行。\n右边的这个窗口为日志。\n"+
                "左边上面填入蜜蜂放置点的坐标（例：700,445）\n左边下面填要点击的点的坐标。"+
                "\n注意：坐标只需要给出x逗号y的形式。要点击的点的坐标在错误时为FF3333(255, 73, 64)的红色。\n"+
                "左边下面用于读取以前保存的坐标，右边则是加载以前的坐标。没有做停止的代码，要停止的话可以把鼠标往右上角移动，触及屏幕边界时 PyAutoGUI 会自动以报错形式停止。\n"+
                "启动时把蜜蜂先放进写字台，然后填完所有必要的信息再启动即可。")

entry_frame = tk.Frame(root)
entry_frame.place(width=300, height=50)
bee_lable = tk.Label(entry_frame, text="蜜蜂放置点", font=font(13))
bee_lable.grid(row=0, column=0)
bee_entry = tk.Entry(entry_frame)
bee_entry.grid(row=0, column=1)

points_text = tk.Text(root)
points_text.place(anchor="center", x=150, y=225, width=300, height=350)

load_button = tk.Button(root, text="读取", command=load)
load_button.place(anchor="center", x=50, y=350, width=100, height=100)
log_queue = queue.Queue()  # 创建一个队列用于线程间通信
start_button = tk.Button(root, text="开始", command=lambda: start_thread(log_queue))
start_button.place(anchor="center", x=150, y=350, width=100, height=100)
save_button = tk.Button(root, text="保存", command=save)
save_button.place(anchor="center", x=250, y=350, width=100, height=100)

root.mainloop()