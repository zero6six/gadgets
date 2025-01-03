import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog  
import requests
import time
import os
import io

class App:
    '''因为 xdoj 的网页写的实在是太烂了，所以自己拿 tkinter 写了个 GUI。'''
    URL = "http://47.92.139.74"
    session = requests.session()

    def __init__(self, root):
        self.root = root        # 初始化传入一个 tkinter 根窗口。
        self.root.title("XDOJ Helper")  
        self.root.geometry("1366x768+50+50")  
        self.root.resizable(width=False, height=False)  
  
        self.leftFrame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)  
        self.leftFrame.place(width=240, height=768)  
  
        self.rightUpFrame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)  
        self.rightUpFrame.place(x=240, width=1126, height=100)  
  
        self.rightDownFrame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)  
        self.rightDownFrame.place(x=240, y=100, width=1126, height=668)  
  
        self.var = tk.IntVar(value=1)
        self.contestId = 0           # 初始化以便于 treeview 控件传递变量
        self.problemId = 0
        self.submitId = 0
        self.create_radio_buttons()
        self.update_widgets()  
  
    def create_radio_buttons(self):  
        login = tk.Radiobutton(self.leftFrame, indicatoron=0, text="登录", variable=self.var, value=1, command=self.update_widgets)  
        login.pack()
        test = tk.Radiobutton(self.leftFrame, indicatoron=0, text="测试", variable=self.var, value=2, command=self.update_widgets)  
        test.pack()
        problem = tk.Radiobutton(self.leftFrame, indicatoron=0, text="题目", variable=self.var, value=3, command=self.update_widgets)  
        problem.pack()
        result = tk.Radiobutton(self.leftFrame, indicatoron=0, text="结果", variable=self.var, value=4, command=self.update_widgets)  
        result.pack()
  
    def update_widgets(self):
        def double_click_event(event):
            e = event.widget
            iid = e.identify("item", event.x, event.y)
            self.contestId = e.item(iid, "text")
            self.session.post(self.URL+'/xdoj-ssm/team/selectContest.do', data={'contestId': self.contestId})
            self.var.set(3)
            self.update_widgets()
        
        def tree_select_problemId(event):
            e = event.widget
            selection = e.selection()
            if selection:
                item_selected = selection[0]
                self.problemId = e.item(item_selected, "text")
            else:
                print("没有选中的项")
        
        def tree_select_submitId(event):
            e = event.widget
            item_selected = e.selection()[0]
            self.submitId = e.item(item_selected, "text")

        for widget in self.rightUpFrame.winfo_children():  
            widget.destroy()  
        for widget in self.rightDownFrame.winfo_children():  
            widget.destroy()  
  
        if self.var.get() == 1:  
            self.login_button = tk.Button(self.rightUpFrame, text="登录", command=self.login)  
            self.login_button.pack(side=tk.LEFT)  
            self.save_button = tk.Button(self.rightUpFrame, text="保存信息", command=self.save)  
            self.save_button.pack(side=tk.LEFT)  
            self.load_button = tk.Button(self.rightUpFrame, text="读取信息并登录", command=self.load_and_login)  
            self.load_button.pack(side=tk.LEFT)  
  
            self.user_label = tk.Label(self.rightDownFrame, text="用户名")  
            self.user_label.grid(row=0, column=0)  
            self.user_entry = tk.Entry(self.rightDownFrame)  
            self.user_entry.grid(row=0, column=1)  
            self.pw_label = tk.Label(self.rightDownFrame, text="密码")  
            self.pw_label.grid(row=1, column=0)  
            self.pw_entry = tk.Entry(self.rightDownFrame)  
            self.pw_entry.grid(row=1, column=1)  
        
        if self.var.get() == 2:
            self.page_left = tk.Button(self.rightUpFrame, text="<", command=lambda: self.set_contests_pages(int(self.page_entry.get())-1))
            self.page_left.pack(side='left')
            self.page_entry = tk.Entry(self.rightUpFrame)
            self.page_entry.insert(tk.END, "1")
            self.page_entry.pack(side='left')
            self.page_label = tk.Label(self.rightUpFrame, text="of 1")
            self.page_label.pack(side='left')
            self.page_right = tk.Button(self.rightUpFrame, text=">", command=lambda: self.set_contests_pages(int(self.page_entry.get())+1))
            self.page_right.pack(side='left')

            self.tree = ttk.Treeview(self.rightDownFrame, columns=('title', 'description', 'startTime', 'endTime'))
            self.tree.heading('#0', text='编号')
            self.tree.heading('#1', text='标题')
            self.tree.heading('#2', text='描述')
            self.tree.heading('#3', text='开始时间')
            self.tree.heading('#4', text='结束时间')
            self.tree.bind("<Double-1>", double_click_event)
            self.set_tree_contests(self.page_entry.get())
            self.tree.pack(side=tk.TOP)

        if self.var.get() == 3:
            self.page_left = tk.Button(self.rightUpFrame, text="<", command=lambda: self.set_problems_pages(int(self.page_entry.get())-1))
            self.page_left.pack(side='left')
            self.page_entry = tk.Entry(self.rightUpFrame)
            self.page_entry.insert(tk.END, "1")
            self.page_entry.pack(side='left')
            self.page_label = tk.Label(self.rightUpFrame, text="of 1")
            self.page_label.pack(side='left')
            self.page_right = tk.Button(self.rightUpFrame, text=">", command=lambda: self.set_problems_pages(int(self.page_entry.get())+1))
            self.page_right.pack(side='left')
            self.dl_button = tk.Button(self.rightUpFrame, text="下载", command=self.download_problem)
            self.dl_button.pack(side='left')
            self.ul_button = tk.Button(self.rightUpFrame, text="上传", command=self.upload)
            self.ul_button.pack(side='left')
            self.refresh_button = tk.Button(self.rightUpFrame, text="刷新", command=lambda: self.set_tree_problems(page=self.page_entry.get()))
            self.refresh_button.pack(side='left')

            self.tree = ttk.Treeview(self.rightDownFrame, columns=('isAccept', 'title', 'categoryName'))
            self.tree.heading('#0', text='编号')
            self.tree.heading('#1', text='完成情况')
            self.tree.heading('#2', text='标题')
            self.tree.heading('#3', text='题目类型')
            self.tree.bind("<<TreeviewSelect>>", tree_select_problemId)
            self.set_tree_problems(self.page_entry.get())
            self.tree.pack(side=tk.TOP)

            self.text = tk.Text(self.rightDownFrame, font=('微软雅黑', 10))
            self.text.pack(side=tk.BOTTOM)
            
        if self.var.get() == 4:
            self.dl_button = tk.Button(self.rightUpFrame, text="下载", command=self.download_submit)
            self.dl_button.pack(side='left')

            self.tree = ttk.Treeview(self.rightDownFrame, columns=('contestId', 'problemId', 'submitTime', 'judgememtText', 'points'))
            self.tree.heading('#0', text='提交编号')
            self.tree.heading('#1', text='考试编号')
            self.tree.heading('#2', text='题目编号')
            self.tree.heading('#3', text='提交时间')
            self.tree.heading('#4', text='评判结果')
            self.tree.heading('#5', text='成绩')
            self.set_tree_submits()
            self.tree.bind("<<TreeviewSelect>>", tree_select_submitId)
            self.tree.pack(side=tk.TOP)

    def login(self):  
        self.userId = self.user_entry.get()  
        password = self.pw_entry.get()

        data = {'userId': self.userId, 'password': password}
        self.session.post(self.URL+'/xdoj-ssm/user/login.do', data=data)
        self.var.set(2)
        self.update_widgets()

    def save(self):
        saveList = [self.user_entry.get(), self.pw_entry.get()]
        file = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Text files", "*.json"), ("All files", "*.*")],
        title="Save As"
        )
        with open(file, "w", encoding='utf-8') as f:
            json.dump(saveList, f, ensure_ascii=False, indent=4)

    def load_and_login(self):
        file_path = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Text files", "*.json"), ("All files", "*.*")],
        title="Open File"
        )

        if file_path:
            # 使用open函数打开文件并指定编码方式为UTF-8
            with open(file_path, "r", encoding="utf-8") as file:
                loadList = json.load(file)
            self.userId = loadList[0]
            data = {'userId': self.userId, 'password': loadList[1]}
            self.session.post(self.URL+'/xdoj-ssm/user/login.do', data=data)
            self.var.set(2)
            self.update_widgets()

    def set_tree_contests(self, page='1'):
        '''设置测试列表的 treeview 控件。'''
        self.tree.delete(*self.tree.get_children())
        t = int(round(time.time() * 1000))
        data = {'_search': 'false', 'nd':t, 'rows': '10', 'page': page, 'sidx':'', 'sord': 'asc'}
        response = self.session.post(self.URL+'/xdoj-ssm/contest/list.do', data=data).json()
        totalpages = response['totalpages']
        for i in response['data']:
            self.tree.insert("", index='end', text=i['id'], values=(i['title'], i['description'], i['startTime'], i['endTime']))
        self.page_label.config(text='of '+str(totalpages))

    def set_tree_problems(self, page='1'):
        '''设置题目列表的 treeview 控件。'''
        self.tree.delete(*self.tree.get_children())
        t = int(round(time.time() * 1000))
        params  = {'contestId': self.contestId, 'userId': self.userId, '_search': 'false', 'nd': t, 'rows': '10', 'page': page, 'sidx': '', 'sord': 'asc'}
        response = self.session.get(self.URL+'/xdoj-ssm/contest/problems.do', params=params).json()
        totalpages = response['totalpages']
        for i in response['data']:
            if i['userAcceptCount'] == 0:
                correct_sign = '×'
            else:
                correct_sign = '✓'
            self.tree.insert("", index='end', text=i['id'], values=(correct_sign, i['title'], i['categoryName']))
        self.page_label.config(text='of '+str(totalpages))

    def set_tree_submits(self, page='1'):
        self.tree.delete(*self.tree.get_children())
        t = int(round(time.time() * 1000))
        params  = {'contestId': self.contestId, 'userId': self.userId}
        data = {'_search': 'false', 'nd': t, 'rows': 10, 'page': page, 'sidx': '', 'sord': 'asc'}
        response = self.session.post(self.URL+'/xdoj-ssm/submission/results.do', params=params, data=data).json()
        for i in response['data']:
            self.tree.insert("", index='end', text=i['id'], values=(i['contestId'], i['problemId'], i['submitTime'], i['judgementText'], i['points']))

    def set_contests_pages(self, pages):
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(tk.END, str(pages))
        self.set_tree_contests(page=self.page_entry.get())

    def set_problems_pages(self, pages):
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(tk.END, str(pages))
        self.set_tree_problems(page=self.page_entry.get())

    def download_problem(self):
        '''保存至用户路径下的下载文件夹，如果下载文件夹移动了可能会产生预期外结果。'''
        response = self.session.get(self.URL+'/xdoj-ssm/problem/downloadTextFile.do', params={'problemId': self.problemId})  
        # 检查请求是否成功  
        if response.status_code == 200:  
            # 从 Content-Disposition 标头中获取文件名  
            content_disposition = response.headers.get('Content-Disposition')  
            if content_disposition:  
                filename = content_disposition.split('filename=')[-1].strip('"')
                file = os.path.join(os.environ.get('USERPROFILE'), 'Downloads', filename)
                # 打开一个文件并写入响应内容  
                with open(file, 'wb') as f:  
                    f.write(response.content)  
                print(f"文件 {filename} 已保存。")  
            else:  
                print("Content-Disposition 标头中未找到文件名。")  
        else:  
            print(f"请求失败，状态码: {response.status_code}")

    def upload(self):
        form_data = {'solutionType': '0', 'contestId': self.contestId, 'userId': self.userId, 'classId': '24CS200212', 'problemId': self.problemId, 'languageId': '1','sourceCode': ''}
        source_code_str = self.text.get("1.0", tk.END)
        # 将字符串转换为字节流，并创建一个类似文件的对象  
        file_like_object = io.BytesIO(source_code_str.encode('utf-8'))
        files = {'sourceFile': ('zero6six.c', file_like_object, 'application/octet-stream')}

        response = self.session.post(self.URL+'/xdoj-ssm/submission/submit.do', data=form_data, files=files) 
        print(response.status_code)
        print(response.text)

    def download_submit(self):
        '''保存至用户路径下的下载文件夹，如果下载文件夹移动了可能会产生预期外结果。'''
        response = self.session.get(self.URL+'/xdoj-ssm/submission/downloadCompile.do', params={'isSubmissionId': 'true', 'id': self.submitId})  
        # 检查请求是否成功  
        if response.status_code == 200:  
            # 从 Content-Disposition 标头中获取文件名  
            content_disposition = response.headers.get('Content-Disposition')  
            if content_disposition:  
                filename = content_disposition.split('filename=')[-1].strip('"')
                file = os.path.join(os.environ.get('USERPROFILE'), 'Downloads', filename)
                # 打开一个文件并写入响应内容  
                with open(file, 'wb') as f:  
                    f.write(response.content)  
                print(f"文件 {filename} 已保存。")  
            else:  
                print("Content-Disposition 标头中未找到文件名。")  
        else:  
            print(f"请求失败，状态码: {response.status_code}")

if __name__ == "__main__":
    root = tk.Tk() 
    app = App(root)
    root.mainloop()