from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
from datetime import datetime

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#121212")  # Dark background
        self.root.state('zoomed')
        
        # Set window to center of screen
        window_width = 1200
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.video_cap = None
        self.course_code = None
        self.course_name = None
        self.year = None
        self.section = None

        # Custom colors
        self.bg_color = "#121212"  # Dark background
        self.card_color = "#1E1E1E"  # Card background
        self.text_color = "#FFFFFF"  # White text
        self.accent_color = "#4A6FA5"  # Blue accent
        self.button_color = "#3A3A3A"  # Button background
        
        # UI Setup
        self.create_ui()
        self.load_years()
        
    def create_ui(self):
        # Main container
        main_frame = Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Title frame
        title_frame = Frame(main_frame, bg=self.accent_color)
        title_frame.pack(fill=X, pady=(0, 20))
        
        Label(title_frame, 
             text="FACE RECOGNITION ATTENDANCE SYSTEM", 
             font=("Helvetica", 20, "bold"), 
             bg=self.accent_color, 
             fg=self.text_color,
             padx=10,
             pady=10
             ).pack()
        
        # Content frame
        content_frame = Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=BOTH, expand=True)
        
        # Left side - Image
        img_frame = Frame(content_frame, bg=self.bg_color)
        img_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        
        try:
            img = Image.open(r"College Images\face_detector_lft.jpg")
            img = img.resize((500, 400), Image.Resampling.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            img_label = Label(img_frame, image=self.photoimg, bg=self.bg_color)
            img_label.pack(pady=10)
        except:
            img_label = Label(img_frame, text="Face Recognition Image", 
                            font=("Helvetica", 12), bg=self.card_color, fg=self.text_color,
                            width=50, height=15)
            img_label.pack(pady=10)
        
        # Right side - Controls
        control_frame = Frame(content_frame, bg=self.card_color, padx=20, pady=20)
        control_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Course selection frame
        course_frame = LabelFrame(control_frame, 
                                text="COURSE DETAILS", 
                                font=("Helvetica", 12, "bold"), 
                                bg=self.card_color, 
                                fg=self.accent_color,
                                padx=10,
                                pady=10)
        course_frame.pack(fill=BOTH, expand=True, pady=10)
        
        # Year selection
        lbl_year = Label(course_frame, 
                        text="Year:", 
                        font=("Helvetica", 12), 
                        bg=self.card_color, 
                        fg=self.text_color)
        lbl_year.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        self.year_var = StringVar()
        self.year_combo = ttk.Combobox(course_frame, 
                                      textvariable=self.year_var, 
                                      font=("Helvetica", 12), 
                                      state="readonly", 
                                      width=18)
        self.year_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.year_combo.bind("<<ComboboxSelected>>", self.load_courses_and_sections)
        
        # Section selection
        lbl_section = Label(course_frame, 
                          text="Section:", 
                          font=("Helvetica", 12), 
                          bg=self.card_color, 
                          fg=self.text_color)
        lbl_section.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        
        self.section_var = StringVar()
        self.section_combo = ttk.Combobox(course_frame, 
                                         textvariable=self.section_var, 
                                         font=("Helvetica", 12), 
                                         state="readonly", 
                                         width=18)
        self.section_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        # Course code selection
        lbl_course_code = Label(course_frame, 
                              text="Course Code:", 
                              font=("Helvetica", 12), 
                              bg=self.card_color, 
                              fg=self.text_color)
        lbl_course_code.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        
        self.course_code_var = StringVar()
        self.course_code_combo = ttk.Combobox(course_frame, 
                                            textvariable=self.course_code_var, 
                                            font=("Helvetica", 12), 
                                            state="readonly", 
                                            width=18)
        self.course_code_combo.grid(row=0, column=3, padx=10, pady=10, sticky=W)
        self.course_code_combo.bind("<<ComboboxSelected>>", self.update_course_name)
        
        # Course name display
        lbl_course_name = Label(course_frame, 
                              text="Course Name:", 
                              font=("Helvetica", 12), 
                              bg=self.card_color, 
                              fg=self.text_color)
        lbl_course_name.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        
        self.course_name_var = StringVar()
        self.course_name_entry = Entry(course_frame, 
                                     textvariable=self.course_name_var, 
                                     font=("Helvetica", 12), 
                                     state="readonly", 
                                     width=20,
                                     bg=self.card_color,
                                     fg=self.text_color,
                                     relief=FLAT)
        self.course_name_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W)
        
        # Start button
        btn_start = Button(course_frame, 
                          text="START RECOGNITION", 
                          command=self.face_recog, 
                          cursor="hand2", 
                          font=("Helvetica", 14, "bold"), 
                          bg=self.accent_color, 
                          fg=self.text_color,
                          activebackground="#3A5F8A",
                          activeforeground=self.text_color,
                          relief=FLAT,
                          padx=20,
                          pady=5)
        btn_start.grid(row=2, column=0, columnspan=4, pady=20, sticky=NSEW)
        
        # Rules/Instructions frame
        rules_frame = LabelFrame(main_frame, 
                               text="INSTRUCTIONS & RULES", 
                               font=("Helvetica", 12, "bold"), 
                               bg=self.card_color, 
                               fg=self.accent_color,
                               padx=10,
                               pady=10)
        rules_frame.pack(fill=BOTH, pady=(10, 0))
        
        rules_text = """
        1. Select your Year, Section, and Course before starting recognition
        2. Ensure proper lighting and face the camera directly
        3. Remove any obstructions (hats, sunglasses) that may hide your face
        4. Attendance will be automatically marked as 'Present' when recognized
        5. Students not recognized will be marked as 'Absent' automatically
        6. Only one attendance record per course per day is allowed
        7. Contact admin for any attendance discrepancies
        """
        
        rules_label = Label(rules_frame, 
                          text=rules_text, 
                          font=("Helvetica", 11), 
                          bg=self.card_color, 
                          fg=self.text_color,
                          justify=LEFT,
                          anchor="w")
        rules_label.pack(fill=BOTH, expand=True)
        
        # Footer
        footer_frame = Frame(main_frame, bg=self.accent_color, height=30)
        footer_frame.pack(fill=X, side=BOTTOM)
        
        footer_label = Label(footer_frame, 
                           text="© 2023 College Attendance System | Developed by Your College", 
                           font=("Helvetica", 10), 
                           bg=self.accent_color, 
                           fg=self.text_color)
        footer_label.pack(pady=5)

    def load_years(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="face_recognition"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT Year FROM student ORDER BY Year")
            years = [str(year[0]) for year in cursor.fetchall()]
            self.year_combo['values'] = years
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load years: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def load_courses_and_sections(self, event=None):
        year = self.year_var.get()
        if not year:
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="face_recognition"
            )
            cursor = conn.cursor()
            
            # Load courses for the selected year
            cursor.execute("SELECT courseCode, courseName FROM course WHERE year=%s", (year,))
            courses = cursor.fetchall()
            self.course_code_combo['values'] = [course[0] for course in courses]
            self.course_details = {code: name for code, name in courses}
            
            # Load sections for the selected year
            cursor.execute("SELECT DISTINCT Section FROM student WHERE Year=%s ORDER BY Section", (year,))
            sections = [section[0] for section in cursor.fetchall()]
            self.section_combo['values'] = sections
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def update_course_name(self, event=None):
        code = self.course_code_var.get()
        if code in self.course_details:
            self.course_name_var.set(self.course_details[code])

    def mark_attendance(self, name, student_id, year, section, department, status="Present"):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="face_recognition"
            )
            cursor = conn.cursor()
    
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%Y-%m-%d")
            course_code = self.course_code_var.get()
            course_name = self.course_name_var.get()
    
            # Check if attendance already marked today for this course
            cursor.execute("""
                SELECT 1 FROM attendance 
                WHERE student_id = %s AND date = %s AND courseCode = %s
                LIMIT 1
            """, (student_id, current_date, course_code))
        
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO attendance 
                    (student_name, student_id, year, section, department, time, date, status, courseCode, courseName)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, student_id, year, section, department, current_time, current_date, status, course_code, course_name))
        
                conn.commit()
                print(f"Attendance marked for {name} (ID: {student_id})")
    
        except Exception as e:
            print(f"Error saving attendance: {e}")
            if 'conn' in locals() and conn.is_connected():
                conn.rollback()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def mark_all_absent(self):
        """Mark all students in the selected year and section as absent for the current course"""
        year = self.year_var.get()
        section = self.section_var.get()
        course_code = self.course_code_var.get()
        course_name = self.course_name_var.get()
        
        if not year or not section or not course_code:
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="vnsvb",
                database="face_recognition"
            )
            cursor = conn.cursor()
            
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Get all students in the selected year and section
            cursor.execute("""
                SELECT StudentID, `Student Name`, Department 
                FROM student 
                WHERE Year=%s AND Section=%s
            """, (year, section))
            
            students = cursor.fetchall()
            
            # Mark each student as absent if not already marked
            for student_id, name, department in students:
                # Check if attendance already exists for today
                cursor.execute("""
                    SELECT 1 FROM attendance 
                    WHERE student_id=%s AND date=%s AND courseCode=%s
                    LIMIT 1
                """, (student_id, current_date, course_code))
                
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO attendance 
                        (student_name, student_id, year, section, department, time, date, status, courseCode, courseName)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (name, student_id, year, section, department, current_time, current_date, "Absent", course_code, course_name))
            
            conn.commit()
            print(f"Marked all unmarked students as absent for {course_code}")
            
        except Exception as e:
            print(f"Error marking absent students: {e}")
            if 'conn' in locals() and conn.is_connected():
                conn.rollback()
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def face_recog(self):
        # Validate selections
        if not self.year_var.get() or not self.section_var.get() or not self.course_code_var.get():
            messagebox.showwarning("Warning", "Please select year, section, and course")
            return
            
        try:
            def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
                coord = []

                for (x, y, w, h) in features:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                    confidence = int((100 * (1 - predict / 300)))

                    conn = mysql.connector.connect(
                        host="localhost", 
                        user="root", 
                        password="vnsvb", 
                        database="face_recognition"
                    )
                    my_cursor = conn.cursor()

                    # Get all student data in one query
                    my_cursor.execute("""
                        SELECT `Student Name`, StudentID, Year, Section, Department 
                        FROM student WHERE StudentID = %s
                    """, (int(id),))
                    
                    student_data = my_cursor.fetchone()
                    
                    # Initialize with default values
                    n = r = a = b = d = "Unknown"
                    
                    if student_data:
                        # Convert all values to strings explicitly
                        n = str(student_data[0]) if student_data[0] is not None else "Unknown"
                        r = str(student_data[1]) if student_data[1] is not None else "Unknown"
                        a = str(student_data[2]) if student_data[2] is not None else "Unknown"
                        b = str(student_data[3]) if student_data[3] is not None else "Unknown"
                        d = str(student_data[4]) if student_data[4] is not None else "Unknown"

                    conn.close()

                    if confidence > 79:
                        # Display information
                        info_lines = [
                            f"ID: {r}",
                            f"Name: {n}",
                            f"Year: {a}",
                            f"Section: {b}",
                            f"Dept: {d}"
                        ]
                        
                        for i, line in enumerate(info_lines):
                            y_pos = y - 75 + (i * 25)
                            cv2.putText(img, line, (x, y_pos), 
                                       cv2.FONT_HERSHEY_COMPLEX, 0.7, 
                                       (255, 255, 255), 2)
                        
                        # Mark attendance with proper values
                        self.mark_attendance(n, r, a, b, d)
                    else:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                        cv2.putText(img, "Unknown Face", (x, y-5), 
                                   cv2.FONT_HERSHEY_COMPLEX, 0.8, 
                                   (255, 255, 255), 3)

                    coord = [x, y, w, h]
                return coord

            def recognize(img, clf, faceCascade):
                coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
                return img

            # Load classifiers
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("classifier.xml")

            # Start video capture
            self.video_cap = cv2.VideoCapture(0)
            if not self.video_cap.isOpened():
                raise Exception("Could not open video device")

            while True:
                ret, img = self.video_cap.read()
                if not ret:
                    break
                img = recognize(img, clf, faceCascade)
                cv2.imshow("Face Recognition", img)
                if cv2.waitKey(1) == 13:  # Enter key to exit
                    break

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # After face recognition is done, mark all unmarked students as absent
            self.mark_all_absent()
            
            if self.video_cap:
                self.video_cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()