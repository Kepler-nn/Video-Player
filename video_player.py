import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Video_player:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('Video player')
		self.root.geometry('720x640')
		self.root.resizable(False, False)

		self.var = tk.DoubleVar()

		self.label = tk.Label(self.root, width=715, height=500)
		self.label.place(x=0, y=40)

		self.label_fps_text = tk.Label(self.root, text='FPS:')
		self.label_fps_text.place(x=100, y=610)

		self.label_fps = tk.Label(self.root, text='')
		self.label_fps.place(x=130, y=610)

		self.label_time_vid = tk.Label(self.root, text='Длина видео:')
		self.label_time_vid.place(x=440, y=610)

		self.label_time_text = tk.Label(self.root, text='')
		self.label_time_text.place(x=530, y=610)

		open_video = tk.Button(self.root, text='Открыть файл', command=self.open_file)
		open_video.place(x=5, y=5)

		self.pause_play = tk.Button(self.root, text='Пауза', command=self.toggle_play)
		self.pause_play.place(x=330, y=610)

		self.scale = tk.Scale(self.root, variable=self.var, orient=tk.HORIZONTAL, from_=0, to=100, length=710, command=self.scale_vid_remove)
		self.scale.place(x=3, y=560)

		self.back = tk.Button(self.root, text='Назад', command=self.back_vid)
		self.back.place(x=280, y=610)

		self.forward = tk.Button(self.root, text='Вперед', command=self.forward_vid)
		self.forward.place(x=380, y=610)

		self.root.mainloop()

	def open_file(self):
		if hasattr(self, 'vid'):
			self.vid.release()

		filepath = filedialog.askopenfilename(filetypes=[('Video files', ('*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv'))])
		if filepath:
			self.vid = cv2.VideoCapture(filepath)
			count_frame = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
			seconds = count_frame % 60
			minutes = count_frame // 1500
			self.result = f'{minutes}:{seconds}'
			self.label_time_text.config(text=self.result)
			self.scale.config(to=count_frame, from_=0)
			self.update_frame()

	def toggle_play(self):
		    if self.pause_play['text'] == 'Пауза':
		        self.pause_play['text'] = 'Воспроизвести'
		        self.pause = True
		    else:
		        self.pause_play.config(text='Пауза')
		        self.pause = False

	def update_frame(self):
		if self.pause_play['text'] == 'Пауза':
			ret, frame = self.vid.read()
		else:
			self.root.after(5, self.update_frame)
			return
		if ret:
			if self.pause_play['text'] == 'Пауза':
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				resized_down = cv2.resize(frame, (715, 500))
				fps = int(self.vid.get(cv2.CAP_PROP_FPS))
				self.label_fps.config(text=fps)
				self.img = ImageTk.PhotoImage(image=Image.fromarray(resized_down))
				self.label.img = self.img
				self.label.config(image=self.img)
				# Над этой частью нужно еще поработать. Увеличение ползунка работает, но видео начинает очень сильно зависать
				# -------------------------------------
				# frame_number = self.scale.get()+1
				# self.scale.set(frame_number)
				# -------------------------------------
				self.root.after(5, self.update_frame)
		else:
			self.vid.release()

	# Перемотка при помощи ползунка работает исправно, но он не увеличивается
	def scale_vid_remove(self, val):
		frame_num = int(self.var.get())
		self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

	# Перемотка при помощи кнопок работает исправно
	def back_vid(self):
		current_time = self.vid.get(cv2.CAP_PROP_POS_MSEC)
		pos = self.vid.set(cv2.CAP_PROP_POS_MSEC, current_time-10000)

	def forward_vid(self):
		current_time = self.vid.get(cv2.CAP_PROP_POS_MSEC)
		pos = self.vid.set(cv2.CAP_PROP_POS_MSEC, current_time+10000)

Video_player()