# -*- coding: utf-8 -*-
import PPTView
import PPTModel
import Tkinter as tk
import tkMessageBox as tm
import tkFileDialog
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class PPTController:

    def __init__(self):

        self.view = PPTView.PPTView(master=tk.Tk())
        self.model = PPTModel.PPTModel()
        self.view.link_button['command'] = self.link_nao
        self.view.ppt_selection_button['command'] = self.set_data
        self.view.ppt_selection1_button['command'] = self.set_img_data
        self.view.start_button['command'] = self.ppt_start
        self.view.previous_button['command'] = self.previous_ppt
        self.view.next_button['command'] = self.next_ppt
        self.view.speak_button['command'] = self.nao_speak
        self.view.quit_button['command'] = self.close_connection
        self.view.english_button['command'] = self.language_sete
        self.view.chinese_button['command'] = self.language_setc
        self.view.reduce_speech_button['command'] = self.speech_reduce
        self.view.increase_speech_button['command'] = self.speech_increase
        self.view.mainloop()

    def set_img_data(self):
        save_dir = tkFileDialog.askdirectory(title="文件儲存的資料夾")
        print(save_dir)
        if len(save_dir) <= 0:
            tm.showinfo(title='wrong', message='請選擇儲存的資料夾')
            pass
        else:
            self.model.set_img_data(save_dir)
            tm.showinfo(title='完成', message='PPT選擇完成')

    def set_data(self):
        default_dir = r"C:\Users"
        ppt_file = tkFileDialog.askopenfilename(title="選擇文件",
                                                initialdir=(os.path.expanduser(default_dir)))

        save_dir = tkFileDialog.askdirectory(title="儲存的資料夾")

        if len(ppt_file) <= 0 or len(save_dir) <= 0:
            tm.showinfo(title='wrong', message='請選擇文件及儲存的資料夾')
            pass
        else:
            self.model.set_data(ppt_file, save_dir)
            tm.showinfo(title='完成', message='PPT轉換完畢')

    def ppt_set(self):
        w_box = self.view.ppt_label.winfo_width()
        h_box = self.view.ppt_label.winfo_height()
        slides_text, tk_image = self.model.img_set(w_box, h_box)
        self.view.var.set(slides_text)
        self.view.page.set(self.model.now_page())
        self.view.ppt_label.config(image=tk_image)
        self.view.ppt_label.image = tk_image
        if int(self.view.text_label.winfo_width() / 13) >= 14:
            font_size = 14
        else:
            font_size = 10

        self.view.text_label.config(font=("Helvetica", font_size, 'bold'),
                                    wraplength=self.view.text_label.winfo_width() - 5)

    def ppt_start(self):
        if len(self.model.save_dir) == 0 or len(self.model.fname) == 0:
            tm.showinfo(title='wrong', message='請先選擇儲存的資料夾')
            pass
        else:
            self.model.ppt_start()
            self.ppt_set()

    def previous_ppt(self):
        if not self.model.folder_setting_completed():
            tm.showinfo(title='wrong', message='沒有投影片')
            pass
        elif self.model.get_ppt_number() == 0:
            tm.showinfo(title='wrong', message='沒有上一頁投影片')
            pass
        else:
            self.model.previous_ppt()
            self.ppt_set()

    def next_ppt(self):
        if not self.model.folder_setting_completed():
            tm.showinfo(title='wrong', message='沒有投影片')
            pass
        elif self.model.get_ppt_number() == self.model.get_ppt_len():
            tm.showinfo(title='wrong', message='已經是最後一頁投影片')
            pass
        else:
            self.model.next_ppt()
            self.ppt_set()

    def link_nao(self):
        ip = self.view.ip_text.get("1.0", "end-1c")
        if len(ip) <= 0:
            tm.showinfo(title='wrong', message='請輸入ip位址')
        else:
            link = self.model.link_nao(ip)
            self.view.link.set(link)

    def nao_speak(self):
        if not self.model.link_success():
            tm.showinfo(title='wrong', message='請連接機器人後才能說話')
        elif not self.model.ppt_is_ready():
            tm.showinfo(title='wrong', message='請設定PPT後才能說話')
        else:
            link = self.model.nao_speak()
            self.view.link.set(link)

    def close_connection(self):
        if not self.model.link_success():
            tm.showinfo(title='wrong', message='尚未連線機器人或已經關閉連線')
        else:
            link = self.model.close_connection()
            self.view.link.set(link)

    def language_setc(self):
        if not self.model.link_success():
            tm.showinfo(title='wrong', message='尚未連線機器人')
        else:
            self.model.nao_command('Chinese')

    def language_sete(self):
        if not self.model.link_success():
            tm.showinfo(title='wrong', message='尚未連線機器人')
        else:
            self.model.nao_command('English')

    def speech_increase(self):
        if not self.model.link_success():
            tm.showinfo(title='wrong', message='尚未連線機器人')
        else:
            self.model.nao_command('Increase')

    def speech_reduce(self):
        if not self.model.link_success():
            tm.showinfo(title='wrong', message='尚未連線機器人')
        else:
            self.model.nao_command('Reduce')


if __name__ == '__main__':
    app = PPTController()
