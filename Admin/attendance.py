from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import os
import csv
from tkinter import filedialog
from PIL import Image, ImageTk

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance Management System")
        self.root.state('zoomed')

        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="vnsvb",
            database="face_recognition"
        )
        
        # Variables
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_department = StringVar()
        self.var_course_code = StringVar()
        self.var_date = StringVar()
        self.var_search = StringVar()
        
        # Images
        self.load_images()
        self.create_ui()
        
        # Load initial data
        self.load_years()
        self.load_departments()
        
    def load_images(self):
        # First Image
        try:
            img = Image.open(r"College Images\train_data.jpg")
            img = img.resize((800, 200), Image.Resampling.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
        except:
            self.photoimg = None

        # Second Image
        try:
            img1 = Image.open(r"College Images\attendance_file.jpg")
            img1 = img1.resize((800, 200), Image.Resampling.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img1)
        except:
            self.photoimg1 = None

        # Background Image
        try:
            img3 = Image.open(r"College Images\Training-Data-Feature-1024x657.jpg")
            img3 = img3.resize((1530, 710), Image.Resampling.LANCZOS)
            self.photoimg3 = ImageTk.PhotoImage(img3)
        except:
            self.photoimg3 = None

    def create_ui(self):
        # Title Frame
        title_frame = Frame(self.root, bg="white")
        title_frame.place(x=0, y=0, width=1530, height=200)
        
        if self.photoimg:
            f_lbl = Label(title_frame, image=self.photoimg)
            f_lbl.place(x=0, y=0, width=800, height=200)
        
        if self.photoimg1:
            f_lbl = Label(title_frame, image=self.photoimg1)
            f_lbl.place(x=800, y=0, width=800, height=200)

        # Main Frame
        main_frame = Frame(self.root, bd=2, bg="white")
        main_frame.place(x=10, y=210, width=1500, height=560)

        # Left Frame (Filters and Controls)
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Attendance Filters", 
                               font=("times new roman", 12, "bold"), bg="white")
        left_frame.place(x=10, y=10, width=730, height=540)

        # Filter Controls
        filter_frame = Frame(left_frame, bd=2, relief=GROOVE, bg="white")
        filter_frame.place(x=5, y=5, width=715, height=150)

        # Year
        lbl_year = Label(filter_frame, text="Year:", font=("times new roman", 12, "bold"), bg="white")
        lbl_year.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.var_year, 
                                     font=("times new roman", 12), state="readonly", width=8)
        self.year_combo.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.year_combo.bind("<<ComboboxSelected>>", self.update_semesters)

        # Semester
        lbl_semester = Label(filter_frame, text="Semester:", font=("times new roman", 12, "bold"), bg="white")
        lbl_semester.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        self.semester_combo = ttk.Combobox(filter_frame, textvariable=self.var_semester, 
                                         font=("times new roman", 12), state="readonly", width=8)
        self.semester_combo.grid(row=0, column=3, padx=5, pady=5, sticky=W)
        self.semester_combo.bind("<<ComboboxSelected>>", self.update_departments)

        # Department
        lbl_department = Label(filter_frame, text="Department:", font=("times new roman", 12, "bold"), bg="white")
        lbl_department.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.department_combo = ttk.Combobox(filter_frame, textvariable=self.var_department, 
                                           font=("times new roman", 12), state="readonly", width=8)
        self.department_combo.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        self.department_combo.bind("<<ComboboxSelected>>", self.update_courses)

        # Course Code
        lbl_course = Label(filter_frame, text="Course Code:", font=("times new roman", 12, "bold"), bg="white")
        lbl_course.grid(row=1, column=2, padx=5, pady=5, sticky=W)

        self.course_combo = ttk.Combobox(filter_frame, textvariable=self.var_course_code, 
                                       font=("times new roman", 12), state="readonly", width=15)
        self.course_combo.grid(row=1, column=3, padx=5, pady=5, sticky=W)
        self.course_combo.bind("<<ComboboxSelected>>", self.update_dates)

        # Date
        lbl_date = Label(filter_frame, text="Date:", font=("times new roman", 12, "bold"), bg="white")
        lbl_date.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        self.date_combo = ttk.Combobox(filter_frame, textvariable=self.var_date, 
                                     font=("times new roman", 12), state="readonly", width=15)
        self.date_combo.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        # Search
        lbl_search = Label(filter_frame, text="Search:", font=("times new roman", 12, "bold"), bg="white")
        lbl_search.grid(row=2, column=2, padx=5, pady=5, sticky=W)

        entry_search = Entry(filter_frame, textvariable=self.var_search, 
                           font=("times new roman", 12), width=15)
        entry_search.grid(row=2, column=3, padx=5, pady=5, sticky=W)

        # Buttons
        btn_frame = Frame(left_frame, bd=2, relief=GROOVE, bg="white")
        btn_frame.place(x=5, y=160, width=715, height=60)

        btn_show = Button(btn_frame, text="Show Attendance", command=self.show_attendance, 
                         font=("times new roman", 13, "bold"), bg="blue", fg="white", width=15)
        btn_show.grid(row=0, column=0, padx=5, pady=5)

        btn_report = Button(btn_frame, text="Download Report", command=self.download_report, 
                           font=("times new roman", 13, "bold"), bg="green", fg="white", width=15)
        btn_report.grid(row=0, column=1, padx=5, pady=5)

        # Statistics Frame
        stats_frame = Frame(left_frame, bd=2, relief=GROOVE, bg="white")
        stats_frame.place(x=5, y=225, width=715, height=150)

        self.lbl_total = Label(stats_frame, text="Total Students: 0", font=("times new roman", 12, "bold"), 
                             bg="white", anchor=W)
        self.lbl_total.pack(fill=X, padx=5, pady=5)

        self.lbl_present = Label(stats_frame, text="Present: 0 (0%)", font=("times new roman", 12, "bold"), 
                               bg="white", fg="green", anchor=W)
        self.lbl_present.pack(fill=X, padx=5, pady=5)

        self.lbl_absent = Label(stats_frame, text="Absent: 0 (0%)", font=("times new roman", 12, "bold"), 
                              bg="white", fg="red", anchor=W)
        self.lbl_absent.pack(fill=X, padx=5, pady=5)

        # Absentees List
        absent_frame = Frame(left_frame, bd=2, relief=GROOVE, bg="white")
        absent_frame.place(x=5, y=380, width=715, height=150)

        lbl_absent = Label(absent_frame, text="Absent Students:", font=("times new roman", 12, "bold"), 
                          bg="white")
        lbl_absent.pack(fill=X, padx=5, pady=2)

        scroll_y = Scrollbar(absent_frame, orient=VERTICAL)
        self.absent_list = Listbox(absent_frame, yscrollcommand=scroll_y.set, 
                                 font=("times new roman", 11), bg="lightgray")
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.absent_list.yview)
        self.absent_list.pack(fill=BOTH, expand=1)

        # Right Frame (Attendance Table)
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Attendance Details", 
                               font=("times new roman", 12, "bold"), bg="white")
        right_frame.place(x=750, y=10, width=730, height=540)

        # Table Frame
        table_frame = Frame(right_frame, bd=2, relief=GROOVE, bg="white")
        table_frame.place(x=5, y=5, width=715, height=525)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(table_frame, columns=(
            "id", "name", "department", "year", "section", "course_code", "course_name", 
            "time", "date", "status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        self.attendance_table.heading("id", text="Student ID")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("department", text="Department")
        self.attendance_table.heading("year", text="Year")
        self.attendance_table.heading("section", text="Section")
        self.attendance_table.heading("course_code", text="Course Code")
        self.attendance_table.heading("course_name", text="Course Name")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("status", text="Status")

        self.attendance_table.column("id", width=100)
        self.attendance_table.column("name", width=150)
        self.attendance_table.column("department", width=100)
        self.attendance_table.column("year", width=50)
        self.attendance_table.column("section", width=50)
        self.attendance_table.column("course_code", width=100)
        self.attendance_table.column("course_name", width=150)
        self.attendance_table.column("time", width=80)
        self.attendance_table.column("date", width=80)
        self.attendance_table.column("status", width=80)

        self.attendance_table.pack(fill=BOTH, expand=1)
        self.attendance_table.bind("<ButtonRelease-1>", self.get_cursor)

    def load_years(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM course ORDER BY year DESC")
        years = [str(year[0]) for year in cursor.fetchall()]
        self.year_combo["values"] = years
        if years:
            self.year_combo.current(0)
            self.update_semesters()
        cursor.close()

    def update_semesters(self, event=None):
        year = self.var_year.get()
        if not year:
            return
            
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT semester FROM course WHERE year = %s ORDER BY semester", (year,))
        semesters = [str(semester[0]) for semester in cursor.fetchall()]
        self.semester_combo["values"] = semesters
        if semesters:
            self.semester_combo.current(0)
            self.update_departments()
        cursor.close()

    def load_departments(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT department FROM course ORDER BY department")
        departments = [dept[0] for dept in cursor.fetchall()]
        self.department_combo["values"] = departments
        cursor.close()

    def update_departments(self, event=None):
        year = self.var_year.get()
        semester = self.var_semester.get()
        if not year or not semester:
            return
            
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT department FROM course WHERE year = %s AND semester = %s ORDER BY department", 
                      (year, semester))
        departments = [dept[0] for dept in cursor.fetchall()]
        self.department_combo["values"] = departments
        if departments:
            self.department_combo.current(0)
            self.update_courses()
        cursor.close()

    def update_courses(self, event=None):
        year = self.var_year.get()
        semester = self.var_semester.get()
        department = self.var_department.get()
        if not year or not semester or not department:
            return
            
        cursor = self.conn.cursor()
        query = """
            SELECT courseCode, CONCAT(courseCode, ' - ', courseName) 
            FROM course 
            WHERE year = %s AND semester = %s AND department = %s
            ORDER BY courseCode
        """
        cursor.execute(query, (year, semester, department))
        courses = cursor.fetchall()
        
        self.course_combo["values"] = [course[1] for course in courses]
        self.course_codes = {course[1]: course[0] for course in courses}
        
        if courses:
            self.course_combo.current(0)
            self.update_dates()
        cursor.close()

    def update_dates(self, event=None):
        course_code = self.get_selected_course_code()
        if not course_code:
            return
            
        cursor = self.conn.cursor()
        query = """
            SELECT DISTINCT date 
            FROM attendance 
            WHERE courseCode = %s
            ORDER BY date DESC
        """
        cursor.execute(query, (course_code,))
        dates = [date[0].strftime("%Y-%m-%d") for date in cursor.fetchall()]
        self.date_combo["values"] = dates
        if dates:
            self.date_combo.current(0)
        cursor.close()

    def get_selected_course_code(self):
        selected_course = self.course_combo.get()
        return self.course_codes.get(selected_course, None)

    def show_attendance(self):
        course_code = self.get_selected_course_code()
        date = self.var_date.get()
        search = self.var_search.get()

        if not course_code:
            messagebox.showwarning("Warning", "Please select a course")
            return
        if not date:
            messagebox.showwarning("Warning", "Please select a date")
            return

        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # Base query
            query = """
                SELECT student_id as id, student_name as name, department, 
                       year, section, courseCode as course_code, courseName as course_name,
                       time, date, status
                FROM attendance
                WHERE courseCode = %s AND date = %s
            """
            params = [course_code, date]
            
            # Add search filter if specified
            if search:
                query += " AND (student_name LIKE %s OR student_id LIKE %s)"
                params.extend([f"%{search}%", f"%{search}%"])
            
            query += " ORDER BY status DESC, student_name"
            
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            
            # Update table
            self.attendance_table.delete(*self.attendance_table.get_children())
            for row in rows:
                self.attendance_table.insert("", END, values=(
                    row["id"], row["name"], row["department"], 
                    row["year"], row["section"], row["course_code"],
                    row["course_name"], row["time"], row["date"], row["status"]
                ))
            
            # Update statistics
            self.update_statistics(rows)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch attendance: {str(e)}")
        finally:
            cursor.close()

    def update_statistics(self, attendance_data):
        total = len(attendance_data)
        present = sum(1 for row in attendance_data if row["status"].lower() == "present")
        absent = total - present
        
        self.lbl_total.config(text=f"Total Students: {total}")
        self.lbl_present.config(text=f"Present: {present} ({present/total*100:.1f}%)" if total > 0 else "Present: 0")
        self.lbl_absent.config(text=f"Absent: {absent} ({absent/total*100:.1f}%)" if total > 0 else "Absent: 0")
        
        # Update absentees list
        self.absent_list.delete(0, END)
        if total > 0:
            absent_students = [row["name"] for row in attendance_data if row["status"].lower() != "present"]
            for student in absent_students:
                self.absent_list.insert(END, student)

    def get_cursor(self, event):
        cursor_row = self.attendance_table.focus()
        content = self.attendance_table.item(cursor_row)
        row = content["values"]
        
        if row:
            # You can add code here to populate fields if you want an edit feature
            pass

    def download_report(self):
        try:
            course_code = self.get_selected_course_code()
            date = self.var_date.get()
            
            if not course_code or not date:
                messagebox.showwarning("Warning", "Please select both course and date")
                return
                
            # Get course details
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT courseName, year, semester, department, facultyName 
                FROM course 
                WHERE courseCode = %s
            """, (course_code,))
            course = cursor.fetchone()
            
            if not course:
                messagebox.showerror("Error", "Course details not found")
                return
            
            # Get attendance data
            query = """
                SELECT student_id as id, student_name as name, department, 
                       year, section, time, status
                FROM attendance
                WHERE courseCode = %s AND date = %s
                ORDER BY status DESC, student_name
            """
            cursor.execute(query, (course_code, date))
            attendance_data = cursor.fetchall()
            
            if not attendance_data:
                messagebox.showwarning("Warning", "No attendance data to generate report")
                return
                
            # Calculate statistics
            total = len(attendance_data)
            present = sum(1 for row in attendance_data if row["status"].lower() == "present")
            absent = total - present
            
            # Ask user where to save the report
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title=f"Save attendance report for {course_code} - {date}",
                initialfile=f"Attendance_{course_code}_{date.replace('-','')}.csv"
            )
            
            if not file_path:
                return
                
            # Write the report
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                
                # Write header information
                writer.writerow(["Attendance Report"])
                writer.writerow([f"Course: {course['courseName']} ({course_code})"])
                writer.writerow([f"Year: {course['year']}, Semester: {course['semester']}"])
                writer.writerow([f"Department: {course['department']}"])
                writer.writerow([f"Faculty: {course['facultyName']}"])
                writer.writerow([f"Date: {date}"])
                writer.writerow([])
                
                # Write statistics
                writer.writerow([f"Total Students: {total}"])
                writer.writerow([f"Present: {present} ({present/total*100:.1f}%)"])
                writer.writerow([f"Absent: {absent} ({absent/total*100:.1f}%)"])
                writer.writerow([])
                
                # Write column headers
                writer.writerow(["Student ID", "Name", "Department", "Year", "Section", "Time", "Status"])
                
                # Write attendance data
                for row in attendance_data:
                    writer.writerow([
                        row["id"], row["name"], row["department"],
                        row["year"], row["section"], row["time"], row["status"]
                    ])
                    
            messagebox.showinfo("Success", f"Attendance report saved to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
        finally:
            cursor.close()

if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()