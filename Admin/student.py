from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

#from train import Train

import os
import numpy as np


class Student:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")


        ##############variables################
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_sec=StringVar()
        self.var_adhar=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_mentor=StringVar()

        #First Image
        img = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\student_pic.jpg")
        img = img.resize((550,130),Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)

        #Second Image
        img1 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\pic_student.jpg")
        img1 = img1.resize((550,130),Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)

         #Third Image
        img2 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\student_pic.jpg")
        img2 = img2.resize((550,130),Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=558,height=130)

        #Background Image
        img3 = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\College_Logo.jpg")
        img3 = img3.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        title_lbl = Label(bg_img,text = "STUDENT MANAGEMENT S/M",font=("times new roman",35,"bold"),bg="blue",fg="white")
        title_lbl.place(x=0,y=0,width=1530,height=45)

        main_frame = Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=20,y=50,width=1480,height=600)

        #Left Side Label Frame
        Left_frame = LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=730,height=580)

        img_left = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\student_details.jpg")
        img_left = img_left.resize((720,130),Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl = Label(Left_frame,image=self.photoimg_left)
        f_lbl.place(x=5,y=0,width=720,height=130)


        #Current Course
        current_course_frame = LabelFrame(Left_frame,bd=2,relief=RIDGE,text="Course Information",font=("times new roman",12,"bold"))
        current_course_frame.place(x=5,y=135,width=720,height=150)
        
        #Department
        dep_label = Label(current_course_frame,text="Department",font=("times new roman",12,"bold"),bg="white")
        dep_label.grid(row=0,column=0,padx=10,sticky=W)

        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep,font=("times new roman", 12, "bold"), width=20, state="readonly")
        dep_combo["values"]=("Select Department","CAI","CSE","CST","CSC","CST","CSD","CSN","Mech","civil","MBA","MCA","B.Sc.","BBA")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        #Course
        course_label = Label(current_course_frame,text="Course",font=("times new roman",12,"bold"),bg="white")
        course_label.grid(row=0,column=2,padx=10,sticky=W)

        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course,font=("times new roman", 12, "bold"), width=20, state="readonly")
        course_combo["values"]=("Select Course","UG","Degree","PG")
        course_combo.current(0)
        course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)

        #YEAR
        year_label = Label(current_course_frame,text="Year",font=("times new roman",12,"bold"),bg="white")
        year_label.grid(row=1,column=0,padx=10,sticky=W)

        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("times new roman", 12, "bold"), width=20, state="readonly")
        year_combo["values"]=("Select Year","1","2","3","4")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)

        #SEMESTER
        semester_label = Label(current_course_frame,text="Semester",font=("times new roman",12,"bold"),bg="white")
        semester_label.grid(row=1,column=2,padx=10,sticky=W)

        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("times new roman", 12, "bold"), width=20, state="readonly")
        semester_combo["values"]=("Select Semester","1","2")
        semester_combo.current(0)
        semester_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)

        #Class Student Information
        class_Student_frame = LabelFrame(Left_frame,bd=2,relief=RIDGE,text="Class Student Information",font=("times new roman",12,"bold"))
        class_Student_frame.place(x=5,y=250,width=720,height=300)

        
        #Student ID Info
        studentID_label = Label(class_Student_frame,text="Student ID: ",font=("times new roman",12,"bold"),bg="white")
        studentID_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        studentID_entry=ttk.Entry(class_Student_frame, textvariable=self.var_std_id,width=20,font=("times new roman",12,"bold"))
        studentID_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)

        #Student Name
        studentName_label = Label(class_Student_frame,text="Student Name: ",font=("times new roman",12,"bold"),bg="white")
        studentName_label.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        studentName_entry=ttk.Entry(class_Student_frame, textvariable=self.var_std_name,width=20,font=("times new roman",12,"bold"))
        studentName_entry.grid(row=0,column=3,padx=10,pady=5,sticky=W)

        #class Division
        class_div_label = Label(class_Student_frame,text="Sec: ",font=("times new roman",12,"bold"),bg="white")
        class_div_label.grid(row=1,column=0,padx=10,pady=5,sticky=W)

        class_div_entry=ttk.Entry(class_Student_frame, textvariable=self.var_sec,width=20,font=("times new roman",12,"bold"))
        class_div_entry.grid(row=1,column=1,padx=10,pady=5,sticky=W)

        #Adhar No.
        adhar_no_label = Label(class_Student_frame,text="Adhar No.: ",font=("times new roman",12,"bold"),bg="white")
        adhar_no_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)

        adhar_no_entry=ttk.Entry(class_Student_frame, textvariable=self.var_adhar,width=20,font=("times new roman",12,"bold"))
        adhar_no_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)

        #Gender
        '''gender_label = Label(class_Student_frame,text="Gender: ",font=("times new roman",12,"bold"),bg="white")
        gender_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)

        gender_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",12,"bold"))
        gender_entry.grid(row=2,column=1,padx=10,pady=5,sticky=W)'''
        gender_label = Label(class_Student_frame,text="Gender",font=("times new roman",12,"bold"),bg="white")
        gender_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)

        gender_combo = ttk.Combobox(class_Student_frame,  textvariable=self.var_gender,font=("times new roman", 12, "bold"), width=18, state="readonly")
        gender_combo["values"]=("Select Gender","F","M","Others")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=10,pady=5,sticky=W)

        #DOB
        dob_label = Label(class_Student_frame,text="DOB: ",font=("times new roman",12,"bold"),bg="white")
        dob_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)

        dob_entry=ttk.Entry(class_Student_frame, textvariable=self.var_dob,width=20,font=("times new roman",12,"bold"))
        dob_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)

        #Email
        email_label = Label(class_Student_frame,text="College Mail: ",font=("times new roman",12,"bold"),bg="white")
        email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)

        email_entry=ttk.Entry(class_Student_frame, textvariable=self.var_email,width=20,font=("times new roman",12,"bold"))
        email_entry.grid(row=3,column=1,padx=10,pady=5,sticky=W)

        #Phone No.
        phone_label = Label(class_Student_frame,text="Mobile No. : ",font=("times new roman",12,"bold"),bg="white")
        phone_label.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        phone_entry=ttk.Entry(class_Student_frame, textvariable=self.var_phone,width=20,font=("times new roman",12,"bold"))
        phone_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)

        #Address
        address_label = Label(class_Student_frame,text="Address: ",font=("times new roman",12,"bold"),bg="white")
        address_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)

        address_entry=ttk.Entry(class_Student_frame, textvariable=self.var_address,width=20,font=("times new roman",12,"bold"))
        address_entry.grid(row=4,column=1,padx=10,pady=5,sticky=W)

        #Mentor
        mentor_label = Label(class_Student_frame,text="Mentor: ",font=("times new roman",12,"bold"),bg="white")
        mentor_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        mentor_entry=ttk.Entry(class_Student_frame, textvariable=self.var_mentor,width=20,font=("times new roman",12,"bold"))
        mentor_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)

        #Radio Buttons
        self.var_radio1=StringVar()
        radiobtn1=ttk.Radiobutton(class_Student_frame,variable=self.var_radio1,text="take Photo Sample",value="YES")
        radiobtn1.grid(row=6,column=0)

        self.var_radio2=StringVar()
        radiobtn2=ttk.Radiobutton(class_Student_frame,variable=self.var_radio1,text="No Photo Sample",value="NO")
        radiobtn2.grid(row=6,column=1)

        #Button Frame

        btn_frame = Frame(class_Student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=200,width=715,height=35)

        save_btn = Button(btn_frame,text="Save",command=self.add_data,width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        update_btn = Button(btn_frame,text="Update",command=self.update_data,width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        delete_btn = Button(btn_frame,text="Delete",command=self.delete_data,width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        reset_btn = Button(btn_frame,text="Reset",command=self.reset_data,width=20,font=("times new roman",12,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        btn_frame1 = Frame(class_Student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame1.place(x=0,y=235,width=715,height=35)

        take_photo_btn = Button(btn_frame1,command=self.generate_dataset,text="Take Photo Sample",width=27,font=("times new roman",12,"bold"),bg="blue",fg="white")
        take_photo_btn.grid(row=0,column=0)

        update_photo_btn = Button(btn_frame1,text="Update Photo Sample",width=27,font=("times new roman",12,"bold"),bg="blue",fg="white")
        update_photo_btn.grid(row=0,column=1)

        train_btn = Button(btn_frame1, text="Train", command=self.train_classifier, width=26, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        train_btn.grid(row=0, column=2)
        
        # Create a frame for the buttons
        btn_frame1 = Frame(root)
        btn_frame1.pack()
        
        # Create a "Train" button and assign the train_classifier method to the button's command

        

        #Right Side Label Frame
        Right_frame = LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
        Right_frame.place(x=750,y=10,width=720,height=580)

        img_right = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\right_frame.png")
        img_right = img_right.resize((720,130),Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl = Label(Right_frame,image=self.photoimg_right)
        f_lbl.place(x=5,y=0,width=720,height=130)

        #****************SEARCH SYSTEM****************
        Search_frame = LabelFrame(Right_frame, bd=2, relief=RIDGE, text="Search System", 
                                font=("times new roman", 12, "bold"))
        Search_frame.place(x=5, y=135, width=1440, height=70)

        Search_label = Label(Search_frame, text="Search By:", font=("times new roman", 15, "bold"), 
                           bg="red", fg="white")
        Search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.search_combo = ttk.Combobox(Search_frame, font=("times new roman", 12, "bold"), 
                                       width=15, state="readonly")
        self.search_combo["values"] = ("Select", "StudentID", "Department")
        self.search_combo.current(0)
        self.search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        self.search_entry = ttk.Entry(Search_frame, width=15, font=("times new roman", 12, "bold"))
        self.search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        Search_btn = Button(Search_frame, text="Search", width=12, font=("times new roman", 12, "bold"), 
                          bg="blue", fg="white", command=self.search_data)
        Search_btn.grid(row=0, column=3, padx=4)

        showAll_btn = Button(Search_frame, text="Show All", width=12, font=("times new roman", 12, "bold"), 
                           bg="blue", fg="white", command=self.fetch_data)
        showAll_btn.grid(row=0, column=4, padx=4)

        
        #========================table frame===============
        Table_frame = Frame(Right_frame,bd=2,bg="white",relief=RIDGE)
        Table_frame.place(x=5,y=210,width=710,height=350)

        scroll_x=ttk.Scrollbar(Table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(Table_frame,orient=VERTICAL)
        self.Student_table=ttk.Treeview(Table_frame,column=("Department","Course","Year","Semester","StudentID","StudentName","AdharNo","Gender","Sec","DOB","MobileNo","Address","Mentor","CollegeMail","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        self.Student_table.heading("Department",text="Department")
        self.Student_table.heading("Course",text="Course")
        self.Student_table.heading("Year",text="Year")
        self.Student_table.heading("Semester",text="Semester")
        self.Student_table.heading("StudentID",text="Student ID")
        self.Student_table.heading("StudentName",text="Student Name")
        self.Student_table.heading("AdharNo",text="Adhar No.")
        self.Student_table.heading("Gender",text="Gender")
        self.Student_table.heading("Sec",text="Section")
        self.Student_table.heading("DOB",text="DOB")
        self.Student_table.heading("MobileNo",text="Mobile No.")
        self.Student_table.heading("Address",text="Address")
        self.Student_table.heading("Mentor",text="Mentor")
        self.Student_table.heading("CollegeMail",text="College Mail")
        self.Student_table.heading("photo",text="PhotoSampleStatus")
        self.Student_table["show"]="headings"

        self.Student_table.column("Department",width=100)
        self.Student_table.column("Course",width=100)
        self.Student_table.column("Year",width=100)
        self.Student_table.column("Semester",width=100)
        self.Student_table.column("StudentID",width=100)
        self.Student_table.column("StudentName",width=100)
        self.Student_table.column("AdharNo",width=100)
        self.Student_table.column("Gender",width=100)
        self.Student_table.column("Sec",width=100)
        self.Student_table.column("DOB",width=100)
        self.Student_table.column("MobileNo",width=100)
        self.Student_table.column("Address",width=100)
        self.Student_table.column("Mentor",width=100)
        self.Student_table.column("CollegeMail",width=100)
        self.Student_table.column("photo",width=150)

        self.Student_table.pack(fill=BOTH,expand=1)
        self.Student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()



    ################function declaration#################

    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                #messagebox.showinfo("Success","Welcome MITSian")
                conn=mysql.connector.connect(host="localhost",username="root",password="vnsvb",database="face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                           self.var_dep.get(),
                                                                                           self.var_course.get(),
                                                                                           self.var_year.get(),
                                                                                           self.var_semester.get(),
                                                                                           self.var_std_id.get(),
                                                                                           self.var_std_name.get(),
                                                                                           self.var_adhar.get(),
                                                                                           self.var_gender.get(),
                                                                                           self.var_sec.get(),
                                                                                           self.var_dob.get(),
                                                                                           self.var_phone.get(),
                                                                                           self.var_address.get(),
                                                                                           self.var_mentor.get(),
                                                                                           self.var_email.get(),
                                                                                           self.var_radio1.get()
                                                                                        ))
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success","Student Details Have been added Successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to : {str(es)}",parent=self.root)       

    # #######################fetch data#################
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="vnsvb",database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()

        if len(data)!=0:
            self.Student_table.delete(*self.Student_table.get_children())
            for i in data:
                self.Student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    # ######### Gett Cursor################
    def get_cursor(self,event=""):
        cursor_focus=self.Student_table.focus()
        content=self.Student_table.item(cursor_focus)
        data=content["values"]

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_semester.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_adhar.set(data[6])
        self.var_gender.set(data[7])
        self.var_sec.set(data[8])
        self.var_dob.set(data[9])
        self.var_phone.set(data[10])
        self.var_address.set(data[11])
        self.var_mentor.set(data[12])
        self.var_email.set(data[13])
        self.var_radio1.set(data[14])

    ########## Update Function ################
    def update_data(self):        
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Update","Do You Want To Update This Student Detail",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="vnsvb",database="face_recognition")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set Department=%s,Course=%s,Year=%s,Semester=%s,`Student Name`=%s,`Adhar No`=%s,Gender=%s,Section=%s,DOB=%s,`Mobile No`=%s,Address=%s,Mentor=%s,CollegeMail=%s,photo=%s where StudentID=%s",(
                                                                                        self.var_dep.get(),
                                                                                           self.var_course.get(),
                                                                                           self.var_year.get(),
                                                                                           self.var_semester.get(),
                                                                                           self.var_std_name.get(),
                                                                                           self.var_adhar.get(),
                                                                                           self.var_gender.get(),
                                                                                           self.var_sec.get(),
                                                                                           self.var_dob.get(),
                                                                                           self.var_phone.get(),
                                                                                           self.var_address.get(),
                                                                                           self.var_mentor.get(),
                                                                                           self.var_email.get(),
                                                                                           self.var_radio1.get(),
                                                                                           self.var_std_id.get()
                                                                                         
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Sucesss","Student details Update Completed Successfully",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.root)

    ########### Delete Function #################
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","StudentId must be required",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student Delete Page","Do you Want To Delete This Student",parent=self.root)
                if delete>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="vnsvb",database="face_recognition")
                    my_cursor = conn.cursor()
                    sql="delete from student where StudentID=%s"
                    val=(self.var_std_id.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete ","Successfully deleted",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.root)

    ############# Reset ################
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_adhar.set("")
        self.var_gender.set("Select Gender")
        self.var_sec.set("")
        self.var_dob.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_mentor.set("")
        self.var_email.set("")
        self.var_radio1.set("")
        
    ################### Generate data set Take Photo Sample #################
    def generate_dataset(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="vnsvb",database="face_recognition")
                my_cursor = conn.cursor()
            
                # Use the student ID from the form directly
                student_id = self.var_std_id.get()
            
                # Update the student record with photo sample status
                my_cursor.execute("update student set Department=%s,Course=%s,Year=%s,Semester=%s,`Student Name`=%s,`Adhar No`=%s,Gender=%s,Section=%s,DOB=%s,`Mobile No`=%s,Address=%s,Mentor=%s,CollegeMail=%s,photo=%s where StudentID=%s",(
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_adhar.get(),
                    self.var_gender.get(),
                    self.var_sec.get(),
                    self.var_dob.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_mentor.get(),
                    self.var_email.get(),
                    self.var_radio1.get(),
                    student_id
                ))
            
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close() 

                ################### Load pre-defined data on face detection##############
                face_classifier = cv2.CascadeClassifier(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\haarcascade_frontalface_default.xml")

                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)
                    for(x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped
                
                cap = cv2.VideoCapture(0)  #web camera = 0
                img_id = 0
                while True:
                    ret,my_frame = cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id += 1
                        face = cv2.resize(face_cropped(my_frame),(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path = f"data/user.{student_id}.{img_id}.jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Cropped Face",face)

                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Generating dataset completed !!!")
            except Exception as es:
                messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.root)

    def train_classifier(self):
        data_dir = ("data")
        path = [os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids = []

        for image in path:
            img = Image.open(image).convert("L") #Gray scale image
            imageNp = np.array(img,'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Traning data",imageNp)
            cv2.waitKey(1)==13
        ids = np.array(ids)

        ################ tarin the classifier and save ###############
        clf = cv2.face.LBPHFaceRecognizer.create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training dataset completed! ")

    def search_data(self):
        if self.search_combo.get() == "Select":
            messagebox.showerror("Error", "Please select a search option", parent=self.root)
        elif self.search_entry.get() == "":
            messagebox.showerror("Error", "Please enter search term", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", 
                                             password="vnsvb", database="face_recognition")
                my_cursor = conn.cursor()
                
                if self.search_combo.get() == "StudentID":
                    my_cursor.execute("select * from student where StudentID=%s", 
                                    (self.search_entry.get(),))
                elif self.search_combo.get() == "Department":
                    my_cursor.execute("select * from student where Department=%s", 
                                    (self.search_entry.get(),))
                    
                data = my_cursor.fetchall()
                
                if len(data) != 0:
                    self.Student_table.delete(*self.Student_table.get_children())
                    for i in data:
                        self.Student_table.insert("", END, values=i)
                    conn.commit()
                else:
                    messagebox.showinfo("Info", "No records found", parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        

                
if  __name__ == "__main__":
    root = Tk()
    obj=Student(root)
    root.mainloop()