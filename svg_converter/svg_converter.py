import tkinter as tk
from PIL import ImageTk, Image
import os, shutil
import tempfile
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import svgutils.transform as sg

class App:
    def __init__(self, window):
        self.window = window
        window.title("Конвертация SVG в PNG/JPG")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Вычисляем координаты окна приложения
        window_width = 350
        window_height = 450
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.temp_dir = tempfile.mkdtemp()
        window.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.label = tk.Label(window, text="Выберите SVG файл:")
        self.label.pack()

        self.select_button = tk.Button(window, text="Выберите файл", command=self.select_file)
        self.select_button.pack()

        self.preview_label = tk.Label(window, text="Выбранный SVG файл:")
        self.preview_label.pack()

        self.canvas = tk.Canvas(window, width=120, height=120)
        self.canvas.pack()
        self.resolution_label = tk.Label(window, text="Выберите нужный размер:")
        self.resolution_label.pack()

        self.resolution = tk.IntVar()
        self.resolution_48 = tk.Radiobutton(window, text="48x48", variable=self.resolution, value=48)
        self.resolution_48.pack()

        self.resolution_128 = tk.Radiobutton(window, text="128x128", variable=self.resolution, value=128)
        self.resolution_128.pack()

        self.resolution_512 = tk.Radiobutton(window, text="512x512", variable=self.resolution, value=512)
        self.resolution_512.pack()

        self.format_label = tk.Label(window, text="Выберите нужный формат:")
        self.format_label.pack()

        self.png_var = tk.BooleanVar()
        self.png_checkbox = tk.Checkbutton(window, text="PNG", variable=self.png_var)
        self.png_checkbox.pack()

        self.jpg_var = tk.BooleanVar()
        self.jpg_checkbox = tk.Checkbutton(window, text="JPG", variable=self.jpg_var)
        self.jpg_checkbox.pack()

        self.convert_button = tk.Button(window, text="Конвертировать", command=self.convert_file)
        self.convert_button.pack()

    def select_file(self):
        self.filepath = tk.filedialog.askopenfilename(title="Выберите SVG файл", filetypes=(("SVG files", "*.svg"),))
        self.label.configure(text=f"Выбранный файл: {os.path.basename(self.filepath)}")
        self.show_preview()
        
    def show_preview(self):
        if hasattr(self, "preview_image"):
            self.canvas.delete(self.preview_image)

        # создание превью изображения из SVG файла
        fig = sg.fromfile(self.filepath)
        fig.set_size(('100', '100'))
        filename = os.path.basename(self.filepath)
        resized_filepath = os.path.join(self.temp_dir, f"{filename}_resized.svg")
        fig.save(resized_filepath)

        # Конвертируем SVG в PNG формат
        drawing = svg2rlg(resized_filepath)
        png_filepath = os.path.join(self.temp_dir, f"{filename}_resized.png")
        renderPM.drawToFile(drawing, png_filepath, fmt="PNG")

        # Загружаем PNG файл для превью
        img = Image.open(png_filepath)
        self.preview_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.preview_image)

    def convert_file(self):
        if not hasattr(self, "filepath"):
            self.label.configure(text="Сначала нужно выбрать SVG файл")
            return

        if not self.png_var.get() and not self.jpg_var.get():
            self.label.configure(text="Выберите формат конвертирования")
            return

        filename, ext = os.path.splitext(os.path.basename(self.filepath))

        if ext.lower() != ".svg":
            self.label.configure(text="Выберите файл формата SVG")
            return
        size = str(self.resolution.get())

        resized_filename = os.path.join(self.temp_dir, f"{filename}_{size}x{size}.svg")
        converted_filename = f"{os.path.splitext(self.filepath)[0]}_converted.png" if self.png_var.get() else f"{os.path.splitext(self.filepath)[0]}_converted.jpg"

        # Масштабируем SVG до нужного рамера
        fig = sg.fromfile(self.filepath)
        fig.set_size((size, size))
        fig.save(resized_filename)

        # Сохраняем SVG в PNG или JPEG 
        drawing = svg2rlg(resized_filename)
        fmt = 'PNG' if self.png_var.get() else 'JPEG'
        renderPM.drawToFile(drawing, converted_filename, fmt=fmt)
        self.label.configure(text=f"{filename} конвертирован в {fmt}")
        folder_path = os.path.dirname(os.path.abspath(converted_filename))
        self.open_button = tk.Button(self.window, text="Показать файл в директории",
                                      command=lambda: os.startfile(folder_path))
        self.open_button.pack()

    def exit_app(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        root.destroy()

root = tk.Tk()
app = App(root)
root.mainloop()
