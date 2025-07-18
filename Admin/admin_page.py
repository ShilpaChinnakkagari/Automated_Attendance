import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
import subprocess
import os
import sys

class AdminDashboard(tk.Toplevel):
    def __init__(self, master, admin_id, admin_name):
        super().__init__(master)
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.title(f"ADMIN PORTAL - MITS | Welcome {self.admin_name}")
        self.geometry("1366x768")
        self.configure(bg="#2c3e50")
        self.state('zoomed')
        
        # Store reference to master (login window)
        self.master = master
        
        # Initialize web_frame
        self.web_frame = None
        
        # Custom styling
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
        
        # Button style
        self.style.configure("Sidebar.TButton", 
                           font=("Arial", 12),
                           background="white",
                           foreground="black",
                           borderwidth=0,
                           padding=10)
        self.style.map("Sidebar.TButton",
                      foreground=[("active", "white"), ("pressed", "white")],
                      background=[("active", "#3d566e"), ("pressed", "#2c3e50")])
        
        # Create UI
        self.create_widgets()
        
        # Load initial website
        self.after(100, self.open_website)

    def create_widgets(self):
        # Header Frame
        header_frame = ttk.Frame(self, style="Header.TLabel")
        header_frame.pack(fill="x", side="top")
        
        header_label = ttk.Label(header_frame, 
                        text=f"ADMIN PORTAL - MITS | Welcome {self.admin_name}", 
                        style="Header.TLabel")
        header_label.pack(expand=True)

        # Main Content Frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Sidebar Frame
        sidebar_frame = ttk.Frame(main_frame, style="Sidebar.TFrame", width=250)
        sidebar_frame.pack(side="left", fill="y")
        sidebar_frame.pack_propagate(False)

        # Content Frame
        content_frame = ttk.Frame(main_frame, style="Content.TFrame")
        content_frame.pack(side="right", fill="both", expand=True)

        # Web Frame
        self.web_frame = HtmlFrame(content_frame)
        self.web_frame.pack(fill="both", expand=True)

        # Back button
        back_button = tk.Button(sidebar_frame, 
                              text="HELLO MITSIAN", 
                              bg="white",
                              fg="black",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        back_button.pack(fill="x", pady=(10, 5), padx=5)

        # Separator
        ttk.Separator(sidebar_frame, orient="horizontal").pack(fill="x", pady=5)
        
        # Options buttons
        self.options = [
            {"name": "Manage Updates", "file": r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\Faculty\manage_updates.py"},
            {"name": "Enroll ADMIN", "file": "admin_manage.py"},
            {"name": "Enroll Faculty", "file": "faculty_enroll.py"},
            {"name": "Add Course Details", "file": "course.py"},
            {"name": "Add Student Details", "file": "student.py"},
            {"name": "Add Student Results", "file": "result_Add.py"},
            {"name": "View Student Results", "file": "results_View.py"},
            {"name": "Hall Ticket Generation", "file": "hallticket_generator.py"},
            {"name": "Fee Receipts", "file": "fee_receipts_generator.py"},
            {"name": "Take Student Attendance", "file": "face_recognition.py"},
            {"name": "View Student Attendance", "file": "attendance.py"},
        ]

        for option in self.options:
            btn = ttk.Button(sidebar_frame, 
                           text=option["name"], 
                           style="Sidebar.TButton", 
                           command=lambda o=option: self.open_python_file(o["file"]))
            btn.pack(fill="x", pady=2, padx=5)

        # Logout button
        logout_button = tk.Button(sidebar_frame, 
                              text="Log out", 
                              bg="#ff0000",
                              fg="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat",
                              command=self.log_out)
        logout_button.pack(fill="x", pady=(10, 5), padx=5, side="bottom")

    def open_python_file(self, filename):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, filename)
            
            if os.path.exists(file_path):
                subprocess.Popen([sys.executable, file_path])
            else:
                self.show_error(f"File not found: {filename}")
        except Exception as e:
            self.show_error(f"Failed to open {filename}: {str(e)}")

    def show_error(self, message):
        if self.web_frame:
            self.web_frame.load_html(f"""
                <div style='padding: 20px; font-family: Arial; color: red;'>
                    <h2>Error</h2>
                    <p>{message}</p>
                </div>
            """)

    def open_website(self):
        if self.web_frame:
            self.web_frame.load_url("https://mits.ac.in/")

    def log_out(self):
        self.destroy()
        self.master.deiconify()  # Show the login window again

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = AdminDashboard(root, "admin001", "Test Admin")
    root.mainloop()