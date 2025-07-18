import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import mysql.connector
import hashlib
import re
from PIL import Image, ImageTk
import os

class AdminLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login System")
        self.root.geometry("1200x700")
        self.root.state('zoomed')

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        # Colors
        self.bg_color = "#f5f5f5"
        self.frame_color = "#ffffff"
        self.primary_color = "#4a6fa5"
        self.secondary_color = "#166088"

        self.root.configure(bg=self.bg_color)

        # Connect to database
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="college_management"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Cannot connect: {err}")
            self.root.destroy()
            return

        self.load_background()
        self.create_login_frame()
        self.center_window()

    def load_background(self):
        try:
            bg_path = r"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\College Images\bg.webp"
            if os.path.exists(bg_path):
                image = Image.open(bg_path)
                image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(image)
                label = tk.Label(self.root, image=self.bg_photo)
                label.place(x=0, y=0, relwidth=1, relheight=1)
                label.lower()
        except Exception as e:
            print(f"Background load error: {e}")
            self.root.configure(bg=self.bg_color)

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root, bg=self.frame_color, bd=2, relief=tk.GROOVE)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=500)

        tk.Label(self.login_frame, text="ADMIN PORTAL", font=self.title_font,
                 fg=self.primary_color, bg=self.frame_color).pack(pady=(30, 10))

        tk.Label(self.login_frame, text="College Management Login", font=self.label_font,
                 fg="#666666", bg=self.frame_color).pack(pady=(0, 30))

        # Admin ID
        tk.Label(self.login_frame, text="Admin ID", font=self.label_font,
                 fg="#333333", bg=self.frame_color).pack(pady=(10, 5), anchor="w", padx=50)
        self.txt_user = tk.Entry(self.login_frame, font=self.label_font, bg="#f0f0f0",
                                 relief=tk.FLAT, highlightthickness=1, highlightbackground="#cccccc")
        self.txt_user.pack(ipady=5, ipadx=10, pady=5, padx=50, fill=tk.X)

        # Password
        tk.Label(self.login_frame, text="Password", font=self.label_font,
                 fg="#333333", bg=self.frame_color).pack(pady=(10, 5), anchor="w", padx=50)
        self.txt_pass = tk.Entry(self.login_frame, font=self.label_font, bg="#f0f0f0",
                                 relief=tk.FLAT, show="*", highlightthickness=1, highlightbackground="#cccccc")
        self.txt_pass.pack(ipady=5, ipadx=10, pady=5, padx=50, fill=tk.X)

        # Login Button
        login_btn = tk.Button(self.login_frame, text="LOGIN", command=self.login,
                              bg=self.primary_color, fg="white", font=self.button_font,
                              activebackground=self.secondary_color, activeforeground="white",
                              relief=tk.FLAT, bd=0, padx=20, pady=10)
        login_btn.pack(pady=20, ipadx=50)

        # Forgot password link
        forgot_btn = tk.Button(self.login_frame, text="Forgot Password?", command=self.forgot_password,
                               font=self.label_font, fg=self.primary_color, bg=self.frame_color,
                               activeforeground=self.secondary_color, bd=0, relief=tk.FLAT)
        forgot_btn.pack(pady=(10, 5))

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def hash_password(self, password):
        salt = "admin_secure_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def login(self):
        if not hasattr(self, 'conn') or not self.conn.is_connected():
            messagebox.showerror("Error", "Database connection lost")
            return

        admin_id = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()

        if not admin_id or not password:
            messagebox.showwarning("Error", "Both Admin ID and Password are required")
            return

        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT admin_id, name FROM admin WHERE admin_id = %s AND password = %s",
                           (admin_id, self.hash_password(password)))
            admin = cursor.fetchone()

            if admin:
                messagebox.showinfo("Success", f"Welcome, {admin['name']} (Admin)")
                self.root.withdraw()  # Hide login window instead of destroying
                
                # Launch admin dashboard
                from admin_page import AdminDashboard
                dashboard = AdminDashboard(self.root, admin['admin_id'], admin['name'])
            else:
                messagebox.showerror("Error", "Invalid Admin ID or Password")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Login failed: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def forgot_password(self):
        messagebox.showinfo("Info", "This feature will allow password reset via email in the future.")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AdminLogin(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")