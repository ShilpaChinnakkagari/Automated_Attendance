import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class ManualAttendance:
    def __init__(self, root):
        self.root = root
        self.root.title("Manual Attendance System")
        self.root.geometry("1200x700")
        self.root.state('zoomed')
        
        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="vnsvb",
            database="face_recognition"
        )
        
        # Variables
        self.year_var = tk.StringVar()
        self.section_var = tk.StringVar()
        self.course_code_var = tk.StringVar()
        self.course_name_var = tk.StringVar()
        self.attendance_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.attendance_status = {}  # To store attendance status for each student
        self.radio_vars = {}  # To store radio button variables
        
        # Create UI
        self.create_widgets()
        
        # Load initial data
        self.load_years()
        self.load_sections()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame (filters and student list)
        left_frame = tk.Frame(main_frame, width=600, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right frame (attendance summary)
        right_frame = tk.Frame(main_frame, width=400, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Filter controls
        filter_frame = tk.LabelFrame(left_frame, text="Filters", padx=10, pady=10)
        filter_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(filter_frame, text="Year:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, state="readonly")
        self.year_combo.grid(row=0, column=1, padx=5, pady=5)
        self.year_combo.bind("<<ComboboxSelected>>", self.load_courses_for_year)
        
        tk.Label(filter_frame, text="Section:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.section_combo = ttk.Combobox(filter_frame, textvariable=self.section_var, state="readonly")
        self.section_combo.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Course Code:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.course_code_combo = ttk.Combobox(filter_frame, textvariable=self.course_code_var, state="readonly")
        self.course_code_combo.grid(row=1, column=1, padx=5, pady=5)
        self.course_code_combo.bind("<<ComboboxSelected>>", self.update_course_name)
        
        tk.Label(filter_frame, text="Course Name:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.course_name_entry = tk.Entry(filter_frame, textvariable=self.course_name_var, state='readonly')
        self.course_name_entry.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Date:").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        tk.Entry(filter_frame, textvariable=self.attendance_date).grid(row=1, column=5, padx=5, pady=5)
        
        # Show button
        tk.Button(filter_frame, text="Show Students", command=self.load_students, 
                 bg="blue", fg="white").grid(row=1, column=6, padx=10, pady=5)
        
        # Student list with attendance
        list_frame = tk.LabelFrame(left_frame, text="Mark Attendance", padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Canvas and scrollbar for student list
        canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame for student entries
        self.student_entries_frame = scrollable_frame
        
        # Save button
        tk.Button(left_frame, text="Save Attendance", command=self.save_attendance, 
                 bg="green", fg="white", padx=10).pack(pady=10)
        
        # Summary frame
        summary_frame = tk.LabelFrame(right_frame, text="Attendance Summary", padx=10, pady=10)
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        self.summary_text = tk.Text(summary_frame, height=20, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # Statistics frame
        stats_frame = tk.LabelFrame(right_frame, text="Absent Students", padx=10, pady=10)
        stats_frame.pack(fill=tk.BOTH, pady=5)
        
        self.absent_listbox = tk.Listbox(stats_frame, height=10)
        self.absent_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Percentage frame
        percent_frame = tk.LabelFrame(right_frame, text="Statistics", padx=10, pady=10)
        percent_frame.pack(fill=tk.BOTH, pady=5)
        
        self.stats_text = tk.Text(percent_frame, height=5, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
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
        
    def load_courses_for_year(self, event=None):
        year = self.year_var.get()
        if not year:
            return
            
        cursor = self.conn.cursor()
        cursor.execute("SELECT courseCode, courseName FROM course WHERE year=%s", (year,))
        courses = cursor.fetchall()
        cursor.close()
        
        # Update course code combobox
        self.course_code_combo['values'] = [course[0] for course in courses]
        
        # Store course details for name lookup
        self.course_details = {code: name for code, name in courses}
        
    def update_course_name(self, event=None):
        code = self.course_code_var.get()
        if code in self.course_details:
            self.course_name_var.set(self.course_details[code])
        
    def load_students(self):
        year = self.year_var.get()
        section = self.section_var.get()
        course_code = self.course_code_var.get()
        
        if not year or not section:
            messagebox.showwarning("Warning", "Please select both year and section")
            return
            
        if not course_code:
            messagebox.showwarning("Warning", "Please select a course code")
            return
            
        # Clear previous student entries
        for widget in self.student_entries_frame.winfo_children():
            widget.destroy()
        self.attendance_status.clear()
        self.radio_vars.clear()
        self.absent_listbox.delete(0, tk.END)
        
        # Add column headers
        header_frame = tk.Frame(self.student_entries_frame, bg="lightgray")
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(header_frame, text="ID", width=10, bg="lightgray", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        tk.Label(header_frame, text="Student Name", width=30, bg="lightgray", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        tk.Label(header_frame, text="Status", width=20, bg="lightgray", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # Load students from database
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT StudentID, `Student Name` 
            FROM student 
            WHERE Year=%s AND Section=%s
            ORDER BY `Student Name`
        """, (year, section))
        
        students = cursor.fetchall()
        cursor.close()
        
        if not students:
            messagebox.showinfo("Info", "No students found for selected year and section")
            return
            
        # Create entry for each student
        for idx, (student_id, student_name) in enumerate(students):
            # Student frame with alternating background
            bg_color = "white" if idx % 2 == 0 else "#f0f0f0"
            student_frame = tk.Frame(self.student_entries_frame, bg=bg_color)
            student_frame.pack(fill=tk.X, pady=1)
            
            # Student info
            tk.Label(student_frame, text=f"{student_id}", width=10, bg=bg_color).pack(side=tk.LEFT)
            tk.Label(student_frame, text=f"{student_name}", width=30, bg=bg_color).pack(side=tk.LEFT)
            
            # Radio buttons for attendance status
            status_var = tk.StringVar(value="")
            self.radio_vars[student_id] = status_var
            
            # Store reference to student frame for highlighting
            status_var.trace_add('write', lambda *args, f=student_frame, sid=student_id: self.highlight_row(f, sid))
            
            tk.Radiobutton(student_frame, text="Present", variable=status_var, 
                          value="P", bg=bg_color).pack(side=tk.LEFT, padx=5)
            tk.Radiobutton(student_frame, text="Absent", variable=status_var, 
                          value="A", bg=bg_color).pack(side=tk.LEFT, padx=5)
            tk.Radiobutton(student_frame, text="Permission", variable=status_var, 
                          value="PM", bg=bg_color).pack(side=tk.LEFT, padx=5)
            
            # Store initial status
            self.attendance_status[student_id] = ""
        
        # Update summary
        self.update_summary()
        
    def highlight_row(self, frame, student_id):
        """Highlight the row based on attendance status"""
        status = self.radio_vars[student_id].get()
        
        if status == "A":  # Absent - red background
            frame.config(bg="#ffcccc")
            for widget in frame.winfo_children():
                widget.config(bg="#ffcccc")
        elif status == "P":  # Present - green background
            frame.config(bg="#ccffcc")
            for widget in frame.winfo_children():
                widget.config(bg="#ccffcc")
        elif status == "PM":  # Permission - yellow background
            frame.config(bg="#ffffcc")
            for widget in frame.winfo_children():
                widget.config(bg="#ffffcc")
        else:  # Not marked - default background
            bg_color = "white" if list(self.radio_vars.keys()).index(student_id) % 2 == 0 else "#f0f0f0"
            frame.config(bg=bg_color)
            for widget in frame.winfo_children():
                widget.config(bg=bg_color)
        
        # Update summary when status changes
        self.update_summary()
        
    def update_summary(self):
        # Get current status from radio buttons
        for student_id, var in self.radio_vars.items():
            self.attendance_status[student_id] = var.get()
        
        # Calculate counts
        total = len(self.attendance_status)
        present = sum(1 for status in self.attendance_status.values() if status == "P")
        absent = sum(1 for status in self.attendance_status.values() if status == "A")
        permission = sum(1 for status in self.attendance_status.values() if status == "PM")
        not_marked = sum(1 for status in self.attendance_status.values() if not status)
        
        # Update summary text
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        
        self.summary_text.insert(tk.END, f"Total Students: {total}\n")
        self.summary_text.insert(tk.END, f"Present (P): {present}\n")
        self.summary_text.insert(tk.END, f"Absent (A): {absent}\n")
        self.summary_text.insert(tk.END, f"Permission (PM): {permission}\n")
        self.summary_text.insert(tk.END, f"Not Marked: {not_marked}\n")
        
        # Update absent students list
        self.absent_listbox.delete(0, tk.END)
        absent_students = [self.get_student_name(sid) for sid, status in self.attendance_status.items() if status == "A"]
        for student in absent_students:
            self.absent_listbox.insert(tk.END, student)
        
        # Update statistics
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        if total > 0:
            present_pct = (present / total) * 100
            absent_pct = (absent / total) * 100
            permission_pct = (permission / total) * 100
            
            self.stats_text.insert(tk.END, f"Present: {present_pct:.1f}%\n")
            self.stats_text.insert(tk.END, f"Absent: {absent_pct:.1f}%\n")
            self.stats_text.insert(tk.END, f"Permission: {permission_pct:.1f}%\n")
        
        self.summary_text.config(state=tk.DISABLED)
        self.stats_text.config(state=tk.DISABLED)
        
    def save_attendance(self):
        year = self.year_var.get()
        section = self.section_var.get()
        date = self.attendance_date.get()
        course_code = self.course_code_var.get()
        course_name = self.course_name_var.get()
        
        if not year or not section:
            messagebox.showwarning("Warning", "Please select year and section")
            return
            
        if not date:
            messagebox.showwarning("Warning", "Please enter attendance date")
            return
            
        if not course_code or not course_name:
            messagebox.showwarning("Warning", "Please select both course code and name")
            return
            
        # Update status from radio buttons
        self.update_summary()
            
        # Check if all students are marked
        if any(not status for status in self.attendance_status.values()):
            if not messagebox.askyesno("Confirm", "Some students are not marked. Save anyway?"):
                return
                
        try:
            cursor = self.conn.cursor()
            
            # Check if attendance already exists for this date and course
            cursor.execute("""
                SELECT COUNT(*) FROM attendance 
                WHERE date=%s AND year=%s AND section=%s AND courseCode=%s
            """, (date, year, section, course_code))
            
            if cursor.fetchone()[0] > 0:
                if not messagebox.askyesno("Confirm", "Attendance already exists for this date and course. Overwrite?"):
                    return
                # Delete existing attendance
                cursor.execute("""
                    DELETE FROM attendance 
                    WHERE date=%s AND year=%s AND section=%s AND courseCode=%s
                """, (date, year, section, course_code))
            
            # Insert new attendance records
            for student_id, status in self.attendance_status.items():
                if status:  # Only save marked records
                    cursor.execute("""
                        INSERT INTO attendance 
                        (student_id, student_name, year, section, status, date, courseCode, courseName) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        student_id,
                        self.get_student_name(student_id),
                        year,
                        section,
                        status,
                        date,
                        course_code,
                        course_name
                    ))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Attendance saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")
            self.conn.rollback()
            
        finally:
            cursor.close()
            
    def get_student_name(self, student_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT `Student Name` FROM student WHERE StudentID=%s", (student_id,))
        name = cursor.fetchone()[0]
        cursor.close()
        return name

if __name__ == "__main__":
    root = tk.Tk()
    app = ManualAttendance(root)
    root.mainloop()