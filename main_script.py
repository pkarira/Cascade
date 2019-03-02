from Tkinter import *
import Tkinter
import tkMessageBox
from PIL import ImageTk, Image
import tkFileDialog as filedialog
from tkMessageBox import showerror
import shutil
from crop_microstructure import cropper
from enumerate_ import enumerater
from feature_map import feature_generater
from classification import classifier
import os
import glob
from threading import Timer
import time

class BusyManager:

    def __init__(self, widget):
        self.toplevel = widget.winfo_toplevel()
        self.widgets = {}

    def busy(self, widget=None):

        if widget is None:
            w = self.toplevel # myself
        else:
            w = widget

        if not self.widgets.has_key(str(w)):
            try:
                # attach cursor to this widget
                cursor = w.cget("cursor")
                if cursor != "watch":
                    self.widgets[str(w)] = (w, cursor)
                    w.config(cursor="watch")
            except TclError:
                pass

        for w in w.children.values():
            self.busy(w)

    def notbusy(self):
        # restore cursors
        for w, cursor in self.widgets.values():
            try:
                w.config(cursor=cursor)
            except TclError:
                pass
        self.widgets = {}

def cursor_busy():
    root.config(cursor="wait")

def cursor_notbusy():
    root.config(cursor="")

def clear_files(folder):
	for the_file in os.listdir(folder):
	    file_path = os.path.join(folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception as e:
	        print(e)

def select_image():
	result_update.delete(0, 'end')
	clear_files('/home/pulkit/Desktop/btp_software/data/micrographs_new')
	clear_files('/home/pulkit/Desktop/btp_software/data/crops_new')
	fname = filedialog.askopenfilename(filetypes=(("All files", "*.*"),("Template files", "*.tplate"),("HTML files", "*.html;*.htm")))
	if fname:
		try:
			microstructure = Image.open(fname)
			microstructure = microstructure.resize((200,200), Image.ANTIALIAS)
			microstructure = ImageTk.PhotoImage(microstructure)
			panel.configure(image=microstructure)
			panel.image = microstructure
			shutil.copy(fname, "data/micrographs_new/")
			#result_update.insert(0,"Processing...")
		except:                     # <- naked except is a bad idea
			showerror("Open Source File", "Failed to read file")
		return
def final_result():
	cropper()
	enumerater()
	feature_generater()
	result = classifier()
	result_update.delete(0, 'end')
	result_update.insert(0,result[0])
	manager.notbusy()

def get_result():
	manager.busy()
	result_update.insert(0,"Processing...")
	final_result()

root = Tkinter.Tk()
root.geometry('500x300')
#root.configure(background='white')
root.title('Microstructure Classifier')

frame = Frame(root)
frame.pack(side = LEFT)

leftframe = Frame(root)
leftframe.pack( side = LEFT )


image = Image.open("white.png")
image = image.resize((200,200), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)

panel = Label(frame, image = image)
panel.pack(anchor=NW,padx=20,pady=10); 
select_image_button=Button(frame, text ="Select Microstructure",bg="white",command = select_image)
select_image_button.pack(anchor=SW,padx=40,pady=10)
result_update = Entry(leftframe, bd =5)
result_update.pack(anchor=SE,padx=70,pady=10)
result = Button(leftframe, text="Get Results",bg="white",command = get_result)
result.pack(anchor=NE,padx=80,pady=10);
copyright = Label(frame,text="@copyright MMED,IIT Roorkee")
copyright.pack(anchor=NW,side=BOTTOM)

manager = BusyManager(root)
root.mainloop()