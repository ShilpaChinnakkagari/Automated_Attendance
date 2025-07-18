import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import mysql.connector
import hashlib
import re
from PIL import Image, ImageTk
import os

class StudentLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Login System")
        self.root.geometry("1200x700")
        self.root.state('zoomed')
        
        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        
        # Color scheme
        self.bg_color = "#f5f5f5"
        self.frame_color = "#ffffff"
        self.primary_color = "#4CAF50"  # Green theme for students
        self.secondary_color = "#2E7D32"
        self.accent_color = "#81C784"
        
        self.root.configure(bg=self.bg_color)
        
        # Database connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="face_recognition"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Cannot connect to database: {err}")
            self.root.destroy()
            return
        
        # Load and display background image
        self.load_background()
        
        # Create login frame
        self.create_login_frame()
        
        # Center the window
        self.center_window()
    
    def load_background(self):
        try:
            bg_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\College Images\bg.webp"
            if os.path.exists(bg_path):
                self.bg_image = Image.open(bg_path)
                self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                bg_label = tk.Label(self.root, image=self.bg_photo)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label.lower()  # Move to background
        except Exception as e:
            print(f"Background image error: {e}")
            # Fallback to solid color
            self.root.configure(bg=self.bg_color)
    
    def create_login_frame(self):
        # Main login frame
        self.login_frame = tk.Frame(self.root, bg=self.frame_color, bd=2, relief=tk.GROOVE)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=500)
        
        # Title
        title_label = tk.Label(self.login_frame, text="STUDENT PORTAL", 
                             font=self.title_font, fg=self.primary_color, bg=self.frame_color)
        title_label.pack(pady=(30, 10))
        
        # Subtitle
        subtitle_label = tk.Label(self.login_frame, text="Department Student Login", 
                                font=self.label_font, fg="#666666", bg=self.frame_color)
        subtitle_label.pack(pady=(0, 30))
        
        # Student ID
        tk.Label(self.login_frame, text="Student ID", 
               font=self.label_font, fg="#333333", bg=self.frame_color).pack(pady=(10, 5), anchor="w", padx=50)
        self.txt_user = tk.Entry(self.login_frame, font=self.label_font, bg="#f0f0f0", 
                                relief=tk.FLAT, highlightthickness=1, highlightbackground="#cccccc")
        self.txt_user.pack(ipady=5, ipadx=10, pady=5, padx=50, fill=tk.X)
        
        # Password
        tk.Label(self.login_frame, text="Password", 
               font=self.label_font, fg="#333333", bg=self.frame_color).pack(pady=(10, 5), anchor="w", padx=50)
        self.txt_pass = tk.Entry(self.login_frame, font=self.label_font, bg="#f0f0f0", 
                                relief=tk.FLAT, show="*", highlightthickness=1, highlightbackground="#cccccc")
        self.txt_pass.pack(ipady=5, ipadx=10, pady=5, padx=50, fill=tk.X)
        
        # Login Button
        login_btn = tk.Button(self.login_frame, text="LOGIN", command=self.login,
                            bg=self.primary_color, fg="white", font=self.button_font,
                            activebackground=self.secondary_color, activeforeground="white",
                            relief=tk.FLAT, bd=0, padx=20, pady=10)
        login_btn.pack(pady=20, ipadx=50)
        
        # Bottom links frame
        links_frame = tk.Frame(self.login_frame, bg=self.frame_color)
        links_frame.pack(fill=tk.X, pady=(10, 20))
        
        # Forgot Password
        forgot_btn = tk.Button(links_frame, text="Forgot Password?", command=self.forgot_password,
                             font=self.label_font, fg=self.primary_color, bg=self.frame_color,
                             activeforeground=self.secondary_color, bd=0, relief=tk.FLAT)
        forgot_btn.pack(side=tk.LEFT, padx=(50, 10))
        
        # Registration
        reg_btn = tk.Button(links_frame, text="New Student? Register", command=self.show_registration,
                          font=self.label_font, fg=self.primary_color, bg=self.frame_color,
                          activeforeground=self.secondary_color, bd=0, relief=tk.FLAT)
        reg_btn.pack(side=tk.RIGHT, padx=(10, 50))
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def hash_password(self, password):
        """Hash password using SHA-256 with salt"""
        salt = "edu_sys_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def login(self):
        if not hasattr(self, 'conn') or not self.conn.is_connected():
            messagebox.showerror("Error", "Database connection lost")
            return
            
        student_id = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()
        
        if not student_id or not password:
            messagebox.showwarning("Error", "Both Student ID and Password are required")
            return
            
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT studentID, `Student Name` 
                FROM student 
                WHERE studentID = %s AND password = %s
            """, (student_id, self.hash_password(password)))
            
            student = cursor.fetchone()
            
            if student:
                messagebox.showinfo("Success", f"Welcome, {student['Student Name']}!")
                self.root.destroy()
                
                from student_page import StudentPortal
                new_root = tk.Tk()
                StudentPortal(new_root, student_id=student['studentID'])
                new_root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid Student ID or Password")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Login failed: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def forgot_password(self):
        forgot_window = tk.Toplevel(self.root)
        forgot_window.title("Password Recovery")
        forgot_window.geometry("500x400")
        forgot_window.resizable(False, False)
        forgot_window.configure(bg=self.bg_color)
        
        forgot_window.update_idletasks()
        fw_width = forgot_window.winfo_width()
        fw_height = forgot_window.winfo_height()
        fw_x = (forgot_window.winfo_screenwidth() // 2) - (fw_width // 2)
        fw_y = (forgot_window.winfo_screenheight() // 2) - (fw_height // 2)
        forgot_window.geometry(f'+{fw_x}+{fw_y}')
        
        main_frame = tk.Frame(forgot_window, bg=self.frame_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Password Recovery", 
               font=self.title_font, fg=self.primary_color, bg=self.frame_color).pack(pady=20)
        
        tk.Label(main_frame, text="Student ID:", 
               font=self.label_font, fg="#333333", bg=self.frame_color).pack(anchor="w", pady=(10, 5))
        student_id_entry = tk.Entry(main_frame, font=self.label_font, bg="#f0f0f0", 
                                  relief=tk.FLAT, highlightthickness=1, highlightbackground="#cccccc")
        student_id_entry.pack(fill=tk.X, ipady=5, ipadx=10, pady=5)
        
        tk.Label(main_frame, text="Registered Email:", 
               font=self.label_font, fg="#333333", bg=self.frame_color).pack(anchor="w", pady=(10, 5))
        email_entry = tk.Entry(main_frame, font=self.label_font, bg="#f0f0f0", 
                             relief=tk.FLAT, highlightthickness=1, highlightbackground="#cccccc")
        email_entry.pack(fill=tk.X, ipady=5, ipadx=10, pady=5)
        
        def verify_and_reset():
            student_id = student_id_entry.get().strip()
            email = email_entry.get().strip()
            
            if not student_id or not email:
                messagebox.showwarning("Error", "Both fields are required")
                return
                
            try:
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT CollegeMail FROM student 
                    WHERE studentID = %s AND CollegeMail = %s
                """, (student_id, email))
                
                if cursor.fetchone():
                    messagebox.showinfo("Success", 
                        "Password reset instructions have been sent to your registered email.")
                    forgot_window.destroy()
                else:
                    messagebox.showerror("Error", 
                        "No matching student found with that ID and email.")
                    
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                if 'cursor' in locals():
                    cursor.close()
        
        reset_btn = tk.Button(main_frame, text="Reset Password", command=verify_and_reset,
                            bg=self.primary_color, fg="white", font=self.button_font,
                            activebackground=self.secondary_color, activeforeground="white",
                            relief=tk.FLAT, bd=0, padx=20, pady=10)
        reset_btn.pack(pady=20, ipadx=50)
    
    def show_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Student Credential Setup")
        reg_window.geometry("500x600")
        reg_window.resizable(False, False)
        reg_window.configure(bg=self.bg_color)
    
        reg_window.update_idletasks()
        width = reg_window.winfo_width()
        height = reg_window.winfo_height()
        x = (reg_window.winfo_screenwidth() // 2) - (width // 2)
        y = (reg_window.winfo_screenheight() // 2) - (height // 2)
        reg_window.geometry(f'+{x}+{y}')

        main_frame = tk.Frame(reg_window, bg=self.frame_color, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Set Your Password", 
                font=self.title_font, fg=self.primary_color, bg=self.frame_color).pack(pady=(0, 20))

        explanation = ("Please enter your student ID and registered email to verify your identity, "
                      "then set your new password.")
        tk.Label(main_frame, text=explanation, wraplength=400, justify=tk.LEFT,
                font=self.label_font, fg="#555555", bg=self.frame_color).pack(pady=(0, 20))

        tk.Label(main_frame, text="Student ID*", anchor="w",
                font=self.label_font, fg="#333333", bg=self.frame_color).pack(fill=tk.X)
        student_id_entry = tk.Entry(main_frame, font=self.label_font, bg="#f0f0f0",
                                  relief=tk.FLAT, highlightthickness=1, highlightbackground="#cccccc")
        student_id_entry.pack(fill=tk.X, ipady=5, pady=(0, 15))

        tk.Label(main_frame, text="Registered Email*", anchor="w",
                font=self.label_font, fg="#333333", bg=self.frame_color).pack(fill=tk.X)
        email_entry = tk.Entry(main_frame, font=self.label_font, bg="#f0f0f0",
                             relief=tk.FLAT, highlightthickness=1, highlightbackground="#cccccc")
        email_entry.pack(fill=tk.X, ipady=5, pady=(0, 15))

        tk.Label(main_frame, text="New Password*", anchor="w",
                font=self.label_font, fg="#333333", bg=self.frame_color).pack(fill=tk.X)
        password_entry = tk.Entry(main_frame, font=self.label_font, bg="#f0f0f0",
                                relief=tk.FLAT, show="*", highlightthickness=1, highlightbackground="#cccccc")
        password_entry.pack(fill=tk.X, ipady=5, pady=(0, 5))

        strength_frame = tk.Frame(main_frame, bg=self.frame_color, height=5)
        strength_frame.pack(fill=tk.X, pady=(0, 15))
        strength_meter = tk.Label(strength_frame, bg="#e0e0e0")
        strength_meter.pack(fill=tk.X)

        tk.Label(main_frame, text="Confirm Password*", anchor="w",
                font=self.label_font, fg="#333333", bg=self.frame_color).pack(fill=tk.X)
        confirm_password_entry = tk.Entry(main_frame, font=self.label_font, bg="#f0f0f0",
                                       relief=tk.FLAT, show="*", highlightthickness=1, highlightbackground="#cccccc")
        confirm_password_entry.pack(fill=tk.X, ipady=5, pady=(0, 20))

        save_btn = tk.Button(main_frame, text="SAVE PASSWORD", command=lambda: self.register_student(
            student_id_entry.get(),
            email_entry.get(),
            password_entry.get(),
            confirm_password_entry.get(),
            reg_window,
            strength_meter
        ), bg=self.primary_color, fg="white", font=self.button_font,
        activebackground=self.secondary_color, activeforeground="white",
        relief=tk.FLAT, bd=0, padx=20, pady=10)
        save_btn.pack(fill=tk.X, ipady=8)

        password_entry.bind("<KeyRelease>", lambda e: self.update_strength_meter(
            password_entry.get(),
            strength_meter
        ))

    def update_strength_meter(self, password, meter):
        length = len(password)
        if length == 0:
            meter.config(bg="#e0e0e0", width=0)
        elif length < 4:
            meter.config(bg="#ff4444", width=50)
        elif length < 8:
            meter.config(bg="#ffbb33", width=150)
        else:
            meter.config(bg="#00C851", width=250)

    def register_student(self, student_id, email, password, confirm_password, window, strength_meter):
        if not all([student_id, email, password, confirm_password]):
            messagebox.showwarning("Error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Error", "Please enter a valid email address")
            return

        if len(password) < 6:
            messagebox.showwarning("Error", "Password must be at least 6 characters")
            strength_meter.config(bg="#ff4444")
            return

        try:
            cursor = self.conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT studentID, CollegeMail, password FROM student 
                WHERE studentID = %s AND CollegeMail = %s
            """, (student_id, email))

            student = cursor.fetchone()

            if not student:
                messagebox.showerror("Error", 
                    "No matching student found. Please check your ID and email.")
                return

            if student['password'] not in (None, '', 'NULL'):
                messagebox.showwarning("Already Registered", 
                    "This student is already registered. Use 'Forgot Password' if needed.")
                return

            hashed_password = self.hash_password(password)
            cursor.execute("""
                UPDATE student SET password = %s 
                WHERE studentID = %s
            """, (hashed_password, student_id))

            self.conn.commit()

            messagebox.showinfo("Success", 
                "Your password has been set successfully!\nYou can now login with your credentials.")
            window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Registration failed: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StudentLogin(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")