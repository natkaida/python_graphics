import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageToGifConverter:
    def __init__(self, window):
        self.window = window
        window.title("Создаем анимированные GIFки")
        window_width = 350
        window_height = 350
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.select_button = tk.Button(window, text="Выберите изображения", command=self.select_images)
        self.select_button.pack()
        self.convert_button = tk.Button(window, text="Создать GIF", command=self.convert_images, state="disabled")
        self.convert_button.pack()
        self.status_label = tk.Label(window, text="Кадры не выбраны")
        self.status_label.pack()
        self.image_filenames = []
        self.anim_frames = []
        self.gif_label = tk.Label(self.window)
        self.anim_index = 0
        self.anim_delay = 100

    def select_images(self):
        self.image_filenames = filedialog.askopenfilenames(title="Выберите кадры для анимации", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("All Files", "*.*")])
        if len(self.image_filenames) == 0:
            self.status_label.config(text="Кадры не выбраны")
            self.convert_button.config(state="disabled")
        else:
            self.status_label.config(text="Выбрано {} кадров".format(len(self.image_filenames)))
            self.convert_button.config(state="normal")

    def convert_images(self):
        frames = []
        for i in self.image_filenames:
            frames.append(Image.open(i))

        save_filename = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif"), ("All Files", "*.*")])
        if save_filename:
            frames[0].save(save_filename, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)

        self.gif_image = Image.open(save_filename)
        try:
            while True:
                self.anim_frames.append(ImageTk.PhotoImage(self.gif_image))
                self.gif_image.seek(len(self.anim_frames)) 
        except EOFError:
            pass
        self.gif_label.config(image=self.anim_frames[0])
        self.gif_label.pack()
        self.animate()
        self.image_filenames = []
        self.status_label.config(text="Готово!")
        self.convert_button.config(state="disabled")

    def animate(self):
        if self.anim_frames:
            self.gif_label.config(image=self.anim_frames[self.anim_index])
            self.anim_index = (self.anim_index + 1) % len(self.anim_frames)
            self.window.after(self.anim_delay, self.animate)

def on_closing():
    root.destroy()
    exit()


root = tk.Tk()
app = ImageToGifConverter(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
