from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
import os
import webbrowser
import sys

class FeeReceiptViewer:
    def __init__(self, root, rollno=None):
        self.root = root
        self.root.title("Fee Receipt Viewer")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f8ff")  # Light blue background
        self.root.state('zoomed')
        
        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vnsvb",
            database="face_recognition"
        )
        
        # Variables
        self.var_rollno = StringVar()
        self.var_dob = StringVar()
        
        # If rollno provided, open receipts directly
        if rollno:
            self.show_receipts_list(rollno)
        else:
            self.create_ui()
        
    def create_ui(self):
        """Create the UI for manual fee receipt viewing"""
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = Frame(self.root, bg="white", bd=2, relief=GROOVE)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=300)
        
        Label(main_frame, text="Fee Receipt Viewer", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        Label(main_frame, text="Roll Number:", font=("Arial", 12), bg="white").pack(pady=5)
        Entry(main_frame, textvariable=self.var_rollno, font=("Arial", 12)).pack(pady=5, ipady=5, ipadx=50)
        
        Label(main_frame, text="Date of Birth (DD-MM-YYYY):", font=("Arial", 12), bg="white").pack(pady=5)
        Entry(main_frame, textvariable=self.var_dob, font=("Arial", 12)).pack(pady=5, ipady=5, ipadx=50)
        
        Button(main_frame, text="View Fee Receipts", 
              command=self.validate_and_show_receipts,
              font=("Arial", 12), bg="#4CAF50", fg="white",
              padx=20, pady=5).pack(pady=20)
        
        self.root.bind('<Return>', lambda event: self.validate_and_show_receipts())

    def validate_and_show_receipts(self):
        rollno = self.var_rollno.get().strip()
        dob = self.var_dob.get().strip()
        
        if not rollno or not dob:
            messagebox.showerror("Error", "Please enter both Roll Number and Date of Birth")
            return
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT StudentID FROM student 
                WHERE StudentID = %s AND DOB = %s
            """, (rollno, dob))
            
            if cursor.fetchone():
                self.show_receipts_list(rollno)
            else:
                messagebox.showerror("Error", "Invalid Roll Number or Date of Birth")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
    
    def show_receipts_list(self, rollno):
        try:
            for widget in self.root.winfo_children():
                widget.destroy()
            
            self.root.title(f"Fee Receipts - {rollno}")
            
            Label(self.root, text=f"Fee Receipts for {rollno}", 
                 font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=20)
            
            frame = Frame(self.root, bd=2, relief=GROOVE)
            frame.pack(pady=10, padx=20, fill=BOTH, expand=True)
            
            scroll_y = Scrollbar(frame)
            scroll_y.pack(side=RIGHT, fill=Y)
            
            self.receipts_table = ttk.Treeview(frame, columns=("receipt_no", "date", "amount", "view"),
                                             yscrollcommand=scroll_y.set)
            scroll_y.config(command=self.receipts_table.yview)
            
            self.receipts_table.heading("receipt_no", text="Receipt No")
            self.receipts_table.heading("date", text="Date")
            self.receipts_table.heading("amount", text="Amount")
            self.receipts_table.heading("view", text="Action")
            
            self.receipts_table.column("receipt_no", width=80, anchor='center')
            self.receipts_table.column("date", width=100, anchor='center')
            self.receipts_table.column("amount", width=80, anchor='center')
            self.receipts_table.column("view", width=100, anchor='center')
            
            self.receipts_table.pack(fill=BOTH, expand=True)
            
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT receipt_no, receipt_date, amount_paid 
                FROM fee_receipts 
                WHERE studentID = %s 
                ORDER BY receipt_date DESC
            """, (rollno,))
            
            receipts = cursor.fetchall()
            cursor.close()
            
            if not receipts:
                Label(self.root, text="No fee receipts found for this student", 
                     font=("Arial", 12), bg="#f0f8ff").pack(pady=20)
                Button(self.root, text="Back", command=self.open_student_page,
                      font=("Arial", 12), bg="orange", fg="white").pack(pady=10)
                return
            
            for receipt in receipts:
                receipt_no = receipt['receipt_no']
                self.receipts_table.insert("", "end", values=(
                    receipt_no,
                    receipt['receipt_date'],
                    f"INR {receipt['amount_paid']:.2f}",
                    "View Receipt"
                ))
            
            self.receipts_table.bind("<ButtonRelease-1>", lambda e: self.open_receipt(rollno))
            Button(self.root, text="Back", command=self.open_student_page,
                  font=("Arial", 12), bg="orange", fg="white").pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load receipts: {str(e)}")
            self.open_student_page()
    
    def open_receipt(self, rollno):
        selected_item = self.receipts_table.focus()
        if not selected_item:
            return
            
        receipt_no = self.receipts_table.item(selected_item)['values'][0]
        
        try:
            file_path = f"C:/Users/chinn/OneDrive/Desktop/Automated Attendance/generated_FeeReceipts/FeeReceipt_{receipt_no}_{rollno}.pdf"

            if os.path.exists(file_path):
                webbrowser.open(file_path)
            else:
                messagebox.showerror("Error", "Receipt file not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open receipt: {str(e)}")
    
    def open_student_page(self):
        """Open the student.py page"""
        self.root.destroy()  # Close the current window
        try:
            # Assuming student.py is in the same directory
            os.system('python student_page.py')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open student page: {str(e)}")


if __name__ == "__main__":
    root = Tk()
    rollno = sys.argv[1] if len(sys.argv) > 1 else None
    app = FeeReceiptViewer(root, rollno)
    root.mainloop()