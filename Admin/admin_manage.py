import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import mysql.connector
import hashlib

class AdminManage:
    def __init__(self, root, admin_id, admin_name):
        self.root = root
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.root.title(f"Admin Management Portal - {self.admin_name}")
        self.root.state('zoomed')
        
        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
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
        
        self.create_widgets()
        self.load_admin_data()
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.primary_color)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(header_frame, text=f"Admin Management Portal - {self.admin_name}", 
                font=self.title_font, bg=self.primary_color, fg="white").pack(side=tk.LEFT, padx=20, pady=10)
        
        logout_btn = tk.Button(header_frame, text="Logout", command=self.logout,
                             bg="#e74c3c", fg="white", font=self.button_font,
                             relief=tk.FLAT)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Admin Management Frame
        admin_frame = tk.LabelFrame(main_frame, text="Admin Accounts Management", 
                                  font=self.label_font, bg=self.frame_color,
                                  bd=2, relief=tk.GROOVE)
        admin_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for admin list
        self.tree = ttk.Treeview(admin_frame, columns=("ID", "Name", "Email", "Phone"), 
                                show="headings", selectmode="browse")
        
        self.tree.heading("ID", text="Admin ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.W)
        self.tree.column("Email", width=200, anchor=tk.W)
        self.tree.column("Phone", width=120, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(admin_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Button Frame
        button_frame = tk.Frame(admin_frame, bg=self.frame_color)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(button_frame, text="Add Admin", command=self.add_admin,
                          bg="#2ecc71", fg="white", font=self.button_font,
                          relief=tk.FLAT)
        add_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
        
        edit_btn = tk.Button(button_frame, text="Edit Admin", command=self.edit_admin,
                           bg="#3498db", fg="white", font=self.button_font,
                           relief=tk.FLAT)
        edit_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
        
        delete_btn = tk.Button(button_frame, text="Delete Admin", command=self.delete_admin,
                             bg="#e74c3c", fg="white", font=self.button_font,
                             relief=tk.FLAT)
        delete_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
        
        reset_btn = tk.Button(button_frame, text="Reset Password", command=self.reset_password,
                             bg="#f39c12", fg="white", font=self.button_font,
                             relief=tk.FLAT)
        reset_btn.pack(side=tk.LEFT, padx=5, ipadx=10)
        
        refresh_btn = tk.Button(button_frame, text="Refresh", command=self.load_admin_data,
                              bg="#9b59b6", fg="white", font=self.button_font,
                              relief=tk.FLAT)
        refresh_btn.pack(side=tk.RIGHT, padx=5, ipadx=10)
    
    def load_admin_data(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT admin_id, name, email, phone FROM admin")
            admin_data = cursor.fetchall()
            
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Insert new data
            for admin in admin_data:
                self.tree.insert("", tk.END, values=(
                    admin['admin_id'],
                    admin['name'],
                    admin['email'],
                    admin['phone']
                ))
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load admin data: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def add_admin(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add New Admin")
        self.add_window.grab_set()
        
        # Form fields
        tk.Label(self.add_window, text="Admin ID:", font=self.label_font).grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.admin_id_entry = tk.Entry(self.add_window, font=self.label_font)
        self.admin_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.add_window, text="Name:", font=self.label_font).grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.name_entry = tk.Entry(self.add_window, font=self.label_font)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.add_window, text="Email:", font=self.label_font).grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.email_entry = tk.Entry(self.add_window, font=self.label_font)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.add_window, text="Phone:", font=self.label_font).grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.phone_entry = tk.Entry(self.add_window, font=self.label_font)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.add_window, text="Password:", font=self.label_font).grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.password_entry = tk.Entry(self.add_window, font=self.label_font, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Buttons
        btn_frame = tk.Frame(self.add_window)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Save", command=self.save_admin, 
                 bg="#2ecc71", fg="white", font=self.button_font).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.add_window.destroy,
                 bg="#e74c3c", fg="white", font=self.button_font).pack(side=tk.LEFT, padx=5)
    
    def save_admin(self):
        # Get form data
        admin_id = self.admin_id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not all([admin_id, name, email, phone, password]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Check if admin ID already exists
            cursor.execute("SELECT admin_id FROM admin WHERE admin_id = %s", (admin_id,))
            if cursor.fetchone():
                messagebox.showerror("Error", f"Admin ID {admin_id} already exists!")
                return
                
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Insert new admin
            cursor.execute("""
                INSERT INTO admin (admin_id, name, email, phone, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (admin_id, name, email, phone, hashed_password))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Admin added successfully!")
            self.add_window.destroy()
            self.load_admin_data()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to add admin: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def edit_admin(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an admin to edit")
            return
            
        admin_data = self.tree.item(selected_item)['values']
        
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Admin")
        self.edit_window.grab_set()
        
        # Form fields with existing data
        tk.Label(self.edit_window, text="Admin ID:", font=self.label_font).grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.edit_admin_id = tk.Label(self.edit_window, text=admin_data[0], font=self.label_font)
        self.edit_admin_id.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.edit_window, text="Name:", font=self.label_font).grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.edit_name_entry = tk.Entry(self.edit_window, font=self.label_font)
        self.edit_name_entry.insert(0, admin_data[1])
        self.edit_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.edit_window, text="Email:", font=self.label_font).grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.edit_email_entry = tk.Entry(self.edit_window, font=self.label_font)
        self.edit_email_entry.insert(0, admin_data[2])
        self.edit_email_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(self.edit_window, text="Phone:", font=self.label_font).grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.edit_phone_entry = tk.Entry(self.edit_window, font=self.label_font)
        self.edit_phone_entry.insert(0, admin_data[3])
        self.edit_phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Buttons
        btn_frame = tk.Frame(self.edit_window)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Update", command=lambda: self.update_admin(admin_data[0]), 
                 bg="#3498db", fg="white", font=self.button_font).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.edit_window.destroy,
                 bg="#e74c3c", fg="white", font=self.button_font).pack(side=tk.LEFT, padx=5)
    
    def update_admin(self, admin_id):
        # Get form data
        name = self.edit_name_entry.get().strip()
        email = self.edit_email_entry.get().strip()
        phone = self.edit_phone_entry.get().strip()
        
        # Validation
        if not all([name, email, phone]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Update admin
            cursor.execute("""
                UPDATE admin 
                SET name = %s, email = %s, phone = %s
                WHERE admin_id = %s
            """, (name, email, phone, admin_id))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Admin updated successfully!")
            self.edit_window.destroy()
            self.load_admin_data()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update admin: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def delete_admin(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an admin to delete")
            return
            
        admin_data = self.tree.item(selected_item)['values']
        
        # Prevent deleting yourself
        if admin_data[0] == self.admin_id:
            messagebox.showwarning("Error", "You cannot delete your own account!")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete {admin_data[1]} ({admin_data[0]})?")
        if not confirm:
            return
            
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM admin WHERE admin_id = %s", (admin_data[0],))
            self.conn.commit()
            messagebox.showinfo("Success", "Admin deleted successfully!")
            self.load_admin_data()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to delete admin: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def reset_password(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an admin to reset password")
            return
            
        admin_data = self.tree.item(selected_item)['values']
        
        self.pass_window = tk.Toplevel(self.root)
        self.pass_window.title("Reset Password")
        self.pass_window.grab_set()
        
        tk.Label(self.pass_window, text=f"Reset password for {admin_data[1]} ({admin_data[0]})", 
                font=self.label_font).pack(padx=20, pady=10)
        
        tk.Label(self.pass_window, text="New Password:", font=self.label_font).pack(padx=20, pady=5)
        self.new_pass_entry = tk.Entry(self.pass_window, font=self.label_font, show="*")
        self.new_pass_entry.pack(padx=20, pady=5)
        
        tk.Label(self.pass_window, text="Confirm Password:", font=self.label_font).pack(padx=20, pady=5)
        self.confirm_pass_entry = tk.Entry(self.pass_window, font=self.label_font, show="*")
        self.confirm_pass_entry.pack(padx=20, pady=5)
        
        btn_frame = tk.Frame(self.pass_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Reset", command=lambda: self.save_new_password(admin_data[0]), 
                 bg="#f39c12", fg="white", font=self.button_font).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.pass_window.destroy,
                 bg="#e74c3c", fg="white", font=self.button_font).pack(side=tk.LEFT, padx=5)
    
    def save_new_password(self, admin_id):
        new_pass = self.new_pass_entry.get().strip()
        confirm_pass = self.confirm_pass_entry.get().strip()
        
        if not new_pass or not confirm_pass:
            messagebox.showwarning("Validation Error", "Both password fields are required!")
            return
            
        if new_pass != confirm_pass:
            messagebox.showwarning("Validation Error", "Passwords do not match!")
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Hash the new password
            hashed_password = self.hash_password(new_pass)
            
            # Update password
            cursor.execute("UPDATE admin SET password = %s WHERE admin_id = %s", 
                          (hashed_password, admin_id))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Password reset successfully!")
            self.pass_window.destroy()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to reset password: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def hash_password(self, password):
        salt = "admin_secure_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def logout(self):
        self.conn.close()
        self.root.destroy()
        # Reopen login window
        from admin_login import AdminLogin
        root = tk.Tk()
        AdminLogin(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminManage(root, "admin1", "Super Admin")
    root.mainloop()