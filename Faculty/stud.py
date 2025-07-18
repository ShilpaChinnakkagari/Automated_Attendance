from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x650")
        self.root.state('zoomed')
        self.root.title("Face Recognition System")
        self.root.configure(bg="white")


        
        title_lbl = Label(root, text="STUDENT MANAGEMENT SYSTEM", font=("times new roman", 35, "bold"), bg="blue", fg="white")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = Frame(root, bd=2, bg="white")
        main_frame.place(x=20, y=50, width=1480, height=680)

        # Right Side Label Frame (only frame now)
        Right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Details", 
                               font=("times new roman", 12, "bold"))
        Right_frame.place(x=10, y=10, width=1460, height=700)

        img_right = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\right_frame.png")
        img_right = img_right.resize((1450, 130), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl = Label(Right_frame, image=self.photoimg_right)
        f_lbl.place(x=5, y=0, width=1450, height=130)

        # ========================Search System========================
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

        # ========================Table Frame========================
        Table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        Table_frame.place(x=5, y=210, width=1440, height=420)

        scroll_x = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_frame, orient=VERTICAL)
        
        self.Student_table = ttk.Treeview(Table_frame, columns=(
            "Department", "Course", "Year", "Semester", "StudentID", "StudentName", "AdharNo", 
            "Gender", "Sec", "DOB", "MobileNo", "Address", "Mentor", "CollegeMail", "photo"), 
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        self.Student_table.heading("Department", text="Department")
        self.Student_table.heading("Course", text="Course")
        self.Student_table.heading("Year", text="Year")
        self.Student_table.heading("Semester", text="Semester")
        self.Student_table.heading("StudentID", text="Student ID")
        self.Student_table.heading("StudentName", text="Student Name")
        self.Student_table.heading("AdharNo", text="Adhar No.")
        self.Student_table.heading("Gender", text="Gender")
        self.Student_table.heading("Sec", text="Section")
        self.Student_table.heading("DOB", text="DOB")
        self.Student_table.heading("MobileNo", text="Mobile No.")
        self.Student_table.heading("Address", text="Address")
        self.Student_table.heading("Mentor", text="Mentor")
        self.Student_table.heading("CollegeMail", text="College Mail")
        self.Student_table.heading("photo", text="Photo Sample Status")
        self.Student_table["show"] = "headings"

        self.Student_table.column("Department", width=100)
        self.Student_table.column("Course", width=100)
        self.Student_table.column("Year", width=100)
        self.Student_table.column("Semester", width=100)
        self.Student_table.column("StudentID", width=100)
        self.Student_table.column("StudentName", width=100)
        self.Student_table.column("AdharNo", width=100)
        self.Student_table.column("Gender", width=100)
        self.Student_table.column("Sec", width=100)
        self.Student_table.column("DOB", width=100)
        self.Student_table.column("MobileNo", width=100)
        self.Student_table.column("Address", width=100)
        self.Student_table.column("Mentor", width=100)
        self.Student_table.column("CollegeMail", width=100)
        self.Student_table.column("photo", width=150)

        self.Student_table.pack(fill=BOTH, expand=1)
        self.fetch_data()

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", 
                                      password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.Student_table.delete(*self.Student_table.get_children())
            for i in data:
                self.Student_table.insert("", END, values=i)
            conn.commit()
        conn.close()

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

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()