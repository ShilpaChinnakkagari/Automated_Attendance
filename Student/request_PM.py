import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from datetime import datetime
from tkinter import *

class StudentPortal:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.root = tk.Tk()
        self.root.title(f"Student Permission Portal - {student_name}")
        self.root.geometry("1000x700")
        self.root.state('zoomed')
        
        # Database connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="college_management"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
            sys.exit(1)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header Frame
        header_frame = Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=X)
        
        Label(header_frame, text=f"Student Permission Portal - {self.student_name}", 
             font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
        
        # Main Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Create New Request
        create_frame = Frame(self.notebook)
        self.notebook.add(create_frame, text="New Request")
        self.setup_request_tab(create_frame)
        
        # Tab 2: My Requests
        requests_frame = Frame(self.notebook)
        self.notebook.add(requests_frame, text="My Requests")
        self.setup_requests_tab(requests_frame)
        
        # Status Bar
        self.status = Label(self.root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(fill=X, side=BOTTOM)
    
    def setup_request_tab(self, parent):
        Label(parent, text="Create New Permission Request", 
             font=("Arial", 12, "bold")).pack(pady=10)
        
        # Request Type
        Label(parent, text="Request Type:").pack(anchor=W, padx=20)
        self.request_type = ttk.Combobox(parent, 
                                      values=["attendance", "promotion", 
                                             "internship", "project", "other"])
        self.request_type.pack(fill=X, padx=20, pady=5)
        self.request_type.current(0)
        
        # Faculty Selection
        Label(parent, text="To Faculty:").pack(anchor=W, padx=20)
        self.faculty_combo = ttk.Combobox(parent)
        self.faculty_combo.pack(fill=X, padx=20, pady=5)
        self.load_faculty_list()
        
        # Subject
        Label(parent, text="Subject:").pack(anchor=W, padx=20)
        self.subject = Entry(parent)
        self.subject.pack(fill=X, padx=20, pady=5)
        
        # Letter Text
        Label(parent, text="Message Content:").pack(anchor=W, padx=20)
        self.message_text = scrolledtext.ScrolledText(parent, height=15)
        self.message_text.pack(fill=BOTH, expand=True, padx=20, pady=5)
        
        # Submit Button
        Button(parent, text="Submit Request", command=self.submit_request,
              bg="#27ae60", fg="white").pack(pady=10)
    
    def setup_requests_tab(self, parent):
        # Treeview to show requests
        self.requests_tree = ttk.Treeview(parent, 
                                        columns=("id", "faculty", "type", "subject", "status", "date"))
        
        self.requests_tree.heading("#0", text="")
        self.requests_tree.heading("id", text="Request ID")
        self.requests_tree.heading("faculty", text="Faculty")
        self.requests_tree.heading("type", text="Type")
        self.requests_tree.heading("subject", text="Subject")
        self.requests_tree.heading("status", text="Status")
        self.requests_tree.heading("date", text="Date")
        
        self.requests_tree.column("#0", width=0, stretch=NO)
        self.requests_tree.column("id", width=80)
        self.requests_tree.column("faculty", width=150)
        self.requests_tree.column("type", width=100)
        self.requests_tree.column("subject", width=200)
        self.requests_tree.column("status", width=100)
        self.requests_tree.column("date", width=120)
        
        scroll_y = Scrollbar(parent, orient=VERTICAL, command=self.requests_tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.requests_tree.configure(yscrollcommand=scroll_y.set)
        
        self.requests_tree.pack(fill=BOTH, expand=True)
        
        # Details Frame
        details_frame = Frame(parent, bd=2, relief=GROOVE, padx=10, pady=10)
        details_frame.pack(fill=X, padx=10, pady=10)
        
        self.request_details = scrolledtext.ScrolledText(details_frame, height=8, state=DISABLED)
        self.request_details.pack(fill=BOTH, expand=True)
        
        # Bind selection event
        self.requests_tree.bind("<<TreeviewSelect>>", self.show_request_details)
        
        # Load requests
        self.load_requests()
    
    def load_faculty_list(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT faculty_id, name FROM faculty ORDER BY name")
            faculty_list = [f"{row['faculty_id']} - {row['name']}" for row in cursor.fetchall()]
            self.faculty_combo['values'] = faculty_list
            if faculty_list:
                self.faculty_combo.current(0)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading faculty list: {err}")
        finally:
            cursor.close()
    
    def submit_request(self):
        request_type = self.request_type.get()
        faculty = self.faculty_combo.get()
        subject = self.subject.get()
        message = self.message_text.get("1.0", END).strip()
        
        if not faculty:
            messagebox.showwarning("Validation Error", "Please select a faculty member")
            return
        if not subject:
            messagebox.showwarning("Validation Error", "Please enter a subject")
            return
        if not message:
            messagebox.showwarning("Validation Error", "Please write your message content")
            return
        
        faculty_id = faculty.split(" - ")[0]
        
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO permission_requests 
                (student_id, student_name, faculty_id, request_type, subject, message, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'pending')
            """
            cursor.execute(query, (self.student_id, self.student_name, faculty_id, request_type, subject, message))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", "Your permission request has been submitted successfully!")
            self.status.config(text=f"Request submitted to {faculty} at {datetime.now().strftime('%H:%M:%S')}")
            
            # Clear form
            self.subject.delete(0, END)
            self.message_text.delete("1.0", END)
            
            # Refresh requests
            self.load_requests()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error submitting request: {err}")
        finally:
            cursor.close()
    
    def load_requests(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT r.request_id, r.request_type, r.subject, r.status, r.created_at,
                       f.name as faculty_name
                FROM permission_requests r
                JOIN faculty f ON r.faculty_id = f.faculty_id
                WHERE r.student_id = %s
                ORDER BY r.created_at DESC
            """
            cursor.execute(query, (self.student_id,))
            
            # Clear existing data
            for item in self.requests_tree.get_children():
                self.requests_tree.delete(item)
            
            # Add new data
            for row in cursor.fetchall():
                self.requests_tree.insert("", "end", 
                                        values=(
                                            row['request_id'],
                                            row['faculty_name'],
                                            row['request_type'],
                                            row['subject'],
                                            row['status'],
                                            row['created_at'].strftime("%Y-%m-%d %H:%M")
                                        ))
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading requests: {err}")
        finally:
            cursor.close()
    
    def show_request_details(self, event):
        selected_item = self.requests_tree.focus()
        if not selected_item:
            return
        
        request_id = self.requests_tree.item(selected_item)['values'][0]
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT r.*, f.name as faculty_name
                FROM permission_requests r
                JOIN faculty f ON r.faculty_id = f.faculty_id
                WHERE r.request_id = %s
            """
            cursor.execute(query, (request_id,))
            request = cursor.fetchone()
            
            if not request:
                return
            
            # Format the details text
            details_text = f"""
Request ID: {request['request_id']}
Type: {request['request_type']}
To: {request['faculty_name']}
Subject: {request['subject']}
Status: {request['status']}
Date Submitted: {request['created_at'].strftime("%Y-%m-%d %H:%M:%S")}

--- Message Content ---
{request['message']}

"""
            if request['status'] != 'pending':
                details_text += f"""
--- Faculty Response ---
Status: {request['status']}
Response Date: {request['decision_date'].strftime("%Y-%m-%d %H:%M:%S") if request['decision_date'] else 'N/A'}
Remarks: {request['faculty_remarks'] or 'None'}
"""
            self.request_details.config(state=NORMAL)
            self.request_details.delete("1.0", END)
            self.request_details.insert("1.0", details_text)
            self.request_details.config(state=DISABLED)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading request details: {err}")
        finally:
            cursor.close()

if __name__ == "__main__":
    import tkinter.simpledialog as simpledialog

    root = tk.Tk()
    root.withdraw()  # Hide the initial window

    student_id = simpledialog.askstring("Student Login", "Enter Student ID:")
    student_name = simpledialog.askstring("Student Login", "Enter Student Name:")

    if student_id and student_name:
        app = StudentPortal(student_id, student_name)
        app.root.mainloop()
    else:
        messagebox.showwarning("Login Failed", "Student ID and Name are required.")
