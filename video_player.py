#!/usr/bin/env python3
import os
import random
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import cv2

# 支持的视频格式
VIDEO_FORMATS = ('.mp4', '.avi', '.mov')

class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频播放器")
        self.root.geometry("1000x500")  # 设置窗口尺寸
        self.root.minsize(600, 400)

        # 使布局在调整窗口大小时能够自适应
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

        self.video_list = []
        self.current_video_path = ""
        self.cap = None
        self.is_playing = False
        self.show_answer = tk.BooleanVar(value=False)

        # 加载背景图片并放置在根窗口底层
        bg_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img/bg.png')
        self.bg_image = Image.open(bg_image_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.resize_bg_image)
        # 右侧视频显示框架
        self.video_frame = ttk.Frame(self.root, style="MainFrame.TFrame")
        self.video_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        self.video_label = tk.Label(self.video_frame, relief="sunken", borderwidth=2, background="black")
        self.video_label.grid(row=0, column=0, sticky="nsew")

        # 进度条，放在视频显示标签下方
        self.progress = ttk.Progressbar(self.video_frame, orient="horizontal", mode="determinate", style="TProgressbar")
        self.progress.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        # 左侧控制框架
        self.main_frame = ttk.Frame(self.root, padding="10", style="MainFrame.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsw", padx=(10, 5), pady=10)


        # 在Windows系统上设置透明度
        self.main_frame.winfo_toplevel().attributes('-alpha', 0.95)

        # 配置框架响应式布局
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        # 添加标题标签
        self.title_label = ttk.Label(self.main_frame, text="视频播放器", anchor="center", style="Title.TLabel")
        self.title_label.grid(column=0, row=0, pady=10, sticky=tk.EW)  # 将columnspan=2去除，因为只有一列

        # 选择文件夹按钮
        self.select_folder_button = ttk.Button(self.main_frame, text="选择视频文件夹", command=self.select_folder,
                                               style="TButton")
        self.select_folder_button.grid(column=0, row=1, padx=5, pady=1, sticky=tk.EW)

        # 播放视频按钮
        self.play_video_button = ttk.Button(self.main_frame, text="随机播放视频片段", command=self.play_random_video,
                                            style="TButton")
        self.play_video_button.grid(column=0, row=2, padx=5, pady=1, sticky=tk.EW)

        # 重新播放按钮
        self.replay_video_button = ttk.Button(self.main_frame, text="重新播放", command=self.replay_video,
                                              style="TButton")
        self.replay_video_button.grid(column=0, row=3, padx=5, pady=1, sticky=tk.EW)

        # 显示路径标签
        self.path_label = ttk.Label(self.main_frame, text="未选择文件夹", anchor="w", style="TLabel")
        self.path_label.grid(column=0, row=4, padx=5, pady=3, sticky=tk.EW)

        # 在上方边缘添加“显示答案”的开关
        self.answer_button = ttk.Checkbutton(self.main_frame, text="显示答案", variable=self.show_answer, onvalue=True,
                                             offvalue=False, command=self.update_display)
        self.answer_button.grid(column=0, row=5, padx=5, pady=5, sticky=tk.EW)

        # 设置占位符，根据当前标签大小生成
        self.root.update_idletasks()
        placeholder_w = self.video_label.winfo_width() or 460
        placeholder_h = self.video_label.winfo_height() or 480
        self.placeholder_image = self.create_placeholder_image(placeholder_w, placeholder_h)
        self.video_label.config(image=self.placeholder_image)
        self.video_label.image = self.placeholder_image

        self.played_videos = set()  # 用来存储已播放视频的路径
        self.play_count_label = ttk.Label(self.main_frame, text="已随机播放视频数量: 0", style="TLabel")
        self.play_count_label.grid(column=0, row=6, padx=5, pady=5, sticky=tk.EW)

        # 添加重置按钮
        self.reset_button = ttk.Button(self.main_frame, text="重置播放记录", command=self.reset_played_videos,
                                       style="TButton")
        self.reset_button.grid(column=0, row=7, padx=5, pady=5, sticky=tk.EW)



        # 美化 UI
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10, background="#E3EFFF", foreground="black")
        self.style.map("TButton", background=[("active", "#C2DFFF")])
        self.style.configure("TLabel", font=("Helvetica", 12), background="#D7EAF4", foreground="black")
        self.style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), background="#D7EAF4", foreground="black")
        self.style.configure("MainFrame.TFrame", background="#D7EAF4")
        self.style.configure("TProgressbar", troughcolor="#555555", background="#007ACC")

        # 设置背景色和其他美化元素
        self.main_frame.configure(style="MainFrame.TFrame")
        self.root.configure(bg="#D7EAF4")


    def update_play_count(self):
        # 更新已播放视频数量的显示
        self.play_count_label.config(text=f"已随机播放视频数量: {len(self.played_videos)}")

    def reset_played_videos(self):
        # 重置已播放视频的记录
        self.played_videos.clear()
        self.update_play_count()
        print("已重置播放记录。")




    def update_display(self):
        # 更新显示内容，根据show_answer状态决定是否显示视频名称
        if self.show_answer.get() and self.current_video_path:
            self.path_label.config(text=f"{os.path.basename(self.current_video_path)}")
        else:
            self.path_label.config(text="未选择文件夹")

    def create_placeholder_image(self, width, height):
        image = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(image)
        text = "VIDEO"
        font_size = 40
        try:
            font = ImageFont.truetype("arial", font_size)
        except IOError:
            font = ImageFont.load_default()
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        draw.text(position, text, fill="white", font=font)
        return ImageTk.PhotoImage(image)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_name = os.path.basename(folder_path)
            self.path_label.config(text=folder_name)
            self.video_list = self.scan_videos(folder_path)
            print(f"选择的文件夹: {folder_path}")
            mp4_files = [file for file in self.video_list if file.endswith('.mp4')]
            if mp4_files:
                print("找到的.mp4视频文件:")
                # for file in mp4_files:
                #     print(file)  # 逐行打印每个.mp4文件的路径
            else:
                print("该文件夹中没有找到.mp4视频文件。")
        else:
            print("没有选择文件夹。")

    def scan_videos(self, folder_path):
        video_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(VIDEO_FORMATS):
                    video_files.append(os.path.join(root, file))
        return video_files


    def play_random_video(self):
        unplayed_videos = [video for video in self.video_list if video not in self.played_videos]
        if unplayed_videos:
            self.current_video_path = random.choice(unplayed_videos)
            self.played_videos.add(self.current_video_path)
            self.play_video_segment(self.current_video_path)
            self.update_display()  # 播放时更新显示
            self.update_play_count()
        else:
            print("所有视频都已播放过。")

    def replay_video(self):
        if self.current_video_path:
            print(f"重新播放视频: {self.current_video_path}")
            self.play_video_segment(self.current_video_path)
        else:
            print("没有视频可以重新播放。")

    def play_video_segment(self, video_path):
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(video_path)

        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps

        if duration >= 8:  # 确保视频至少有8秒长
            start_time = random.uniform(0, duration - 8)  # 随机选择开始时间，确保有足够的时间播放
            segment_duration = random.uniform(7, 8)  # 随机选择片段长度
        else:
            start_time = 0  # 如果视频不足8秒，从头开始播放
            segment_duration = duration  # 尽可能播放整个视频

        start_frame = int(start_time * fps)
        end_frame = int((start_time + segment_duration) * fps)

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        self.is_playing = True
        self.progress["maximum"] = end_frame - start_frame

        # 禁用按钮
        self.play_video_button.config(state='disabled')
        self.replay_video_button.config(state='disabled')

        self.update_progress_bar(0)
        self.play_segment_until_frame(end_frame, start_frame)

    def play_segment_until_frame(self, end_frame, start_frame):
        if self.cap.isOpened() and self.is_playing:
            ret, frame = self.cap.read()
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

            if ret and current_frame <= end_frame:
                # 获取帧率并计算帧间隔时间
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                frame_interval = 1 / fps  # 计算每帧的理论间隔时间



                label_width = self.video_label.winfo_width() or 460
                label_height = self.video_label.winfo_height() or 480
                frame = cv2.resize(frame, (label_width, label_height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                image_tk = ImageTk.PhotoImage(image)

                self.video_label.config(image=image_tk)
                self.video_label.image = image_tk  # 保持引用

                # 更新进度条
                self.update_progress_bar(current_frame - start_frame)

                # 继续播放下一帧，但添加适当的延时来控制播放速度
                self.root.after(int(frame_interval * 500),
                                lambda: self.play_segment_until_frame(end_frame, start_frame))
            else:
                self.finish_playing()
        else:
            self.finish_playing()

    def update_progress_bar(self, value):
        self.progress["value"] = value

    def resize_bg_image(self, event):
        # 获取新的宽度和高度
        new_width = event.width
        new_height = event.height

        # 调整图片大小，保持宽高比
        image = self.bg_image.resize((new_width, new_height), Image.LANCZOS)  # 使用Image.LANCZOS代替Image.ANTIALIAS
        self.bg_photo = ImageTk.PhotoImage(image)

        # 更新背景图片
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo  # 避免垃圾回收

        if not self.is_playing:
            placeholder_w = self.video_label.winfo_width() or 460
            placeholder_h = self.video_label.winfo_height() or 480
            self.placeholder_image = self.create_placeholder_image(placeholder_w, placeholder_h)
            self.video_label.config(image=self.placeholder_image)
            self.video_label.image = self.placeholder_image

    def finish_playing(self):
        if self.cap:
            self.cap.release()
        self.is_playing = False
        placeholder_w = self.video_label.winfo_width() or 460
        placeholder_h = self.video_label.winfo_height() or 480
        self.placeholder_image = self.create_placeholder_image(placeholder_w, placeholder_h)
        self.video_label.config(image=self.placeholder_image)
        self.video_label.image = self.placeholder_image

        # 启用按钮
        self.play_video_button.config(state='normal')
        self.replay_video_button.config(state='normal')


# 创建并运行Tkinter主循环
def main():
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
