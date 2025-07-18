import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from datetime import datetime
from tkinter import *

class FacultyPortal:
    def __init__(self, faculty_id, faculty_name):
        self.faculty_id = faculty_id
        self.faculty_name = faculty_name
        self.root = tk.Tk()
        self.root.title(f"Faculty Portal - {faculty_name}")
        self.root.state('zoomed')
        
        # Database connection with error handling
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="college_management"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
            self.root.destroy()
            return
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header Frame
        header_frame = Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=X)
        
        Label(header_frame, text=f"Faculty Portal - {self.faculty_name}", 
             font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
        
        # Main Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Pending Requests
        pending_frame = Frame(self.notebook)
        self.notebook.add(pending_frame, text="Pending Requests")
        self.setup_pending_tab(pending_frame)
        
        # Tab 2: All Requests
        all_requests_frame = Frame(self.notebook)
        self.notebook.add(all_requests_frame, text="All Requests")
        self.setup_all_requests_tab(all_requests_frame)
        
        # Status Bar
        self.status = Label(self.root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(fill=X, side=BOTTOM)
    
    def setup_pending_tab(self, parent):
        Label(parent, text="Pending Permission Requests", 
             font=("Arial", 12, "bold")).pack(pady=10)
        
        # Treeview to show pending requests
        self.pending_tree = ttk.Treeview(parent, 
                                       columns=("id", "student", "type", "subject", "date"))
        
        self.pending_tree.heading("#0", text="")
        self.pending_tree.heading("id", text="Request ID")
        self.pending_tree.heading("student", text="Student")
        self.pending_tree.heading("type", text="Type")
        self.pending_tree.heading("subject", text="Subject")
        self.pending_tree.heading("date", text="Date")
        
        self.pending_tree.column("#0", width=0, stretch=NO)
        self.pending_tree.column("id", width=80)
        self.pending_tree.column("student", width=150)
        self.pending_tree.column("type", width=100)
        self.pending_tree.column("subject", width=200)
        self.pending_tree.column("date", width=120)
        
        scroll_y = Scrollbar(parent, orient=VERTICAL, command=self.pending_tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.pending_tree.configure(yscrollcommand=scroll_y.set)
        
        self.pending_tree.pack(fill=BOTH, expand=True)
        
        # Details Frame
        details_frame = Frame(parent, bd=2, relief=GROOVE, padx=10, pady=10)
        details_frame.pack(fill=X, padx=10, pady=10)
        
        self.request_details = scrolledtext.ScrolledText(details_frame, height=8, state=DISABLED)
        self.request_details.pack(fill=BOTH, expand=True)
        
        # Action Buttons
        button_frame = Frame(parent)
        button_frame.pack(pady=10)
        
        Button(button_frame, text="Approve", command=self.approve_request,
              bg="#27ae60", fg="white").pack(side=LEFT, padx=5)
        Button(button_frame, text="Reject", command=self.reject_request,
              bg="#e74c3c", fg="white").pack(side=LEFT, padx=5)
        
        # Bind selection event
        self.pending_tree.bind("<<TreeviewSelect>>", self.show_request_details)
        
        # Load pending requests
        self.load_pending_requests()
    
    def setup_all_requests_tab(self, parent):
        Label(parent, text="All Permission Requests", 
             font=("Arial", 12, "bold")).pack(pady=10)
        
        # Treeview to show all requests
        self.all_requests_tree = ttk.Treeview(parent, 
                                            columns=("id", "student", "type", "subject", "status", "date"))
        
        self.all_requests_tree.heading("#0", text="")
        self.all_requests_tree.heading("id", text="Request ID")
        self.all_requests_tree.heading("student", text="Student")
        self.all_requests_tree.heading("type", text="Type")
        self.all_requests_tree.heading("subject", text="Subject")
        self.all_requests_tree.heading("status", text="Status")
        self.all_requests_tree.heading("date", text="Date")
        
        self.all_requests_tree.column("#0", width=0, stretch=NO)
        self.all_requests_tree.column("id", width=80)
        self.all_requests_tree.column("student", width=150)
        self.all_requests_tree.column("type", width=100)
        self.all_requests_tree.column("subject", width=200)
        self.all_requests_tree.column("status", width=100)
        self.all_requests_tree.column("date", width=120)
        
        scroll_y = Scrollbar(parent, orient=VERTICAL, command=self.all_requests_tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.all_requests_tree.configure(yscrollcommand=scroll_y.set)
        
        self.all_requests_tree.pack(fill=BOTH, expand=True)
        
        # Details Frame
        details_frame = Frame(parent, bd=2, relief=GROOVE, padx=10, pady=10)
        details_frame.pack(fill=X, padx=10, pady=10)
        
        self.all_details = scrolledtext.ScrolledText(details_frame, height=8, state=DISABLED)
        self.all_details.pack(fill=BOTH, expand=True)
        
        # Bind selection event
        self.all_requests_tree.bind("<<TreeviewSelect>>", self.show_all_request_details)
        
        # Load all requests
        self.load_all_requests()
    
    def load_pending_requests(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # First clear existing data
            for item in self.pending_tree.get_children():
                self.pending_tree.delete(item)
            
            # Fetch pending requests for this faculty
            query = """
                SELECT r.request_id, r.student_name, r.request_type, r.subject, r.created_at
                FROM permission_requests r
                WHERE r.faculty_id = %s AND r.status = 'pending'
                ORDER BY r.created_at DESC
            """
            cursor.execute(query, (self.faculty_id,))
            
            # Add new data
            for row in cursor.fetchall():
                self.pending_tree.insert("", "end", 
                                      values=(
                                          row['request_id'],
                                          row['student_name'],
                                          row['request_type'],
                                          row['subject'],
                                          row['created_at'].strftime("%Y-%m-%d %H:%M")
                                      ))
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading pending requests: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def load_all_requests(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # First clear existing data
            for item in self.all_requests_tree.get_children():
                self.all_requests_tree.delete(item)
            
            # Fetch all requests for this faculty
            query = """
                SELECT r.request_id, r.student_name, r.request_type, r.subject, 
                       r.status, r.created_at, r.decision_date
                FROM permission_requests r
                WHERE r.faculty_id = %s
                ORDER BY r.created_at DESC
            """
            cursor.execute(query, (self.faculty_id,))
            
            # Add new data
            for row in cursor.fetchall():
                self.all_requests_tree.insert("", "end", 
                                           values=(
                                               row['request_id'],
                                               row['student_name'],
                                               row['request_type'],
                                               row['subject'],
                                               row['status'],
                                               row['created_at'].strftime("%Y-%m-%d %H:%M")
                                           ))
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading all requests: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def show_request_details(self, event):
        selected_item = self.pending_tree.focus()
        if not selected_item:
            return
        
        request_id = self.pending_tree.item(selected_item)['values'][0]
        self.show_details(request_id, self.request_details)
    
    def show_all_request_details(self, event):
        selected_item = self.all_requests_tree.focus()
        if not selected_item:
            return
        
        request_id = self.all_requests_tree.item(selected_item)['values'][0]
        self.show_details(request_id, self.all_details)
    
    def show_details(self, request_id, text_widget):
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
Student: {request['student_name']}
Type: {request['request_type']}
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
            text_widget.config(state=NORMAL)
            text_widget.delete("1.0", END)
            text_widget.insert("1.0", details_text)
            text_widget.config(state=DISABLED)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading request details: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def approve_request(self):
        self.process_request("approved")
    
    def reject_request(self):
        self.process_request("rejected")
    
    def process_request(self, action):
        selected_item = self.pending_tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a request first")
            return
        
        request_id = self.pending_tree.item(selected_item)['values'][0]
        
        # Ask for remarks if rejecting
        remarks = ""
        if action == "rejected":
            remarks = simpledialog.askstring("Remarks", "Please enter reason for rejection:")
            if remarks is None:  # User cancelled
                return
        
        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE permission_requests 
                SET status = %s, 
                    faculty_remarks = %s,
                    decision_date = NOW()
                WHERE request_id = %s
            """
            cursor.execute(query, (action, remarks, request_id))
            self.conn.commit()
            
            messagebox.showinfo("Success", f"Request has been {action}!")
            self.status.config(text=f"Request {action} at {datetime.now().strftime('%H:%M:%S')}")
            
            # Refresh both tabs
            self.load_pending_requests()
            self.load_all_requests()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating request: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()

if __name__ == "__main__":
    import tkinter.simpledialog as simpledialog

    root = tk.Tk()
    root.withdraw()  # Hide the initial window

    faculty_id = simpledialog.askstring("Faculty Login", "Enter Faculty ID:")
    faculty_name = simpledialog.askstring("Faculty Login", "Enter Faculty Name:")

    if faculty_id and faculty_name:
        app = FacultyPortal(faculty_id, faculty_name)
        app.root.mainloop()
    else:
        messagebox.showwarning("Login Failed", "Faculty ID and Name are required.")