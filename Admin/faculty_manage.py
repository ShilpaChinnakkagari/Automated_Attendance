import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *

class FacultyCabinManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Faculty Cabin Management System")
        self.root.geometry("1400x800")  # Increased size for additional fields
        self.root.configure(bg="#f5f5f5")
        self.root.state('zoomed')
        
        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vnsvb",
            database="face_recognition"
        )
        
        # Create tables if not exists
        self.create_tables()
        
        # GUI Setup
        self.setup_ui()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Main faculty cabin table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faculty_cabins (
                faculty_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                department VARCHAR(50) NOT NULL,
                block VARCHAR(30) NOT NULL,
                floor INT NOT NULL,
                room_number VARCHAR(10) NOT NULL,
                cabin_number VARCHAR(10) NOT NULL,
                FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
                UNIQUE(block, floor, room_number, cabin_number)
            )
        """)
        
        # Faculty directory table (for contact info and availability)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faculty_directory (
                faculty_id VARCHAR(20) PRIMARY KEY,
                contact_email VARCHAR(50),
                available_hours VARCHAR(100),
                FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
            )
        """)
        
        # Block information table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campus_blocks (
                block_name VARCHAR(30) PRIMARY KEY,
                floors INT NOT NULL,
                rooms_per_floor INT NOT NULL
            )
        """)
        
        # Insert default block data if empty
        cursor.execute("SELECT COUNT(*) FROM campus_blocks")
        if cursor.fetchone()[0] == 0:
            blocks = [
                ('South Block', 5, 22),
                ('West Block', 4, 22),
                ('East Block', 3, 22),
                ('Administrative Block', 6, 22),
                ('Circular Block', 2, 22),
                ('Library', 3, 22),
                ('NPN Block', 4, 22),
                ('KK Block', 3, 22)
            ]
            cursor.executemany("INSERT INTO campus_blocks VALUES (%s, %s, %s)", blocks)
        
        self.conn.commit()
        cursor.close()
    
    def setup_ui(self):
        # Header Frame
        header_frame = Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=X)
        
        Label(header_frame, 
              text="Faculty Cabin Allocation System", 
              font=("Arial", 20, "bold"), 
              bg="#2c3e50", fg="white").pack(pady=20)
        
        # Main Content Frame
        content_frame = Frame(self.root, bg="#f5f5f5", padx=20, pady=20)
        content_frame.pack(fill=BOTH, expand=True)
        
        # Left Frame - Add/Edit Faculty Cabin
        left_frame = Frame(content_frame, bg="#ecf0f1", bd=2, relief=GROOVE, padx=15, pady=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Right Frame - View Allocations
        right_frame = Frame(content_frame, bg="#ecf0f1", bd=2, relief=GROOVE, padx=15, pady=15)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left Frame Content - Add/Edit Form
        Label(left_frame, text="Faculty Cabin Allocation", font=("Arial", 14, "bold"), 
             bg="#ecf0f1").grid(row=0, column=0, columnspan=2, pady=10)
        
        # Form Fields - Cabin Allocation
        cabin_fields = [
            ("Faculty ID:", "faculty_id"),
            ("Name:", "name"),
            ("Department:", "department"),
            ("Block:", "block"),
            ("Floor:", "floor"),
            ("Room Number:", "room_number"),
            ("Cabin Number:", "cabin_number")
        ]
        
        self.entry_vars = {}
        for i, (label_text, field_name) in enumerate(cabin_fields):
            Label(left_frame, text=label_text, font=("Arial", 12), 
                 bg="#ecf0f1").grid(row=i+1, column=0, sticky=W, pady=5)
            
            if field_name == "faculty_id":
                # Faculty ID dropdown with autocomplete
                self.entry_vars[field_name] = StringVar()
                faculty_combo = ttk.Combobox(left_frame, textvariable=self.entry_vars[field_name], 
                                           font=("Arial", 12), state="normal")
                faculty_combo.grid(row=i+1, column=1, sticky=EW, pady=5)
                self.load_faculty_ids(faculty_combo)
                faculty_combo.bind("<<ComboboxSelected>>", self.on_faculty_select)
                faculty_combo.bind("<KeyRelease>", self.on_faculty_id_change)
            elif field_name == "block":
                # Block dropdown
                self.entry_vars[field_name] = StringVar()
                block_combo = ttk.Combobox(left_frame, textvariable=self.entry_vars[field_name], 
                                         font=("Arial", 12), state="readonly")
                block_combo.grid(row=i+1, column=1, sticky=EW, pady=5)
                self.load_blocks(block_combo)
            else:
                # Regular entry fields
                self.entry_vars[field_name] = StringVar()
                entry = Entry(left_frame, textvariable=self.entry_vars[field_name], 
                            font=("Arial", 12))
                entry.grid(row=i+1, column=1, sticky=EW, pady=5)
        
        # Additional Contact Information Fields
        Label(left_frame, text="Contact Information", font=("Arial", 14, "bold"), 
             bg="#ecf0f1").grid(row=len(cabin_fields)+2, column=0, columnspan=2, pady=(15, 5))
        
        contact_fields = [
            ("Contact Email:", "contact_email"),
            ("Available Hours:", "available_hours")
        ]
        
        for i, (label_text, field_name) in enumerate(contact_fields):
            Label(left_frame, text=label_text, font=("Arial", 12), 
                 bg="#ecf0f1").grid(row=len(cabin_fields)+3+i, column=0, sticky=W, pady=5)
            
            self.entry_vars[field_name] = StringVar()
            entry = Entry(left_frame, textvariable=self.entry_vars[field_name], 
                        font=("Arial", 12))
            entry.grid(row=len(cabin_fields)+3+i, column=1, sticky=EW, pady=5)
        
        # Buttons
        btn_frame = Frame(left_frame, bg="#ecf0f1")
        btn_frame.grid(row=len(cabin_fields)+len(contact_fields)+4, column=0, columnspan=2, pady=15)
        
        Button(btn_frame, text="Add/Update", command=self.save_cabin,
              font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
              width=12).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Clear", command=self.clear_form,
              font=("Arial", 12), bg="#e74c3c", fg="white",
              width=12).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Delete", command=self.delete_cabin,
              font=("Arial", 12), bg="#f39c12", fg="white",
              width=12).pack(side=LEFT, padx=5)
        
        # Right Frame Content - View Allocations
        Label(right_frame, text="Current Cabin Allocations", font=("Arial", 14, "bold"), 
             bg="#ecf0f1").pack(pady=10)
        
        # Treeview with scrollbars
        tree_frame = Frame(right_frame, bg="#ecf0f1")
        tree_frame.pack(fill=BOTH, expand=True)
        
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.tree = ttk.Treeview(tree_frame, 
                                columns=("faculty_id", "name", "department", "block", "floor", "room", "cabin", "email", "hours"),
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Configure columns
        self.tree.heading("#0", text="ID")
        self.tree.heading("faculty_id", text="Faculty ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("department", text="Department")
        self.tree.heading("block", text="Block")
        self.tree.heading("floor", text="Floor")
        self.tree.heading("room", text="Room No.")
        self.tree.heading("cabin", text="Cabin No.")
        self.tree.heading("email", text="Email")
        self.tree.heading("hours", text="Available Hours")
        
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("faculty_id", width=100, anchor=CENTER)
        self.tree.column("name", width=150, anchor=W)
        self.tree.column("department", width=150, anchor=W)
        self.tree.column("block", width=120, anchor=W)
        self.tree.column("floor", width=60, anchor=CENTER)
        self.tree.column("room", width=80, anchor=CENTER)
        self.tree.column("cabin", width=80, anchor=CENTER)
        self.tree.column("email", width=150, anchor=W)
        self.tree.column("hours", width=150, anchor=W)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.pack(fill=BOTH, expand=True)
        
        # Bind tree selection to form
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Filter Frame
        filter_frame = Frame(right_frame, bg="#ecf0f1", pady=10)
        filter_frame.pack(fill=X)
        
        Label(filter_frame, text="Filter By:", font=("Arial", 12), 
             bg="#ecf0f1").pack(side=LEFT, padx=5)
        
        self.filter_type = StringVar(value="block")
        filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type, 
                    values=["block", "department"], 
                    font=("Arial", 12), state="readonly", width=10)
        filter_type_combo.pack(side=LEFT, padx=5)
        self.filter_type.trace('w', lambda *args: self.update_filter_options())
        
        self.filter_value = StringVar()
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_value, 
                                   font=("Arial", 12), state="readonly")
        self.filter_combo.pack(side=LEFT, padx=5)
        self.update_filter_options()
        
        Button(filter_frame, text="Apply Filter", command=self.load_cabins,
              font=("Arial", 12), bg="#3498db", fg="white").pack(side=LEFT, padx=10)
        
        Button(filter_frame, text="Reset", command=self.reset_filter,
              font=("Arial", 12), bg="#95a5a6", fg="white").pack(side=LEFT, padx=5)
        
        # Status Bar
        self.status = Label(self.root, text="Ready", bd=1, relief=SUNKEN, anchor=W,
                          font=("Arial", 10), bg="#2c3e50", fg="white")
        self.status.pack(fill=X, side=BOTTOM)
        
        # Load initial data
        self.load_cabins()
    
    def load_faculty_ids(self, combo):
        cursor = self.conn.cursor()
        cursor.execute("SELECT faculty_id, faculty_name FROM faculty ORDER BY faculty_id")
        faculty_data = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        combo['values'] = faculty_data
        cursor.close()
    
    def on_faculty_select(self, event):
        selected = self.entry_vars["faculty_id"].get()
        if not selected:
            return
            
        faculty_id = selected.split(" - ")[0]
        self.fetch_faculty_details(faculty_id)
    
    def on_faculty_id_change(self, event):
        current_text = self.entry_vars["faculty_id"].get()
        if " - " in current_text:
            faculty_id = current_text.split(" - ")[0]
            self.fetch_faculty_details(faculty_id)
    
    def fetch_faculty_details(self, faculty_id):
        cursor = self.conn.cursor(dictionary=True)
        
        # Get basic faculty info
        cursor.execute("SELECT faculty_name, department FROM faculty WHERE faculty_id = %s", (faculty_id,))
        faculty = cursor.fetchone()
        
        if faculty:
            self.entry_vars["name"].set(faculty['faculty_name'])
            self.entry_vars["department"].set(faculty['department'])
            
            # Get cabin allocation if exists
            cursor.execute("SELECT * FROM faculty_cabins WHERE faculty_id = %s", (faculty_id,))
            cabin = cursor.fetchone()
            if cabin:
                self.entry_vars["block"].set(cabin['block'])
                self.entry_vars["floor"].set(cabin['floor'])
                self.entry_vars["room_number"].set(cabin['room_number'])
                self.entry_vars["cabin_number"].set(cabin['cabin_number'])
            
            # Get contact info if exists
            cursor.execute("SELECT * FROM faculty_directory WHERE faculty_id = %s", (faculty_id,))
            directory = cursor.fetchone()
            if directory:
                self.entry_vars["contact_email"].set(directory.get('contact_email', ''))
                self.entry_vars["available_hours"].set(directory.get('available_hours', ''))
            else:
                self.entry_vars["contact_email"].set('')
                self.entry_vars["available_hours"].set('')
        else:
            # Clear all fields if faculty not found
            for field in ["name", "department", "block", "floor", "room_number", "cabin_number", 
                         "contact_email", "available_hours"]:
                if field in self.entry_vars:
                    self.entry_vars[field].set("")
        
        cursor.close()
    
    def load_blocks(self, combo):
        cursor = self.conn.cursor()
        cursor.execute("SELECT block_name FROM campus_blocks ORDER BY block_name")
        blocks = [row[0] for row in cursor.fetchall()]
        combo['values'] = blocks
        if len(blocks) > 0:
            combo.current(0)
        cursor.close()
    
    def update_filter_options(self):
        filter_type = self.filter_type.get()
        cursor = self.conn.cursor()
        
        try:
            if filter_type == "block":
                cursor.execute("SELECT block_name FROM campus_blocks ORDER BY block_name")
                options = [row[0] for row in cursor.fetchall()]
            else:  # department
                cursor.execute("SELECT DISTINCT department FROM faculty_cabins ORDER BY department")
                options = [row[0] for row in cursor.fetchall()]
                if not options:  # If no departments in faculty_cabins, try faculty table
                    cursor.execute("SELECT DISTINCT department FROM faculty ORDER BY department")
                    options = [row[0] for row in cursor.fetchall()]
            
            self.filter_value.set("")
            self.filter_combo['values'] = options
            if len(options) > 0:
                self.filter_combo.current(0)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading filter options: {err}")
        finally:
            cursor.close()
    
    def load_cabins(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Build query based on filter
        filter_type = self.filter_type.get()
        filter_value = self.filter_value.get()
        
        if not filter_value or filter_value == "All":
            query = """
                SELECT fc.faculty_id, fc.name, fc.department, fc.block, fc.floor, 
                       fc.room_number, fc.cabin_number, fd.contact_email, fd.available_hours
                FROM faculty_cabins fc
                LEFT JOIN faculty_directory fd ON fc.faculty_id = fd.faculty_id
                ORDER BY block, floor, room_number
            """
            params = ()
        else:
            if filter_type == "block":
                query = """
                    SELECT fc.faculty_id, fc.name, fc.department, fc.block, fc.floor, 
                           fc.room_number, fc.cabin_number, fd.contact_email, fd.available_hours
                    FROM faculty_cabins fc
                    LEFT JOIN faculty_directory fd ON fc.faculty_id = fd.faculty_id
                    WHERE fc.block = %s
                    ORDER BY floor, room_number
                """
            else:  # department
                query = """
                    SELECT fc.faculty_id, fc.name, fc.department, fc.block, fc.floor, 
                           fc.room_number, fc.cabin_number, fd.contact_email, fd.available_hours
                    FROM faculty_cabins fc
                    LEFT JOIN faculty_directory fd ON fc.faculty_id = fd.faculty_id
                    WHERE fc.department = %s
                    ORDER BY block, floor, room_number
                """
            params = (filter_value,)
            
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, params)
            
            for faculty in cursor.fetchall():
                self.tree.insert("", "end", 
                               values=(
                                   faculty['faculty_id'],
                                   faculty['name'],
                                   faculty['department'],
                                   faculty['block'],
                                   faculty['floor'],
                                   faculty['room_number'],
                                   faculty['cabin_number'],
                                   faculty.get('contact_email', ''),
                                   faculty.get('available_hours', '')
                               ))
            
            self.status.config(text=f"Loaded {self.tree.get_children().__len__()} cabin allocations")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading cabin data: {err}")
        finally:
            cursor.close()
    
    def reset_filter(self):
        self.filter_type.set("block")
        self.filter_value.set("")
        self.update_filter_options()
        self.load_cabins()
    
    def on_tree_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
            
        values = self.tree.item(selected, 'values')
        if values:
            faculty_id, name = values[0], values[1]
            self.entry_vars["faculty_id"].set(f"{faculty_id} - {name}")
            self.entry_vars["name"].set(name)
            self.entry_vars["department"].set(values[2])
            self.entry_vars["block"].set(values[3])
            self.entry_vars["floor"].set(values[4])
            self.entry_vars["room_number"].set(values[5])
            self.entry_vars["cabin_number"].set(values[6])
            self.entry_vars["contact_email"].set(values[7] if len(values) > 7 else "")
            self.entry_vars["available_hours"].set(values[8] if len(values) > 8 else "")
    
    def clear_form(self):
        for var in self.entry_vars.values():
            if isinstance(var, StringVar):
                var.set("")
    
    def validate_form(self):
        required_fields = [
            ("faculty_id", "Faculty ID"),
            ("name", "Name"),
            ("department", "Department"),
            ("block", "Block"),
            ("floor", "Floor"),
            ("room_number", "Room Number"),
            ("cabin_number", "Cabin Number")
        ]
        
        for field, name in required_fields:
            if not self.entry_vars[field].get():
                messagebox.showwarning("Validation Error", f"{name} is required")
                return False
                
        # Extract faculty ID from combo box
        faculty_id = self.entry_vars["faculty_id"].get().split(" - ")[0]
        if not faculty_id:
            messagebox.showwarning("Validation Error", "Invalid faculty selection")
            return False
            
        # Validate floor is numeric
        try:
            floor = int(self.entry_vars["floor"].get())
            if floor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error", "Floor must be a positive integer")
            return False
            
        # Validate room number is not empty
        if not self.entry_vars["room_number"].get():
            messagebox.showwarning("Validation Error", "Room number is required")
            return False
            
        # Validate email format if provided
        email = self.entry_vars["contact_email"].get()
        if email and "@" not in email:
            messagebox.showwarning("Validation Error", "Please enter a valid email address")
            return False
            
        return True
    
    def save_cabin(self):
        if not self.validate_form():
            return
            
        # Extract faculty ID from combo box
        faculty_id = self.entry_vars["faculty_id"].get().split(" - ")[0]
        
        # Cabin allocation data
        cabin_data = (
            faculty_id,
            self.entry_vars["name"].get(),
            self.entry_vars["department"].get(),
            self.entry_vars["block"].get(),
            int(self.entry_vars["floor"].get()),
            self.entry_vars["room_number"].get(),
            self.entry_vars["cabin_number"].get()
        )
        
        # Contact information data
        contact_data = (
            faculty_id,
            self.entry_vars["contact_email"].get(),
            self.entry_vars["available_hours"].get()
        )
        
        try:
            cursor = self.conn.cursor()
            
            # Check if faculty exists in faculty table
            cursor.execute("SELECT 1 FROM faculty WHERE faculty_id = %s", (faculty_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Faculty ID does not exist in faculty table")
                return
                
            # Handle cabin allocation (insert or update)
            cursor.execute("SELECT 1 FROM faculty_cabins WHERE faculty_id = %s", (faculty_id,))
            if cursor.fetchone():
                # Update existing cabin record
                cabin_query = """
                    UPDATE faculty_cabins 
                    SET name = %s, department = %s, block = %s, 
                        floor = %s, room_number = %s, cabin_number = %s
                    WHERE faculty_id = %s
                """
                cursor.execute(cabin_query, (cabin_data[1], cabin_data[2], cabin_data[3], 
                              cabin_data[4], cabin_data[5], cabin_data[6], cabin_data[0]))
            else:
                # Insert new cabin record
                cabin_query = """
                    INSERT INTO faculty_cabins 
                    (faculty_id, name, department, block, floor, room_number, cabin_number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(cabin_query, cabin_data)
            
            # Handle contact information (insert or update)
            cursor.execute("SELECT 1 FROM faculty_directory WHERE faculty_id = %s", (faculty_id,))
            if cursor.fetchone():
                # Update existing contact record
                contact_query = """
                    UPDATE faculty_directory 
                    SET contact_email = %s, available_hours = %s
                    WHERE faculty_id = %s
                """
                cursor.execute(contact_query, (contact_data[1], contact_data[2], contact_data[0]))
            else:
                # Insert new contact record
                contact_query = """
                    INSERT INTO faculty_directory 
                    (faculty_id, contact_email, available_hours)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(contact_query, contact_data)
                
            self.conn.commit()
            messagebox.showinfo("Success", "Faculty information saved successfully")
            self.load_cabins()
            self.clear_form()
            
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Error", "This room/cabin combination is already assigned to another faculty")
            else:
                messagebox.showerror("Database Error", f"Error: {e}")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
    
    def delete_cabin(self):
        faculty_id = self.entry_vars["faculty_id"].get().split(" - ")[0] if " - " in self.entry_vars["faculty_id"].get() else ""
        if not faculty_id:
            messagebox.showwarning("Error", "No faculty selected for deletion")
            return
            
        if not messagebox.askyesno("Confirm Delete", 
                                 f"Delete all information for {self.entry_vars['name'].get()}?"):
            return
            
        try:
            cursor = self.conn.cursor()
            
            # Delete from both tables
            cursor.execute("DELETE FROM faculty_cabins WHERE faculty_id = %s", (faculty_id,))
            cursor.execute("DELETE FROM faculty_directory WHERE faculty_id = %s", (faculty_id,))
            
            self.conn.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Faculty information deleted successfully")
                self.load_cabins()
                self.clear_form()
            else:
                messagebox.showwarning("Error", "No record found to delete")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FacultyCabinManager(root)
    root.mainloop()