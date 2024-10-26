# 本脚本用于麦课的安全教育自动刷课

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time

# 模板图片路径（替换为你的“下一页”按钮的图片文件路径）
template_path = 'temp.png'

# 读取模板图片并转换为灰度图
template = cv2.imread(template_path, 0)
w, h = template.shape[::-1]

# 每隔多少秒点击一次（根据网课的播放时间设置）
interval = 1  # 每隔60秒点击一次

while True:
    # 截取屏幕
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)

    # 将截图转换为灰度图
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 进行模板匹配
    res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9  # 匹配度阈值
    loc = np.where(res >= threshold)

    # 遍历匹配结果
    if len(loc[0]) > 0:
        for pt in zip(*loc[::-1]):
            # 计算中心点位置
            center_location = (pt[0] + w // 2, pt[1] + h // 2)
            # 移动并点击
            pyautogui.moveTo(center_location)
            pyautogui.click()
            print(f"点击了'下一页'按钮，位置：{center_location}")
            break
    else:
        print("未找到'下一页'按钮，继续查找...")
    
    # 等待指定的时间后再进行下一次操作
    time.sleep(interval)
