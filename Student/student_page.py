from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os
import sys
import subprocess
import webbrowser

class StudentPortal:
    def __init__(self, root, student_id):
        self.root = root
        self.student_id = student_id
        self.root.title("Student Portal")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f5f5")
        self.root.state('zoomed')
        
        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vnsvb",
            database="face_recognition"
        )
        
        # Main container
        main_frame = Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = Frame(main_frame, bg="#003366", height=80)
        header_frame.pack(fill=X, pady=(0,20))
        
        # Get student name from database
        self.student_name = self.get_student_name()
        
        Label(header_frame, 
             text=f"Welcome, {self.student_name} (ID: {self.student_id})",
             font=("Arial", 16, "bold"), 
             bg="#003366", fg="white"
             ).pack(side=LEFT, padx=20)
        
        # Dashboard
        dashboard_frame = Frame(main_frame, bg="#f5f5f5")
        dashboard_frame.pack(fill=BOTH, expand=True)
        
        # Left sidebar (navigation)
        sidebar = Frame(dashboard_frame, bg="#e1e1e1", width=250)
        sidebar.pack(side=LEFT, fill=Y, padx=(0,20))
        
        # Navigation buttons with icons
        nav_buttons = [
            ("📊 View Attendance", self.open_attendance),
            ("📚 Study Portal", self.open_study_portal),
            ("🎫 Download Hall Tickets", self.open_hall_ticket),
            ("📝 View Results", self.open_result_viewer),
            ("💬 Give Feedback", None),
            ("👨‍🏫 Faculty Details", self.open_faculty_details),
            ("✉️Request Permission", self.requestPM),
            ("📅Course Syllabus", self.academic_Syllabus),
            ("📄 Previous Year Papers", self.open_question_papers),
            ("💰 Fee Receipts", self.open_fee_receipts),
            ("📰 Campus News", self.latest_news),
            ("📅 Academic Calendar", self.TimeTable)
        ]
        ttk.Button(dashboard_frame, 
                     text="Logout",
                     style="Sidebar.TButton",
                     command=self.logout).pack(fill="x", pady=5, padx=5, side="bottom")
        
        for text, command in nav_buttons:
            btn = Button(sidebar, text=text, 
                        font=("Arial", 12), 
                        bg="#f0f0f0", bd=0, 
                        anchor=W, padx=20, pady=10,
                        activebackground="#d0d0d0",
                        command=command if command else lambda: None)
            btn.pack(fill=X, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#d0d0d0"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#f0f0f0"))
        
        # Right content area
        self.content_area = Frame(dashboard_frame, bg="white", bd=2, relief=GROOVE)
        self.content_area.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Initial content
        Label(self.content_area, 
             text="Select an option from the sidebar",
             font=("Arial", 14), 
             bg="white", pady=50
             ).pack(expand=True)
        
        # Footer
        footer_frame = Frame(main_frame, bg="#003366", height=40)
        footer_frame.pack(fill=X, pady=(20,0))
        
        Label(footer_frame, 
             text="© 2023 College Name - Student Portal",
             font=("Arial", 10), 
             bg="#003366", fg="white"
             ).pack(pady=10)
        
    def logout(self):
        try:
            self.root.destroy()
            from student_login import StudentLogin
            login_root = Tk()
            StudentLogin(login_root)
            login_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Logout failed: {e}")
    
    def get_student_name(self):
        """Get student name from database using student_id"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT `Student Name` FROM student WHERE StudentID = %s", (self.student_id,))
            result = cursor.fetchone()
            return result['Student Name'] if result else "Student"
        except Exception as e:
            print(f"Error fetching student name: {e}")
            return "Student"
        finally:
            cursor.close()
    
    def open_attendance(self):
        """Open the view_stud_attend.py script with student_id as argument"""
        script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\view_stud_attend.py"
        
        try:
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"File not found: {script_path}")
            
            # Pass student_id as argument to the script
            subprocess.Popen([sys.executable, script_path, self.student_id, "--no-validate"])
            
        except Exception as e:
            error_msg = f"Failed to open attendance viewer:\n{str(e)}"
            messagebox.showerror("Error", error_msg)

    def open_faculty_details(self):
        """Open the view_stud_attend.py script with student_id as argument"""
        script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\faculty_details.py"
        
        try:
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"File not found: {script_path}")
            
            # Pass student_id as argument to the script
            subprocess.Popen([sys.executable, script_path, self.student_id, "--no-validate"])
            
        except Exception as e:
            error_msg = f"Failed to open attendance viewer:\n{str(e)}"
            messagebox.showerror("Error", error_msg)

    def requestPM(self):
        """Open the view_stud_attend.py script with student_id as argument"""
        script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\request_PM.py"
        
        try:
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"File not found: {script_path}")
            
            # Pass student_id as argument to the script
            subprocess.Popen([sys.executable, script_path, self.student_id, "--no-validate"])
            
        except Exception as e:
            error_msg = f"Failed to open attendance viewer:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
    def open_fee_receipts(self):
        """Open the view_stud_attend.py script with student_id as argument"""
        script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\fee_receipts_viewer.py"
        
        try:
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"File not found: {script_path}")
            
            # Pass student_id as argument to the script
            subprocess.Popen([sys.executable, script_path, self.student_id, "--no-validate"])
            
        except Exception as e:
            error_msg = f"Failed to open attendance viewer:\n{str(e)}"
            messagebox.showerror("Error", error_msg)

    def open_study_portal(self):
        """Open the study_portal.py script"""
        script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\study_portal.py"
        
        try:
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"File not found: {script_path}")
            
            subprocess.Popen([sys.executable, script_path])
            
        except Exception as e:
            error_msg = f"Failed to open study portal:\n{str(e)}"
            messagebox.showerror("Error", error_msg)

    def open_question_papers(self):
        """Open the study portal link in the default web browser"""
        url = "https://mits.ac.in/ugc-autonomous-exam-portal#ugc-pro10"

        try:
            webbrowser.open(url)
        except Exception as e:
            error_msg = f"Failed to open study portal:\n{str(e)}"
            messagebox.showerror("Error", error_msg)

    def latest_news(self):
        """Open the study portal link in the default web browser"""
        url = "https://mits.ac.in"

        try:
            webbrowser.open(url)
        except Exception as e:
            error_msg = f"Failed to open study portal:\n{str(e)}"
            messagebox.showerror("Error", error_msg)

    def academic_Syllabus(self):
        """Open the study portal link in the default web browser"""
        url = "https://mits.ac.in/department/28#ug-tab67"

        try:
            webbrowser.open(url)
        except Exception as e:
            error_msg = f"Failed to open study portal:\n{str(e)}"
            messagebox.showerror("Error", error_msg)


    def TimeTable(self):
        """Open the study portal link in the default web browser"""
        url = "https://mits.ac.in/department/28#ug-tab72"

        try:
            webbrowser.open(url)
        except Exception as e:
            error_msg = f"Failed to open study portal:\n{str(e)}"
            messagebox.showerror("Error", error_msg)

    def open_hall_ticket(self):
        script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\view_hallTickets.py"
        subprocess.Popen([sys.executable, script_path, self.student_id])

    def open_result_viewer(self):
        script_path =r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\view_stud_results.py"
        subprocess.Popen([sys.executable, script_path, self.student_id, self.student_name])
    
    def open_study_portal(self):
        """Open the study_portal.py script"""
        script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Student\study_portal.py"
        
        try:
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"File not found: {script_path}")
            
            subprocess.Popen([sys.executable, script_path])
            
        except Exception as e:
            error_msg = f"Failed to open study portal:\n{str(e)}"
            messagebox.showerror("Error", error_msg)


if __name__ == "__main__":
    root = Tk()
    app = StudentPortal(root, student_id="12345")  # Default ID for testing
    root.mainloop()