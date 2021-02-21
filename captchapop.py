import tkinter as tk
from PIL import Image, ImageTk

class CaptchaBox:
    def __init__(self, img_path) -> None:
        self.root = tk.Tk()
        self.root.title('Captcha')
        w,h = 295,150
        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        x = screen_width//2 - w//2
        y = screen_height//2 - h//2
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.resizable(0,0)
        self.root.propagate(False)
        canvas = tk.Canvas(self.root, width=295, height=70)
        canvas.pack()
        #img = tk.PhotoImage(file=img_path)
        self.img = ImageTk.PhotoImage(Image.open(img_path))
        canvas.create_image(0,0, anchor=tk.NW, image=self.img)
        label1 = tk.Label(text='Enter the above Captcha:')
        label1.pack()
        self.inpt = tk.Entry()
        self.inpt.pack()
        button = tk.Button(text='Submit')
        button.bind('<Button-1>',self.onclick)
        button.pack()

    def onclick(self,event):
        self.captcha = self.inpt.get()
        self.root.destroy()

    def show(self):
        self.root.mainloop()
