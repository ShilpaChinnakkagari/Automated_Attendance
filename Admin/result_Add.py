from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from tkinter import simpledialog
from datetime import datetime

class Result:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management")
        self.root.geometry("1530x780+0+0")
        self.root.config(bg="white")
        self.root.state('zoomed')

        #========== variables===========
        self.var_studentID = StringVar()
        self.var_studentName = StringVar()
        self.var_courseCode = StringVar()
        self.var_marks = StringVar()
        self.var_fullMarks = StringVar()
        self.var_department = StringVar()
        self.var_semester = StringVar()
        self.var_academic_year = StringVar()
        self.var_grade = StringVar()
        
        self.var_studentID_list = []
        self.var_courseCode_list = []
        self.var_department_list = ["CSE", "ECE", "EEE", "MECH", "CIVIL","CAI"]
        self.var_semester_list = ["1", "2"]
        self.var_academic_year_list = ["1","2","3","4"]
        
        self.fetch_studentID()
        self.fetch_courseCode()

        # Title with subtle animation
        self.title = Label(self.root, text="Result Management", 
                         font=("lucida", 20, "bold","italic"), bg="orange", fg="black")
        self.title.place(x=0, y=0, relwidth=1, height=50)
        self.animate_title()
        
        self.bg_img = Image.open(r"C:\Users\chinn\OneDrive\Desktop\Face Recognition System\College Images\bg2.jpg")
        self.bg_img = self.bg_img.resize((1530, 790), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.bg_lbl = Label(self.root, image=self.bg_img)
        self.bg_lbl.place(x=0, y=50, width=1530, height=790)

        #============ Input Frame ==============
        input_frame = Frame(self.bg_lbl, bg="white", bd=2, relief=RIDGE)
        input_frame.place(x=10, y=60, width=480, height=400)  # Increased height for additional fields

        # Student ID
        studentID_label = Label(input_frame, text="Student ID:", font=("times new roman", 12, "bold"), bg="white")
        studentID_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.studentID_entry = ttk.Combobox(input_frame, textvariable=self.var_studentID, values=self.var_studentID_list, 
                                          font=("times new roman", 12, "bold"), width=20, state="readonly")
        self.studentID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        self.studentID_entry.set("Select")

        # Student Name
        name_label = Label(input_frame, text="Name", font=("times new roman", 12, "bold"), bg="white", fg="black")
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.name_entry = Entry(input_frame, textvariable=self.var_studentName, font=("times new roman", 12), 
                             bg="lightgray", fg="black", state="readonly")
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Course Code
        courseCode_label = Label(input_frame, text="Course Code:", font=("times new roman", 12, "bold"), bg="white", fg="black")
        courseCode_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        self.courseCode_entry = ttk.Combobox(input_frame, textvariable=self.var_courseCode, values=self.var_courseCode_list, 
                                           font=("times new roman", 12), width=20, state="readonly")
        self.courseCode_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        self.courseCode_entry.set("Select")

        # Department
        department_label = Label(input_frame, text="Department:", font=("times new roman", 12, "bold"), bg="white", fg="black")
        department_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        self.department_entry = ttk.Combobox(input_frame, textvariable=self.var_department, values=self.var_department_list, 
                                           font=("times new roman", 12), width=20, state="readonly")
        self.department_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        self.department_entry.set("Select")

        # Semester
        semester_label = Label(input_frame, text="Semester:", font=("times new roman", 12, "bold"), bg="white", fg="black")
        semester_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        self.semester_entry = ttk.Combobox(input_frame, textvariable=self.var_semester, values=self.var_semester_list, 
                                         font=("times new roman", 12), width=20, state="readonly")
        self.semester_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        self.semester_entry.set("Select")

        # Academic Year
        academic_year_label = Label(input_frame, text="Academic Year:", font=("times new roman", 12, "bold"), bg="white", fg="black")
        academic_year_label.grid(row=5, column=0, padx=10, pady=5, sticky=W)

        self.academic_year_entry = ttk.Combobox(input_frame, textvariable=self.var_academic_year, values=self.var_academic_year_list, 
                                              font=("times new roman", 12), width=20, state="readonly")
        self.academic_year_entry.grid(row=5, column=1, padx=10, pady=5, sticky=W)
        self.academic_year_entry.set("Select")

        # Marks
        marks_label = Label(input_frame, text="Marks:", font=("times new roman", 12, "bold"), bg="white", fg="black")
        marks_label.grid(row=6, column=0, padx=10, pady=5, sticky=W)

        marks_entry = Entry(input_frame, textvariable=self.var_marks, font=("times new roman", 12), bg="lightgray", fg="black")
        marks_entry.grid(row=6, column=1, padx=10, pady=5, sticky=W)
        
        # Full Marks
        fullMarks_label = Label(input_frame, text="Full Marks:", font=("times new roman", 12, "bold"), bg="white", fg="black")
        fullMarks_label.grid(row=7, column=0, padx=10, pady=5, sticky=W)

        fullMarks_combobox = ttk.Combobox(input_frame, textvariable=self.var_fullMarks, font=("times new roman", 12), width=20)
        fullMarks_combobox["values"] = ("Select Full Marks", "70", "100")
        fullMarks_combobox.current(0)
        fullMarks_combobox.grid(row=7, column=1, padx=10, pady=5, sticky=W)

        # Grade (auto-calculated, readonly)
        grade_label = Label(input_frame, text="Grade:", font=("times new roman", 12, "bold"), bg="white", fg="black")
        grade_label.grid(row=8, column=0, padx=10, pady=5, sticky=W)

        self.grade_entry = Entry(input_frame, textvariable=self.var_grade, font=("times new roman", 12), 
                              bg="lightgray", fg="black", state="readonly")
        self.grade_entry.grid(row=8, column=1, padx=10, pady=5, sticky=W)

        # Bind marks entry to calculate grade
        marks_entry.bind("<FocusOut>", self.calculate_grade)

        # Button Frame
        btn_frame = Frame(input_frame, bg="white", bd=2, relief=RIDGE)
        btn_frame.place(x=5, y=300, width=465, height=90)

        # Search Button
        btn_search = Button(btn_frame, text="Search", command=self.search_name, font=("times new roman", 12, "bold"), 
                          bg="skyblue", fg="white", cursor="hand2")
        btn_search.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        # Save Button
        save_btn = Button(btn_frame, text="Save", width=10, cursor="hand2", command=self.add_data, 
                        font=("times new roman", 12, "bold"), bg="red", fg="white")
        save_btn.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Update Button
        update_btn = Button(btn_frame, text="Update", width=10, cursor="hand2", command=self.update_data, 
                          font=("times new roman", 12, "bold"), bg="red", fg="white")
        update_btn.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        # Delete Button
        delete_btn = Button(btn_frame, text="Delete", width=10, cursor="hand2", command=self.delete_data, 
                          font=("times new roman", 12, "bold"), bg="red", fg="white")
        delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        # Reset Button
        reset_btn = Button(btn_frame, text="Reset", width=10, cursor="hand2", command=self.reset_data, 
                         font=("times new roman", 12, "bold"), bg="red", fg="white")
        reset_btn.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        #============ Table 1: Student Details ==============
        table1_frame = Frame(self.bg_lbl, bg="white", bd=2, relief=RIDGE)
        table1_frame.place(x=500, y=60, width=400, height=50)  # Small table for student details

        self.Student_table = ttk.Treeview(table1_frame, columns=("studentID", "studentName"), show="headings")

        self.Student_table.heading("studentID", text="Student ID")
        self.Student_table.heading("studentName", text="Student Name")
        self.Student_table.column("studentID", width=100)
        self.Student_table.column("studentName", width=100)

        self.Student_table.pack(fill=BOTH, expand=1)

        #============ Table 2: Course Details ==============
        table2_frame = Frame(self.bg_lbl, bg="white", bd=2, relief=RIDGE)
        table2_frame.place(x=500, y=120, width=1000, height=150)

        scroll_x2 = ttk.Scrollbar(table2_frame, orient=HORIZONTAL)
        scroll_y2 = ttk.Scrollbar(table2_frame, orient=VERTICAL)
        self.Course_table = ttk.Treeview(table2_frame, columns=("courseCode", "marks", "fullMarks", "grade", "department", "semester", "academic_year"), 
                                       xscrollcommand=scroll_x2.set, yscrollcommand=scroll_y2.set)

        scroll_x2.pack(side=BOTTOM, fill=X)
        scroll_y2.pack(side=RIGHT, fill=Y)
        scroll_x2.config(command=self.Course_table.xview)
        scroll_y2.config(command=self.Course_table.yview)

        self.Course_table.heading("courseCode", text="Course Code")
        self.Course_table.heading("marks", text="Marks")
        self.Course_table.heading("fullMarks", text="Full Marks")
        self.Course_table.heading("grade", text="Grade")
        self.Course_table.heading("department", text="Department")
        self.Course_table.heading("semester", text="Semester")
        self.Course_table.heading("academic_year", text="Academic Year")
        self.Course_table["show"] = "headings"

        self.Course_table.column("courseCode", width=100)
        self.Course_table.column("marks", width=80)
        self.Course_table.column("fullMarks", width=80)
        self.Course_table.column("grade", width=80)
        self.Course_table.column("department", width=100)
        self.Course_table.column("semester", width=80)
        self.Course_table.column("academic_year", width=120)

        self.Course_table.pack(fill=BOTH, expand=1)

    def animate_title(self):
        """Simple animation for the title"""
        colors = ["orange", "lightblue", "lightgreen", "pink"]
        current_color = self.title.cget("bg")
        next_color = colors[(colors.index(current_color) + 1) % len(colors)] if current_color in colors else colors[0]
        self.title.config(bg=next_color)
        self.root.after(2000, self.animate_title)

    def calculate_grade(self, event=None):
        """Calculate grade based on marks and full marks"""
        try:
            if self.var_marks.get() and self.var_fullMarks.get() and self.var_fullMarks.get() != "Select Full Marks":
                marks = float(self.var_marks.get())
                full_marks = float(self.var_fullMarks.get())
                percentage = (marks / full_marks) * 100
                
                if percentage >= 90:
                    grade = "A+"
                elif percentage >= 80:
                    grade = "A"
                elif percentage >= 70:
                    grade = "B+"
                elif percentage >= 60:
                    grade = "B"
                elif percentage >= 50:
                    grade = "C+"
                elif percentage >= 40:
                    grade = "C"
                else:
                    grade = "F"
                
                self.var_grade.set(grade)
        except ValueError:
            pass

    def fetch_studentID(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        try:
            my_cursor.execute("select studentID from student")
            rows = my_cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.var_studentID_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def fetch_courseCode(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        try:
            my_cursor.execute("select courseCode from course")
            rows = my_cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.var_courseCode_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def search_name(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        try:
            if self.var_studentID.get() == "Select":
                messagebox.showerror("Error", "Please select a Student ID")
                return
        
            query = "SELECT `Student Name`, Department FROM student WHERE studentID = %s"
            my_cursor.execute(query, (self.var_studentID.get(),))  # Ensure tuple format
        
            row = my_cursor.fetchone()  # Fetch one result

            if row:
                self.var_studentName.set(row[0])  # Set the student name
                self.var_department.set(row[1])  # Set the department
                # Display student details in Table 1
                self.Student_table.delete(*self.Student_table.get_children())
                self.Student_table.insert("", END, values=(self.var_studentID.get(), self.var_studentName.get()))
                # Fetch course data for the selected student
                self.fetch_course_data()
            else:
                messagebox.showinfo("Result", "No student found with this ID")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        finally:
            conn.close()

    def fetch_course_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("""
            SELECT courseCode, marks, fullMarks, grade, department, semester, academic_year 
            FROM result 
            WHERE studentID=%s
        """, (self.var_studentID.get(),))
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.Course_table.delete(*self.Course_table.get_children())
            for i in data:
                self.Course_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def add_data(self):
        if (self.var_studentID.get() == "Select" or self.var_courseCode.get() == "Select" or 
            self.var_marks.get() == "" or self.var_fullMarks.get() == "Select Full Marks" or
            self.var_department.get() == "Select" or self.var_semester.get() == "Select" or
            self.var_academic_year.get() == "Select"):
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                # Calculate grade if not already calculated
                if not self.var_grade.get():
                    self.calculate_grade()
                
                conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
                my_cursor = conn.cursor()
                
                # Check if result already exists
                my_cursor.execute("""
                    SELECT * FROM result 
                    WHERE studentID=%s AND courseCode=%s AND semester=%s AND academic_year=%s
                """, (
                    self.var_studentID.get(),
                    self.var_courseCode.get(),
                    self.var_semester.get(),
                    self.var_academic_year.get()
                ))
                
                if my_cursor.fetchone():
                    messagebox.showerror("Error", "Result for this course in selected semester and academic year already exists", parent=self.root)
                    return
                
                # Insert new result
                my_cursor.execute("""
                    INSERT INTO result 
                    (studentID, studentName, courseCode, marks, fullMarks, grade, department, semester, academic_year) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.var_studentID.get(),
                    self.var_studentName.get(),
                    self.var_courseCode.get(),
                    self.var_marks.get(),
                    self.var_fullMarks.get(),
                    self.var_grade.get(),
                    self.var_department.get(),
                    self.var_semester.get(),
                    self.var_academic_year.get()
                ))
                
                conn.commit()
                conn.close()
                self.fetch_course_data()
                
                # Reset only course-related fields
                self.var_courseCode.set("Select")
                self.var_marks.set("")
                self.var_fullMarks.set("Select Full Marks")
                self.var_grade.set("")
                self.var_semester.set("Select")
                self.var_academic_year.set("Select")
                
                messagebox.showinfo("Success", "Results Details Have been added Successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to : {str(es)}", parent=self.root)

    def update_data(self):
        if (self.var_studentID.get() == "Select" or self.var_courseCode.get() == "Select" or 
            self.var_marks.get() == "" or self.var_fullMarks.get() == "Select Full Marks" or
            self.var_department.get() == "Select" or self.var_semester.get() == "Select" or
            self.var_academic_year.get() == "Select"):
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                # Calculate grade if not already calculated
                if not self.var_grade.get():
                    self.calculate_grade()
                
                conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
                my_cursor = conn.cursor()

                # Check if the result exists
                my_cursor.execute("""
                    SELECT * FROM result 
                    WHERE studentID=%s AND courseCode=%s AND semester=%s AND academic_year=%s
                """, (
                    self.var_studentID.get(),
                    self.var_courseCode.get(),
                    self.var_semester.get(),
                    self.var_academic_year.get()
                ))
                row = my_cursor.fetchone()

                if row:  # If the result exists
                    my_cursor.execute("""
                        UPDATE result 
                        SET studentName=%s, marks=%s, fullMarks=%s, grade=%s, department=%s 
                        WHERE studentID=%s AND courseCode=%s AND semester=%s AND academic_year=%s
                    """, (
                        self.var_studentName.get(),
                        self.var_marks.get(),
                        self.var_fullMarks.get(),
                        self.var_grade.get(),
                        self.var_department.get(),
                        self.var_studentID.get(),
                        self.var_courseCode.get(),
                        self.var_semester.get(),
                        self.var_academic_year.get()
                    ))
                    conn.commit()
                    conn.close()
                    self.fetch_course_data()
                    messagebox.showinfo("Success", "Result details Updated Successfully", parent=self.root)
                else:
                    # If the result does not exist
                    messagebox.showerror("Error", f"No result found for this combination", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due to : {str(es)}", parent=self.root)

    def delete_data(self):
        if (self.var_studentID.get() == "Select" or self.var_courseCode.get() == "Select" or 
            self.var_semester.get() == "Select" or self.var_academic_year.get() == "Select"):
            messagebox.showerror("Error", "Please select Student ID, Course Code, Semester and Academic Year", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do You Want To Delete This Result", parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
                    my_cursor = conn.cursor()
                    my_cursor.execute("""
                        DELETE FROM result 
                        WHERE studentID=%s AND courseCode=%s AND semester=%s AND academic_year=%s
                    """, (
                        self.var_studentID.get(),
                        self.var_courseCode.get(),
                        self.var_semester.get(),
                        self.var_academic_year.get()
                    ))
                    conn.commit()
                    conn.close()
                    
                    # Refresh the course data table after deletion
                    self.fetch_course_data()
                    
                    # Reset the input fields
                    self.reset_data()
                    
                    messagebox.showinfo("Success", "Result Deleted Successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to : {str(es)}", parent=self.root)

    def reset_data(self):
        # Reset all fields
        self.var_studentID.set("Select")
        self.var_studentName.set("")
        self.var_courseCode.set("Select")
        self.var_marks.set("")
        self.var_fullMarks.set("Select Full Marks")
        self.var_grade.set("")
        self.var_department.set("Select")
        self.var_semester.set("Select")
        self.var_academic_year.set("Select")

        self.Course_table.delete(*self.Course_table.get_children())
        self.Student_table.delete(*self.Student_table.get_children())

if __name__ == "__main__":
    root = Tk()
    obj = Result(root)
    root.mainloop()