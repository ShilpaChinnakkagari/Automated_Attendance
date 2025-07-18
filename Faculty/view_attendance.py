from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector


class ViewAttendance:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Analytics")
        self.root.geometry("1400x700")
        self.root.configure(bg="#f0f0f0")
        self.root.state('zoomed')

        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vnsvb",
            database="face_recognition"
        )

        # Variables
        self.var_year = StringVar()
        self.var_section = StringVar()
        self.var_course = StringVar()
        self.var_date = StringVar()

        self.create_ui()
        self.load_years()
        self.load_sections()
        self.load_courses()

    def create_ui(self):
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        title_frame = Frame(main_frame, bg="#003366")
        title_frame.pack(fill=X, pady=(0, 10))

        Label(title_frame, text="STUDENT ATTENDANCE ANALYTICS",
              font=("Arial", 16, "bold"), bg="#003366", fg="white").pack(pady=10)

        # Filter controls
        filter_frame = Frame(main_frame, bg="#f0f0f0")
        filter_frame.pack(fill=X, pady=5)

        Label(filter_frame, text="Year:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=0, column=0, padx=5, pady=5, sticky=W)

        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.var_year,
                                       font=("Arial", 12), state="readonly", width=12)
        self.year_combo.grid(row=0, column=1, padx=5, pady=5)
        self.year_combo.bind("<<ComboboxSelected>>", self.update_date_list)

        Label(filter_frame, text="Section:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=0, column=2, padx=5, pady=5, sticky=W)

        self.section_combo = ttk.Combobox(filter_frame, textvariable=self.var_section,
                                          font=("Arial", 12), state="readonly", width=12)
        self.section_combo.grid(row=0, column=3, padx=5, pady=5)
        self.section_combo.bind("<<ComboboxSelected>>", self.update_date_list)

        Label(filter_frame, text="Course:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=0, column=4, padx=5, pady=5, sticky=W)

        self.course_combo = ttk.Combobox(filter_frame, textvariable=self.var_course,
                                         font=("Arial", 12), state="readonly", width=15)
        self.course_combo.grid(row=0, column=5, padx=5, pady=5)
        self.course_combo.bind("<<ComboboxSelected>>", self.update_date_list)

        Label(filter_frame, text="Date:", font=("Arial", 12), bg="#f0f0f0").grid(
            row=0, column=6, padx=5, pady=5, sticky=W)

        self.date_combo = ttk.Combobox(filter_frame, textvariable=self.var_date,
                                       font=("Arial", 12), state="readonly", width=15)
        self.date_combo.grid(row=0, column=7, padx=5, pady=5)

        Button(filter_frame, text="Show Attendance", command=self.search_attendance,
               font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15
               ).grid(row=0, column=8, padx=10, pady=5)

        # Statistics frame
        stats_frame = Frame(main_frame, bg="#f0f0f0")
        stats_frame.pack(fill=X, pady=10)

        self.lbl_total = Label(stats_frame, text="Total Students: 0",
                               font=("Arial", 12), bg="#f0f0f0")
        self.lbl_total.pack(side=LEFT, padx=20)

        self.lbl_present = Label(stats_frame, text="Present: 0",
                                 font=("Arial", 12), bg="#f0f0f0")
        self.lbl_present.pack(side=LEFT, padx=20)

        self.lbl_absent = Label(stats_frame, text="Absent: 0",
                                font=("Arial", 12), bg="#f0f0f0")
        self.lbl_absent.pack(side=LEFT, padx=20)

        self.lbl_permission = Label(stats_frame, text="Permission: 0",
                                    font=("Arial", 12), bg="#f0f0f0")
        self.lbl_permission.pack(side=LEFT, padx=20)

        # Table frame
        table_frame = Frame(main_frame)
        table_frame.pack(fill=BOTH, expand=True)

        scroll_y = Scrollbar(table_frame)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.attendance_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "status"),
            yscrollcommand=scroll_y.set
        )
        self.attendance_table.pack(fill=BOTH, expand=True)

        scroll_y.config(command=self.attendance_table.yview)

        self.attendance_table.heading("id", text="Student ID")
        self.attendance_table.heading("name", text="Student Name")
        self.attendance_table.heading("status", text="Status")

        self.attendance_table.column("id", width=100, anchor=CENTER)
        self.attendance_table.column("name", width=250, anchor=W)
        self.attendance_table.column("status", width=100, anchor=CENTER)

    def load_years(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT Year FROM student ORDER BY Year")
        years = [str(year[0]) for year in cursor.fetchall()]
        self.year_combo["values"] = years
        cursor.close()

    def load_sections(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT Section FROM student ORDER BY Section")
        sections = [section[0] for section in cursor.fetchall()]
        self.section_combo["values"] = sections
        cursor.close()

    def load_courses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT courseCode FROM course ORDER BY courseCode")
        courses = [course[0] for course in cursor.fetchall()]
        self.course_combo["values"] = courses
        cursor.close()

    def update_date_list(self, event=None):
        year = self.var_year.get()
        section = self.var_section.get()
        course_code = self.var_course.get()

        if not year or not section or not course_code:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT DISTINCT date 
                FROM attendance 
                WHERE year=%s AND section=%s AND courseCode=%s 
                ORDER BY date
            """, (year, section, course_code))

            dates = [row[0] for row in cursor.fetchall()]
            self.date_combo["values"] = dates
            if dates:
                self.date_combo.current(0)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch dates: {str(e)}")
        finally:
            cursor.close()

    def search_attendance(self):
        year = self.var_year.get()
        section = self.var_section.get()
        course_code = self.var_course.get()
        date = self.var_date.get()

        if not year or not section or not course_code or not date:
            messagebox.showwarning("Warning", "Please select year, section, course, and date")
            return

        try:
            cursor = self.conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    s.StudentID as id,
                    s.`Student Name` as name,
                    COALESCE(a.status, 'Not Marked') as status
                FROM student s
                LEFT JOIN attendance a ON s.StudentID = a.student_id 
                    AND a.year = %s 
                    AND a.section = %s 
                    AND a.courseCode = %s
                    AND a.date = %s
                WHERE s.Year = %s AND s.Section = %s
                ORDER BY s.`Student Name`
            """, (year, section, course_code, date, year, section))

            rows = cursor.fetchall()

            # Clear table
            self.attendance_table.delete(*self.attendance_table.get_children())

            total = len(rows)
            present = sum(1 for row in rows if row["status"] == "P")
            absent = sum(1 for row in rows if row["status"] == "A")
            permission = sum(1 for row in rows if row["status"] == "PM")

            for row in rows:
                self.attendance_table.insert("", END, values=(
                    row["id"],
                    row["name"],
                    row["status"]
                ))

            self.lbl_total.config(text=f"Total Students: {total}")
            self.lbl_present.config(text=f"Present: {present}")
            self.lbl_absent.config(text=f"Absent: {absent}")
            self.lbl_permission.config(text=f"Permission: {permission}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch attendance: {str(e)}")
        finally:
            cursor.close()


if __name__ == "__main__":
    root = Tk()
    obj = ViewAttendance(root)
    root.mainloop()
