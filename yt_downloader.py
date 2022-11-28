import tkinter
import time
import tkinter.messagebox
import customtkinter
import re
from threading import Thread
from pytube import YouTube
from pytube import Playlist

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

ORGANIZATION = "79aim"
APP_NAME = "YT Downloader"
INFO = "Download your playlist/ music with just a few steps: \n 1. Obtain the URL of your playlist or music. \n 2. Select your output folder. \n 3. Press 'Download' button. "

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 300

    def __init__(self):
        super().__init__()

        
        self.youtube_link = tkinter.StringVar()
        self.download_location = tkinter.StringVar()

        self.title(ORGANIZATION + " " + APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text=ORGANIZATION,
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=5, padx=10)

        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text=APP_NAME,
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_2.grid(row=2, column=0, pady=10, padx=10)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=4, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=INFO,
                                                   height=100,
                                                   corner_radius=6,
                                                   fg_color=("white", "gray38"),
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.entry = customtkinter.CTkEntry(master=self.frame_info,
                                            textvariable=self.youtube_link,
                                            width=120,
                                            placeholder_text="YouTube Link")
        self.entry.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)


        # ============ frame_right ============

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            textvariable=self.download_location,
                                            width=120,
                                            placeholder_text="Download location")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Download",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")

    def yt_download(self):
        self.label_info_1.configure(text = "Downloading...")
        destination = str(self.download_location.get()) or '.'
        time.sleep(1)
        
        # try:

        if self.youtube_link.get().find("playlist"):
            youtube_playlist = Playlist(self.youtube_link.get())
            youtube_playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            for index, url in enumerate(youtube_playlist.videos):
                self.label_info_1.configure(text = "%s of %s" %(index, len(youtube_playlist.video_urls)))
                url = url.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                url.download(output_path=destination)

        else:
            youtube_item = YouTube(self.youtube_link.get())
            youtube_item = youtube_item.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            youtube_item.download(output_path=destination)

        self.label_info_1.configure(text = "Ready")
        # except:
        #     self.label_info_1.configure(text = "Download error")
        
        self.youtube_link.set("")
        self.download_location.set("")

    def button_event(self):
        
        thread = Thread(target=self.yt_download)
        thread.start()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
