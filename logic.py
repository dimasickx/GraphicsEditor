from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox

from PIL import ImageDraw, Image, ImageTk, ImageChops
import PIL
import os


class Painter:
    def __init__(self, root, frm):
        self.root = root
        self.frm = frm
        self.color = 'black'
        self.size_brush = 6
        self.entity = 1
        self.not_white = (255, 0, 0, 0)
        self.bg_clr = (255, 255, 255, 255)
        self.image = 0
        self.image1 = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                             self.frm.height_scroll),
                                    self.not_white)
        self.draw_to_save = ImageDraw.Draw(self.image1)
        self.back_ground = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                                  self.frm.height_scroll),
                                         self.bg_clr)
        self.create_images = []
        self.count_dload = -1
        self.move = 0
        self.name_move = None
        self.download_image = None
        self.x1_paste = None
        self.x2_paste = None

        self.composite = 0
        self.i = 1
        self.check_changes_cvar = []
        self.photo_create = 0
        self.button_list = []
        self.info = {}
        self.image_increase = 0
        self.image_layers = 0
        self.dict_layers = {}

    def set_command(self):
        self.frm.canv.bind('<B1-Motion>',
                           lambda event: self.draw_brush(event, self.color,
                                                         self.size_brush))
        self.frm.eraser.configure(command=self.change_on_eraser)
        self.frm.brush.configure(command=self.change_on_brush)
        self.frm.btn_change_color.configure(command=self.change_color)
        self.frm.save_size.bind('<Button-1>', self.get_size_brush)
        self.frm.save_image.bind('<ButtonRelease-1>', self.save_image)
        self.frm.ch_height_cnv.bind('<ButtonRelease-1>', self.increase_canvas)
        self.frm.btn_new_layers.bind('<Button-1>', self.create_layers)
        self.frm.add_image.bind('<ButtonRelease-1>', self.add_image)
        self.frm.add_gif.bind('<ButtonRelease-1>', self.cut_gif)
        self.frm.glue_gif.bind('<ButtonRelease-1>', self.glue_gif)
        self.frm.clear_layers.bind('<ButtonRelease-1>', self.delete_layers)

    def draw_brush(self, event, clr, sze):
        size = sze
        color = clr
        a, b, c, d = self.bg_clr
        eraser = '#{:02x}{:02x}{:02x}{:02x}'.format(a, b, c, d)  # RGBA to hex
        x1 = self.frm.canv.canvasx(event.x - size)
        y1 = self.frm.canv.canvasy(event.y - size)
        x2 = self.frm.canv.canvasx(event.x + size)
        y2 = self.frm.canv.canvasy(event.y + size)
        if self.move == 0:
            try:
                image_x = self.frm.canv.coords(self.name_move)[0] - \
                          self.download_image.width / 2
                a = self.download_image.height / 2
                image_y = self.frm.canv.coords(self.name_move)[1] - a
                mouse_x = self.frm.canv.canvasx(event.x)
                mouse_y = self.frm.canv.canvasx(event.y)
                if self.move == 0:
                    if (image_x < mouse_x) and \
                            (mouse_x < image_x + self.download_image.width):
                        if (image_y < mouse_y) and \
                                (mouse_y < image_y +
                                 self.download_image.height):
                            return -1
            except Exception:
                pass
        if self.entity != 0:
            self.frm.canv.create_oval(x1, y1, x2, y2, outline=color,
                                      fill=color, tag='oval')
            self.draw_to_save.ellipse([x1, y1, x2, y2], fill=color)
        elif self.entity == 0:
            self.frm.canv.create_rectangle(x1, y1, x2, y2,
                                           outline=eraser[:7],
                                           fill=eraser[:7])
            self.draw_to_save.rectangle([x1, y1, x2, y2], fill=eraser[:7])

    def change_color(self):
        self.color = colorchooser.askcolor()[1]

    def change_on_brush(self):
        self.entity = 1

    def change_on_eraser(self):
        self.entity = 0

    def get_size_brush(self, event):
        self.size_brush = int(self.frm.size.get())

    def save_image(self, event):
        filename = asksaveasfilename()
        if filename:
            if self.composite == 0:
                self.image1 = ImageChops.composite(self.image1,
                                                   self.back_ground,
                                                   self.image1)
                self.image1.save(filename)
            else:
                self.composite.save(filename)

    def add_image(self, event):
        filename = askopenfilename()
        if filename:
            self.download_image = Image.open(filename)
            self.move = 0
            self.count_dload += 1
        else:
            raise AttributeError('invalid file name or name not exist')
        size = self.frm.width_cnv, self.frm.height_cnv
        self.download_image.thumbnail(size)
        self.draw_to_save = ImageDraw.Draw(self.image1)
        self.image = ImageTk.PhotoImage(self.download_image)
        self.create_images.append(self.image)
        self.name_move = 'image' + str(self.count_dload)
        self.frm.canv.tag_bind(self.name_move, '<B1-Motion>',
                               lambda event: self.move_image(event))
        self.frm.canv.create_image((self.download_image.width / 2,
                                    self.download_image.height / 2),
                                   image=self.image, tag=self.name_move)

    def gif_on_layers(self, count_layers_gif, event):
        for i in range(count_layers_gif):
            self.create_layers(event)
        count_layers_without = len(self.dict_layers) - count_layers_gif
        for i in range(count_layers_without, len(self.dict_layers)):
            image = PIL.Image.new('RGBA',
                                  (self.frm.width_scroll,
                                   self.frm.height_scroll),
                                  self.not_white)
            size = self.frm.width_cnv, self.frm.height_cnv
            download_image = Image.open('{}.png'.format(i))
            download_image.thumbnail(size)
            image.paste(download_image)
            self.dict_layers[i + 1] = image
        os.chdir('../')

    def cut_gif(self, event):
        filename = askopenfilename()
        with Image.open(filename) as im:
            count = im.n_frames
            if not os.path.exists('cadrs'):
                os.mkdir('cadrs')
            os.chdir('cadrs')
            for i in range(im.n_frames):
                im.seek(im.n_frames // im.n_frames * i)
                im.save('{}.png'.format(i))
        self.gif_on_layers(count, event)

    def glue_gif(self, event):
        images = []
        for i in range(len(self.check_changes_cvar)):
            if self.check_changes_cvar[i]:
                images.append(ImageChops.composite(self.dict_layers[i+1],
                                                   self.back_ground,
                                                   self.dict_layers[i+1]))
        gif = images[0]
        gif.save('temp.gif', 'GIF', save_all=True, append_images=images)

    def move_image(self, event):
        if self.move == 1:
            self.frm.canv.bind('<ButtonRelease-1>', self.stop_paste)
            return -1
        self.frm.canv.coords(self.name_move,
                             self.frm.canv.canvasx(event.x + 10),
                             self.frm.canv.canvasy(event.y + 10))
        self.frm.canv.bind('<ButtonRelease-1>', self.paste_img)

    @staticmethod
    def stop_paste(event):
        return "break"

    def paste_img(self, event):
        self.move = 1
        try:
            x1, x2 = self.frm.canv.coords(self.name_move)
        except ValueError:
            return
        self.x1_paste = x1 - self.download_image.width / 2
        self.x2_paste = x2 - self.download_image.height / 2
        try:
            self.image1.paste(self.download_image,
                              (int(self.x1_paste), int(self.x2_paste)),
                              self.download_image)
        except ValueError:
            self.image1.paste(self.download_image,
                              (int(self.x1_paste), int(self.x2_paste)))

    def change_layers(self):
        toggle = 0

        for k in range(len(self.check_changes_cvar) - 1, -1, -1):
            if self.check_changes_cvar[k] != self.info[k + 1].get():
                self.check_changes_cvar[k] = self.info[k + 1].get()
                toggle = k
                break

        if self.info[toggle + 1].get():
            self.frm.canv.delete('all')
            self.image_layers = PIL.Image.new('RGBA',
                                              (self.frm.width_scroll,
                                               self.frm.height_scroll),
                                              self.not_white)
            self.draw_to_save = ImageDraw.Draw(self.image_layers)
        else:
            ph = self.dict_layers[toggle + 1].copy()
            if self.move == 1:
                try:
                    self.image_layers.paste(self.download_image,
                                            (int(self.x1_paste),
                                             int(self.x2_paste)))
                    self.download_image = None
                except ValueError:
                    pass
            else:
                pass
            a = ImageChops.composite(self.image_layers, ph, self.image_layers)
            self.dict_layers[toggle + 1] = a.copy()

            self.image1 = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                                 self.frm.height_scroll),
                                        self.not_white)
            self.draw_to_save = ImageDraw.Draw(self.image1)

        self.composite = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                                self.frm.height_scroll),
                                       self.not_white)

        for j in range(len(self.dict_layers) - 1, -1, -1):
            if self.check_changes_cvar[j]:
                self.composite = ImageChops.composite(self.dict_layers[j + 1],
                                                      self.composite,
                                                      self.dict_layers[j + 1])

        self.composite = ImageChops.composite(self.composite,
                                              self.back_ground,
                                              self.composite)
        self.photo_create = ImageTk.PhotoImage(self.composite)
        self.frm.canv.create_image((self.frm.width_scroll / 2,
                                    self.frm.height_scroll / 2),
                                   image=self.photo_create)

    def create_layers(self, event):
        cvar2 = BooleanVar()
        cvar2.set(0)
        self.info[self.i] = cvar2
        check = Checkbutton(self.frm.listbox, text="layers №" + str(self.i),
                            variable=self.info[self.i], onvalue=1, offvalue=0)
        check.pack()
        check.configure(command=self.change_layers)
        self.button_list.append(check)
        self.frm.listbox.window_create(END, window=check)
        self.frm.listbox.insert(END, "\n")

        self.image_layers = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                                   self.frm.height_scroll),
                                          self.not_white)
        self.frm.canv.delete('all')
        self.dict_layers[self.i] = self.image1.copy()
        self.check_changes_cvar.append(self.info[self.i].get())
        self.i += 1
        self.image1 = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                             self.frm.height_scroll),
                                    self.not_white)

    def delete_layers(self, event):
        self.dict_layers.clear()
        self.button_list.clear()
        self.check_changes_cvar.clear()
        self.info.clear()
        self.image_layers = 0
        self.image1 = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                             self.frm.height_scroll),
                                    self.not_white)
        self.draw_to_save = ImageDraw.Draw(self.image1)
        self.frm.canv.delete('all')
        self.frm.listbox.delete('0.0', END)
        self.i = 1

    def increase_canvas(self, event):
        h = self.frm.add_height_cnv.get()
        w = self.frm.add_width_cnv.get()
        if h == '' and w != '':
            h = 0
            w = int(w)
        elif h != '' and w == '':
            h = int(h)
            w = 0
        elif h == '' and w == '':
            messagebox.showerror('invalid size', 'input size')
            return
        else:
            h = int(h)
            w = int(w)
        self.frm.width_scroll = self.frm.width_scroll + w
        self.frm.height_scroll = self.frm.height_scroll + h
        self.frm.canv.config(scrollregion=(0, 0, self.frm.width_scroll,
                                           self.frm.height_scroll))
        self.image_increase = self.image1.copy()
        self.image1 = PIL.Image.new('RGBA',
                                    (self.frm.width_scroll,
                                     self.frm.height_scroll),
                                    self.not_white)
        self.image1.paste(self.image_increase)
        self.back_ground = PIL.Image.new('RGBA', (self.frm.width_scroll,
                                                  self.frm.height_scroll),
                                         self.bg_clr)
        self.draw_to_save = ImageDraw.Draw(self.image1)
