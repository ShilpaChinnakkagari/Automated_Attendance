from tkinter import *
from tkinter import messagebox
import mysql.connector
import os
import webbrowser
import sys

class HallTicketViewer:
    def __init__(self, root, rollno=None):
        self.root = root
        self.root.title("Hall Ticket Viewer")
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
        
        # If rollno provided, open ticket directly
        if rollno:
            self.open_hall_ticket(rollno)
        else:
            # Create UI for manual entry
            self.create_ui()
        
    def create_ui(self):
        """Create the UI for manual hall ticket viewing"""
        # Main frame
        main_frame = Frame(self.root, bg="white", bd=2, relief=GROOVE)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=300)
        
        # Title
        Label(main_frame, text="Hall Ticket Viewer", 
             font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        # Roll Number Entry
        Label(main_frame, text="Roll Number:", 
             font=("Arial", 12), bg="white").pack(pady=5)
        
        Entry(main_frame, textvariable=self.var_rollno, 
             font=("Arial", 12)).pack(pady=5, ipady=5, ipadx=50)
        
        # Date of Birth Entry
        Label(main_frame, text="Date of Birth (DD-MM-YYYY):", 
             font=("Arial", 12), bg="white").pack(pady=5)
        
        Entry(main_frame, textvariable=self.var_dob, 
             font=("Arial", 12)).pack(pady=5, ipady=5, ipadx=50)
        
        # View Ticket Button
        Button(main_frame, text="View Hall Ticket", 
              command=self.validate_and_open_ticket,
              font=("Arial", 12), bg="#4CAF50", fg="white",
              padx=20, pady=5).pack(pady=20)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.validate_and_open_ticket())
        
    def validate_and_open_ticket(self):
        """Validate credentials and open hall ticket"""
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
                self.open_hall_ticket(rollno)
            else:
                messagebox.showerror("Error", "Invalid Roll Number or Date of Birth")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            cursor.close()
    
    def open_hall_ticket(self, rollno):
        """Open the hall ticket PDF for the given roll number"""
        try:
            file_path = fr"C:\Users\chinn\OneDrive\Desktop\Automated Attendance\generated_HallTickets\HallTicket_{rollno}.pdf"
            
            if os.path.exists(file_path):
                webbrowser.open(file_path)
                messagebox.showinfo("Success", f"Opening hall ticket for Roll No: {rollno}")
                self.root.destroy()  # Close the window after opening
            else:
                messagebox.showerror("Error", "Hall ticket not found for this student")
                if not hasattr(self, 'var_rollno'):  # If launched with rollno parameter
                    self.create_ui()  # Show the manual entry UI
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open hall ticket: {str(e)}")
            if not hasattr(self, 'var_rollno'):  # If launched with rollno parameter
                self.create_ui()  # Show the manual entry UI

if __name__ == "__main__":
    root = Tk()
    
    # Check if roll number was passed as argument
    rollno = sys.argv[1] if len(sys.argv) > 1 else None
    
    app = HallTicketViewer(root, rollno)
    root.mainloop()