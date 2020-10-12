import tkinter as tk
import unittest
from unittest.mock import Mock
from unittest.mock import patch
import os


import configuration
import logic


class TestChecker(unittest.TestCase):
    def setUp(self):
        with patch('configuration.Form') as mock:
            self.mock_form = mock()
            self.mock_form.width_scroll = 500
            self.mock_form.height_scroll = 500
            self.mock_form.height_cnv = 300
            self.mock_form.width_cnv = 300
        self.root = tk.Tk()
        self.frm = configuration.Form(self.root)
        self.event = Mock()
        self.d = logic.Painter(self.root, self.mock_form)
        self.event.x = 100
        self.event.y = 100

    def test_draw(self):
        self.d.move = 1
        self.d.draw_brush(self.event, clr='black', sze=6)

    def test_change_layers_on(self):
        self.d.create_layers(self.event)
        self.d.info[1].get = Mock(return_value=True)
        self.d.change_layers()

    def test_change_layers_off(self):
        self.d.create_layers(self.event)
        self.d.info[1] = Mock(return_value=False)
        self.d.change_layers()

    def test_increase_cnv_one(self):
        self.mock_form.add_height_cnv.get = Mock(return_value='')
        self.mock_form.add_wight_cnv.get = Mock(return_value='40')
        self.d.increase_canvas(self.event)

    def test_increase_cnv_two(self):
        self.mock_form.add_height_cnv.get = Mock(return_value='50')
        self.mock_form.add_wight_cnv.get = Mock(return_value='')
        self.d.increase_canvas(self.event)

    def test_set_command(self):
        self.d.set_command()

    def test_add_image(self):
        logic.askopenfilename = Mock(return_value='test_open.png')
        self.d.add_image(self.event)

    def test_add_image_no_name(self):
        logic.askopenfilename = Mock(return_value='')
        with self.assertRaises(AttributeError):
            self.d.add_image(self.event)

    def test_save_image(self):
        self.d.composite = 0
        logic.asksaveasfilename = Mock(return_value='test_save.png')
        self.d.save_image(self.event)

    def test_save_layers(self):
        self.d.composite = 1
        logic.asksaveasfilename = Mock(return_value='test_save.png')
        with self.assertRaises(AttributeError):
            self.d.save_image(self.event)

    def test_brush(self):
        self.d.change_on_brush()
        self.assertEqual(self.d.entity, 1)

    def test_eraser(self):
        self.d.change_on_eraser()
        self.assertEqual(self.d.entity, 0)

    def test_get_size(self):
        self.mock_form.size.get = Mock(return_value=10)
        self.d.get_size_brush(self.event)
        self.assertEqual(self.d.size_brush, 10)

    def test_choose_color(self):
        logic.colorchooser.askcolor = Mock(return_value='#ff80ff')
        self.d.change_color()
        self.assertEqual(self.d.color, 'f')

    def test_paste(self):
        d = logic.Painter(self.root, self.frm)
        with self.assertRaises(tk.TclError):
            d.paste_img(self.event)

    def test_move(self):
        self.d.move = 1
        self.assertEqual(self.d.move_image(self.event), -1)

    def test_move_value(self):
        self.d.paste_img(self.event)
        self.assertEqual(self.d.move, 1)

    def test_stop_paste(self):
        self.assertEqual(self.d.stop_paste(self.event), "break")

    def test_cut_gif(self):
        logic.askopenfilename = Mock(return_value='image.gif')
        self.d.cut_gif(self.event)
        self.assertEqual(len([i for i in os.listdir('cadrs/')]), 5)

    def test_delete_layers(self):
        self.d.i = 12
        self.d.dict_layers = {1: 'a', 2: 'b'}
        self.d.button_list = [1, 2, 3, 4]
        self.d.check_changes_cvar = [1, 2, 3]
        self.info = {6: 'g', 7: 'h'}
        self.d.delete_layers(self.event)
        self.assertEqual(self.d.i, 1)
        self.assertEqual(len(self.d.dict_layers), 0)
        self.assertEqual(len(self.d.button_list), 0)
        self.assertEqual(len(self.d.check_changes_cvar), 0)
        self.assertEqual(len(self.d.info), 0)


if __name__ == '__main__':
    unittest.main()
