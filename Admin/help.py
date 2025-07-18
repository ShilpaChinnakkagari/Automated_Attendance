from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

class Help:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Developer")

        title_lbl = Label(self.root,text = "HELP DESK",font=("times new roman",35,"bold"),bg="blue",fg="white")
        title_lbl.place(x=0,y=0,width=1530,height=45)

        img_top = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\chat bot.jpg")
        img_top = img_top.resize((1530,790),Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=1530,height=720)

        # Help info
        dev_label = Label(f_lbl, text="Email: chinn@ac.in", font=("times new roman", 17, "bold"), bg="white")
        dev_label.place(x=690,y=290)

        # To make it centered in the grid, set row and column weights
        f_lbl.grid_rowconfigure(12, weight=1)
        f_lbl.grid_columnconfigure(4, weight=1)



if  __name__ == "__main__":
    root = Tk()
    obj=Help(root)
    root.mainloop()