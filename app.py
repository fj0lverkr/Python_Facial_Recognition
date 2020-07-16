import tkinter as tk
import PIL.Image
import PIL.ImageTk
import requests
import shutil
from tkinter import ttk, filedialog
from pathlib import Path

from processors.Image_Processor import ImageProcessor

PREVIEW_MAX_SIZE = 500
WINDOW_START_SIZE = (600, 480)
TEMP_ONLINE_IMAGE = 'temp/online_image.jpg'


def process_image():
    processor = ImageProcessor(image_name.get())
    landmark = landmark_mode.get()
    if landmark:
        processor.landmark_face()
    else:
        processor.rectangle_face()


def resize_image(image, target_size):
    portrait = False
    if image.height >= image.width:
        portrait = True

    if portrait:
        size_divisor = image.height / target_size
    else:
        size_divisor = image.width / target_size

    size = (int(image.width / size_divisor), int(image.height / size_divisor))
    return image.resize(size, PIL.Image.ANTIALIAS)


def set_preview(file_path):
    image_name.set(file_path)
    im = PIL.Image.open(file_path)
    if im.height > PREVIEW_MAX_SIZE or im.width > PREVIEW_MAX_SIZE:
        im = resize_image(im, PREVIEW_MAX_SIZE)

    img = PIL.ImageTk.PhotoImage(im)
    label_preview_image.config(image=img)
    label_preview_image.image = img


def get_open_file():
    file = filedialog.askopenfilename(initialdir=home, title="Select image",
                                      filetypes=[('image files', ('.png', '.jpg'))])
    if file != '':
        label_file_name.config(text=file)
        set_preview(file)


def get_online_file():
    url = entry_url.get()
    im_response = requests.get(url, stream=True)
    with open(TEMP_ONLINE_IMAGE, 'wb') as file:
        shutil.copyfileobj(im_response.raw, file)
    del im_response
    try:
        im_test = PIL.Image.open(TEMP_ONLINE_IMAGE)
        label_file_name.config(text=TEMP_ONLINE_IMAGE)
        set_preview(TEMP_ONLINE_IMAGE)
        del im_test
    except IOError:
        print(f'No valid image found at url {url}, falling back to local demo image.')
        set_preview('demo/demo_faces.jpg')


window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.minsize(WINDOW_START_SIZE[0], WINDOW_START_SIZE[1])
start_pos_y = int(screen_height/2 - WINDOW_START_SIZE[1]/2)
start_pos_x = int(screen_width/2 - WINDOW_START_SIZE[0]/2)
entry_url = tk.StringVar(window)
image_name = tk.StringVar(window)
landmark_mode = tk.BooleanVar(window)
landmark_mode.set(False)
home = str(Path.home())
window.title(string='Face detector')
window.geometry(f'+{start_pos_x}+{start_pos_y}')

main = ttk.Frame(window)
frame_open_from_web = ttk.Frame(main)
frame_or_text = ttk.Frame(main)
frame_file_select = ttk.Frame(main)
frame_options = ttk.Frame(main)
frame_submit = ttk.Frame(main)
frame_preview = ttk.Frame(main)

textfield_url = ttk.Entry(frame_open_from_web, textvariable=entry_url)
button_select_url = ttk.Button(frame_open_from_web, command=get_online_file, text='Load image from web')
label_or = ttk.Label(frame_or_text, text='--OR--')
button_open_file = ttk.Button(frame_file_select, command=get_open_file, text='Select image...')
label_file_name = ttk.Label(frame_file_select)
checkbutton_landmark_mode = ttk.Checkbutton(frame_options, text='Use landmarks in stead of boxes?', onvalue=True,
                                            offvalue=False, variable=landmark_mode)
button_submit = ttk.Button(frame_submit, command=process_image, text='Process image')
sep = ttk.Separator(main, orient=tk.HORIZONTAL)
label_preview_image = tk.Label(frame_preview)

main.pack(fill='both', expand=True)
frame_open_from_web.pack(fill='x', padx=10, pady=(10, 2))
textfield_url.pack(side='left')
button_select_url.pack(side='left', padx=(5, 0))
frame_or_text.pack(fill='x', padx=10, pady=(2, 2))
label_or.pack(side='left')
frame_file_select.pack(fill='x', padx=10, pady=(2, 2))
button_open_file.pack(side='left')
label_file_name.pack(side='left')
frame_options.pack(fill='x', padx=10, pady=(2, 2))
checkbutton_landmark_mode.pack(side='left')
frame_submit.pack(fill='x', padx=10, pady=(2, 10))
button_submit.pack(side='left')
sep.pack(fill='x', padx=(10, 10))
frame_preview.pack(fill='both', expand=True, padx=1, pady=(10, 10))
label_preview_image.pack()


if __name__ == '__main__':
    set_preview('demo/demo_faces.jpg')
    window.mainloop()
