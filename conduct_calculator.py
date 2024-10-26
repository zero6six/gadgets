import tkinter as tk

def compute():
    voltage = int(voltage_entry.get())
    amperage = int(amperage_entry.get())
    loss = int(loss_entry.get())
    distance = int(distance_entry.get())

    line1 = '在 GTCEu 中，一个小方块机器最大接收 2A 电流，每 A 电流都会损失线损 x 距离的电流。\n'
    line2 = '按照输入的数据计算：\n'
    line3 = f'线损最大时最大输出功率为 {(voltage-loss*distance)*amperage} eu/t\n'
    line4 = f'线损后单机器接收功率为 {(voltage-loss*distance)*2} eu/t\n'
    line5 = f'无线损时单机器最大接收 {voltage*2} eu/t。'
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, line1+line2+line3+line4+line5)

# 创建一个窗口对象
root = tk.Tk()

# 设置窗口标题
root.title("导线计算器")

# 设置窗口大小
root.geometry("300x440+250+100") # 在屏幕左上角往右 250px，往下 100px 打开窗口

root.resizable(width=False, height=False)

font1 = ('微软雅黑', 18)
font2 = ('微软雅黑', 12)

entry_frame = tk.Frame(root)
entry_frame.place(width=300, height=160)
voltage_lable = tk.Label(entry_frame, text="电压", font=font1)
voltage_lable.grid(row=0, column=0)
voltage_entry = tk.Entry(entry_frame)
voltage_entry.grid(row=0, column=1)

amperage_lable = tk.Label(entry_frame, text="电流", font=font1)
amperage_lable.grid(row=1, column=0)
amperage_entry = tk.Entry(entry_frame)
amperage_entry.grid(row=1, column=1)

loss_lable = tk.Label(entry_frame, text="线损", font=font1)
loss_lable.grid(row=2, column=0)
loss_entry = tk.Entry(entry_frame)
loss_entry.grid(row=2, column=1)

distance_lable = tk.Label(entry_frame, text="距离", font=font1)
distance_lable.grid(row=3, column=0)
distance_entry = tk.Entry(entry_frame)
distance_entry.grid(row=3, column=1)

btn = tk.Button(root, text="计算", font=font1, command=compute)
btn.place(anchor="center", x=150, y=195, width=300, height=70)

output_text=tk.Text(root, font=font2)
output_text.place(anchor="center", x=150, y=335, width=300, height=210)

# 进入主循环
root.mainloop()