from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import os
import sys
import time
from tkinter import filedialog
from datetime import datetime
import webbrowser

class StudentResultViewer:
    def __init__(self, root, student_id=None, student_name=None):
        self.root = root
        self.student_id = student_id
        self.student_name = student_name
        self.root.title("Student Result Viewer")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f5f5")
        self.root.state('zoomed')
        
        # Modern color scheme
        self.colors = {
            "primary": "#3498db",
            "secondary": "#2980b9",
            "accent": "#e74c3c",
            "background": "#f5f5f5",
            "card": "#ffffff",
            "text": "#2c3e50",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "danger": "#e74c3c"
        }
        
        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vnsvb",
            database="face_recognition"
        )
        
        # Initialize filter variables
        self.selected_year = StringVar()
        self.selected_semester = StringVar()
        
        # Get available years and semesters
        self.years = self.get_available_years()
        self.semesters = self.get_available_semesters()
        
        # Set default to latest year and semester
        if self.years:
            self.selected_year.set(self.years[0])  # Latest year first
        if self.semesters:
            self.selected_semester.set(self.semesters[0])  # Latest semester first
        
        # Animation assets
        self.loading_images = []
        self.load_assets()
        
        # UI Setup
        self.setup_ui()
        
        # If student_id provided, show filter options first
        if self.student_id:
            self.show_loading_animation()
            self.root.after(1500, self.show_filter_options)
    
    def get_available_years(self):
        """Get distinct academic years from database for this student"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT DISTINCT academic_year 
                FROM result 
                WHERE studentID = %s
                ORDER BY academic_year DESC
            """, (self.student_id,))
            return [year[0] for year in cursor.fetchall()]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching years: {err}")
            return []
        finally:
            cursor.close()
    
    def get_available_semesters(self):
        """Get distinct semesters from database for this student"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT DISTINCT semester 
                FROM result 
                WHERE studentID = %s
                ORDER BY semester DESC
            """, (self.student_id,))
            return [semester[0] for semester in cursor.fetchall()]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching semesters: {err}")
            return []
        finally:
            cursor.close()
    
    def load_assets(self):
        """Load animation assets"""
        try:
            for i in range(1, 6):
                img = Image.open(f"assets/loading_{i}.png").resize((100, 100))
                self.loading_images.append(ImageTk.PhotoImage(img))
        except:
            pass
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Header
        self.header_frame = Frame(self.root, bg=self.colors["primary"], height=80)
        self.header_frame.pack(fill=X)
        
        # Student info
        self.student_info_frame = Frame(self.header_frame, bg=self.colors["primary"])
        self.student_info_frame.pack(side=LEFT, padx=20)
        
        Label(self.student_info_frame, 
             text=f"{self.student_name or 'Student'} (ID: {self.student_id or 'Not logged in'})",
             font=("Arial", 14, "bold"), 
             bg=self.colors["primary"], fg="white").pack(pady=10)
        
        # Navigation buttons
        self.nav_frame = Frame(self.header_frame, bg=self.colors["primary"])
        self.nav_frame.pack(side=RIGHT, padx=20)
        
        nav_buttons = [
            ("📚 View Results", self.show_filter_options),
            ("⚠️ Backlogs", self.display_backlogs),
            ("📄 Download Report", self.download_report)
        ]
        
        for text, command in nav_buttons:
            btn = Button(self.nav_frame, text=text, command=command,
                        font=("Arial", 10), bg=self.colors["secondary"], fg="white",
                        padx=10, pady=5, bd=0, activebackground=self.colors["primary"])
            btn.pack(side=LEFT, padx=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["accent"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["secondary"]))
        
        # Main content area
        self.content_frame = Frame(self.root, bg=self.colors["background"])
        self.content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Status bar
        self.status_bar = Label(self.root, text="Ready", bd=1, relief=SUNKEN, anchor=W,
                              font=("Arial", 10), bg=self.colors["primary"], fg="white")
        self.status_bar.pack(fill=X, side=BOTTOM)
    
    def show_filter_options(self):
        """Show filter options for year and semester"""
        self.show_loading_animation()
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create filter card
        filter_card = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
        filter_card.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Card header
        header = Frame(filter_card, bg=self.colors["primary"])
        header.pack(fill=X)
        
        Label(header, text="Select Academic Year and Semester", 
             font=("Arial", 14, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
        
        # Filter form
        form_frame = Frame(filter_card, bg=self.colors["card"])
        form_frame.pack(pady=20)
        
        # Year selection
        Label(form_frame, text="Academic Year:", font=("Arial", 12), 
             bg=self.colors["card"], fg=self.colors["text"]).grid(row=0, column=0, padx=10, pady=10, sticky=E)
        
        if not self.years:
            Label(form_frame, text="No academic years found", font=("Arial", 12), 
                 bg=self.colors["card"], fg=self.colors["danger"]).grid(row=0, column=1, sticky=W)
        else:
            year_menu = OptionMenu(form_frame, self.selected_year, *self.years)
            year_menu.config(font=("Arial", 12), width=15)
            year_menu.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        # Semester selection
        Label(form_frame, text="Semester:", font=("Arial", 12), 
             bg=self.colors["card"], fg=self.colors["text"]).grid(row=1, column=0, padx=10, pady=10, sticky=E)
        
        if not self.semesters:
            Label(form_frame, text="No semesters found", font=("Arial", 12), 
                 bg=self.colors["card"], fg=self.colors["danger"]).grid(row=1, column=1, sticky=W)
        else:
            semester_menu = OptionMenu(form_frame, self.selected_semester, *self.semesters)
            semester_menu.config(font=("Arial", 12), width=15)
            semester_menu.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        # View Results button
        if self.years and self.semesters:
            Button(filter_card, text="View Results", command=self.display_filtered_results,
                  font=("Arial", 12, "bold"), bg=self.colors["success"], fg="white",
                  padx=20, pady=5).pack(pady=20)
        
        self.update_status("Select academic year and semester to view results")
    
    def show_loading_animation(self):
        """Show loading animation"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        loading_label = Label(self.content_frame, bg=self.colors["background"])
        loading_label.pack(pady=100)
        
        def update_animation(frame=0):
            if frame < len(self.loading_images):
                loading_label.config(image=self.loading_images[frame])
                self.root.after(200, update_animation, frame+1)
            else:
                loading_label.destroy()
        
        update_animation()
        self.update_status("Loading...")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.update()
    
    def display_filtered_results(self):
        """Display results filtered by selected year and semester"""
        self.show_loading_animation()
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        year = self.selected_year.get()
        semester = self.selected_semester.get()
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT courseCode, marks, fullMarks 
                FROM result 
                WHERE studentID = %s AND academic_year = %s AND semester = %s
                ORDER BY courseCode
            """, (self.student_id, year, semester))
            
            results = cursor.fetchall()
            
            if not results:
                self.show_no_results_message()
                return
            
            # Calculate additional result information
            for result in results:
                percentage = (result['marks'] / result['fullMarks']) * 100
                result['grade'] = self.calculate_grade(percentage)
                result['status'] = 'Pass' if percentage >= 40 else 'Fail'
                result['subject_name'] = self.get_subject_name(result['courseCode'])
            
            # Create results card
            result_card = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
            result_card.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            # Card header
            header = Frame(result_card, bg=self.colors["primary"])
            header.pack(fill=X)
            
            Label(header, text=f"Results for {semester} Semester, {year}", 
                 font=("Arial", 14, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
            
            # Results table
            columns = ("Course Code", "Subject Name", "Marks", "Full Marks", "Grade", "Status")
            tree = ttk.Treeview(result_card, columns=columns, show="headings", height=len(results))
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor=CENTER)
            
            tree.column("Subject Name", width=200, anchor=W)
            
            # Add data to table
            for result in results:
                tree.insert("", "end", values=(
                    result['courseCode'],
                    result['subject_name'],
                    result['marks'],
                    result['fullMarks'],
                    result['grade'],
                    result['status']
                ), tags=(result['status'],))
            
            tree.tag_configure("Pass", foreground=self.colors["success"])
            tree.tag_configure("Fail", foreground=self.colors["danger"])
            tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            # Add summary
            self.add_summary_section(result_card, results)
            
            self.update_status(f"Displaying {len(results)} results for {semester} Semester, {year}")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
    
    def display_backlogs(self):
        """Display only failed subjects across all semesters"""
        self.show_loading_animation()
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT courseCode, marks, fullMarks, academic_year, semester
                FROM result 
                WHERE studentID = %s
                ORDER BY academic_year DESC, semester DESC, courseCode
            """, (self.student_id,))
            
            all_results = cursor.fetchall()
            
            if not all_results:
                self.show_no_results_message()
                return
            
            # Filter and process only failed subjects
            backlogs = []
            for result in all_results:
                percentage = (result['marks'] / result['fullMarks']) * 100
                if percentage < 40:
                    result['grade'] = self.calculate_grade(percentage)
                    result['subject_name'] = self.get_subject_name(result['courseCode'])
                    backlogs.append(result)
            
            if not backlogs:
                no_backlogs_frame = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
                no_backlogs_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
                
                Label(no_backlogs_frame, text="🎉 No Backlogs Found 🎉", 
                     font=("Arial", 18, "bold"), bg=self.colors["card"], 
                     fg=self.colors["success"]).pack(pady=50)
                
                self.update_status("No backlogs found - Good job!")
                return
            
            # Create backlogs card
            backlogs_card = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
            backlogs_card.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            # Card header
            header = Frame(backlogs_card, bg=self.colors["primary"])
            header.pack(fill=X)
            
            Label(header, text=f"Backlog Subjects ({len(backlogs)})", 
                 font=("Arial", 14, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
            
            # Backlogs table
            columns = ("Course Code", "Subject Name", "Marks", "Full Marks", "Grade", "Year", "Semester")
            tree = ttk.Treeview(backlogs_card, columns=columns, show="headings", height=len(backlogs))
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor=CENTER)
            
            tree.column("Subject Name", width=200, anchor=W)
            
            # Add data
            for backlog in backlogs:
                tree.insert("", "end", values=(
                    backlog['courseCode'],
                    backlog['subject_name'],
                    backlog['marks'],
                    backlog['fullMarks'],
                    backlog['grade'],
                    backlog['academic_year'],
                    backlog['semester']
                ), tags=("Fail",))
            
            tree.tag_configure("Fail", foreground=self.colors["danger"])
            tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            self.update_status(f"Found {len(backlogs)} backlog subjects across all semesters")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
    
    def calculate_grade(self, percentage):
        """Calculate grade based on percentage"""
        if percentage >= 90: return 'A+'
        elif percentage >= 80: return 'A'
        elif percentage >= 70: return 'B'
        elif percentage >= 60: return 'C'
        elif percentage >= 50: return 'D'
        elif percentage >= 40: return 'E'
        else: return 'F'
    
    def get_subject_name(self, course_code):
        """Get subject name from course code"""
        # In a real implementation, you might query a subjects table
        # For now, we'll just return a placeholder
        subject_names = {
            "CS101": "Introduction to Programming",
            "MA101": "Discrete Mathematics",
            "PH101": "Physics",
            "CS201": "Data Structures",
            "MA201": "Linear Algebra"
        }
        return subject_names.get(course_code, course_code)
    
    def add_summary_section(self, parent, results):
        """Add summary section to results card"""
        summary_frame = Frame(parent, bg=self.colors["card"])
        summary_frame.pack(fill=X, padx=10, pady=10)
        
        # Calculate summary stats
        total_subjects = len(results)
        passed = sum(1 for r in results if (r['marks']/r['fullMarks'])*100 >= 40)
        failed = total_subjects - passed
        percentage = (passed / total_subjects) * 100 if total_subjects > 0 else 0
        
        # Create summary labels with icons
        summary_data = [
            ("📚 Total Subjects", str(total_subjects), self.colors["primary"]),
            ("✅ Passed", str(passed), self.colors["success"]),
            ("❌ Failed", str(failed), self.colors["danger"]),
            ("📊 Percentage", f"{percentage:.2f}%", self.colors["warning"])
        ]
        
        for i, (label, value, color) in enumerate(summary_data):
            frame = Frame(summary_frame, bg=self.colors["card"])
            frame.grid(row=0, column=i, padx=10, pady=5)
            
            Label(frame, text=label, font=("Arial", 10), 
                 bg=self.colors["card"], fg=self.colors["text"]).pack()
            Label(frame, text=value, font=("Arial", 12, "bold"), 
                 bg=self.colors["card"], fg=color).pack()
    
    def download_report(self):
        """Download result report as PDF"""
        messagebox.showinfo("Download", "Result report will be downloaded as PDF")
        self.update_status("Preparing report for download...")
    
    def show_no_results_message(self):
        """Show message when no results found"""
        no_results_frame = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
        no_results_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(no_results_frame, text="No results found for this student", 
             font=("Arial", 14), bg=self.colors["card"]).pack(pady=50)
        
        self.update_status("No results found")

if __name__ == "__main__":
    root = Tk()
    
    # Check if student_id was passed as argument
    student_id = sys.argv[1] if len(sys.argv) > 1 else None
    student_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    app = StudentResultViewer(root, student_id=student_id, student_name=student_name)
    root.mainloop()