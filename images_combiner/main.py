# An image combiner that combines multiple images into a single image

import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
from PIL import Image 

root = Tk() 
root.title("Image Combiner")
 
# adding file(s)
def add_file():
    files = filedialog.askopenfilenames(title="Select image(s)", \
        filetypes=(('PNG file', '*.png'), ('other files', '*.*')), \
        initialdir='C:/Users/iriskim/Code') # the very first location

    for file in files:
        list_file.insert(END, file)

# deleting file(s)
def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# file path (folder)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '': # if user cancels action
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# combines images (later used in method start())
def merge_image():
    # print('Width:', cmb_width.get())
    # print('Space:', cmb_space.get())
    # print('Format:', cmb_format.get())

    try:
        # width
        img_width = cmb_width.get()
        if img_width == 'Original size':
            img_width = -1
        else:
            img_width = int(img_width)

        # space
        img_space = cmb_space.get()
        if img_space == 'Narrow':
            img_space = 30
        elif img_space == 'Normal':
            img_space = 60
        elif img_space == 'Wide':
            img_space = 90
        else: # None
            img_space = 0

        # format
        img_format = cmb_format.get().lower()

        ###############################################

        images = [Image.open(x) for x in list_file.get(0, END)]

        # put image sizes in a list to adjust them
        image_sizes = [] # [(width1, height1), (width2, height2),...]
        if img_width > -1:
            # adjust width
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            # use origianl size
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        widths, heights = zip(*(image_sizes))

        # gets max width and total height 
        max_width, total_height = max(widths), sum(heights)

        # final image size
        if img_space > 0: # applying image spaces
            total_height += (img_space * (len(images) - 1))

        result_img = Image.new('RGB', (max_width, total_height), (255, 255, 255)) # white bg
        y_offset = 0 # location of y

        for idx, img in enumerate(images):
            # adjust image size according to user's choice of width
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space) # image height + image space

            progress = ((idx + 1) / len(images)) * 100 # gets the progress in percentage
            p_var.set(progress)
            progress_bar.update()


        # format option
        file_name = 'final_photo.' + img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo('Info', 'Images successfully combined')
    except Exception as err:
        msgbox.showerror('Error', err)

# start
def start(): 
    # checks if there are files(images) selected
    if list_file.size() == 0:
        msgbox.showwarning('Warning', 'There are no images selected')
        return

    # checks if user has chosen a file path
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning('Warning', 'There is no file path selected')
        return

    # combines images
    merge_image()
    

# file frame (add/delete files)
file_frame = Frame(root)
file_frame.pack(fill='x', padx=5, pady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text='Add file(s)', command=add_file)
btn_add_file.pack(side='left')

btn_delete_file = Button(file_frame, padx=5, pady=5, width=12, text='Delete file(s)', command=del_file)
btn_delete_file.pack(side='right')

# list frame
list_frame = Frame(root)
list_frame.pack(fill='both', padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side='right', fill='y')

list_file = Listbox(list_frame, selectmode='extended', height=15, yscrollcommand=scrollbar.set)
list_file.pack(side='left', fill='both', expand=True)
scrollbar.config(command=list_file.yview)

# file path frame
path_frame = LabelFrame(root, text='File path')
path_frame.pack(fill='x', padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side='left', fill='x', expand=True, padx=5, pady=5, ipady=4) # adjusting height

btn_dest_path = Button(path_frame, text='Search', width=10, command=browse_dest_path)
btn_dest_path.pack(side='right', padx=5, pady=5)


# option frame
option_frame = LabelFrame(root, text='Option')
option_frame.pack(padx=5, pady=5, ipady=5)

# Option 1. width size 
lbl_width = Label(option_frame, text='Width:', width=8)
lbl_width.pack(side='left', pady=5)

opt_width = ['Original size', '1024', '800', '640']
cmb_width = ttk.Combobox(option_frame, state='readonly', values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side='left', padx=5, pady=5)


# Option 2. space size 
lbl_space = Label(option_frame, text='Space:', width=8)
lbl_space.pack(side='left', pady=5)

opt_space = ['None', 'Narrow', 'Normal', 'Wide']
cmb_space = ttk.Combobox(option_frame, state='readonly', values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side='left', padx=5, pady=5)

# Option 3. file format option 
lbl_format = Label(option_frame, text='Format:', width=8)
lbl_format.pack(side='left', pady=5)

opt_format = ['PNG', 'JPG', 'BMP']
cmb_format = ttk.Combobox(option_frame, state='readonly', values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side='left', padx=5, pady=5)


# progress bar
progress_frame = LabelFrame(root, text='Saving file ...')
progress_frame.pack(fill='x', padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar= ttk.Progressbar(progress_frame, maximum=100, variable=p_var)
progress_bar.pack(fill='x', padx=10, pady=10)


# run frame
run_frame = Frame(root)
run_frame.pack(fill='x', padx=5, pady=5)

btn_close = Button(run_frame, padx=5, pady=5, text='Close', width=12, command=root.quit)
btn_close.pack(side='right', padx=5, pady=5)

btn_start = Button(run_frame, padx=5, pady=5, text='Start', width=12, command=start)
btn_start.pack(side='right', padx=5, pady=5)

root.resizable(False, False) 
root.mainloop()