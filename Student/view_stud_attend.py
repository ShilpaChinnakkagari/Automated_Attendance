from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import time
from PIL import Image, ImageTk
import sys

class StudentAttendanceView:
    def __init__(self, root, student_id=None, no_validate=False):
        self.root = root
        self.student_id = student_id
        self.no_validate = no_validate
        self.root.title("Student Attendance Portal")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f5f5")
        self.root.state('zoomed')
        
        # Modern color scheme
        self.colors = {
            "primary": "#4a6fa5",
            "secondary": "#166088",
            "accent": "#4fc3f7",
            "background": "#f5f5f5",
            "card": "#ffffff",
            "text": "#333333",
            "light_bg": "#f0f8ff"
        }
        
        # Load animation assets
        self.load_assets()
        
        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vnsvb",
            database="face_recognition"
        )

        self.student_name = None

        if self.student_id and self.no_validate:
            # Directly show dashboard if student_id provided and no validation requested
            self.student_name = self.get_student_name()
            self.show_attendance_dashboard()
        elif self.student_id:
            # Validate student if only student_id provided
            self.validate_student_direct()
        else:
            # Show login screen if no student_id provided
            self.create_login_ui()

    def validate_student_direct(self):
        """Validate student directly without UI"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT StudentID, `Student Name` 
                FROM student 
                WHERE StudentID = %s
            """, (self.student_id,))
            
            student = cursor.fetchone()
            
            if student:
                self.student_id = student['StudentID']
                self.student_name = student['Student Name']
                self.show_attendance_dashboard()
            else:
                messagebox.showerror("Error", "Student not found")
                self.root.destroy()
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
            self.root.destroy()
        finally:
            cursor.close()

    def load_assets(self):
        # Load animation images (replace with your own paths)
        try:
            self.login_bg = ImageTk.PhotoImage(Image.open("assets/login_bg.jpg").resize((1200, 700), Image.Resampling.LANCZOS))
            self.dashboard_bg = ImageTk.PhotoImage(Image.open("assets/dashboard_bg.jpg").resize((1200, 700), Image.Resampling.LANCZOS))
        except:
            self.login_bg = None
            self.dashboard_bg = None

    def get_student_name(self):
        """Get student name from database"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT `Student Name` FROM student WHERE StudentID = %s", (self.student_id,))
            result = cursor.fetchone()
            return result['Student Name'] if result else "Student"
        except Exception as e:
            print(f"Error fetching student name: {e}")
            return "Student"
        finally:
            cursor.close()

    def show_attendance_dashboard(self):
        """Show attendance dashboard with all animations and circles"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Background - using solid color instead of transparent
        bg_color = self.colors["light_bg"] if not self.dashboard_bg else None
        bg_frame = Frame(self.root, bg=bg_color)
        bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # If we have a background image, use it
        if self.dashboard_bg:
            bg_label = Label(bg_frame, image=self.dashboard_bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Header Frame
        header_frame = Frame(bg_frame, bg=self.colors["primary"], bd=0)
        header_frame.pack(fill=X, pady=10)
        
        # Centered header content
        header_content = Frame(header_frame, bg=self.colors["primary"])
        header_content.pack(expand=True)
        
        # Customize header text based on student name
        if self.student_name.lower() == "rashmika":
            header_text = f"{self.student_name} Dashboard"
        else:
            header_text = f"{self.student_name} Dashboard"
            
        Label(header_content, text=header_text, 
              font=("Arial", 18, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
        
        # Main content frame
        main_frame = Frame(bg_frame, bg=self.colors["background"])
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Overall Attendance Card with circle animation
        self.create_overall_attendance_card(main_frame)
        
        # Subject-wise Attendance Card
        self.create_subject_attendance_card(main_frame)

    def create_overall_attendance_card(self, parent):
        """Create the overall attendance card with circle animation"""
        overall_card = Frame(parent, bg=self.colors["card"], bd=0)
        overall_card.pack(fill=X, pady=10)
        self.round_corners(overall_card)
        
        # Card header
        card_header = Frame(overall_card, bg=self.colors["primary"])
        card_header.pack(fill=X)
        
        title_frame = Frame(card_header, bg=self.colors["primary"])
        title_frame.pack(expand=True)
        
        Label(title_frame, text="Overall Attendance Summary", 
              font=("Arial", 14, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN status = 'Present' THEN 1 END) as present,
                    COUNT(CASE WHEN status = 'Absent' THEN 1 END) as absent,
                    COUNT(*) as total
                FROM attendance 
                WHERE student_id = %s
            """, (self.student_id,))
            
            overall = cursor.fetchone()
            
            if overall['total'] > 0:
                percentage = (overall['present'] / overall['total']) * 100
            else:
                percentage = 0
                
            # Create progress frame with circle animation
            progress_frame = Frame(overall_card, bg=self.colors["card"])
            progress_frame.pack(side=LEFT, padx=30, pady=20)
            
            canvas = Canvas(progress_frame, width=150, height=150, bg=self.colors["card"], highlightthickness=0)
            canvas.pack()
            
            # Animate the circle
            self.animate_circle(canvas, percentage)
            
            # Display stats
            stats_frame = Frame(overall_card, bg=self.colors["card"])
            stats_frame.pack(side=LEFT, padx=20, pady=20, fill=BOTH, expand=True)
            
            stats = [
                ("Total Classes", f"{overall['total']}", "#4a6fa5"),
                ("Present", f"{overall['present']}", "#4CAF50"),
                ("Absent", f"{overall['absent']}", "#F44336")
            ]
            
            for i, (label, value, color) in enumerate(stats):
                frame = Frame(stats_frame, bg=self.colors["card"])
                frame.pack(fill=X, pady=5)
                
                Label(frame, text=label, font=("Arial", 12), 
                      bg=self.colors["card"], fg=self.colors["text"]).pack(side=LEFT, anchor=W)
                
                Label(frame, text=value, font=("Arial", 12, "bold"), 
                      bg=self.colors["card"], fg=color).pack(side=RIGHT, anchor=E)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch overall attendance: {str(e)}")
        finally:
            cursor.close()

    def animate_circle(self, canvas, percentage):
        """Animate the percentage circle"""
        center_x, center_y = 75, 75
        radius = 65
        start_angle = 90
        extent = -360 * (percentage / 100)
        
        # Draw background circle
        canvas.create_oval(center_x-radius, center_y-radius, 
                          center_x+radius, center_y+radius,
                          outline="#e0e0e0", width=5)
        
        # Animate the progress arc
        for i in range(0, int(abs(extent)), 5):
            current_extent = -i if extent < 0 else i
            canvas.delete("progress")
            canvas.create_arc(center_x-radius, center_y-radius,
                            center_x+radius, center_y+radius,
                            start=start_angle, extent=current_extent,
                            outline=self.colors["accent"], width=5,
                            style="arc", tags="progress")
            canvas.update()
            time.sleep(0.02)
        
        # Draw final circle and percentage text
        canvas.delete("progress")
        canvas.create_arc(center_x-radius, center_y-radius,
                        center_x+radius, center_y+radius,
                        start=start_angle, extent=extent,
                        outline=self.colors["accent"], width=5,
                        style="arc")
        canvas.create_text(center_x, center_y, text=f"{percentage:.1f}%", 
                         font=("Arial", 20, "bold"), fill=self.colors["primary"])

    def create_subject_attendance_card(self, parent):
        """Create the subject-wise attendance card"""
        subject_card = Frame(parent, bg=self.colors["card"], bd=0)
        subject_card.pack(fill=BOTH, expand=True, pady=10)
        self.round_corners(subject_card)
        
        # Card header
        card_header = Frame(subject_card, bg=self.colors["primary"])
        card_header.pack(fill=X)
        
        title_frame = Frame(card_header, bg=self.colors["primary"])
        title_frame.pack(expand=True)
        
        Label(title_frame, text="Subject-wise Attendance", 
              font=("Arial", 14, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
        
        # Create table
        columns = ("subject_code", "subject_name", "present", "absent", "total", "percentage")
        self.subject_table = ttk.Treeview(
            subject_card,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )
        
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       background=self.colors["card"], 
                       fieldbackground=self.colors["card"],
                       foreground=self.colors["text"],
                       rowheight=30,
                       font=("Arial", 11))
        
        style.configure("Custom.Treeview.Heading", 
                       background=self.colors["primary"],
                       foreground="white",
                       font=("Arial", 12, "bold"))
        
        style.map("Custom.Treeview", 
                 background=[('selected', self.colors["accent"])],
                 foreground=[('selected', 'white')])
        
        # Define headings
        self.subject_table.heading("subject_code", text="Subject Code")
        self.subject_table.heading("subject_name", text="Subject Name")
        self.subject_table.heading("present", text="Present")
        self.subject_table.heading("absent", text="Absent")
        self.subject_table.heading("total", text="Total")
        self.subject_table.heading("percentage", text="Percentage")
        
        # Set column widths
        self.subject_table.column("subject_code", width=120, anchor=CENTER)
        self.subject_table.column("subject_name", width=250, anchor=W)
        self.subject_table.column("present", width=80, anchor=CENTER)
        self.subject_table.column("absent", width=80, anchor=CENTER)
        self.subject_table.column("total", width=80, anchor=CENTER)
        self.subject_table.column("percentage", width=100, anchor=CENTER)
        
        self.subject_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Add scrollbar
        scroll_y = Scrollbar(subject_card, orient="vertical", command=self.subject_table.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.subject_table.configure(yscrollcommand=scroll_y.set)

        # Load data
        self.load_subject_attendance()

    def load_subject_attendance(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT DISTINCT a.courseCode, c.courseName
                FROM attendance a
                JOIN course c ON a.courseCode = c.courseCode
                WHERE a.student_id = %s
                ORDER BY a.courseCode
            """, (self.student_id,))
            
            subjects = cursor.fetchall()
            
            self.subject_table.delete(*self.subject_table.get_children())
            
            for subject in subjects:
                cursor.execute("""
                    SELECT 
                        COUNT(CASE WHEN status = 'Present' THEN 1 END) as present,
                        COUNT(CASE WHEN status = 'Absent' THEN 1 END) as absent,
                        COUNT(*) as total
                    FROM attendance 
                    WHERE student_id = %s AND courseCode = %s
                """, (self.student_id, subject['courseCode']))
                
                stats = cursor.fetchone()
                percentage = (stats['present'] / stats['total']) * 100 if stats['total'] > 0 else 0
                
                tags = ("good",) if percentage >= 75 else ("average",) if percentage >= 50 else ("poor",)
                
                self.subject_table.insert("", END, values=(
                    subject['courseCode'],
                    subject['courseName'],
                    stats['present'],
                    stats['absent'],
                    stats['total'],
                    f"{percentage:.2f}%"
                ), tags=tags)
            
            self.subject_table.tag_configure("good", background="#e8f5e9")
            self.subject_table.tag_configure("average", background="#fff8e1")
            self.subject_table.tag_configure("poor", background="#ffebee")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch subject attendance: {str(e)}")
        finally:
            cursor.close()

    def round_corners(self, widget, radius=10):
        widget.configure(highlightbackground=self.colors["card"])
        widget.configure(highlightcolor=self.colors["card"])
        widget.configure(bd=0)
        widget.configure(relief="solid")
        widget.configure(highlightthickness=0)
        widget.configure(bg=self.colors["card"])

    # Removed create_login_ui and validate_student methods since we don't need them anymore

if __name__ == "__main__":
    root = Tk()
    
    # Check command line arguments
    student_id = None
    no_validate = False
    
    for arg in sys.argv[1:]:
        if arg == "--no-validate":
            no_validate = True
        else:
            student_id = arg
    
    obj = StudentAttendanceView(root, student_id=student_id, no_validate=no_validate)
    root.mainloop()