# -*- coding: utf-8 -*-
import Tkinter as tk


class PPTView(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.root = master
        self.var = tk.StringVar()
        self.page = tk.StringVar()
        self.link = tk.StringVar()
        self.root.title("PPT播放工具")
        self.root.geometry("1280x960")
        self.root.minsize(1024, 768)

        self.init_gui()

    def init_gui(self):
        self.link.set('尚未連線')
        self.pack(fill='both', expand=1)
        self.ip_text = tk.Text(self)
        self.ip_text.place(relx=0.85, relheight=0.05, relwidth=0.15)

        self.link_button = tk.Button(self, text='Link robot')
        self.link_button.place(relx=0.85, rely=0.05, relheight=0.03, relwidth=0.15)

        self.link_label = tk.Label(self, textvariable=self.link, bg='LightCyan')
        self.link_label.place(relx=0.85, rely=0.08, relheight=0.05, relwidth=0.15)

        self.ppt_selection_button = tk.Button(self, text="轉換PPT")
        self.ppt_selection_button.place(relx=0.85, rely=0.13, relheight=0.05, relwidth=0.075)

        self.ppt_selection1_button = tk.Button(self, text="選擇PPT資料夾")
        self.ppt_selection1_button.place(relx=0.925, rely=0.13, relheight=0.05, relwidth=0.075)

        self.start_button = tk.Button(self, text="Start")
        self.start_button.place(relx=0.85, rely=0.18, relheight=0.04, relwidth=0.15)

        self.previous_button = tk.Button(self, text="Previous slide")
        self.previous_button.place(relx=0.85, rely=0.22, relheight=0.04, relwidth=0.075)

        self.next_button = tk.Button(self, text="Next slide")
        self.next_button.place(relx=0.925, rely=0.22, relheight=0.04, relwidth=0.075)

        self.speak_button = tk.Button(self, text="Speak")
        self.speak_button.place(relx=0.85, rely=0.26, relheight=0.04, relwidth=0.15)

        self.quit_button = tk.Button(self, text="Quit PPT Mode")
        self.quit_button.place(relx=0.85, rely=0.30, relheight=0.04, relwidth=0.15)

        self.chinese_button = tk.Button(self, text="中文")
        self.chinese_button.place(relx=0.925, rely=0.34, relheight=0.04, relwidth=0.075)

        self.english_button = tk.Button(self, text="English")
        self.english_button.place(relx=0.85, rely=0.34, relheight=0.04, relwidth=0.075)

        self.increase_speech_button = tk.Button(self, text="語速增加")
        self.increase_speech_button.place(relx=0.925, rely=0.38, relheight=0.04, relwidth=0.075)

        self.reduce_speech_button = tk.Button(self, text="語速減少")
        self.reduce_speech_button.place(relx=0.85, rely=0.38, relheight=0.04, relwidth=0.075)

        self.ppt_label = tk.Label(self, bg='white')
        self.ppt_label.place(relheight=1, relwidth=0.85)

        self.text_label = tk.Label(self, textvariable=self.var, bg='gray',
                                   wraplength=150, anchor='nw', justify='left')
        self.text_label.place(relx=0.85, rely=0.42, relheight=0.52, relwidth=0.15)

        self.page_label = tk.Label(self, textvariable=self.page, bg='white',
                                   wraplength=150, anchor='nw', justify='left')
        self.page_label.place(relx=0.85, rely=0.94, relheight=0.06, relwidth=0.15)


if __name__ == '__main__':
    root = tk.Tk()
    app = PPTView(master=root)
    root.mainloop()
