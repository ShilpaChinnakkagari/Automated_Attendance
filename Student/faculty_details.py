import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *
from datetime import datetime
import re
import sys

class FacultyLocator:
    def __init__(self, root):
        self.root = root
        self.root.title("Faculty Locator System - Student Portal")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f5f7fa")
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
        
        # GUI Setup
        self.setup_ui()
    
    def setup_ui(self):
        # Header Frame
        header_frame = Frame(self.root, bg="#2c3e50", height=90)
        header_frame.pack(fill=X)
        
        Label(header_frame, 
              text="Faculty Office Locator", 
              font=("Arial", 18, "bold"),
              bg="#2c3e50",
              fg="white").pack(pady=20)
        
        # Search and Filter Frame
        control_frame = Frame(self.root, bg="#f5f7fa", padx=10, pady=10)
        control_frame.pack(fill=X)
        
        # Search Section
        search_frame = Frame(control_frame, bg="#f5f7fa")
        search_frame.pack(side=LEFT, padx=10)
        
        Label(search_frame, text="Search Faculty:", font=("Arial", 12), bg="#f5f7fa").pack(anchor=W)
        
        self.search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=30)
        search_entry.pack()
        search_entry.bind("<Return>", lambda e: self.search_faculty())
        
        Button(search_frame, text="Search", command=self.search_faculty,
              font=("Arial", 11), bg="#3498db", fg="white").pack(pady=5)
        
        # Filter Section
        filter_frame = Frame(control_frame, bg="#f5f7fa")
        filter_frame.pack(side=LEFT, padx=20)
        
        Label(filter_frame, text="Filter Options:", font=("Arial", 12), bg="#f5f7fa").pack(anchor=W)
        
        # Department Filter
        Label(filter_frame, text="By Department:", font=("Arial", 10), bg="#f5f7fa").pack(anchor=W)
        self.dept_var = StringVar()
        dept_combo = ttk.Combobox(filter_frame, textvariable=self.dept_var, 
                                 values=self.get_departments(), state="readonly", width=22)
        dept_combo.pack()
        dept_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_by_department())
        
        # Block Filter
        Label(filter_frame, text="By Building Block:", font=("Arial", 10), bg="#f5f7fa").pack(anchor=W, pady=(5,0))
        self.block_var = StringVar()
        block_combo = ttk.Combobox(filter_frame, textvariable=self.block_var, 
                                  values=self.get_blocks(), state="readonly", width=22)
        block_combo.pack()
        block_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_by_block())
        
        # Reset Button
        Button(control_frame, text="Reset Filters", command=self.reset_filters,
              font=("Arial", 11), bg="#e74c3c", fg="white").pack(side=RIGHT, padx=10)
        
        # Results Frame
        results_frame = Frame(self.root, bg="#f5f7fa", padx=10, pady=5)
        results_frame.pack(fill=BOTH, expand=True)
        
        # Treeview with scrollbars
        scroll_y = Scrollbar(results_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = Scrollbar(results_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tree = ttk.Treeview(results_frame, 
                               columns=("id", "name", "dept", "designation", "block", "floor", "room", "cabin"),
                               yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Configure columns
        self.tree.heading("#0", text="")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Faculty Name")
        self.tree.heading("dept", text="Department")
        self.tree.heading("designation", text="Designation")
        self.tree.heading("block", text="Building")
        self.tree.heading("floor", text="Floor")
        self.tree.heading("room", text="Room")
        self.tree.heading("cabin", text="Cabin")
        
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("id", width=80, anchor=CENTER)
        self.tree.column("name", width=150, anchor=W)
        self.tree.column("dept", width=120, anchor=W)
        self.tree.column("designation", width=120, anchor=W)
        self.tree.column("block", width=100, anchor=W)
        self.tree.column("floor", width=60, anchor=CENTER)
        self.tree.column("room", width=60, anchor=CENTER)
        self.tree.column("cabin", width=60, anchor=CENTER)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.pack(fill=BOTH, expand=True)
        
        # Details Frame
        details_frame = Frame(self.root, bg="white", bd=2, relief=GROOVE, padx=15, pady=15)
        details_frame.pack(fill=X, padx=10, pady=5)
        
        # Faculty details with emphasis on location
        Label(details_frame, text="Faculty Office Details", 
             font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=5, sticky=W)
        
        # Location info in a separate frame for emphasis
        loc_frame = Frame(details_frame, bg="#eaf2f8", bd=1, relief=SOLID, padx=10, pady=10)
        loc_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        Label(loc_frame, text="Office Location:", font=("Arial", 11, "bold"), bg="#eaf2f8").pack(anchor=W)
        
        self.loc_label = Label(loc_frame, text="Select a faculty member to view location", 
                             font=("Arial", 11), bg="#eaf2f8", justify=LEFT)
        self.loc_label.pack(anchor=W, fill=X)
        
        # Other details
        details_fields = [
            ("Faculty ID:", "id"),
            ("Name:", "name"),
            ("Department:", "dept"),
            ("Designation:", "designation"),
            ("Contact:", "contact"),
            ("Availability:", "availability")
        ]
        
        self.details_labels = {}
        for i, (label_text, field_name) in enumerate(details_fields):
            row = i + 2  # Start from row 2 after the title and location frame
            
            Label(details_frame, text=label_text, font=("Arial", 11), 
                 bg="white", anchor=E).grid(row=row, column=0, sticky=E, pady=2)
            
            self.details_labels[field_name] = Label(details_frame, text="", font=("Arial", 11), 
                                                  bg="white", anchor=W)
            self.details_labels[field_name].grid(row=row, column=1, sticky=W, pady=2, padx=5)
        
        # Bind tree selection event
        self.tree.bind("<<TreeviewSelect>>", self.show_faculty_details)
        
        # Load all faculty initially
        self.load_faculty_with_cabins()
    
    def get_departments(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT department FROM faculty ORDER BY department")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading departments: {err}")
            return []
        finally:
            cursor.close()
    
    def get_blocks(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT block FROM faculty_cabins ORDER BY block")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading blocks: {err}")
            return []
        finally:
            cursor.close()
    
    def load_faculty_with_cabins(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT f.faculty_id, f.name, f.department, f.designation, f.contact_number,
                       c.block, c.floor, c.room_number, c.cabin_number
                FROM faculty f
                LEFT JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                ORDER BY f.name
            """
            cursor.execute(query)
            self.display_results(cursor)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading faculty: {err}")
        finally:
            cursor.close()
    
    def search_faculty(self):
        search_term = self.search_var.get().strip()
        if not search_term:
            self.load_faculty_with_cabins()
            return
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT f.faculty_id, f.name, f.department, f.designation, f.contact_number,
                       c.block, c.floor, c.room_number, c.cabin_number
                FROM faculty f
                LEFT JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                WHERE f.faculty_id LIKE %s OR f.name LIKE %s OR f.department LIKE %s
                ORDER BY f.name
            """
            search_param = f"%{search_term}%"
            cursor.execute(query, (search_param, search_param, search_param))
            self.display_results(cursor)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error searching faculty: {err}")
        finally:
            cursor.close()
    
    def filter_by_department(self):
        department = self.dept_var.get()
        if not department:
            self.load_faculty_with_cabins()
            return
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT f.faculty_id, f.name, f.department, f.designation, f.contact_number,
                       c.block, c.floor, c.room_number, c.cabin_number
                FROM faculty f
                LEFT JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                WHERE f.department = %s
                ORDER BY f.name
            """
            cursor.execute(query, (department,))
            self.display_results(cursor)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error filtering by department: {err}")
        finally:
            cursor.close()
    
    def filter_by_block(self):
        block = self.block_var.get()
        if not block:
            self.load_faculty_with_cabins()
            return
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT f.faculty_id, f.name, f.department, f.designation, f.contact_number,
                       c.block, c.floor, c.room_number, c.cabin_number
                FROM faculty f
                JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                WHERE c.block = %s
                ORDER BY c.floor, c.room_number, c.cabin_number
            """
            cursor.execute(query, (block,))
            self.display_results(cursor)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error filtering by block: {err}")
        finally:
            cursor.close()
    
    def reset_filters(self):
        self.search_var.set("")
        self.dept_var.set("")
        self.block_var.set("")
        self.load_faculty_with_cabins()
    
    def display_results(self, cursor):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new data
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row['faculty_id'],
                row['name'],
                row['department'],
                row['designation'],
                row.get('block', ''),
                row.get('floor', ''),
                row.get('room_number', ''),
                row.get('cabin_number', '')
            ))
    
    def show_faculty_details(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        
        faculty_id = self.tree.item(selected_item)['values'][0]
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # Get faculty info
            cursor.execute("""
                SELECT faculty_id, name, department, designation, contact_number
                FROM faculty
                WHERE faculty_id = %s
            """, (faculty_id,))
            faculty_info = cursor.fetchone()
            
            # Get cabin info
            cursor.execute("""
                SELECT block, floor, room_number, cabin_number
                FROM faculty_cabins
                WHERE faculty_id = %s
            """, (faculty_id,))
            cabin_info = cursor.fetchone()
            
            # Update details labels
            self.details_labels['id'].config(text=faculty_info['faculty_id'])
            self.details_labels['name'].config(text=faculty_info['name'])
            self.details_labels['dept'].config(text=faculty_info['department'])
            self.details_labels['designation'].config(text=faculty_info['designation'])
            self.details_labels['contact'].config(text=faculty_info['contact_number'] or "Not available")
            
            # Special handling for availability (example)
            self.details_labels['availability'].config(text="Available 10AM-4PM (Mon-Fri)")  # This could be from DB
            
            # Update location info with emphasis
            if cabin_info:
                location_text = f"""
Building: {cabin_info['block']}
Floor: {cabin_info['floor']}
Room: {cabin_info['room_number']}
Cabin: {cabin_info['cabin_number']}

Directions: Take elevator to floor {cabin_info['floor']}, turn left from elevator, 
third door on the right.
                """
                self.loc_label.config(text=location_text)
            else:
                self.loc_label.config(text="Office location not assigned", fg="red")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading faculty details: {err}")
        finally:
            cursor.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FacultyLocator(root)
    root.mainloop()