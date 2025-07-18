from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

class Developer:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Developer")
        self.root.state('zoomed')

        title_lbl = Label(self.root,text = "DEVELOPER",font=("times new roman",35,"bold"),bg="blue",fg="white")
        title_lbl.place(x=0,y=0,width=1530,height=45)

        img_top = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\Dev_file.jpg")
        img_top = img_top.resize((1530,790),Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=1530,height=720)

        #Frame
        main_frame = Frame(f_lbl,bd=2,bg="white")
        main_frame.place(x=50,y=0,width=500,height=600)

        img_top1 = Image.open(r"C:\Users\chinn\OneDrive\Pictures\Shilpa  pic.jpg")
        img_top1 = img_top1.resize((125,200),Image.Resampling.LANCZOS)
        self.photoimg_top1 = ImageTk.PhotoImage(img_top1)

        f_lbl = Label(main_frame,image=self.photoimg_top1)
        f_lbl.place(x=300,y=0,width=200,height=200)

        #Developer info
        dev_label = Label(main_frame,text="Hello, I'm C.Shilpa",font=("times new roman",12,"bold"),bg="white")
        dev_label.grid(row=0, column=0, padx=5, pady=5)

        dev_label1 = Label(main_frame,text="I am an AI Student in MITS-Madanapalle..",font=("times new roman",14,"bold"),bg="white")
        dev_label1.grid(row=1, column=0, padx=5, pady=5)

        img2 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\Developer.jpg")
        img2 = img2.resize((500,400),Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(main_frame,image=self.photoimg2)
        f_lbl.place(x=0,y=210,width=500,height=390)




if  __name__ == "__main__":
    root = Tk()
    obj=Developer(root)
    root.mainloop()