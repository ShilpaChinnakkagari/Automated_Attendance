from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import webbrowser
class StudyPortal:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Study Portal")
        self.root.state('zoomed')
        
        #Heading Image
        img = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\studyportal.jpg")
        img = img.resize((790,130),Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=790,height=130)


        #Heading Image
        img1 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\attendance_file.jpg")
        img1 = img1.resize((790,130),Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root,image=self.photoimg1)
        f_lbl.place(x=790,y=0,width=790,height=130)

        title_lbl = Label(self.root,text = "Madanapalle Institute of Technology & Science",font=("arial",33,"bold"),bg="skyblue",fg="black")
        title_lbl.place(x=0,y=130,width=1530,height=45)


        #Background Image
        img3 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\bg2.jpg")
        img3 = img3.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=175,width=1530,height=710)

        '''title_lbl = Label(bg_img,text = "WELCOME",font=("times new roman",35,"bold"),bg="blue",fg="white")
        title_lbl.place(x=0,y=0,width=1530,height=45)'''

        #Student Button
        img4 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\student_icon.jpg")
        img4 = img4.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img,image=self.photoimg4,cursor="hand2")
        b1.place(x=360,y=150,width=220,height=220)

        b1_1 = Button(bg_img,text="Study Portal",cursor="hand2",font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=360,y=360,width=220,height=40)


        #Detect Face Button
        img5 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\studyimg.jpg")
        img5 = img5.resize((220,220),Image.Resampling.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)

        b1 = Button(bg_img,image=self.photoimg5,cursor="hand2",command=self.mits_moodle)
        b1.place(x=800,y=150,width=220,height=220)

        b1_1 = Button(bg_img,text="MITS-Moodle",cursor="hand2",command=self.mits_moodle,font=("times new roman",11,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=800,y=360,width=220,height=40)
        
    def mits_moodle(self):
        webbrowser.open('http://20.0.121.215/')



if  __name__ == "__main__":
    root = Tk()
    obj=StudyPortal(root)
    root.mainloop()