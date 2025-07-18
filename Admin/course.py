from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from tkinter import filedialog

class Course:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Management System")
        self.root.geometry("1530x790+0+0")
        self.root.config(bg="white")
        self.root.state('zoomed')
        #======vbls=========
        self.var_year=StringVar()
        self.var_semester = StringVar()
        self.var_department = StringVar()

        # Variables
        self.var_courseCode = StringVar()
        self.var_courseName = StringVar()
        self.var_facultyID = StringVar()
        self.var_facultyName = StringVar()
        self.var_facultyMail = StringVar()
        self.var_filepath = StringVar()

        # Icons
        logo_dash = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Student Result Management\images\College_Logo.jpg")
        logo_dash = logo_dash.resize((70, 70), Image.Resampling.LANCZOS)
        self.logo_dash = ImageTk.PhotoImage(logo_dash)

        # Title
        title = Label(self.root, text="Course Management System", padx=10, compound=LEFT, image=self.logo_dash,
                      font=("lucida", 20, "bold","italic"), bg="red", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)

        
        self.bg_img = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\bg2.jpg")
        self.bg_img = self.bg_img.resize((1530, 700), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.bg_lbl = Label(self.root, image=self.bg_img)
        self.bg_lbl.place(x=0, y=70, width=1530, height=700)

        # Menu Frame
        mainframe = LabelFrame(self.bg_lbl, text="Menu", font=("times new roman", 15, "bold"), bg="azure", fg="black")
        mainframe.place(x=100, y=50, width=350, height=240)

        year_label = Label(mainframe,text="Year",font=("times new roman",12,"bold"),bg="white")
        year_label.grid(row=1,column=0,padx=10,sticky=W)

        year_combo = ttk.Combobox(mainframe,cursor="hand2" ,textvariable=self.var_year, font=("times new roman", 12, "bold"), width=20, state="readonly")
        year_combo["values"]=("Select Year","1","2","3","4")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)

        sem_combo = Label(mainframe,text="Semester",font=("times new roman",12,"bold"),bg="white")
        sem_combo.grid(row=2,column=0,padx=10,sticky=W)

        sem_combo = ttk.Combobox(mainframe, textvariable=self.var_semester,cursor="hand2", font=("times new roman", 12, "bold"), width=20, state="readonly")
        sem_combo["values"]=("Select Sem","1","2")
        sem_combo.current(0)
        sem_combo.grid(row=2,column=1,padx=2,pady=10,sticky=W)

        dep_label = Label(mainframe,text="Department",font=("times new roman",12,"bold"),bg="white")
        dep_label.grid(row=3,column=0,padx=10,sticky=W)

        dep_combo = ttk.Combobox(mainframe, textvariable=self.var_department,font=("times new roman", 12, "bold"), width=20, state="readonly")
        dep_combo["values"]=("Select Department","CAI","CSE","CST","CSC","CST","CSD","CSN","Mech","civil","MBA","MCA","B.Sc.","BBA")
        dep_combo.current(0)
        dep_combo.grid(row=3,column=1,padx=2,pady=10,sticky=W)

        lbl_syllabus = Label(mainframe, text="Syllabus Copy", font=("goudy old style", 15, "bold"), bg="white")
        lbl_syllabus.grid(row=4,column=0,padx=2,pady=10,sticky=W)
        btn_syllabus = Button(mainframe, text="Upload File",command=self.upload_file,cursor="hand2", font=("goudy old style", 12), bg="lightblue")
        btn_syllabus.grid(row=4,column=1,padx=2,pady=10,sticky=W)

        #Course frame

        mainframe2 = LabelFrame(self.bg_lbl, text="Manage course details", font=("times new roman", 15, "bold"), bg="azure", fg="black")
        mainframe2.place(x=550, y=5, width=600, height=280)

        lbl_courseCode = Label(mainframe2, text="Course code", font=("goudy old style", 15, "bold"), bg="white")
        lbl_courseCode.grid(row=0,column=0,padx=2,pady=10,sticky=W)
        txt_courseCode = Entry(mainframe2, textvariable=self.var_courseCode, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_courseCode.grid(row=0,column=1,padx=2,pady=10,sticky=W)
        
        lbl_courseName = Label(mainframe2, text="Course name", font=("goudy old style", 15, "bold"), bg="white")
        lbl_courseName.grid(row=1,column=0,padx=2,pady=10,sticky=W)
        txt_courseName = Entry(mainframe2, textvariable=self.var_courseName, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_courseName.grid(row=1,column=1,padx=2,pady=10,sticky=W)
        
        lbl_facultyID= Label(mainframe2, text="faculty id", font=("goudy old style", 15, "bold"), bg="white")
        lbl_facultyID.grid(row=2,column=0,padx=2,pady=10,sticky=W)
        txt_facultyID = Entry(mainframe2, textvariable=self.var_facultyID, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_facultyID.grid(row=2,column=1,padx=2,pady=10,sticky=W)

        lbl_facultyName= Label(mainframe2, text="faculty name", font=("goudy old style", 15, "bold"), bg="white")
        lbl_facultyName.grid(row=3,column=0,padx=2,pady=10,sticky=W)
        txt_facultyName = Entry(mainframe2, textvariable=self.var_facultyName, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_facultyName.grid(row=3,column=1,padx=2,pady=10,sticky=W)

        lbl_facultyMail= Label(mainframe2, text="faculty mail", font=("goudy old style", 15, "bold"), bg="white")
        lbl_facultyMail.grid(row=4,column=0,padx=2,pady=10,sticky=W)
        txt_facultyMail= Entry(mainframe2, textvariable=self.var_facultyMail, font=("goudy old style", 15, "bold"), bg="lightyellow")
        txt_facultyMail.grid(row=4,column=1,padx=2,pady=10,sticky=W)
        
        

        

        #update,delete,reset
        save_btn = Button(self.bg_lbl,text="Save",width=20,command=self.add_data,cursor="hand2",font=("times new roman",15,"bold"),bg="red",fg="white")
        save_btn.place(x=1170, y=30, width=70, height=35)

        update_btn = Button(self.bg_lbl,text="Update",width=20,command=self.update_data,cursor="hand2",font=("times new roman",15,"bold"),bg="red",fg="white")
        update_btn.place(x=1170, y=80, width=70, height=35)

        delete_btn = Button(self.bg_lbl,text="Delete",width=20,command=self.delete_data,cursor="hand2",font=("times new roman",15,"bold"),bg="red",fg="white")
        delete_btn.place(x=1170, y=130, width=70, height=35)

        reset_btn = Button(self.bg_lbl,text="Reset",width=20,command=self.reset_data,cursor="hand2",font=("times new roman",15,"bold"),bg="red",fg="white")
        reset_btn.place(x=1170, y=180, width=70, height=35)

        #==============table frame================

        # Title
        title = Label(self.bg_lbl, text="Course Details",cursor="hand2", font=("goudy old style", 20, "bold"), bg="#033054", fg="white")
        title.place(x=0, y=300, width=1520, height=35)

        mainframe3 = LabelFrame(self.bg_lbl, text="Course details", font=("times new roman", 15, "bold"), bg="azure", fg="black")
        mainframe3.place(x=35, y=345, width=1450, height=360)

        Table_frame = Frame(mainframe3,bd=2,bg="white",relief=RIDGE)
        Table_frame.place(x=0,y=0,width=1450,height=360)

        scroll_x=ttk.Scrollbar(Table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(Table_frame,orient=VERTICAL)
        self.Course_table=ttk.Treeview(Table_frame,column=("year","semester","department","courseCode","courseName","facultyID","facultyName","facultyMail","filepath"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Course_table.xview)
        scroll_y.config(command=self.Course_table.yview)

        self.Course_table.heading("year",text="Year")
        self.Course_table.heading("semester",text="Semester")
        self.Course_table.heading("department",text="Department")
        self.Course_table.heading("courseCode",text="course code")
        self.Course_table.heading("courseName",text="course name")
        self.Course_table.heading("facultyID",text="faculty ID")
        self.Course_table.heading("facultyName",text="faculty Name")
        self.Course_table.heading("facultyMail",text="faculty Mail")
        self.Course_table.heading("filepath",text="syllabus copy")
        self.Course_table["show"]="headings"

        self.Course_table.column("year",width=100)
        self.Course_table.column("semester",width=100)
        self.Course_table.column("department",width=100)
        self.Course_table.column("courseCode",width=100)
        self.Course_table.column("courseName",width=100)
        self.Course_table.column("facultyID",width=100)
        self.Course_table.column("facultyName",width=100)
        self.Course_table.column("facultyMail",width=100)
        self.Course_table.column("filepath",width=100)

        self.Course_table.pack(fill=BOTH,expand=1)
        self.Course_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()


    #========fun call===========
    def add_data(self):
        if self.var_department.get() == "Select Department" or self.var_courseCode.get() == "" or self.var_facultyID.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into course values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_department.get(),
                    self.var_courseCode.get(),
                    self.var_courseName.get(),
                    self.var_facultyID.get(),
                    self.var_facultyName.get(),
                    self.var_facultyMail.get(),
                    self.var_filepath.get()  # Include the file path
                ))
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Course Details Have been added Successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to : {str(es)}", parent=self.root)

    '''def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from course")
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.Course_table.delete(*self.Course_table.get_children())
            for i in data:
                # Insert data into the table
                self.Course_table.insert("", END, values=i)
            
                # Add a button in the last column
                self.add_button_to_row(i[-1])  # Pass the filepath to the button
            conn.commit()
        conn.close()

    def add_button_to_row(self, filepath):
        # Get the last inserted row ID
        last_row_id = self.Course_table.get_children()[-1]
    
        # Create a button for the last column
        btn = Button(self.Course_table, text="Open File", cursor="hand2", command=lambda f=filepath: self.open_file(f))
        btn.configure(width=10, bg="lightblue", fg="black")
    
        # Place the button in the last column of the row
        self.Course_table.set(last_row_id, "filepath", btn)'''
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from course")
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.Course_table.delete(*self.Course_table.get_children())
            for i in data:
                # Insert data into the table
                self.Course_table.insert("", END, values=i)
            
                # Add a button in the last column
                self.add_button_to_row(i[-1])  # Pass the filepath to the button
            conn.commit()
        conn.close()

    def add_button_to_row(self, filepath):
        # Get the last inserted row ID
        last_row_id = self.Course_table.get_children()[-1]
    
        # Get the bounding box of the last column
        bbox = self.Course_table.bbox(last_row_id, column="filepath")
    
        if bbox:  # Ensure the bounding box is valid
            # Create a button for the last column
            btn = Button(self.Course_table, text="Open File", cursor="hand2", command=lambda f=filepath: self.open_file(f))
            btn.configure(width=10, bg="lightblue", fg="black")
        
            # Place the button in the last column of the row
            btn.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

    def open_file(self, filepath):
        if filepath:
            try:
                import os
                os.startfile(filepath)  # Open the file using the default application
            except Exception as es:
                messagebox.showerror("Error", f"Unable to open file: {str(es)}", parent=self.root)
        else:
            messagebox.showwarning("Warning", "No file path found.", parent=self.root)

    
    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a Syllabus File", filetypes=[("PDF Files", "*.pdf"), ("Word Documents", "*.docx"), ("All Files", "*.*")])
        if file_path:
            self.var_filepath.set(file_path)
            messagebox.showinfo("File Selected", f"Syllabus file selected: {file_path}")

    def get_cursor(self,event=""):
        cursor_focus=self.Course_table.focus()
        content=self.Course_table.item(cursor_focus)
        data=content["values"]
        self.var_year.set(data[0])
        self.var_semester.set(data[1])
        self.var_department.set(data[2])
        self.var_courseCode.set(data[3])
        self.var_courseName.set(data[4])
        self.var_facultyID.set(data[5])
        self.var_facultyName.set(data[6])
        self.var_facultyMail.set(data[7])
        self.var_filepath.set(data[8])

    
    def update_data(self):        
        if self.var_department.get() == "Select Department" or self.var_courseCode.get() == "" or self.var_facultyID.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Update","Do You Want To Update This Cousre Details",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="vnsvb",database="face_recognition")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update course set year=%s,semester=%s,department=%s,courseName=%s,facultyID=%s,facultyName=%s,facultyMail=%s,filepath=%s where courseCode=%s",(
                                                                                        self.var_year.get(),
                                                                                           self.var_semester.get(),
                                                                                           self.var_department.get(),
                                                                                           self.var_courseName.get(),
                                                                                           self.var_facultyID.get(),
                                                                                           self.var_facultyName.get(),
                                                                                           self.var_facultyMail.get(),
                                                                                           self.var_filepath.get(),
                                                                                           self.var_courseCode.get()
                                                                                         
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Sucesss","Course details Update Completed Successfully",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.root)

    ########### Delete Function #################
    def delete_data(self):
        if self.var_courseCode.get()=="":
            messagebox.showerror("Error","Course Code must be required",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Course Delete Page","Do you Want To Delete This Course",parent=self.root)
                if delete>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="vnsvb",database="face_recognition")
                    my_cursor = conn.cursor()
                    sql="delete from course where courseCode=%s"
                    val=(self.var_courseCode.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete ","Successfully deleted",parent=self.root)
                for record in self.Course_table.get_children():
                    self.Course_table.delete(record)
                    self.fetch_data()
                    self.reset_data()
                    

            except Exception as es:
                messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.root)

    def reset_data(self):
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_department.set("Select Department")
        self.var_courseCode.set("")
        self.var_courseName.set("")
        self.var_facultyID.set("")
        self.var_facultyName.set("")
        self.var_facultyMail.set("")
        self.var_filepath.set("")
        


if __name__ == "__main__":
    root = Tk()
    obj = Course(root)
    root.mainloop()

