import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *
from datetime import datetime, date
import re
import sys
from calendar import monthrange

class AdvancedFacultyManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Faculty Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f7fa")
        self.root.state('zoomed')
        
        # Initialize attributes
        self.dept_codes = {
            "CST": "37", "CAI": "31", "CSN": "29", 
            "Mathematics": "45", "Physics": "22", 
            "Chemistry": "18", "Electronics": "33", 
            "Mechanical": "27", "Electrical": "41"
        }

        self.designation_salary = {
            "Professor": 120000,
            "Associate Professor": 90000,
            "Assistant Professor": 70000,
            "HOD": 100000,
            "Visiting Faculty": 60000
        }
        
        # Database connection
        try:
            temp_conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb"
            )
            cursor = temp_conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS college_management")
            cursor.close()
            temp_conn.close()
            
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="college_management"
            )
            
            self.create_tables()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
            sys.exit(1)
        
        self.setup_ui()
    
    def create_tables(self):
        cursor = self.conn.cursor()
    
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS faculty (
                    faculty_id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    department VARCHAR(50) NOT NULL,
                    designation VARCHAR(50),
                    qualification VARCHAR(100),
                    specialization VARCHAR(100),
                    date_of_joining DATE,
                    contact_number VARCHAR(15),
                    email VARCHAR(50) UNIQUE,
                    base_salary DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS faculty_cabins (
                    faculty_id VARCHAR(20) PRIMARY KEY,
                    block VARCHAR(30) NOT NULL,
                    floor INT NOT NULL,
                    room_number VARCHAR(10) NOT NULL,
                    cabin_number VARCHAR(10) NOT NULL,
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
                    UNIQUE(block, floor, room_number, cabin_number)
                )
            """)
        
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS faculty_salary_payments (
                    payment_id VARCHAR(20) PRIMARY KEY,
                    faculty_id VARCHAR(20),
                    month_year VARCHAR(10) NOT NULL,
                    base_amount DECIMAL(10,2) NOT NULL,
                    bonus DECIMAL(10,2) DEFAULT 0,
                    deductions DECIMAL(10,2) DEFAULT 0,
                    net_amount DECIMAL(10,2) NOT NULL,
                    payment_date DATE NOT NULL,
                    payment_method VARCHAR(50) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    remarks VARCHAR(200),
                    processed_by VARCHAR(50),
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
                )
            """)
        
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS salary_structures (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    designation VARCHAR(50) UNIQUE NOT NULL,
                    base_salary DECIMAL(10,2) NOT NULL,
                    hra_percent DECIMAL(5,2) DEFAULT 40,
                    da_percent DECIMAL(5,2) DEFAULT 30,
                    ta_percent DECIMAL(5,2) DEFAULT 10
                )
            """)
        
            cursor.execute("SELECT COUNT(*) FROM salary_structures")
            if cursor.fetchone()[0] == 0:
                for designation, salary in self.designation_salary.items():
                    cursor.execute("""
                        INSERT INTO salary_structures (designation, base_salary)
                        VALUES (%s, %s)
                    """, (designation, salary))
        
            self.conn.commit()
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error creating tables: {err}")
        finally:
            cursor.close()
    
    def load_faculty_list(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.faculty_id, f.name, f.designation, f.department 
                FROM faculty f 
                ORDER BY f.department, f.name
            """)
            
            faculty_list = []
            for row in cursor.fetchall():
                faculty_list.append(f"{row['faculty_id']} - {row['name']} ({row['department']})")
            
            if hasattr(self, 'faculty_combo'):
                self.faculty_combo['values'] = faculty_list
                if faculty_list:
                    self.faculty_combo.current(0)
            
            if hasattr(self, 'salary_faculty_combo'):
                self.salary_faculty_combo['values'] = faculty_list
                if faculty_list:
                    self.salary_faculty_combo.current(0)
            
            if hasattr(self, 'faculty_view_combo'):
                self.faculty_view_combo['values'] = faculty_list
                if faculty_list:
                    self.faculty_view_combo.current(0)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading faculty list: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def setup_ui(self):
        # Header Frame
        header_frame = Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=X)
        
        Label(header_frame, 
              text="Advanced Faculty Management System", 
              font=("Arial", 14, "bold"),
              bg="#2c3e50",
              fg="white").pack(pady=20)
        
        # Main Notebook (Tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Faculty Registration
        reg_frame = Frame(notebook, bg="#f5f7fa")
        notebook.add(reg_frame, text="Faculty Registration")
        self.setup_registration_tab(reg_frame)
        
        # Tab 2: Cabin Allocation
        cabin_frame = Frame(notebook, bg="#f5f7fa")
        notebook.add(cabin_frame, text="Cabin Allocation")
        self.setup_cabin_tab(cabin_frame)
        
        # Tab 3: Salary Management
        salary_frame = Frame(notebook, bg="#f5f7fa")
        notebook.add(salary_frame, text="Salary Management")
        self.setup_salary_tab(salary_frame)
        
        # Tab 4: Faculty View
        view_frame = Frame(notebook, bg="#f5f7fa")
        notebook.add(view_frame, text="Faculty Details")
        self.setup_faculty_view_tab(view_frame)
        
        # Status Bar
        self.status = Label(self.root, text="Ready", bd=1, relief=SUNKEN, anchor=W,
                          font=("Arial", 10), bg="#2c3e50", fg="white")
        self.status.pack(fill=X, side=BOTTOM)
    
    def setup_registration_tab(self, parent):
        form_frame = Frame(parent, bg="white", bd=2, relief=GROOVE, padx=15, pady=15)
        form_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(form_frame, text="Faculty Registration Form", font=("Arial", 14, "bold"), 
             bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=W)
        
        # Form Fields
        fields = [
            ("Department*", "department", ""),
            ("Full Name*", "name", ""),
            ("Designation*", "designation", ""),
            ("Qualification", "qualification", ""),
            ("Specialization", "specialization", ""),
            ("Date of Joining", "doj", "DD-MM-YYYY"),
            ("Contact Number", "contact", ""),
            ("Email*", "email", ""),
            ("Faculty ID", "faculty_id", "Will be generated automatically")
        ]
        
        self.reg_vars = {}
        for i, (label_text, field_name, placeholder) in enumerate(fields):
            Label(form_frame, text=label_text, font=("Arial", 11), 
                 bg="white").grid(row=i+1, column=0, sticky=W, pady=5, padx=10)
            
            self.reg_vars[field_name] = StringVar()
            
            if field_name == "department":
                dept_combo = ttk.Combobox(form_frame, textvariable=self.reg_vars[field_name], 
                                         values=list(self.dept_codes.keys()), state="readonly")
                dept_combo.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
                dept_combo.bind("<<ComboboxSelected>>", self.generate_faculty_id)
            elif field_name == "designation":
                desig_combo = ttk.Combobox(form_frame, textvariable=self.reg_vars[field_name], 
                                          values=list(self.designation_salary.keys()), state="readonly")
                desig_combo.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
            elif field_name == "faculty_id":
                entry = Entry(form_frame, textvariable=self.reg_vars[field_name], 
                            font=("Arial", 11), state="readonly")
                entry.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
            else:
                entry = Entry(form_frame, textvariable=self.reg_vars[field_name], 
                            font=("Arial", 11))
                entry.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
                
                if placeholder:
                    entry.insert(0, placeholder)
                    entry.config(fg="grey")
                    entry.bind("<FocusIn>", lambda e, entry=entry: self.clear_placeholder(e, entry))
                    entry.bind("<FocusOut>", lambda e, entry=entry, ph=placeholder: 
                              self.add_placeholder(e, entry, ph))
        
        # Button Frame
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=15)
        
        Button(btn_frame, text="Register Faculty", command=self.register_faculty,
              font=("Arial", 12, "bold"), bg="#27ae60", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="Clear Form", command=self.clear_reg_form,
              font=("Arial", 12), bg="#e74c3c", fg="white", width=15).pack(side=LEFT, padx=10)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def generate_faculty_id(self, event=None):
        dept = self.reg_vars["department"].get()
        if not dept:
            return
        
        dept_code = self.dept_codes.get(dept, "00")
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT MAX(CAST(SUBSTRING(faculty_id, 4) AS UNSIGNED)) 
                FROM faculty 
                WHERE faculty_id LIKE %s
            """, (f"{dept_code}-%",))
            
            max_num = cursor.fetchone()[0] or 0
            new_id = f"{dept_code}-{max_num + 1:03d}"
            
            self.reg_vars["faculty_id"].set(new_id)
            self.status.config(text=f"Generated Faculty ID: {new_id}")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error generating ID: {err}")
        finally:
            cursor.close()
    
    def clear_placeholder(self, event, entry):
        if entry.get() in ["DD-MM-YYYY", "Will be generated automatically"]:
            entry.delete(0, END)
            entry.config(fg="black")
    
    def add_placeholder(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey")
    
    def clear_reg_form(self):
        for var in self.reg_vars.values():
            var.set("")
        
        if hasattr(self, 'dept_codes'):
            self.reg_vars["department"].set(list(self.dept_codes.keys())[0])
        if hasattr(self, 'designation_salary'):
            self.reg_vars["designation"].set(list(self.designation_salary.keys())[0])
    
    def register_faculty(self):
        required_fields = ["department", "name", "email", "designation"]
        for field in required_fields:
            if not self.reg_vars[field].get():
                messagebox.showwarning("Validation Error", f"{field.capitalize()} is required")
                return
        
        email = self.reg_vars["email"].get()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Validation Error", "Please enter a valid email address")
            return
        
        faculty_id = self.reg_vars["faculty_id"].get()
        if not faculty_id or faculty_id == "Will be generated automatically":
            messagebox.showwarning("Validation Error", "Please generate a faculty ID first")
            return
        
        try:
            cursor = self.conn.cursor()
            
            designation = self.reg_vars["designation"].get()
            base_salary = self.designation_salary.get(designation, 0)
            
            query = """
                INSERT INTO faculty (
                    faculty_id, name, department, designation, 
                    qualification, specialization, date_of_joining, 
                    contact_number, email, base_salary
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            doj = self.reg_vars["doj"].get()
            if doj == "DD-MM-YYYY":
                doj = None
            else:
                try:
                    doj = datetime.strptime(doj, "%d-%m-%Y").strftime("%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Validation Error", "Date must be in DD-MM-YYYY format")
                    return
            
            cursor.execute(query, (
                faculty_id,
                self.reg_vars["name"].get(),
                self.reg_vars["department"].get(),
                designation,
                self.reg_vars["qualification"].get(),
                self.reg_vars["specialization"].get(),
                doj,
                self.reg_vars["contact"].get(),
                email,
                base_salary
            ))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", f"Faculty {self.reg_vars['name'].get()} registered successfully!")
            self.clear_reg_form()
            self.status.config(text=f"Last registered: {faculty_id} at {datetime.now().strftime('%H:%M:%S')}")
            
            self.load_faculty_list()
            
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Error", "This faculty ID or email already exists")
            else:
                messagebox.showerror("Database Error", f"Error: {e}")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def setup_cabin_tab(self, parent):
        form_frame = Frame(parent, bg="white", bd=2, relief=GROOVE, padx=15, pady=15)
        form_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(form_frame, text="Faculty Cabin Allocation", font=("Arial", 14, "bold"), 
             bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=W)
        
        # Faculty Selection
        Label(form_frame, text="Select Faculty:", font=("Arial", 11), 
             bg="white").grid(row=1, column=0, sticky=W, pady=5, padx=10)
        
        self.faculty_combo = ttk.Combobox(form_frame, font=("Arial", 11), state="readonly")
        self.faculty_combo.grid(row=1, column=1, sticky=EW, pady=5, padx=10)
        self.load_faculty_list()
        
        # Cabin Details
        cabin_fields = [
            ("Block:", "block"),
            ("Floor:", "floor"),
            ("Room Number:", "room_number"),
            ("Cabin Number:", "cabin_no")
        ]
        
        self.cabin_vars = {}
        for i, (label_text, field_name) in enumerate(cabin_fields):
            Label(form_frame, text=label_text, font=("Arial", 11), 
                 bg="white").grid(row=i+2, column=0, sticky=W, pady=5, padx=10)
            
            self.cabin_vars[field_name] = StringVar()
            
            if field_name == "block":
                block_combo = ttk.Combobox(form_frame, textvariable=self.cabin_vars[field_name], 
                                          values=["Main Block", "Science Block", "Admin Block", "Library"], 
                                          state="readonly")
                block_combo.grid(row=i+2, column=1, sticky=EW, pady=5, padx=10)
            else:
                entry = Entry(form_frame, textvariable=self.cabin_vars[field_name], 
                            font=("Arial", 11))
                entry.grid(row=i+2, column=1, sticky=EW, pady=5, padx=10)
        
        # Button Frame
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=len(cabin_fields)+3, column=0, columnspan=2, pady=15)
        
        Button(btn_frame, text="Allocate Cabin", command=self.allocate_cabin,
              font=("Arial", 12, "bold"), bg="#3498db", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="View All Allocations", command=self.view_all_allocations,
              font=("Arial", 12), bg="#9b59b6", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="View by Department", command=self.view_dept_allocations,
              font=("Arial", 12), bg="#e67e22", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="View by Block", command=self.view_block_allocations,
              font=("Arial", 12), bg="#2ecc71", fg="white", width=15).pack(side=LEFT, padx=10)
        
        form_frame.grid_columnconfigure(1, weight=1)

    def allocate_cabin(self):
        faculty = self.faculty_combo.get()
        if not faculty:
            messagebox.showwarning("Validation Error", "Please select a faculty member")
            return
        
        faculty_id = faculty.split(" - ")[0]
        
        required_fields = ["block", "floor", "room_number", "cabin_no"]
        for field in required_fields:
            if not self.cabin_vars[field].get():
                messagebox.showwarning("Validation Error", f"{field.replace('_', ' ').capitalize()} is required")
                return
        
        try:
            floor = int(self.cabin_vars["floor"].get())
            if floor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error", "Floor must be a positive integer")
            return
        
        try:
            cursor = self.conn.cursor()
            
            query = """
                INSERT INTO faculty_cabins (faculty_id, block, floor, room_number, cabin_number)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                block = VALUES(block),
                floor = VALUES(floor),
                room_number = VALUES(room_number),
                cabin_number = VALUES(cabin_number)
            """
            
            cursor.execute(query, (
                faculty_id,
                self.cabin_vars["block"].get(),
                floor,
                self.cabin_vars["room_number"].get(),
                self.cabin_vars["cabin_no"].get()
            ))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", "Cabin allocated successfully!")
            self.status.config(text=f"Cabin allocated to {faculty_id} at {datetime.now().strftime('%H:%M:%S')}")
            
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Error", "This cabin is already allocated to another faculty member")
            else:
                messagebox.showerror("Database Error", f"Error: {e}")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def view_all_allocations(self):
        view_window = Toplevel(self.root)
        view_window.title("Faculty Cabin Allocations")
        view_window.geometry("900x500")
    
        tree_frame = Frame(view_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
        tree = ttk.Treeview(tree_frame, 
                      columns=("faculty_id", "name", "dept", "block", "floor", "room", "cabin"),
                      show="headings")
    
        tree.heading("faculty_id", text="Faculty ID")
        tree.heading("name", text="Name")
        tree.heading("dept", text="Department")
        tree.heading("block", text="Block")
        tree.heading("floor", text="Floor")
        tree.heading("room", text="Room No.")
        tree.heading("cabin", text="Cabin No.")
    
        tree.column("faculty_id", width=100, anchor=CENTER)
        tree.column("name", width=150, anchor=W)
        tree.column("dept", width=120, anchor=W)
        tree.column("block", width=100, anchor=W)
        tree.column("floor", width=60, anchor=CENTER)
        tree.column("room", width=80, anchor=CENTER)
        tree.column("cabin", width=80, anchor=CENTER)
    
        scroll_y = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x = Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        scroll_x.pack(side=BOTTOM, fill=X)
        tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    
        tree.pack(fill=BOTH, expand=True)
    
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.faculty_id, f.name, f.department, c.block, c.floor, c.room_number, c.cabin_number
                FROM faculty f
                JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                ORDER BY c.block, c.floor, c.room_number, c.cabin_number
            """)
        
            for row in cursor.fetchall():
                tree.insert("", "end", 
                           values=(
                               row['faculty_id'],
                                row['name'],
                                row['department'],
                                row['block'],
                                row['floor'],
                                row['room_number'],
                                row['cabin_number']
                        ))
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading allocations: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def view_dept_allocations(self):
        dept_window = Toplevel(self.root)
        dept_window.title("Cabin Allocations by Department")
        dept_window.geometry("600x400")
        
        dept_frame = Frame(dept_window, padx=10, pady=10)
        dept_frame.pack(fill=X)
        
        Label(dept_frame, text="Select Department:").pack(side=LEFT)
        
        dept_var = StringVar()
        dept_combo = ttk.Combobox(dept_frame, textvariable=dept_var, 
                                 values=list(self.dept_codes.keys()), state="readonly")
        dept_combo.pack(side=LEFT, padx=10)
        dept_combo.current(0)
        
        Button(dept_frame, text="View", 
              command=lambda: self.show_dept_allocations(dept_var.get())).pack(side=LEFT)
        
        tree_frame = Frame(dept_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        self.dept_tree = ttk.Treeview(tree_frame, 
                          columns=("faculty_id", "name", "block", "floor", "cabin"),
                          yscrollcommand=scroll_y.set)
        
        self.dept_tree.heading("#0", text="ID")
        self.dept_tree.heading("faculty_id", text="Faculty ID")
        self.dept_tree.heading("name", text="Name")
        self.dept_tree.heading("block", text="Block")
        self.dept_tree.heading("floor", text="Floor")
        self.dept_tree.heading("cabin", text="Cabin No.")
        
        self.dept_tree.column("#0", width=0, stretch=NO)
        self.dept_tree.column("faculty_id", width=100, anchor=CENTER)
        self.dept_tree.column("name", width=150, anchor=W)
        self.dept_tree.column("block", width=100, anchor=W)
        self.dept_tree.column("floor", width=60, anchor=CENTER)
        self.dept_tree.column("cabin", width=80, anchor=CENTER)
        
        scroll_y.config(command=self.dept_tree.yview)
        
        self.dept_tree.pack(fill=BOTH, expand=True)
    
    def show_dept_allocations(self, department):
        if not hasattr(self, 'dept_tree'):
            return
            
        for item in self.dept_tree.get_children():
            self.dept_tree.delete(item)
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.faculty_id, f.name, c.block, c.floor, c.cabin_number
                FROM faculty f
                JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                WHERE f.department = %s
                ORDER BY c.block, c.floor, c.cabin_number
            """, (department,))
            
            for row in cursor.fetchall():
                self.dept_tree.insert("", "end", 
                           values=(
                               row['faculty_id'],
                               row['name'],
                               row['block'],
                               row['floor'],
                               row['cabin_number']
                           ))
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading allocations: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def view_block_allocations(self):
        if not hasattr(self, 'block_window') or not self.block_window.winfo_exists():
            self.block_window = Toplevel(self.root)
            self.block_window.title("Cabin Allocations by Block")
            self.block_window.geometry("1000x500")
            
            block_frame = Frame(self.block_window, padx=10, pady=10)
            block_frame.pack(fill=X)
            
            Label(block_frame, text="Select Block:").pack(side=LEFT)
            
            self.block_var = StringVar()
            self.block_combo = ttk.Combobox(block_frame, textvariable=self.block_var, 
                                      values=["Main Block", "Science Block", "Admin Block", "Library"], 
                                      state="readonly")
            self.block_combo.pack(side=LEFT, padx=10)
            self.block_combo.current(0)
            
            Button(block_frame, text="View", 
                  command=lambda: self.show_block_allocations(self.block_var.get())).pack(side=LEFT)
            
            tree_frame = Frame(self.block_window)
            tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            scroll_y = Scrollbar(tree_frame)
            scroll_y.pack(side=RIGHT, fill=Y)
            
            self.block_tree = ttk.Treeview(tree_frame, 
                                  columns=("faculty_id", "name", "dept", "floor", "room", "cabin"),
                                  show="headings",
                                  yscrollcommand=scroll_y.set)

            self.block_tree.heading("faculty_id", text="Faculty ID")
            self.block_tree.heading("name", text="Name")
            self.block_tree.heading("dept", text="Department")
            self.block_tree.heading("floor", text="Floor")
            self.block_tree.heading("room", text="Room No.")
            self.block_tree.heading("cabin", text="Cabin No.")
            
            self.block_tree.column("faculty_id", width=100, anchor=CENTER)
            self.block_tree.column("name", width=130, anchor=W)
            self.block_tree.column("dept", width=100, anchor=W)
            self.block_tree.column("floor", width=60, anchor=CENTER)
            self.block_tree.column("room", width=60, anchor=CENTER)
            self.block_tree.column("cabin", width=60, anchor=CENTER)
            
            scroll_y.config(command=self.block_tree.yview)
            
            self.block_tree.pack(fill=BOTH, expand=True)
        
        self.block_window.lift()
    
    def show_block_allocations(self, block):
        if not hasattr(self, 'block_tree'):
            return
        
        for item in self.block_tree.get_children():
            self.block_tree.delete(item)

        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.faculty_id, f.name, f.department, c.floor, c.room_number, c.cabin_number
                FROM faculty f
                JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                WHERE c.block = %s
                ORDER BY c.floor, c.room_number, c.cabin_number
            """, (block,))
        
            for row in cursor.fetchall():
                self.block_tree.insert("", "end", 
                           values=(
                                row['faculty_id'],
                                row['name'],
                                row['department'],
                                row['floor'],
                                row['room_number'],
                                row['cabin_number']
                            ))
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading allocations: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def setup_salary_tab(self, parent):
        form_frame = Frame(parent, bg="white", bd=2, relief=GROOVE, padx=15, pady=15)
        form_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(form_frame, text="Faculty Salary Management", font=("Arial", 14, "bold"), 
             bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=W)
        
        salary_fields = [
            ("Faculty ID:", "salary_faculty_id"),
            ("Month-Year:", "salary_month"),
            ("Base Amount (₹):", "salary_base_amount"),
            ("Bonus (₹):", "salary_bonus"),
            ("Deductions (₹):", "salary_deductions"),
            ("Net Amount (₹):", "salary_net_amount"),
            ("Payment Date:", "salary_date"),
            ("Payment Method:", "salary_method"),
            ("Status:", "salary_status"),
            ("Remarks:", "salary_remarks")
        ]
        
        self.salary_vars = {}
        for i, (label_text, field_name) in enumerate(salary_fields):
            Label(form_frame, text=label_text, font=("Arial", 11), 
                 bg="white").grid(row=i+1, column=0, sticky=W, pady=5, padx=10)
            
            self.salary_vars[field_name] = StringVar()
            
            if field_name == "salary_faculty_id":
                self.salary_faculty_combo = ttk.Combobox(form_frame, textvariable=self.salary_vars[field_name], 
                                            font=("Arial", 11))
                self.salary_faculty_combo.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
                self.salary_faculty_combo.bind("<<ComboboxSelected>>", self.load_faculty_salary_details)
                self.load_faculty_list()
            elif field_name == "salary_month":
                month_combo = ttk.Combobox(form_frame, textvariable=self.salary_vars[field_name], 
                                          values=self.generate_month_year_list(), state="readonly")
                month_combo.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
                month_combo.current(0)
            elif field_name == "salary_method":
                method_combo = ttk.Combobox(form_frame, textvariable=self.salary_vars[field_name], 
                                           values=["Cash", "Cheque", "Online Transfer", "DD"], 
                                           state="readonly")
                method_combo.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
                method_combo.current(0)
            elif field_name == "salary_status":
                status_combo = ttk.Combobox(form_frame, textvariable=self.salary_vars[field_name], 
                                          values=["Paid", "Pending", "Cancelled"], state="readonly")
                status_combo.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
                status_combo.current(0)
            elif field_name in ["salary_base_amount", "salary_bonus", "salary_deductions", "salary_net_amount"]:
                entry = Entry(form_frame, textvariable=self.salary_vars[field_name], 
                            font=("Arial", 11), state="readonly" if field_name == "salary_net_amount" else "normal")
                entry.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
                if field_name in ["salary_bonus", "salary_deductions"]:
                    entry.bind("<KeyRelease>", self.calculate_net_amount)
            else:
                entry = Entry(form_frame, textvariable=self.salary_vars[field_name], 
                            font=("Arial", 11))
                entry.grid(row=i+1, column=1, sticky=EW, pady=5, padx=10)
        
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=len(salary_fields)+1, column=0, columnspan=2, pady=15)
        
        Button(btn_frame, text="Process Payment", command=self.record_salary_payment,
              font=("Arial", 12, "bold"), bg="#3498db", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="View All Payments", command=self.view_all_payments,
              font=("Arial", 12), bg="#9b59b6", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="View by Faculty", command=self.view_faculty_payments,
              font=("Arial", 12), bg="#e67e22", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="Department Report", command=self.generate_dept_salary_report,
              font=("Arial", 12), bg="#2ecc71", fg="white", width=15).pack(side=LEFT, padx=10)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def load_faculty_salary_details(self, event=None):
        faculty = self.salary_vars["salary_faculty_id"].get()
        if not faculty:
            return
    
        faculty_id = faculty.split(" - ")[0]
    
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.designation, f.base_salary, s.hra_percent, s.da_percent, s.ta_percent
                FROM faculty f
                LEFT JOIN salary_structures s ON f.designation = s.designation
                WHERE f.faculty_id = %s
            """, (faculty_id,))
        
            result = cursor.fetchone()
            if result:
                base_salary = float(result['base_salary']) if result['base_salary'] is not None else 0
                hra_percent = float(result['hra_percent'] or 40)
                da_percent = float(result['da_percent'] or 30)
                ta_percent = float(result['ta_percent'] or 10)
            
                hra = base_salary * (hra_percent / 100)
                da = base_salary * (da_percent / 100)
                ta = base_salary * (ta_percent / 100)
                total = base_salary + hra + da + ta
            
                self.salary_vars["salary_base_amount"].set(f"{total:.2f}")
                self.salary_vars["salary_bonus"].set("0.00")
                self.salary_vars["salary_deductions"].set("0.00")
                self.calculate_net_amount()
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading faculty details: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def calculate_net_amount(self, event=None):
        try:
            base_amount = float(self.salary_vars["salary_base_amount"].get() or 0)
            bonus = float(self.salary_vars["salary_bonus"].get() or 0)
            deductions = float(self.salary_vars["salary_deductions"].get() or 0)
            
            net_amount = base_amount + bonus - deductions
            self.salary_vars["salary_net_amount"].set(f"{net_amount:.2f}")
        except ValueError:
            pass
    
    def generate_month_year_list(self):
        current_date = datetime.now()
        months = []
        for i in range(12):
            year = current_date.year
            month = current_date.month - i
            if month < 1:
                month += 12
                year -= 1
            date = current_date.replace(year=year, month=month)
            months.append(date.strftime("%b-%Y"))
        return months
    
    def record_salary_payment(self):
        faculty = self.salary_vars["salary_faculty_id"].get()
        if not faculty:
            messagebox.showwarning("Validation Error", "Please select a faculty member")
            return
        
        faculty_id = faculty.split(" - ")[0]
        
        required_fields = ["salary_month", "salary_base_amount", "salary_method", "salary_status"]
        for field in required_fields:
            if not self.salary_vars[field].get():
                messagebox.showwarning("Validation Error", f"{field.split('_')[1].capitalize()} is required")
                return
        
        try:
            base_amount = float(self.salary_vars["salary_base_amount"].get())
            bonus = float(self.salary_vars["salary_bonus"].get() or 0)
            deductions = float(self.salary_vars["salary_deductions"].get() or 0)
            net_amount = float(self.salary_vars["salary_net_amount"].get())
            
            if net_amount <= 0:
                raise ValueError("Net amount must be positive")
        except ValueError as e:
            messagebox.showwarning("Validation Error", f"Invalid amount: {str(e)}")
            return
        
        try:
            cursor = self.conn.cursor()
            
            payment_id = f"SAL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            query = """
                INSERT INTO faculty_salary_payments (
                    payment_id, faculty_id, month_year, base_amount, 
                    bonus, deductions, net_amount, payment_date, 
                    payment_method, status, remarks, processed_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            pay_date = self.salary_vars["salary_date"].get()
            if not pay_date:
                pay_date = datetime.now().strftime("%Y-%m-%d")
            else:
                try:
                    pay_date = datetime.strptime(pay_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Validation Error", "Date must be in DD-MM-YYYY format")
                    return
            
            cursor.execute(query, (
                payment_id,
                faculty_id,
                self.salary_vars["salary_month"].get(),
                base_amount,
                bonus,
                deductions,
                net_amount,
                pay_date,
                self.salary_vars["salary_method"].get(),
                self.salary_vars["salary_status"].get(),
                self.salary_vars["salary_remarks"].get(),
                "Admin"
            ))
            
            self.conn.commit()
            
            messagebox.showinfo("Success", f"Salary payment recorded successfully!\nPayment ID: {payment_id}")
            self.status.config(text=f"Salary recorded for {faculty_id} at {datetime.now().strftime('%H:%M:%S')}")
            
            for var in self.salary_vars.values():
                var.set("")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def view_all_payments(self):
        view_window = Toplevel(self.root)
        view_window.title("All Salary Payments")
        view_window.geometry("1200x600")
        
        tree_frame = Frame(view_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        tree = ttk.Treeview(tree_frame, 
                          columns=("payment_id", "faculty_id", "name", "dept", "month", "base", "bonus", 
                                  "deductions", "net", "date", "method", "status"),
                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        tree.heading("#0", text="ID")
        tree.heading("payment_id", text="Payment ID")
        tree.heading("faculty_id", text="Faculty ID")
        tree.heading("name", text="Name")
        tree.heading("dept", text="Department")
        tree.heading("month", text="Month-Year")
        tree.heading("base", text="Base (₹)")
        tree.heading("bonus", text="Bonus (₹)")
        tree.heading("deductions", text="Deductions (₹)")
        tree.heading("net", text="Net (₹)")
        tree.heading("date", text="Payment Date")
        tree.heading("method", text="Method")
        tree.heading("status", text="Status")
        
        tree.column("#0", width=0, stretch=NO)
        tree.column("payment_id", width=120, anchor=CENTER)
        tree.column("faculty_id", width=100, anchor=CENTER)
        tree.column("name", width=150, anchor=W)
        tree.column("dept", width=120, anchor=W)
        tree.column("month", width=100, anchor=CENTER)
        tree.column("base", width=100, anchor=CENTER)
        tree.column("bonus", width=80, anchor=CENTER)
        tree.column("deductions", width=100, anchor=CENTER)
        tree.column("net", width=100, anchor=CENTER)
        tree.column("date", width=100, anchor=CENTER)
        tree.column("method", width=100, anchor=CENTER)
        tree.column("status", width=80, anchor=CENTER)
        
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        tree.pack(fill=BOTH, expand=True)
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.payment_id, p.faculty_id, f.name, f.department, p.month_year, 
                       p.base_amount, p.bonus, p.deductions, p.net_amount, 
                       p.payment_date, p.payment_method, p.status
                FROM faculty_salary_payments p
                JOIN faculty f ON p.faculty_id = f.faculty_id
                ORDER BY p.payment_date DESC
            """)
            
            for row in cursor.fetchall():
                tree.insert("", "end", 
                           values=(
                               row['payment_id'],
                               row['faculty_id'],
                               row['name'],
                               row['department'],
                               row['month_year'],
                               f"{row['base_amount']:,.2f}",
                               f"{row['bonus']:,.2f}",
                               f"{row['deductions']:,.2f}",
                               f"{row['net_amount']:,.2f}",
                               row['payment_date'].strftime("%d-%m-%Y") if row['payment_date'] else "",
                               row['payment_method'],
                               row['status']
                           ))
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading payments: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def view_faculty_payments(self):
        faculty_window = Toplevel(self.root)
        faculty_window.title("Salary Payments by Faculty")
        faculty_window.geometry("1000x500")
        
        faculty_frame = Frame(faculty_window, padx=10, pady=10)
        faculty_frame.pack(fill=X)
        
        Label(faculty_frame, text="Select Faculty:").pack(side=LEFT)
        
        faculty_var = StringVar()
        faculty_combo = ttk.Combobox(faculty_frame, textvariable=faculty_var, 
                                   font=("Arial", 11))
        faculty_combo.pack(side=LEFT, padx=10)
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT faculty_id, name FROM faculty ORDER BY name")
            faculty_list = [f"{row['faculty_id']} - {row['name']}" for row in cursor.fetchall()]
            faculty_combo['values'] = faculty_list
            if faculty_list:
                faculty_combo.current(0)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading faculty: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
        
        Button(faculty_frame, text="View", 
              command=lambda: self.show_faculty_payments(faculty_var.get())).pack(side=LEFT)
        
        tree_frame = Frame(faculty_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.faculty_payments_tree = ttk.Treeview(tree_frame, 
                          columns=("payment_id", "month", "base", "bonus", "deductions", "net", "date", "method", "status", "remarks"),
                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.faculty_payments_tree.heading("#0", text="ID")
        self.faculty_payments_tree.heading("payment_id", text="Payment ID")
        self.faculty_payments_tree.heading("month", text="Month-Year")
        self.faculty_payments_tree.heading("base", text="Base (₹)")
        self.faculty_payments_tree.heading("bonus", text="Bonus (₹)")
        self.faculty_payments_tree.heading("deductions", text="Deductions (₹)")
        self.faculty_payments_tree.heading("net", text="Net (₹)")
        self.faculty_payments_tree.heading("date", text="Payment Date")
        self.faculty_payments_tree.heading("method", text="Method")
        self.faculty_payments_tree.heading("status", text="Status")
        self.faculty_payments_tree.heading("remarks", text="Remarks")
        
        self.faculty_payments_tree.column("#0", width=0, stretch=NO)
        self.faculty_payments_tree.column("payment_id", width=120, anchor=CENTER)
        self.faculty_payments_tree.column("month", width=100, anchor=CENTER)
        self.faculty_payments_tree.column("base", width=100, anchor=CENTER)
        self.faculty_payments_tree.column("bonus", width=80, anchor=CENTER)
        self.faculty_payments_tree.column("deductions", width=100, anchor=CENTER)
        self.faculty_payments_tree.column("net", width=100, anchor=CENTER)
        self.faculty_payments_tree.column("date", width=100, anchor=CENTER)
        self.faculty_payments_tree.column("method", width=100, anchor=CENTER)
        self.faculty_payments_tree.column("status", width=80, anchor=CENTER)
        self.faculty_payments_tree.column("remarks", width=200, anchor=W)
        
        scroll_y.config(command=self.faculty_payments_tree.yview)
        scroll_x.config(command=self.faculty_payments_tree.xview)
        
        self.faculty_payments_tree.pack(fill=BOTH, expand=True)
    
    def show_faculty_payments(self, faculty):
        if not hasattr(self, 'faculty_payments_tree'):
            return
            
        if not faculty:
            messagebox.showwarning("Validation Error", "Please select a faculty member")
            return
            
        faculty_id = faculty.split(" - ")[0]
        
        for item in self.faculty_payments_tree.get_children():
            self.faculty_payments_tree.delete(item)
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.payment_id, p.month_year, 
                       p.base_amount, p.bonus, p.deductions, p.net_amount,
                       p.payment_date, p.payment_method, p.status, p.remarks
                FROM faculty_salary_payments p
                WHERE p.faculty_id = %s
                ORDER BY p.payment_date DESC
            """, (faculty_id,))
            
            for row in cursor.fetchall():
                self.faculty_payments_tree.insert("", "end", 
                           values=(
                               row['payment_id'],
                               row['month_year'],
                               f"{row['base_amount']:,.2f}",
                               f"{row['bonus']:,.2f}",
                               f"{row['deductions']:,.2f}",
                               f"{row['net_amount']:,.2f}",
                               row['payment_date'].strftime("%d-%m-%Y") if row['payment_date'] else "",
                               row['payment_method'],
                               row['status'],
                               row['remarks'] or ""
                           ))
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading payments: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def generate_dept_salary_report(self):
        report_window = Toplevel(self.root)
        report_window.title("Department Salary Report")
        report_window.geometry("1000x600")
        
        month_frame = Frame(report_window, padx=10, pady=10)
        month_frame.pack(fill=X)
        
        Label(month_frame, text="Select Month-Year:").pack(side=LEFT)
        
        month_var = StringVar()
        month_combo = ttk.Combobox(month_frame, textvariable=month_var, 
                                  values=self.generate_month_year_list(), state="readonly")
        month_combo.pack(side=LEFT, padx=10)
        month_combo.current(0)
        
        Button(month_frame, text="Generate Report", 
              command=lambda: self.show_dept_salary_report(month_var.get())).pack(side=LEFT)
        
        tree_frame = Frame(report_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.dept_report_tree = ttk.Treeview(tree_frame, 
                          columns=("dept", "faculty_count", "total_base", "total_bonus", 
                                  "total_deductions", "total_net"),
                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.dept_report_tree.heading("#0", text="ID")
        self.dept_report_tree.heading("dept", text="Department")
        self.dept_report_tree.heading("faculty_count", text="Faculty Count")
        self.dept_report_tree.heading("total_base", text="Total Base (₹)")
        self.dept_report_tree.heading("total_bonus", text="Total Bonus (₹)")
        self.dept_report_tree.heading("total_deductions", text="Total Deductions (₹)")
        self.dept_report_tree.heading("total_net", text="Total Net (₹)")
        
        self.dept_report_tree.column("#0", width=0, stretch=NO)
        self.dept_report_tree.column("dept", width=200, anchor=W)
        self.dept_report_tree.column("faculty_count", width=100, anchor=CENTER)
        self.dept_report_tree.column("total_base", width=150, anchor=CENTER)
        self.dept_report_tree.column("total_bonus", width=150, anchor=CENTER)
        self.dept_report_tree.column("total_deductions", width=150, anchor=CENTER)
        self.dept_report_tree.column("total_net", width=150, anchor=CENTER)
        
        scroll_y.config(command=self.dept_report_tree.yview)
        scroll_x.config(command=self.dept_report_tree.xview)
        
        self.dept_report_tree.pack(fill=BOTH, expand=True)
    
    def show_dept_salary_report(self, month_year):
        if not hasattr(self, 'dept_report_tree'):
            return
            
        for item in self.dept_report_tree.get_children():
            self.dept_report_tree.delete(item)
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    f.department AS dept,
                    COUNT(DISTINCT p.faculty_id) AS faculty_count,
                    SUM(p.base_amount) AS total_base,
                    SUM(p.bonus) AS total_bonus,
                    SUM(p.deductions) AS total_deductions,
                    SUM(p.net_amount) AS total_net
                FROM faculty_salary_payments p
                JOIN faculty f ON p.faculty_id = f.faculty_id
                WHERE p.month_year = %s
                GROUP BY f.department
                ORDER BY f.department
            """, (month_year,))
            
            grand_total = {
                'faculty_count': 0,
                'total_base': 0,
                'total_bonus': 0,
                'total_deductions': 0,
                'total_net': 0
            }
            
            for row in cursor.fetchall():
                self.dept_report_tree.insert("", "end", 
                           values=(
                               row['dept'],
                               row['faculty_count'],
                               f"{row['total_base']:,.2f}",
                               f"{row['total_bonus']:,.2f}",
                               f"{row['total_deductions']:,.2f}",
                               f"{row['total_net']:,.2f}"
                           ))
                
                grand_total['faculty_count'] += row['faculty_count']
                grand_total['total_base'] += row['total_base']
                grand_total['total_bonus'] += row['total_bonus']
                grand_total['total_deductions'] += row['total_deductions']
                grand_total['total_net'] += row['total_net']
            
            self.dept_report_tree.insert("", "end", 
                       values=(
                           "GRAND TOTAL",
                           grand_total['faculty_count'],
                           f"{grand_total['total_base']:,.2f}",
                           f"{grand_total['total_bonus']:,.2f}",
                           f"{grand_total['total_deductions']:,.2f}",
                           f"{grand_total['total_net']:,.2f}"
                       ))
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading report: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def setup_faculty_view_tab(self, parent):
        form_frame = Frame(parent, bg="white", bd=2, relief=GROOVE, padx=15, pady=15)
        form_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(form_frame, text="Faculty Details View", font=("Arial", 14, "bold"), 
             bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=W)
        
        Label(form_frame, text="Select Faculty:", font=("Arial", 11), 
             bg="white").grid(row=1, column=0, sticky=W, pady=5, padx=10)
        
        self.faculty_view_combo = ttk.Combobox(form_frame, font=("Arial", 11), state="readonly")
        self.faculty_view_combo.grid(row=1, column=1, sticky=EW, pady=5, padx=10)
        self.load_faculty_list()
        
        Button(form_frame, text="View Details", command=self.show_faculty_details,
              font=("Arial", 12), bg="#3498db", fg="white").grid(row=2, column=0, columnspan=2, pady=10)
        
        details_frame = Frame(form_frame, bg="white", bd=1, relief=GROOVE)
        details_frame.grid(row=3, column=0, columnspan=2, sticky=EW, pady=10)
        
        self.faculty_details = {
            "faculty_id": {"label": "Faculty ID:", "value": StringVar()},
            "name": {"label": "Name:", "value": StringVar()},
            "department": {"label": "Department:", "value": StringVar()},
            "designation": {"label": "Designation:", "value": StringVar()},
            "qualification": {"label": "Qualification:", "value": StringVar()},
            "specialization": {"label": "Specialization:", "value": StringVar()},
            "doj": {"label": "Date of Joining:", "value": StringVar()},
            "contact": {"label": "Contact:", "value": StringVar()},
            "email": {"label": "Email:", "value": StringVar()},
            "base_salary": {"label": "Base Salary:", "value": StringVar()},
            "cabin": {"label": "Cabin:", "value": StringVar()}
        }
        
        for i, (field, data) in enumerate(self.faculty_details.items()):
            Label(details_frame, text=data["label"], font=("Arial", 11, "bold"), 
                 bg="white").grid(row=i, column=0, sticky=W, padx=5, pady=2)
            Label(details_frame, textvariable=data["value"], font=("Arial", 11), 
                 bg="white").grid(row=i, column=1, sticky=W, padx=5, pady=2)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def show_faculty_details(self):
        faculty = self.faculty_view_combo.get()
        if not faculty:
            messagebox.showwarning("Validation Error", "Please select a faculty member")
            return
    
        faculty_id = faculty.split(" - ")[0]
    
        try:
            cursor = self.conn.cursor(dictionary=True)
        
            cursor.execute("""
                SELECT f.*, 
                       CONCAT(c.block, ', Floor ', c.floor, ', Room ', c.room_number, ', Cabin ', c.cabin_number) AS cabin_details
                FROM faculty f
                LEFT JOIN faculty_cabins c ON f.faculty_id = c.faculty_id
                WHERE f.faculty_id = %s
            """, (faculty_id,))
        
            faculty_data = cursor.fetchone()
        
            if faculty_data:
                base_salary = faculty_data.get('base_salary')
                salary_display = f"₹{base_salary:,.2f}" if base_salary is not None else "N/A"
            
                self.faculty_details["faculty_id"]["value"].set(faculty_data['faculty_id'])
                self.faculty_details["name"]["value"].set(faculty_data['name'])
                self.faculty_details["department"]["value"].set(faculty_data['department'])
                self.faculty_details["designation"]["value"].set(faculty_data['designation'])
                self.faculty_details["qualification"]["value"].set(faculty_data['qualification'] or "N/A")
                self.faculty_details["specialization"]["value"].set(faculty_data['specialization'] or "N/A")
                self.faculty_details["doj"]["value"].set(faculty_data['date_of_joining'].strftime("%d-%m-%Y") if faculty_data['date_of_joining'] else "N/A")
                self.faculty_details["contact"]["value"].set(faculty_data['contact_number'] or "N/A")
                self.faculty_details["email"]["value"].set(faculty_data['email'])
                self.faculty_details["base_salary"]["value"].set(salary_display)
                self.faculty_details["cabin"]["value"].set(faculty_data['cabin_details'] or "Not allocated")
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading faculty details: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedFacultyManagement(root)
    root.mainloop()