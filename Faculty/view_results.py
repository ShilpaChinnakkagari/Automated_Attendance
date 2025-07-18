from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import filedialog

class ViewResults:
    def __init__(self, root, department=None):
        self.root = root
        self.department = department
        self.root.title("Student Results Viewer")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f5f5")
        
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
        
        # Filter variables
        self.selected_year = StringVar()
        self.selected_semester = StringVar()
        self.search_text = StringVar()
        self.search_by = StringVar(value="studentID")
        
        # UI Setup
        self.setup_ui()
        
        # Load initial data
        self.show_filter_options()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Header
        self.header_frame = Frame(self.root, bg=self.colors["primary"], height=80)
        self.header_frame.pack(fill=X)
        
        Label(self.header_frame, 
             text=f"{self.department} Department - Results Viewer",
             font=("Arial", 16, "bold"), 
             bg=self.colors["primary"], fg="white").pack(side=LEFT, padx=20)
        
        # Navigation buttons
        self.nav_frame = Frame(self.header_frame, bg=self.colors["primary"])
        self.nav_frame.pack(side=RIGHT, padx=20)
        
        nav_buttons = [
            ("🔍 Search Results", self.show_filter_options),
            ("📊 View All Results", self.display_all_results),
            ("⚠️ View Backlogs", self.display_backlogs)
        ]
        
        for text, command in nav_buttons:
            btn = Button(self.nav_frame, text=text, command=command,
                        font=("Arial", 10), bg=self.colors["secondary"], fg="white",
                        padx=10, pady=5, bd=0)
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
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.update()
    
    def show_filter_options(self):
        """Show filter options for results"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create filter card
        filter_card = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
        filter_card.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Card header
        header = Frame(filter_card, bg=self.colors["primary"])
        header.pack(fill=X)
        
        Label(header, text="Filter Results", 
             font=("Arial", 14, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
        
        # Filter form
        form_frame = Frame(filter_card, bg=self.colors["card"])
        form_frame.pack(pady=20)
        
        # Get available years and semesters
        years = self.get_available_years()
        semesters = self.get_available_semesters()
        
        # Search criteria
        Label(form_frame, text="Search By:", font=("Arial", 12), 
             bg=self.colors["card"], fg=self.colors["text"]).grid(row=0, column=0, padx=10, pady=10, sticky=E)
        
        search_combo = ttk.Combobox(form_frame, textvariable=self.search_by, 
                                  values=["studentID", "studentName", "courseCode"], 
                                  font=("Arial", 12), state="readonly")
        search_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        Label(form_frame, text="Search Text:", font=("Arial", 12), 
             bg=self.colors["card"], fg=self.colors["text"]).grid(row=1, column=0, padx=10, pady=10, sticky=E)
        
        Entry(form_frame, textvariable=self.search_text, font=("Arial", 12), 
             bd=1, relief=GROOVE).grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        # Year selection
        Label(form_frame, text="Academic Year:", font=("Arial", 12), 
             bg=self.colors["card"], fg=self.colors["text"]).grid(row=2, column=0, padx=10, pady=10, sticky=E)
        
        if years:
            year_combo = ttk.Combobox(form_frame, textvariable=self.selected_year, 
                                     values=years, font=("Arial", 12), state="readonly")
            year_combo.current(0)
            year_combo.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        else:
            Label(form_frame, text="No years available", font=("Arial", 12), 
                 bg=self.colors["card"], fg=self.colors["danger"]).grid(row=2, column=1, sticky=W)
        
        # Semester selection
        Label(form_frame, text="Semester:", font=("Arial", 12), 
             bg=self.colors["card"], fg=self.colors["text"]).grid(row=3, column=0, padx=10, pady=10, sticky=E)
        
        if semesters:
            semester_combo = ttk.Combobox(form_frame, textvariable=self.selected_semester, 
                                        values=semesters, font=("Arial", 12), state="readonly")
            semester_combo.current(0)
            semester_combo.grid(row=3, column=1, padx=10, pady=10, sticky=W)
        else:
            Label(form_frame, text="No semesters available", font=("Arial", 12), 
                 bg=self.colors["card"], fg=self.colors["danger"]).grid(row=3, column=1, sticky=W)
        
        # Search button
        search_btn = Button(filter_card, text="Search Results", command=self.display_filtered_results,
                          font=("Arial", 12, "bold"), bg=self.colors["success"], fg="white",
                          padx=20, pady=10)
        search_btn.pack(pady=20)
        
        self.update_status("Select filters and click Search")
    
    def get_available_years(self):
        """Get distinct academic years from database"""
        try:
            cursor = self.conn.cursor()
            query = "SELECT DISTINCT academic_year FROM result WHERE department=%s ORDER BY academic_year DESC"
            cursor.execute(query, (self.department,))
            return [year[0] for year in cursor.fetchall()]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching years: {err}")
            return []
        finally:
            cursor.close()
    
    def get_available_semesters(self):
        """Get distinct semesters from database"""
        try:
            cursor = self.conn.cursor()
            query = "SELECT DISTINCT semester FROM result WHERE department=%s ORDER BY semester DESC"
            cursor.execute(query, (self.department,))
            return [semester[0] for semester in cursor.fetchall()]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching semesters: {err}")
            return []
        finally:
            cursor.close()
    
    def display_filtered_results(self):
        """Display results based on selected filters"""
        year = self.selected_year.get()
        semester = self.selected_semester.get()
        search_by = self.search_by.get()
        search_text = self.search_text.get()
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # Build query with filters
            query = """
                SELECT studentID, studentName, courseCode, marks, fullMarks, grade, academic_year, semester 
                FROM result 
                WHERE department=%s
            """
            params = [self.department]
            
            # Add filters
            if year:
                query += " AND academic_year=%s"
                params.append(year)
            
            if semester:
                query += " AND semester=%s"
                params.append(semester)
            
            if search_text:
                query += f" AND {search_by} LIKE %s"
                params.append(f"%{search_text}%")
            
            query += " ORDER BY studentID, courseCode"
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            
            if not results:
                self.show_no_results_message()
                return
            
            self.display_results_table(results, f"Filtered Results: {year} {semester}")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
    
    def display_all_results(self):
        """Display all results for the department"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT studentID, studentName, courseCode, marks, fullMarks, grade, academic_year, semester 
                FROM result 
                WHERE department=%s
                ORDER BY academic_year DESC, semester DESC, studentID
            """, (self.department,))
            
            results = cursor.fetchall()
            
            if not results:
                self.show_no_results_message()
                return
            
            self.display_results_table(results, "All Results")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
    
    def display_backlogs(self):
        """Display only failed subjects"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT studentID, studentName, courseCode, marks, fullMarks, grade, academic_year, semester 
                FROM result 
                WHERE department=%s AND grade='F'
                ORDER BY academic_year DESC, semester DESC, studentID
            """, (self.department,))
            
            results = cursor.fetchall()
            
            if not results:
                no_backlogs_frame = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
                no_backlogs_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
                
                Label(no_backlogs_frame, text="🎉 No Backlogs Found 🎉", 
                     font=("Arial", 18, "bold"), bg=self.colors["card"], 
                     fg=self.colors["success"]).pack(pady=50)
                
                self.update_status("No backlogs found - Good job!")
                return
            
            self.display_results_table(results, "Backlog Subjects")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
    
    def display_results_table(self, results, title):
        """Display results in a table"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create results card
        result_card = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
        result_card.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Card header
        header = Frame(result_card, bg=self.colors["primary"])
        header.pack(fill=X)
        
        Label(header, text=title, 
             font=("Arial", 14, "bold"), bg=self.colors["primary"], fg="white").pack(pady=10)
        
        # Results table with scrollbar
        table_frame = Frame(result_card, bg=self.colors["card"])
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scroll_y = Scrollbar(table_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        columns = ("studentID", "studentName", "courseCode", "marks", "fullMarks", "percentage", "grade", "year", "semester")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Configure columns
        self.results_tree.heading("studentID", text="Student ID")
        self.results_tree.heading("studentName", text="Student Name")
        self.results_tree.heading("courseCode", text="Course Code")
        self.results_tree.heading("marks", text="Marks")
        self.results_tree.heading("fullMarks", text="Full Marks")
        self.results_tree.heading("percentage", text="Percentage")
        self.results_tree.heading("grade", text="Grade")
        self.results_tree.heading("year", text="Academic Year")
        self.results_tree.heading("semester", text="Semester")
        
        self.results_tree.column("studentID", width=100)
        self.results_tree.column("studentName", width=150)
        self.results_tree.column("courseCode", width=100)
        self.results_tree.column("marks", width=80)
        self.results_tree.column("fullMarks", width=80)
        self.results_tree.column("percentage", width=80)
        self.results_tree.column("grade", width=60)
        self.results_tree.column("year", width=100)
        self.results_tree.column("semester", width=80)
        
        scroll_y.config(command=self.results_tree.yview)
        scroll_x.config(command=self.results_tree.xview)
        
        # Add data
        for result in results:
            percentage = (result['marks'] / result['fullMarks']) * 100
            self.results_tree.insert("", "end", values=(
                result['studentID'],
                result['studentName'],
                result['courseCode'],
                result['marks'],
                result['fullMarks'],
                f"{percentage:.2f}%",
                result['grade'],
                result['academic_year'],
                result['semester']
            ), tags=(result['grade'],))
        
        self.results_tree.tag_configure("F", foreground=self.colors["danger"])
        self.results_tree.pack(fill=BOTH, expand=True)
        
        # Add summary section
        self.add_summary_section(result_card, results)
        
        # Add export button
        export_btn = Button(result_card, text="📄 Export to CSV", command=self.export_to_csv,
                          font=("Arial", 10), bg=self.colors["secondary"], fg="white")
        export_btn.pack(side=RIGHT, padx=10, pady=10)
        
        self.update_status(f"Displaying {len(results)} records")
    
    def add_summary_section(self, parent, results):
        """Add summary statistics section"""
        summary_frame = Frame(parent, bg=self.colors["card"])
        summary_frame.pack(fill=X, padx=10, pady=10)
        
        # Calculate statistics
        total_students = len({r['studentID'] for r in results})
        total_courses = len(results)
        passed = sum(1 for r in results if r['grade'] != 'F')
        failed = total_courses - passed
        pass_percentage = (passed / total_courses) * 100 if total_courses > 0 else 0
        
        # Summary cards with icons
        stats = [
            ("👥 Total Students", total_students, self.colors["primary"]),
            ("📚 Total Courses", total_courses, self.colors["secondary"]),
            ("✅ Passed", passed, self.colors["success"]),
            ("❌ Failed", failed, self.colors["danger"]),
            ("📊 Pass Percentage", f"{pass_percentage:.2f}%", self.colors["warning"])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = Frame(summary_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
            stat_frame.grid(row=0, column=i, padx=5, pady=5)
            
            Label(stat_frame, text=label, font=("Arial", 10), 
                 bg=self.colors["card"], fg=self.colors["text"]).pack(pady=5)
            Label(stat_frame, text=str(value), font=("Arial", 12, "bold"), 
                 bg=self.colors["card"], fg=color).pack(pady=5)
    
    def export_to_csv(self):
        """Export results to CSV file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                title="Save Results As"
            )
            
            if not file_path:
                return
                
            with open(file_path, 'w') as f:
                # Write header
                f.write("Student ID,Student Name,Course Code,Marks,Full Marks,Percentage,Grade,Academic Year,Semester\n")
                
                # Write data
                for item in self.results_tree.get_children():
                    values = self.results_tree.item(item)['values']
                    f.write(','.join(str(v) for v in values) + '\n')
            
            messagebox.showinfo("Success", f"Results exported to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")
    
    def show_no_results_message(self):
        """Show message when no results found"""
        no_results_frame = Frame(self.content_frame, bg=self.colors["card"], bd=1, relief=GROOVE)
        no_results_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(no_results_frame, text="No results found for the selected criteria", 
             font=("Arial", 14), bg=self.colors["card"]).pack(pady=50)
        
        self.update_status("No results found")

if __name__ == "__main__":
    root = Tk()
    # For testing, pass a department - in actual use, this comes from login
    app = ViewResults(root, department="CAI")
    root.mainloop()