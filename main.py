from tkinter import *
import os
from tkinter import messagebox
from tkinter import filedialog
import PIL.ImageOps
from PIL import Image
import deff as fl
import errno
import os

##Creating a folder at the root of the program-------------------------------------------------------------------------#
fl.make_sure_path_exists('Edited photos')
#----------------------------------------------------------------------------------------------------------------------#
##Creating a folder at the root of the program
def make_sure_path_exists(path):
    try: os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

##Фуfunction that translates from cm to pixel
def cm_in_px(cm):
    global px
    px = int(cm) * 38
    return px
##ФScale and store aspect ratio
def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=w, height=h))

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Width or height required!')

    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('The scaled image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))
#----------------------------------------------------------------------------------------------------------------------#

##Signature checkbox 2
def chek_cb2():
    global message_entry
    if ismarried2.get() == 0:
        message_entry = Entry(window, state=DISABLED, bd=2, width = 48)
        message_entry.place(x=10, y=275)
        return Label(window, text='Add ending to file name:', font=('Arial', 10)).place(x=10, y=250)
    else:
        message_entry = Entry(window, state=NORMAL, bd=2, width = 48)
        message_entry.place(x=10, y=275)
        return Label(window, text='Add ending to file name:', font=('Arial', 10)).place(x=10, y=250)
#----------------------------------------------------------------------------------------------------------------------#

##file renaming
def rename():
    global last_name
    if ismarried2.get() == 1:
        last_name = '_' + message_entry.get()
    else:
        last_name = ''
    return last_name
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
##Path to upload images
number_f = 0
def clicked_dialogOpen():
    global choosefile
    global number_f
    choosefile = filedialog.askopenfilename(multiple=True, parent = window, filetypes=(("Image files", "*.png"), ("all files", "*.*")))
    number_f = len(choosefile)
    label_file()
#----------------------------------------------------------------------------------------------------------------------#
##Check for characters in the string
def check_name():
    global d
    d = 0
    for i in message_entry.get():
        if i.isalpha():
            d += 1
        elif i.isdigit():
            d+= 1
        else:
            d+= 1
    return d
#----------------------------------------------------------------------------------------------------------------------#
##Display information about the number of selected images
def label_file():

    if number_f == 0:
        lbl2 = Label(window, text="Image not selected", font=('Arial', 9), fg = 'red')
        lbl2.place(x=start_pos_x, y=start_pos_y + step_des * 0.9)
    elif number_f == 1:
        lbl2 = Label(window, text='File selected             '.format(number_f), font=('Arial', 9), fg = 'green')
        lbl2.place(x=start_pos_x, y=start_pos_y + step_des * 0.9)
    else:
        lbl2 = Label(window, text='Files selected - {}       '.format(number_f), font=('Arial', 9), fg = 'green')
        lbl2.place(x=start_pos_x, y=start_pos_y + step_des * 0.9)
#----------------------------------------------------------------------------------------------------------------------#
##Open the path to save the file
filename = 0
def browse_button():
    global filename
    filename = filedialog.askdirectory()
    label_folder()
#----------------------------------------------------------------------------------------------------------------------#
##Display save directory information
def label_folder():

    if filename == 0:
        lbl = Label(window, text="Path not selected", font=('Arial', 9), fg = 'red')
        lbl.place(x=start_pos_x, y=start_pos_y + step_des * 2.3)
    elif filename == '':
        lbl = Label(window, text=os.getcwd() + '/Edited photos/', font=('Arial', 9), fg = 'green')
        lbl.place(x=start_pos_x, y=start_pos_y + step_des * 2.3)
    else:
        lbl = Label(window, text=filename, font=('Arial', 9), fg = 'green')
        lbl.place(x=start_pos_x, y=start_pos_y + step_des * 2.3)
#----------------------------------------------------------------------------------------------------------------------#
##Zoom and record an image
def scale():
    check_name()
    if number_f < 1:
        messagebox.showerror("Error", "No file selected")
    if ismarried2.get() == 1 and d < 1:
        messagebox.showerror("Error", "Parameter not entered: Add ending to file name")
    else:
        for i in range(number_f):
            try:
                with open(choosefile[i]) as im:
                    r = os.path.splitext(choosefile[i])
                    var = (os.path.basename(r[0]), r[1])

                    if filename == 0:
                        folder = os.getcwd() + '/Edited photos/'
                        output_name = folder + var[0] + rename() + var[1]
                        scale_image(input_image_path=choosefile[i],
                            output_image_path=output_name,
                            height=fl.cm_in_px(message_cm.get()))

                        if ismarried.get() == 1:
                            image = Image.open(output_name)
                            if image.mode == 'RGBA':
                                r, g, b, a = image.split()
                                rgb_image = Image.merge('RGB', (r, g, b))
                                inverted_image = PIL.ImageOps.invert(rgb_image)
                                r2, g2, b2 = inverted_image.split()
                                final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))
                                final_transparent_image.save(output_name)
                            else:
                                inverted_image = PIL.ImageOps.invert(image)
                                inverted_image.save(output_name)

                    else:
                        folder = filename
                        output_name = filename + '/' + var[0] + rename() + var[1]
                        scale_image(input_image_path=choosefile[i],
                            output_image_path = output_name,
                            height=fl.cm_in_px(message_cm.get()))

                        if ismarried.get() == 1:
                            image = Image.open(output_name)
                            if image.mode == 'RGBA':
                                r, g, b, a = image.split()
                                rgb_image = Image.merge('RGB', (r, g, b))
                                inverted_image = PIL.ImageOps.invert(rgb_image)
                                r2, g2, b2 = inverted_image.split()
                                final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))
                                final_transparent_image.save(output_name)
                            else:
                                inverted_image = PIL.ImageOps.invert(image)
                                inverted_image.save(output_name)
                    print("Çhose",choosefile[0])
            except:
                print('Error')
                messagebox.showerror("Error", "An error has occurred.\n\nThe program is intended for image processing only.\n\nContact the e-mail address:\nolehlastovetskyi99@gmail.com")
                quit()
        messagebox.showinfo("Message", "Completed!\nChanged {} files.\nFiles saved in the directory:\n{}".format(number_f, folder))
#----------------------------------------------------------------------------------------------------------------------#

##--------------------------------------------------------------------------------------------------------------------##

window = Tk()
ismarried = IntVar(value= 2)
ismarried.set(0)
ismarried2 = IntVar(value= 2)
ismarried2.set(0)
chek_cb2()
rename()
##------------------------------------------------------------------------------------------------------------------------##

start_pos_x = 10
start_pos_y = 10


height_button = 2
width_button = 32

font_button = ("Arial Bold", 11)
font_checkbox = ("Arial", 11)
font_combobox = ('Arial', 11)
font_label = ("Arial Bold", 11)
step_des = 60

label_folder()
label_file()

window.title("Scale")

btn_dialogOpen = Button(window, text="Image files", command=clicked_dialogOpen, height=height_button,
                        width=width_button, font=font_button)
btn_dialogOpen.place(x=start_pos_x, y=start_pos_y)

btn_browsebutton = Button(window, text="Save in folder", command=browse_button, height=height_button,
                          width=width_button, font=font_button)

btn_browsebutton.place(x=start_pos_x, y=start_pos_y + step_des + 25)

lbl = Label(window, text="Image height (cm):", font=font_label)
lbl.place(x=start_pos_x + 1, y=start_pos_y + step_des * 2.95)

message_cm = Entry(width=7)
message_cm.place(x=start_pos_x + 150, y=start_pos_y + step_des * 2.97)
message_cm.insert(0, "9.8")

ismarried_checkbutton = Checkbutton(text="Invert color", variable=ismarried, font =font_checkbox)
ismarried_checkbutton.place(x=start_pos_x + 1, y=start_pos_y + step_des * 3.4)

ismarried_checkbutton2 = Checkbutton(text="Rename the file", variable=ismarried2,
                                     font = font_checkbox, command = chek_cb2)
ismarried_checkbutton2.place(x=start_pos_x + 170, y=start_pos_y + step_des * 3.4)

btn_scale = Button(window, text="Convert", command=scale, height=height_button, width=width_button,
                   font=font_button, state = NORMAL)

btn_scale.place(x=start_pos_x, y=start_pos_y + step_des * 5.2)

Label(window, text='Github:', font=('Arial', 8)).place(x=10, y=385)

x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
window.wm_geometry("+%d+%d" % (x, y))

window.maxsize(320,410)
window.minsize(320,410)
window.resizable(0, 0)

window.mainloop()
