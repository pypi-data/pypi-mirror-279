import logging
import platform

import tkinter as tk
import ttkbootstrap as ttk

from ..image_comparator import ImageComparator
from ..util import Coordinates, Size
from .image_canvas import ImageCanvas
from .image_scaling import ImageScaling
from .zoom_menu import ZoomMenu


log = logging.getLogger(__name__)


class ImageFrame(ttk.Frame):
    def __init__(
        self, parent, update_item=None, left_label='left', right_label='right'
    ):
        super().__init__(parent)
        self.update_item_command = update_item
        self.left_label = left_label
        self.right_label = right_label

        self.high_contrast = tk.BooleanVar()
        self.high_contrast.set(False)

        self.zoom_menu = ZoomMenu(self)
        self.button_zoom_100 = ttk.Radiobutton(
            self,
            text='1:1',
            variable=self.zoom_menu.mode_var,
            value='Original',
            command=self.zoom_original,
        )
        self.button_zoom_fit_if_larger = ttk.Radiobutton(
            self,
            text='Fit if larger',
            variable=self.zoom_menu.mode_var,
            value='FitIfLarger',
            command=self.zoom_fit_if_larger,
        )
        self.button_zoom_menu = ttk.Button(
            self, text='Zoom...', command=self.post_zoom_menu
        )
        self.button_high_contrast = ttk.Checkbutton(
            self,
            text='High constrast',
            variable=self.high_contrast,
            command=self.show_diff,
        )

        self.image_layout_style = tk.IntVar()
        self.image_layout_style.set(3)
        self.button_layout1 = ttk.Radiobutton(
            self,
            text='1',
            variable=self.image_layout_style,
            value=1,
            command=self.layout_images,
        )
        self.button_layout2 = ttk.Radiobutton(
            self,
            text='2',
            variable=self.image_layout_style,
            value=2,
            command=self.layout_images,
        )
        self.button_layout3 = ttk.Radiobutton(
            self,
            text='3',
            variable=self.image_layout_style,
            value=3,
            command=self.layout_images,
        )

        self.image_frame = ttk.Frame(self)
        self.images = {
            'left': ImageCanvas(self.image_frame, 'left'),
            'right': ImageCanvas(self.image_frame, 'right'),
            'diff': ImageCanvas(self.image_frame, 'diff'),
        }

        self.comparator = None
        self.button_zoom_fit_if_larger.invoke()

        self.operate_buttons = []

        self.layout()
        self.bind_events()

    def add_operate_buttons(self, *buttons):
        self.operate_buttons.extend(buttons)
        self.layout()

    def add_standard_operate_buttons(self):
        self.add_operate_buttons(
            ttk.Button(self, text='Delete', command=self.delete),
            ttk.Button(self, text='⟵', command=self.copy_right_to_left),
            ttk.Button(self, text='⟶', command=self.copy_left_to_right),
        )

    def layout(self):
        buttons = (
            self.button_zoom_100,
            self.button_zoom_fit_if_larger,
            self.button_zoom_menu,
            self.button_high_contrast,
            self.button_layout1,
            self.button_layout2,
            self.button_layout3,
        )
        for col, button in enumerate(buttons):
            button.grid(column=col, row=0, padx=5, pady=5, sticky='w')

        for col, button in enumerate(self.operate_buttons):
            button.grid(column=len(buttons) + 1 + col, row=0, padx=5, pady=5, sticky='e')

        self.image_frame.grid(
            column=0,
            row=1,
            columnspan=len(buttons) + 1 + len(self.operate_buttons),
            sticky='nsew',
        )
        self.image_frame.rowconfigure(0, weight=1)

        self.layout_images()

        self.columnconfigure(len(buttons), weight=1)
        self.rowconfigure(1, weight=1)

    def layout_images(self):
        if platform.system() == 'Linux':
            mouse_wheel_seqs = ('<Button-4>', '<Button-5>')
        else:
            mouse_wheel_seqs = ('<MouseWheel>',)

        n = self.image_layout_style.get()
        if n == 3:
            self.images['left'].grid(column=0, row=0, sticky='nsew')
            self.images['right'].grid(column=1, row=0, sticky='nsew')
            self.images['diff'].grid(column=2, row=0, sticky='nsew')

            self.image_frame.columnconfigure(0, weight=1)
            self.image_frame.columnconfigure(1, weight=1)
            self.image_frame.columnconfigure(2, weight=1)

            for seq in mouse_wheel_seqs:
                self.image_frame.unbind(seq)
                for image in self.images.values():
                    image.unbind(seq)

        elif n == 2:
            self.images['left'].grid(column=0, row=0, sticky='nsew')
            self.images['right'].grid_forget()
            self.images['diff'].grid(column=1, row=0, sticky='nsew')

            self.image_frame.columnconfigure(0, weight=1)
            self.image_frame.columnconfigure(1, weight=1)
            self.image_frame.columnconfigure(2, weight=0)

            for seq in mouse_wheel_seqs:
                self.image_frame.bind(seq, self.on_mouse_wheel)
                for image in self.images.values():
                    image.bind(seq, self.on_mouse_wheel)

        else:
            assert n == 1
            self.images['left'].grid(column=0, row=0, sticky='nsew')
            self.images['right'].grid_forget()
            self.images['diff'].grid_forget()

            self.image_frame.columnconfigure(0, weight=1)
            self.image_frame.columnconfigure(1, weight=0)
            self.image_frame.columnconfigure(2, weight=0)

            for seq in mouse_wheel_seqs:
                self.image_frame.bind(seq, self.on_mouse_wheel)
                for image in self.images.values():
                    image.bind(seq, self.on_mouse_wheel)

    def bind_events(self):
        for key in self.images.keys():
            for otherkey in set(self.images.keys()) - {key}:
                self.images[key].bind(
                    '<Button1-Motion>', self.images[otherkey].on_motion, add='+'
                )
                self.images[key].bind(
                    '<ButtonRelease-1>', self.images[otherkey].on_left_up, add='+'
                )

    def on_mouse_wheel(self, evt):
        if platform.system() == 'Linux':
            mouse_wheel_up = evt.num == 5
        else:
            mouse_wheel_up = evt.delta > 0

        n = self.image_layout_style.get()
        if n == 2:
            if self.images['left'].grid_info():
                self.images['left'].grid_forget()
                self.images['right'].grid(column=0, row=0, sticky='nsew')
            else:
                assert self.images['right'].grid_info()
                self.images['left'].grid(column=0, row=0, sticky='nsew')
                self.images['right'].grid_forget()
        else:
            assert n == 1
            if self.images['left'].grid_info():
                next_image = 'right' if mouse_wheel_up else 'diff'
                self.images['left'].grid_forget()
                self.images[next_image].grid(column=0, row=0, sticky='nsew')
            elif self.images['right'].grid_info():
                next_image = 'diff' if mouse_wheel_up else 'left'
                self.images['right'].grid_forget()
                self.images[next_image].grid(column=0, row=0, sticky='nsew')
            else:
                assert self.images['diff'].grid_info()
                next_image = 'left' if mouse_wheel_up else 'right'
                self.images['diff'].grid_forget()
                self.images[next_image].grid(column=0, row=0, sticky='nsew')

    def minsize(self):
        width = (
            self.button_zoom_100.winfo_width()
            + self.button_zoom_fit_if_larger.winfo_width()
            + self.button_zoom_menu.winfo_width()
            + self.button_high_contrast.winfo_width()
        )
        height = self.button_zoom_100.winfo_height()
        return Size((width + 400, height + 600))

    def zoom_original(self):
        self.zoom(ImageScaling.Mode.Original)

    def zoom_fit_if_larger(self):
        self.zoom(ImageScaling.Mode.Fit, factor=1, shrink=True, expand=False)

    def zoom(self, mode, factor=1, shrink=True, expand=True):
        for image in self.images.values():
            image.zoom(mode, factor=factor, shrink=shrink, expand=expand)

    def post_zoom_menu(self):
        pos = Coordinates(
            (self.button_zoom_menu.winfo_rootx(), self.button_zoom_menu.winfo_rooty())
        )
        pos.y += self.button_zoom_menu.winfo_height()
        self.zoom_menu.post(pos)

    def show_diff(self):
        if self.high_contrast.get():
            if self.comparator:
                self.images['diff'].scaled_image = None
                self.images['diff'].load_image(self.comparator.high_contrast_diff)
        else:
            if self.comparator:
                self.images['diff'].scaled_image = None
                self.images['diff'].load_image(self.comparator.diff)

    def load_images(self, left, right):
        self.comparator = ImageComparator(left, right)
        self.images['left'].load_image(self.comparator.left)
        self.images['right'].load_image(self.comparator.right)
        self.show_diff()

    def load_comparator(self, comparator):
        self.comparator = comparator
        self.images['left'].load_image(self.comparator.left)
        self.images['right'].load_image(self.comparator.right)
        self.show_diff()

    def clear(self):
        for image in self.images.values():
            self.after_idle(image.clear)

    def delete(self):
        if self.comparator:
            left_file, right_file = (
                self.comparator.left_file,
                self.comparator.right_file,
            )
            log.info(f'DELETE: {left_file} {right_file}')
            self.comparator.delete_files()
            self.comparator = None
            self.clear()
            if self.update_item_command:
                self.update_item_command(left_file, self.comparator)

    def copy_left_to_right(self):
        if self.comparator:
            left_file, right_file = (
                self.comparator.left_file,
                self.comparator.right_file,
            )
            log.info(f'COPY: {left_file} -> {right_file}')
            self.comparator.copy_left_to_right()
            if self.comparator.right:
                self.images['right'].load_image(self.comparator.right)
                self.images['diff'].load_image(self.comparator.diff)
            if self.update_item_command:
                self.update_item_command(right_file, self.comparator)

    def copy_right_to_left(self):
        if self.comparator:
            left_file, right_file = (
                self.comparator.left_file,
                self.comparator.right_file,
            )
            log.info(f'COPY: {right_file} -> {left_file}')
            self.comparator.copy_right_to_left()
            if self.comparator.left:
                self.images['left'].load_image(self.comparator.left)
                self.images['diff'].load_image(self.comparator.diff)
            if self.update_item_command:
                self.update_item_command(left_file, self.comparator)
