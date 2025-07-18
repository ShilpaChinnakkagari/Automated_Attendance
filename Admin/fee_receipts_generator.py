from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from fpdf import FPDF
import os
import webbrowser
from datetime import datetime
import random
import string

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Use built-in font instead of external TTF to avoid file not found errors
        self.set_font('Arial', '', 12)  # Built-in font

class FeeReceipt:
    def __init__(self, root):
        self.root = root
        self.root.title("Fee Receipt Generator")
        self.root.geometry("1530x780+0+0")
        self.root.config(bg="white")
        self.root.state('zoomed')
        # Variables
        self.search = StringVar()
        self.student_id = StringVar()
        self.receipt_date = StringVar()
        self.amount_paid = StringVar()
        self.payment_mode = StringVar()
        self.transaction_id = StringVar()
        self.academic_year = StringVar()
        self.semester = StringVar()

        # Database connection
        self.conn = self.create_db_connection()
        
        # Get all departments for dropdown
        self.departments = self.get_all_departments()

        # UI Setup
        self.setup_ui()

        # Create fee_receipts table if not exists
        self.create_fee_receipts_table()
        self.load_generated_receipts()

    def create_db_connection(self):
        """Create and return database connection with error handling"""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="face_recognition"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            self.root.destroy()
            exit()

    def setup_ui(self):
        """Setup all UI components"""
        # Title
        title = Label(self.root, text="Fee Receipt Generator", 
                     font=("lucida", 20, "bold", "italic"), bg="orange", fg="black")
        title.pack(side=TOP, fill=X)

        # Search Section
        self.setup_search_section()
        
        # Payment Details Section
        self.setup_payment_section()
        
        # Tables
        self.setup_tables()
        
        # Generate Button
        Button(self.root, text="Generate Receipt", command=self.generate_receipt,
              font=("times new roman", 12, "bold"), bg="green", fg="white", 
              cursor="hand2").place(x=400, y=670, width=180, height=30)

    def setup_search_section(self):
        """Setup search section with department dropdown"""
        Label(self.root, text="Select Department:", 
             font=("times new roman", 14, "bold"), bg="white").place(x=50, y=60)
        
        self.department_combo = ttk.Combobox(self.root, textvariable=self.search, 
                                           font=("times new roman", 14), state="readonly")
        self.department_combo['values'] = self.departments
        self.department_combo.place(x=220, y=60, width=200)
        self.department_combo.bind("<<ComboboxSelected>>", lambda e: self.search_name())

        Label(self.root, text="Student ID:", 
             font=("times new roman", 15, "bold"), bg="white").place(x=50, y=100)
        Entry(self.root, textvariable=self.student_id, width=25,
             font=("times new roman", 12, "bold"), bg="lightyellow").place(x=220, y=100)

        Button(self.root, text="Search", command=self.search_both,
              font=("times new roman", 12, "bold"), bg="skyblue", fg="white", 
              cursor="hand2").place(x=470, y=80, width=100, height=30)
        Button(self.root, text="Reset", command=self.reset_fields,
              font=("times new roman", 12, "bold"), bg="red", fg="white", 
              cursor="hand2").place(x=570, y=80, width=100, height=30)

    def setup_payment_section(self):
        """Setup payment details section"""
        Label(self.root, text="Receipt Date:", 
             font=("times new roman", 14, "bold"), bg="white").place(x=50, y=140)
        Entry(self.root, textvariable=self.receipt_date, 
             font=("times new roman", 14), bg="lightyellow").place(x=220, y=140, width=200)
        self.receipt_date.set(datetime.now().strftime("%d-%m-%Y"))

        Label(self.root, text="Amount Paid:", 
             font=("times new roman", 14, "bold"), bg="white").place(x=50, y=180)
        Entry(self.root, textvariable=self.amount_paid, 
             font=("times new roman", 14), bg="lightyellow").place(x=220, y=180, width=200)

        Label(self.root, text="Payment Mode:", 
             font=("times new roman", 14, "bold"), bg="white").place(x=50, y=220)
        self.payment_mode_combo = ttk.Combobox(self.root, textvariable=self.payment_mode, 
                                             font=("times new roman", 14), state="readonly")
        self.payment_mode_combo['values'] = ("Cash", "Cheque", "Online Transfer", "DD", "Card")
        self.payment_mode_combo.place(x=220, y=220, width=200)
        self.payment_mode_combo.current(0)
        self.payment_mode_combo.bind("<<ComboboxSelected>>", self.update_transaction_id_field)

        Label(self.root, text="Transaction ID:", 
             font=("times new roman", 14, "bold"), bg="white").place(x=50, y=260)
        self.transaction_id_entry = Entry(self.root, textvariable=self.transaction_id, 
                                        font=("times new roman", 14), bg="lightyellow", state='disabled')
        self.transaction_id_entry.place(x=220, y=260, width=200)
        self.update_transaction_id_field()

        Label(self.root, text="Academic Year:", 
             font=("times new roman", 14, "bold"), bg="white").place(x=50, y=300)
        self.academic_year_combo = ttk.Combobox(self.root, textvariable=self.academic_year, 
                                              font=("times new roman", 14), state="readonly")
        current_year = datetime.now().year
        self.academic_year_combo['values'] = (f"{current_year-1}-{current_year}", 
                                            f"{current_year}-{current_year+1}")
        self.academic_year_combo.place(x=220, y=300, width=200)
        self.academic_year_combo.current(0)

        Label(self.root, text="Semester:", 
             font=("times new roman", 14, "bold"), bg="white").place(x=50, y=340)
        self.semester_combo = ttk.Combobox(self.root, textvariable=self.semester, 
                                         font=("times new roman", 14), state="readonly")
        self.semester_combo['values'] = ("1", "2", "3", "4", "5", "6", "7", "8")
        self.semester_combo.place(x=220, y=340, width=200)
        self.semester_combo.current(0)

    def setup_tables(self):
        """Setup student and fee history tables"""
        # Student Table Frame
        frame1 = Frame(self.root, bd=2, relief=RIDGE)
        frame1.place(x=50, y=380, width=900, height=150)

        scroll_x1 = Scrollbar(frame1, orient=HORIZONTAL)
        scroll_y1 = Scrollbar(frame1, orient=VERTICAL)
        scroll_x1.pack(side=BOTTOM, fill=X)
        scroll_y1.pack(side=RIGHT, fill=Y)

        self.student_table = ttk.Treeview(frame1, columns=("studentID", "Student Name", "Department", "Course", "Year", "Semester"),
                                         xscrollcommand=scroll_x1.set, yscrollcommand=scroll_y1.set)
        scroll_x1.config(command=self.student_table.xview)
        scroll_y1.config(command=self.student_table.yview)

        self.student_table.heading("studentID", text="Student ID")
        self.student_table.heading("Student Name", text="Student Name")
        self.student_table.heading("Department", text="Department")
        self.student_table.heading("Course", text="Course")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("Semester", text="Semester")

        self.student_table["show"] = "headings"

        self.student_table.column("studentID", width=90)
        self.student_table.column("Student Name", width=120)
        self.student_table.column("Department", width=120)
        self.student_table.column("Course", width=80)
        self.student_table.column("Year", width=50)
        self.student_table.column("Semester", width=70)

        self.student_table.pack(fill=BOTH, expand=1)

        # Fee History Table Frame
        frame2 = Frame(self.root, bd=2, relief=RIDGE)
        frame2.place(x=50, y=540, width=900, height=120)

        scroll_x2 = Scrollbar(frame2, orient=HORIZONTAL)
        scroll_y2 = Scrollbar(frame2, orient=VERTICAL)
        scroll_x2.pack(side=BOTTOM, fill=X)
        scroll_y2.pack(side=RIGHT, fill=Y)

        self.fee_table = ttk.Treeview(frame2, columns=("receipt_no", "date", "amount", "payment_mode", "academic_year", "semester"),
                                     xscrollcommand=scroll_x2.set, yscrollcommand=scroll_y2.set)
        scroll_x2.config(command=self.fee_table.xview)
        scroll_y2.config(command=self.fee_table.yview)

        self.fee_table.heading("receipt_no", text="Receipt No")
        self.fee_table.heading("date", text="Date")
        self.fee_table.heading("amount", text="Amount")
        self.fee_table.heading("payment_mode", text="Payment Mode")
        self.fee_table.heading("academic_year", text="Academic Year")
        self.fee_table.heading("semester", text="Semester")

        self.fee_table["show"] = "headings"

        self.fee_table.column("receipt_no", width=80)
        self.fee_table.column("date", width=80)
        self.fee_table.column("amount", width=80)
        self.fee_table.column("payment_mode", width=100)
        self.fee_table.column("academic_year", width=100)
        self.fee_table.column("semester", width=70)

        self.fee_table.pack(fill=BOTH, expand=1)

        # Generated Receipts Frame
        frame_generated = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame_generated.place(x=1000, y=160, width=450, height=500)

        Label(frame_generated, text="Generated Fee Receipts",
             font=("times new roman", 15, "bold"), bg="white", fg="black").pack(side=TOP, fill=X)

        scroll_x = Scrollbar(frame_generated, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame_generated, orient=VERTICAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.generated_table = ttk.Treeview(frame_generated, columns=("studentID", "receipt_no", "view"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.generated_table.xview)
        scroll_y.config(command=self.generated_table.yview)

        self.generated_table.heading("studentID", text="Student ID")
        self.generated_table.heading("receipt_no", text="Receipt No")
        self.generated_table.heading("view", text="Receipt")

        self.generated_table["show"] = "headings"
        self.generated_table.column("studentID", width=100)
        self.generated_table.column("receipt_no", width=80)
        self.generated_table.column("view", width=150)

        self.generated_table.pack(fill=BOTH, expand=1)
        self.generated_table.bind("<ButtonRelease-1>", self.open_selected_pdf)

    def get_all_departments(self):
        """Fetch all unique departments from student table"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT Department FROM student ORDER BY Department")
            departments = [row[0] for row in cursor.fetchall() if row[0]]
            return departments if departments else ["No departments found"]
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching departments: {str(e)}")
            return ["Error loading departments"]
        finally:
            cursor.close()

    def create_fee_receipts_table(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fee_receipts (
                    receipt_no INT AUTO_INCREMENT PRIMARY KEY,
                    studentID VARCHAR(15),
                    receipt_date VARCHAR(15),
                    amount_paid DECIMAL(10,2),
                    payment_mode VARCHAR(20),
                    transaction_id VARCHAR(30),
                    academic_year VARCHAR(20),
                    semester VARCHAR(5),
                    FOREIGN KEY (studentID) REFERENCES student(studentID)
                )
            """)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error creating fee_receipts table: {str(e)}")
        finally:
            cursor.close()

    def update_transaction_id_field(self, event=None):
        """Enable/disable transaction ID field based on payment mode"""
        try:
            if self.payment_mode.get() == "Cash":
                self.transaction_id_entry.config(state='disabled')
                self.transaction_id.set("CASH-" + datetime.now().strftime("%Y%m%d"))
            else:
                self.transaction_id_entry.config(state='normal')
                letters = string.ascii_uppercase
                random_str = ''.join(random.choice(letters) for i in range(6))
                self.transaction_id.set(f"{self.payment_mode.get()[:3]}-{random_str}-{datetime.now().strftime('%m%d')}")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating transaction ID: {str(e)}")

    def search_name(self):
        cursor = self.conn.cursor()
        try:
            department = self.search.get()
            if not department or department == "No departments found":
                messagebox.showerror("Error", "Please select a valid department")
                return

            query = """
                SELECT studentID, `Student Name`, Department, Course, Year, Semester 
                FROM student 
                WHERE Department = %s
                ORDER BY `Student Name`
            """
            cursor.execute(query, (department,))
            rows = cursor.fetchall()

            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", "end", values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error searching students: {str(ex)}")
        finally:
            cursor.close()

    def search_id_(self):
        cursor = self.conn.cursor()
        try:
            studentID = self.student_id.get().strip()
            if not studentID:
                return

            query = """
                SELECT studentID, `Student Name`, Department, Course, Year, Semester 
                FROM student 
                WHERE studentID = %s
            """
            cursor.execute(query, (studentID,))
            row = cursor.fetchone()

            if row:
                self.student_table.delete(*self.student_table.get_children())
                self.student_table.insert("", "end", values=row)
                self.search.set(row[2])  # Auto-fill department
                self.load_fee_history(studentID)
                self.update_transaction_id_field()

        except Exception as ex:
            messagebox.showerror("Error", f"Error searching student ID: {str(ex)}")
        finally:
            cursor.close()

    def load_fee_history(self, studentID):
        cursor = self.conn.cursor()
        try:
            query = """
                SELECT receipt_no, receipt_date, amount_paid, payment_mode, academic_year, semester 
                FROM fee_receipts 
                WHERE studentID = %s
                ORDER BY receipt_date DESC
            """
            cursor.execute(query, (studentID,))
            rows = cursor.fetchall()

            self.fee_table.delete(*self.fee_table.get_children())
            for row in rows:
                self.fee_table.insert("", "end", values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error loading fee history: {str(ex)}")
        finally:
            cursor.close()

    def reset_fields(self):
        try:
            self.search.set("")
            self.student_id.set("")
            self.student_table.delete(*self.student_table.get_children())
            self.fee_table.delete(*self.fee_table.get_children())
            self.amount_paid.set("")
            self.transaction_id.set("")
            self.update_transaction_id_field()
            self.department_combo.set('')
            self.academic_year_combo.current(0)
            self.semester_combo.current(0)
            self.payment_mode_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Error resetting fields: {str(e)}")

    def search_both(self):
        try:
            self.search_name()
            self.search_id_()
        except Exception as e:
            messagebox.showerror("Error", f"Error in search: {str(e)}")

    def generate_receipt(self):
        try:
            # Validate student selection
            student_items = self.student_table.get_children()
            if not student_items:
                messagebox.showerror("Error", "Please select a student first")
                return
                
            student_data = self.student_table.item(student_items[0])['values']
            if len(student_data) < 6:
                messagebox.showerror("Error", "Invalid student data")
                return
                
            studentID, studentName, department, course, year, semester = student_data[:6]
            
            # Validate amount
            try:
                amount = float(self.amount_paid.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid amount: {str(ve)}")
                return
                
            # Validate other fields
            if not self.payment_mode.get():
                messagebox.showerror("Error", "Please select payment mode")
                return
                
            if self.payment_mode.get() != "Cash" and not self.transaction_id.get():
                messagebox.showerror("Error", "Please enter transaction ID for non-cash payments")
                return
                
            if not self.academic_year.get() or not self.semester.get():
                messagebox.showerror("Error", "Please select academic year and semester")
                return

            # Save to database
            cursor = self.conn.cursor()
            query = """
                INSERT INTO fee_receipts 
                (studentID, receipt_date, amount_paid, payment_mode, transaction_id, academic_year, semester)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                str(studentID),
                str(self.receipt_date.get()),
                float(self.amount_paid.get()),
                str(self.payment_mode.get()),
                str(self.transaction_id.get()),
                str(self.academic_year.get()),
                str(self.semester.get())
            )
            cursor.execute(query, values)
            self.conn.commit()
            receipt_no = cursor.lastrowid
            cursor.close()

            # Generate PDF receipt using built-in font
            folder_path = "generated_FeeReceipts"
            os.makedirs(folder_path, exist_ok=True)

            pdf = PDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Title
            pdf.set_xy(10, 50)
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, "FEE RECEIPT", ln=True, align='C')
            
            # Receipt details
            pdf.set_font('Arial', '', 12)
            pdf.cell(95, 10, f"Receipt No: {receipt_no}", ln=0)
            pdf.cell(95, 10, f"Date: {self.receipt_date.get()}", ln=1, align='R')
            pdf.ln(10)

            # Student details
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "Student Details", ln=True)
            pdf.set_font('Arial', '', 12)
            
            details = [
                ("Student ID:", str(studentID)),
                ("Name:", str(studentName)),
                ("Department:", str(department)),
                ("Course:", str(course)),
                ("Year/Semester:", f"{str(year)}/{str(self.semester.get())}"),
                ("Academic Year:", str(self.academic_year.get()))
            ]
            
            for label, value in details:
                pdf.cell(40, 8, label, ln=0)
                pdf.cell(0, 8, value, ln=1)
            
            pdf.ln(10)

            # Payment details
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "Payment Details", ln=True)
            pdf.set_font('Arial', '', 12)
            
            pdf.cell(40, 8, "Amount Paid:", ln=0)
            pdf.cell(0, 8, f"INR {float(self.amount_paid.get()):.2f}", ln=1)

            
            pdf.cell(40, 8, "Payment Mode:", ln=0)
            pdf.cell(0, 8, str(self.payment_mode.get()), ln=1)
            
            if self.transaction_id.get():
                pdf.cell(40, 8, "Transaction ID:", ln=0)
                pdf.cell(0, 8, str(self.transaction_id.get()), ln=1)
            
            pdf.ln(15)

            # Signature section
            pdf.cell(95, 8, "Student Signature", ln=0)
            pdf.cell(95, 8, "Authorized Signatory", ln=1, align='R')
            pdf.line(20, pdf.get_y(), 60, pdf.get_y())
            pdf.line(150, pdf.get_y(), 190, pdf.get_y())

            # Save PDF
            filename = os.path.join(folder_path, f"FeeReceipt_{receipt_no}_{studentID}.pdf")
            pdf.output(filename)
            
            messagebox.showinfo("Success", f"Fee Receipt generated successfully!\nReceipt No: {receipt_no}")
            
            # Refresh tables
            self.load_fee_history(studentID)
            self.load_generated_receipts()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate fee receipt: {str(e)}")

    def open_selected_pdf(self, event):
        try:
            region = self.generated_table.identify("region", event.x, event.y)
            column = self.generated_table.identify_column(event.x)

            if region != "cell" or column != "#3":
                return

            selected_item = self.generated_table.focus()
            if not selected_item:
                return

            values = self.generated_table.item(selected_item, 'values')
            if len(values) != 3:
                return

            filename = values[2]
            filepath = os.path.join("generated_FeeReceipts", filename)
            if os.path.exists(filepath):
                webbrowser.open_new(filepath)
            else:
                messagebox.showerror("Error", f"File not found: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening PDF: {str(e)}")

    def load_generated_receipts(self):
        try:
            self.generated_table.delete(*self.generated_table.get_children())
            folder_path = "generated_FeeReceipts"
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith(".pdf") and filename.startswith("FeeReceipt_"):
                        parts = filename.split("_")
                        if len(parts) >= 3:
                            receipt_no = parts[1]
                            student_id = parts[2].split(".")[0]
                            self.generated_table.insert("", "end", values=(student_id, receipt_no, filename))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading receipts: {str(e)}")


if __name__ == "__main__":
    root = Tk()
    obj = FeeReceipt(root)
    root.mainloop()