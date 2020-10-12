from tkinter import *


class Form:
    def __init__(self, window):
        window.title('Graphics editor')
        window.configure(bg='#ffdfd1')
        window.geometry('900x600+100+10')
        window.minsize(615, 450)
        self.width_cnv = 800
        self.height_cnv = 450
        self.width_scroll = 800
        self.height_scroll = 450

        self.frame = Frame(window, height=95, width=810, bd=3, bg='#fcdbcc')
        self.label_height = Label(text='height', width=5)
        self.label_height.place(x=255, y=26)
        self.label_width = Label(text='width', width=5)
        self.label_width.place(x=255, y=2)

        self.size = Entry(self.frame, width=2)
        self.size.place(x=1, y=1)
        self.save_size = Button(self.frame, text='accept size', height=2,
                                width=8, bg='light green', font='arial 9')
        self.save_size.place(x=20, y=0)
        self.brush = Button(self.frame, text='brush', height=2,
                            width=5, bg='light green')
        self.brush.place(x=90, y=0)
        self.eraser = Button(self.frame, text='eraser', height=2,
                             width=5, bg='light green')
        self.eraser.place(x=135, y=0)
        self.save_image = Button(self.frame, text='save image', height=4,
                                 width=10, bg='light green')
        self.save_image.place(x=400, y=0)

        self.add_image = Button(self.frame, text='add\nimage', height=2,
                                width=5, bg='light green')
        self.add_image.place(x=350, y=0)

        self.add_gif = Button(self.frame, text='add\ngif', height=2,
                              width=5, bg='light green')
        self.add_gif.place(x=720, y=0)

        self.glue_gif = Button(self.frame, text='glue\nselected', height=2,
                               width=5, bg='light green')
        self.glue_gif.place(x=720, y=40)

        self.ch_height_cnv = Button(self.frame, text='change\nsize\ncanvas',
                                    height=3, width=5, bg='light green')
        self.ch_height_cnv.place(x=180, y=0)
        self.add_height_cnv = Entry(self.frame, width=3)
        self.add_height_cnv.place(x=227, y=24)

        self.add_width_cnv = Entry(self.frame, width=3)
        self.add_width_cnv.place(x=227, y=1)

        self.btn_change_color = Button(self.frame, text='choose\ncolor',
                                       height=2, width=5, bg='light green')
        self.btn_change_color.place(x=297, y=1)

        self.btn_new_layers = Button(self.frame, text='create new layers',
                                     height=1, width=12, bg='light green')
        self.btn_new_layers.place(x=610, y=0)

        self.clear_layers = Button(self.frame, text='del all layers',
                                   height=1, width=12, bg='light green')
        self.clear_layers.place(x=610, y=25)

        self.frame.place(x=0, y=0)

        self.frame_canvas = Frame(window, width=800, height=450, bd=1)
        self.frame_canvas.place(x=5, y=100)

        self.scrollbar_canv_y = Scrollbar(self.frame_canvas)
        self.scrollbar_canv_y.pack(side='right', fill='y')

        self.scrollbar_canv_x = Scrollbar(self.frame_canvas,
                                          orient=HORIZONTAL)
        self.scrollbar_canv_x.pack(side='bottom', fill='x')

        self.canv = Canvas(self.frame_canvas, width=self.width_cnv,
                           height=self.height_cnv, bd=1, bg='white')
        self.canv.config(scrollregion=(0, 0, self.width_scroll,
                                       self.height_scroll))
        self.canv.config(xscrollcommand=self.scrollbar_canv_x.set,
                         yscrollcommand=self.scrollbar_canv_y.set)
        self.canv.pack(side='top')
        self.scrollbar_canv_y.config(command=self.canv.yview)
        self.scrollbar_canv_x.config(command=self.canv.xview)

        self.frame_layers1 = Frame(window, width=130, height=80, bd=1)
        self.frame_layers1.place(x=500, y=2)

        self.scrollbar = Scrollbar(self.frame_layers1)
        self.scrollbar.pack(side='right', fill='y')

        self.listbox = Text(self.frame_layers1, width=10, height=5,
                            yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side='left')

        self.scrollbar.config(command=self.listbox.yview)


if __name__ == '__main__':
    pass
