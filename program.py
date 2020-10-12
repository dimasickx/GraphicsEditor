import configuration
from tkinter import *
import logic


def main():
    root = Tk()
    frm = configuration.Form(root)
    do = logic.Painter(root, frm)
    do.set_command()
    root.mainloop()


if __name__ == '__main__':
    main()
