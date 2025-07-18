from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os
import sys
import subprocess
import webbrowser

class FacultyDashboard:
    def __init__(self, root, faculty_id, faculty_name, department):
        self.root = root
        self.faculty_id = faculty_id
        self.faculty_name = faculty_name
        self.department = department
        
        try:
            self.root.geometry("1366x768")
            self.root.title(f"Faculty Dashboard - {self.department}")
            self.root.state('zoomed')
            
            # Initialize variables
            self.initialize_variables()
            
            # Custom styling
            self.configure_styles()
            
            # Create main frames
            self.create_main_frames()
            
            # Create sidebar with all options
            self.create_sidebar_with_all_options()
            
            # Create content area
            self.create_content_area()
            
            # Database connection
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="face_recognition"
            )
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize dashboard: {e}")
            self.root.destroy()
            raise

    def initialize_variables(self):
        """Initialize all tkinter variables"""
        self.var_dep = StringVar(value=self.department)
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_sec = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        try:
            self.style = ttk.Style()
            self.style.theme_use('clam')
            
            # Header style
            self.style.configure("Header.TLabel", 
                                font=("Arial", 24, "bold"), 
                                background="#2c3e50", 
                                foreground="white",
                                padding=10)
            
            # Sidebar frame style
            self.style.configure("Sidebar.TFrame", background="#34495e")
            
            # Sidebar button style
            self.style.configure("Sidebar.TButton", 
                               font=("Arial", 12),
                               background="white",
                               foreground="black",
                               borderwidth=0,
                               padding=10)
            self.style.map("Sidebar.TButton",
                          foreground=[("active", "white"), ("pressed", "white")],
                          background=[("active", "#3d566e"), ("pressed", "#2c3e50")])
            
            # Submenu styles
            self.style.configure("Submenu.TFrame", background="#2c3e50")
            self.style.configure("Submenu.TButton", 
                               font=("Arial", 10),
                               background="#3d566e",
                               foreground="white",
                               borderwidth=0,
                               padding=8)
            
            # Content frame style
            self.style.configure("Content.TFrame", background="white")
        except Exception as e:
            raise Exception(f"Style configuration failed: {e}")

    def create_main_frames(self):
        """Create the main frames for the application"""
        try:
            # Header Frame
            self.header_frame = ttk.Frame(self.root, style="Header.TLabel")
            self.header_frame.pack(fill="x", side="top")
            
            ttk.Label(self.header_frame, 
                    text=f"{self.department} FACULTY DASHBOARD", 
                    style="Header.TLabel").pack(side=LEFT, padx=20)
            
            ttk.Label(self.header_frame, 
                    text=f"Welcome, {self.faculty_name} (ID: {self.faculty_id})",
                    font=("Arial", 12),
                    background="#2c3e50",
                    foreground="white").pack(side=RIGHT, padx=20)

            # Main Content Frame
            self.main_frame = ttk.Frame(self.root)
            self.main_frame.pack(fill="both", expand=True)
        except Exception as e:
            raise Exception(f"Frame creation failed: {e}")

    def create_sidebar_with_all_options(self):
        """Create sidebar with all navigation options"""
        try:
            # Sidebar Frame
            self.sidebar_frame = ttk.Frame(self.main_frame, style="Sidebar.TFrame", width=280)
            self.sidebar_frame.pack(side="left", fill="y")
            self.sidebar_frame.pack_propagate(False)

            # Attendance Section
            attendance_frame = ttk.Frame(self.sidebar_frame, style="Submenu.TFrame")
            attendance_frame.pack(fill="x", pady=5)
            
            self.attendance_btn = ttk.Button(attendance_frame,
                                          text="Attendance ▼",
                                          style="Sidebar.TButton",
                                          command=self.toggle_attendance_submenu)
            self.attendance_btn.pack(fill="x", padx=5)

            # Attendance submenu
            self.attendance_submenu = ttk.Frame(attendance_frame, style="Submenu.TFrame")
            
            ttk.Button(self.attendance_submenu,
                    text="Face Recognition Attendance",
                    style="Submenu.TButton",
                    command=self.open_camera_attendance).pack(fill="x", pady=2, padx=10)
            
            ttk.Button(self.attendance_submenu,
                    text="Manual Mark Attendance",
                    style="Submenu.TButton",
                    command=self.open_manual_attendance).pack(fill="x", pady=2, padx=10)
            
            ttk.Button(self.attendance_submenu,
                    text="View Attendance Records",
                    style="Submenu.TButton",
                    command=self.open_view_attendance).pack(fill="x", pady=2, padx=10)
            
            ttk.Button(self.sidebar_frame, 
                     text="Manage Updates",
                     style="Sidebar.TButton",
                     command=self.open_manual_updates).pack(fill="x", pady=2, padx=5)

            # Exam Portal Section
            exam_frame = ttk.Frame(self.sidebar_frame, style="Submenu.TFrame")
            exam_frame.pack(fill="x", pady=5)
            
            self.exam_btn = ttk.Button(exam_frame,
                                    text="Exam Portal ▼",
                                    style="Sidebar.TButton",
                                    command=self.toggle_exam_submenu)
            self.exam_btn.pack(fill="x", padx=5)

            # Exam submenu
            self.exam_submenu = ttk.Frame(exam_frame, style="Submenu.TFrame")
            
            
            
            ttk.Button(self.exam_submenu,
                    text="View Exam Results",
                    style="Submenu.TButton",
                    command=self.open_view_results).pack(fill="x", pady=2, padx=10)

            # Student Management
            ttk.Button(self.sidebar_frame,
                     text="View Students",
                     style="Sidebar.TButton",
                     command=self.open_view_students).pack(fill="x", pady=2, padx=5)

            # Other Options
            ttk.Button(self.sidebar_frame, 
                     text="Moodle Portal",
                     style="Sidebar.TButton",
                     command=self.open_moodle_portal).pack(fill="x", pady=2, padx=5)
            
            ttk.Button(self.sidebar_frame, 
                     text="Approve PM",
                     style="Sidebar.TButton",
                     command=self.open_requestPM).pack(fill="x", pady=2, padx=5)
            
            ttk.Button(self.sidebar_frame, 
                     text="Logout",
                     style="Sidebar.TButton",
                     command=self.logout).pack(fill="x", pady=5, padx=5, side="bottom")
        except Exception as e:
            raise Exception(f"Sidebar creation failed: {e}")
    # In faculty_page.py when creating the permission portal
    def open_permission_portal(self):
        permission_window = Toplevel(self.root)
        FacultyDashboard(self.faculty_id, self.faculty_name)  # Pass the logged-in faculty's ID and name

    def toggle_attendance_submenu(self):
        try:
            if self.attendance_submenu.winfo_ismapped():
                self.attendance_submenu.pack_forget()
                self.attendance_btn.config(text="Attendance ▼")
            else:
                self.attendance_submenu.pack(fill="x", pady=5)
                self.attendance_btn.config(text="Attendance ▲")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot toggle menu: {e}")

    def toggle_exam_submenu(self):
        try:
            if self.exam_submenu.winfo_ismapped():
                self.exam_submenu.pack_forget()
                self.exam_btn.config(text="Exam Portal ▼")
            else:
                self.exam_submenu.pack(fill="x", pady=5)
                self.exam_btn.config(text="Exam Portal ▲")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot toggle menu: {e}")

    def create_content_area(self):
        """Create the main content area"""
        try:
            self.content_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
            self.content_frame.pack(side="right", fill="both", expand=True)
            self.show_welcome_message()
        except Exception as e:
            raise Exception(f"Content area creation failed: {e}")

    def show_welcome_message(self):
        """Show welcome message in content area"""
        try:
            for widget in self.content_frame.winfo_children():
                widget.destroy()
                
            Label(self.content_frame, 
                text=f"Welcome to {self.department} Faculty Dashboard\n\n"
                     f"You have access to manage {self.department} department students",
                font=("Arial", 18),
                bg="white").pack(pady=50)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot show welcome message: {e}")

    def open_file_with_department(self, file_path, file_description):
        """Generic function to open department-specific files"""
        try:
            if not hasattr(self, 'department'):
                raise Exception("Department not set")
                
            if os.path.exists(file_path):
                subprocess.Popen([sys.executable, file_path, "--department", self.department])
            else:
                messagebox.showerror("Error", f"{file_description} module not found at: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open {file_description}: {e}")

    def open_camera_attendance(self):
        self.open_file_with_department(
            r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Admin\face_recognition.py",
            "Face Recognition Attendance"
        )

    def open_manual_attendance(self):
        self.open_file_with_department(
            r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\manualAttend.py",
            "Manual Attendance"
        )

    def open_manual_updates(self):
        self.open_file_with_department(
            r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\manage_updates.py",
            "Manage Updates"
        )
    def open_requestPM(self):
        """Open permission management window with auto-filled faculty details"""
        try:
            # Path to your accept_PM.py script
            pm_script_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\accept_PM.py"
        
            if os.path.exists(pm_script_path):
                # Pass faculty_id and faculty_name as command line arguments
                subprocess.Popen([
                    sys.executable, 
                    pm_script_path,
                    "--faculty_id", self.faculty_id,
                    "--faculty_name", self.faculty_name,
                    "--department", self.department
                ])
            else:
                messagebox.showerror("Error", "Permission Management module not found")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open Permission Management: {e}")

    def open_view_attendance(self):
        self.open_file_with_department(
            r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\view_attendance.py",
            "Attendance Viewer"
        )

    def open_add_results(self):
        self.open_file_with_department(
            r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\add_results.py",
            "Add Results"
        )

    def open_view_results(self):
        self.open_file_with_department(
            r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\view_results.py",
            "Results Viewer"
        )
        

    def open_view_students(self):
        self.open_file_with_department(
            r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\stud.py",
            "Student Viewer"
        )

    def open_moodle_portal(self):
        try:
            webbrowser.open("http://20.0.121.215/")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open Moodle: {e}")

    def logout(self):
        try:
            self.root.destroy()
            from faculty_login import FacultyLogin
            login_root = Tk()
            FacultyLogin(login_root)
            login_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Logout failed: {e}")

if __name__ == "__main__":
    try:
        root = Tk()
        # For testing only - use real values from login in production
        obj = FacultyDashboard(root, "560001", "Test Faculty", "CAI") 
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")