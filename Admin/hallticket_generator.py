from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from fpdf import FPDF
import os 
import webbrowser  # at the top of your file if not already

class Result:
    def __init__(self, root):
        self.root = root
        self.root.title("Hall Ticket Generation")
        self.root.geometry("1530x780+0+0")
        self.root.config(bg="white")
        self.root.state('zoomed')

        self.search = StringVar()
        self.student_id = StringVar()
        self.exam_month = StringVar()


        # Title
        title = Label(self.root, text="Print Hall Ticket", 
                      font=("lucida", 20, "bold", "italic"), bg="orange", fg="black")
        title.pack(side=TOP, fill=X)

        # Search Section
        lbl_search = Label(self.root, text="Search Department:", 
                           font=("times new roman", 14, "bold"), bg="white").place(x=50, y=60)
        text_search = Entry(self.root, textvariable=self.search, font=("times new roman", 14), bg="lightyellow").place(x=220, y=60, width=200)


        student_id_label = Label(self.root,text="Student ID : ",font=("times new roman",15,"bold"),bg="white")
        student_id_label.place(x=50,y=100)
    

        student_id_entry=Entry(self.root, textvariable=self.student_id,width=25,font=("times new roman",12,"bold"), bg="lightyellow")
        student_id_entry.place(x=220,y=100)

        
        btn_search = Button(self.root, text="Search", command=self.search_both,
                            font=("times new roman", 12, "bold"), bg="skyblue", fg="white", cursor="hand2").place(x=470, y=80, width=100, height=30)
        btn_reset = Button(self.root, text="Reset", command=self.reset_fields, 
                           font=("times new roman", 12, "bold"), bg="red", fg="white", cursor="hand2").place(x=570, y=80, width=100, height=30)
        

        btn_generate = Button(self.root, text="Generate Hall Ticket", command=self.generate_hall_ticket,
                      font=("times new roman", 12, "bold"), bg="green", fg="white", cursor="hand2")
        btn_generate.place(x=400, y=670, width=180, height=30)

        exam_label = Label(self.root, text="Exam Month:", font=("times new roman", 14, "bold"), bg="white")
        exam_label.place(x=50, y=140)

        exam_entry = Entry(self.root, textvariable=self.exam_month, font=("times new roman", 14), bg="lightyellow")
        exam_entry.place(x=220, y=140, width=200)



        # Table Frame
        frame1 = Frame(self.root, bd=2, relief=RIDGE)
        frame1.place(x=50, y=360, width=900, height=300)

        # Scrollbars
        scroll_x1 = Scrollbar(frame1, orient=HORIZONTAL)
        scroll_y1 = Scrollbar(frame1, orient=VERTICAL)

        # Table
        self.course_table = ttk.Treeview(frame1, columns=("courseCode","courseName"),
                                         xscrollcommand=scroll_x1.set, yscrollcommand=scroll_y1.set)

        scroll_x1.pack(side=BOTTOM, fill=X)
        scroll_y1.pack(side=RIGHT, fill=Y)
        scroll_x1.config(command=self.course_table.xview)
        scroll_y1.config(command=self.course_table.yview)

        self.course_table.heading("courseCode", text="courseCode")
        self.course_table.heading("courseName", text="courseName")
        

        self.course_table["show"] = "headings"

        self.course_table.column("courseCode", width=160)
        self.course_table.column("courseName", width=160)
        
        self.course_table.pack(fill=BOTH, expand=1)


        #Table -2
        # Table Frame
        frame2 = Frame(self.root, bd=2, relief=RIDGE)
        frame2.place(x=50, y=180, width=900, height=150)

        # Scrollbars
        scroll_x2 = Scrollbar(frame2, orient=HORIZONTAL)
        scroll_y2 = Scrollbar(frame2, orient=VERTICAL)

        # Table
        self.student_table = ttk.Treeview(frame2, columns=("studentID","Student Name"),
                                         xscrollcommand=scroll_x2.set, yscrollcommand=scroll_y2.set)

        scroll_x2.pack(side=BOTTOM, fill=X)
        scroll_y2.pack(side=RIGHT, fill=Y)
        scroll_x2.config(command=self.student_table.xview)
        scroll_y2.config(command=self.student_table.yview)

        self.student_table.heading("studentID", text="studentID")
        self.student_table.heading("Student Name", text="Student Name")
        

        self.student_table["show"] = "headings"

        self.student_table.column("studentID", width=90)
        self.student_table.column("Student Name", width=90)
        
        self.student_table.pack(fill=BOTH, expand=1)


        # Frame for Generated PDFs (Left side)
        frame_generated = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame_generated.place(x=1000, y=160, width=450, height=440)

        title2 = Label(frame_generated, text="Generated Hall Tickets",
               font=("times new roman", 15, "bold"), bg="white", fg="black")
        title2.pack(side=TOP, fill=X)

        # Scrollbars
        scroll_x = Scrollbar(frame_generated, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame_generated, orient=VERTICAL)

        self.generated_table = ttk.Treeview(frame_generated, columns=("studentID", "view"),
                                    xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.generated_table.xview)
        scroll_y.config(command=self.generated_table.yview)

        self.generated_table.heading("studentID", text="Student ID")
        self.generated_table.heading("view", text="Hall Ticket")

        self.generated_table["show"] = "headings"
        self.generated_table.column("studentID", width=100)
        self.generated_table.column("view", width=250)

        self.generated_table.pack(fill=BOTH, expand=1)

        # Bind click to open PDF
        self.generated_table.bind("<ButtonRelease-1>", self.open_selected_pdf)
        


    def search_name(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        try:
            department = self.search.get().strip()
            if not department:
                messagebox.showerror("Error", "Please enter Department")
                return

            # Fetch student results for all subjects
            query = "SELECT courseCode, courseName FROM course WHERE department = %s"
            my_cursor.execute(query, (department,))
            rows = my_cursor.fetchall()

            if rows:
                self.course_table.delete(*self.course_table.get_children())  # Clear previous records
                

                for row in rows:
                    courseCode, courseName = row
                    
                    self.course_table.insert("", "end", values=(courseCode, courseName))

                    

                
            else:
                messagebox.showinfo("Result", "No student records found!")
                self.reset_fields()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        finally:
            conn.close()

    
    def search_id_(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        try:
            studentID = self.student_id.get().strip()
            if not studentID:
                messagebox.showerror("Error", "Please enter Department")
                return

            # Fetch student results for all subjects
            query = "SELECT studentID, `Student Name` FROM student WHERE studentID = %s"
            my_cursor.execute(query, (studentID,))
            rows = my_cursor.fetchall()

            if rows:
                self.student_table.delete(*self.student_table.get_children())  # Clear previous records
                

                for row in rows:
                    studentID, studentName = row
                    
                    self.student_table.insert("", "end", values=(studentID, studentName))

                    

                
            else:
                messagebox.showinfo("Result", "No student records found!")
                self.reset_fields()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        finally:
            conn.close()


    def reset_fields(self):
        self.search.set("")
        self.course_table.delete(*self.course_table.get_children())  # Clear table
        self.student_table.delete(*self.student_table.get_children())  # Clear table

    def search_both(self):
        self.search_name()
        self.search_id_()


    def generate_hall_ticket(self):
        try:
            student_items = self.student_table.get_children()
            if not student_items:
                messagebox.showerror("Error", "No student data to generate hall ticket.")
                return

            student_data = self.student_table.item(student_items[0])['values']
            studentID, studentName = student_data

            course_items = self.course_table.get_children()
            if not course_items:
                messagebox.showerror("Error", "No course data to generate hall ticket.")
                return

            folder_path = "generated_HallTickets"
            os.makedirs(folder_path, exist_ok=True)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # College heading image (replaces logo + text)
            clg_heading_path = "C:/Users/chinn/OneDrive/Desktop/Automated Attendance/College Images/clg_name.jpg"
            pdf.image(clg_heading_path, x=10, y=10, w=190)

            self.var = self.exam_month.get() + " Examinations"
            pdf.set_xy(10, 50)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10,self.var , ln=True, align='C')
            pdf.ln(5)

            pdf.ln(50)

            # Student Photo Placeholder (right side)
            pdf.set_font("Arial", "", 10)
            pdf.set_xy(150, 60)
            pdf.cell(40, 40, "Paste\nPassport\nPhoto", border=1, align='C')

             # Student Info (left side)
            pdf.set_xy(10, 65)
            pdf.set_font("Arial", "", 12)
            pdf.cell(100, 10, f"Student ID   : {studentID}", ln=True)
            pdf.set_x(10)
            pdf.cell(100, 10, f"Student Name : {studentName}", ln=True)

            pdf.ln(20)

            # Course Table
            pdf.set_font("Arial", "B", 12)
            pdf.cell(50, 10, "Course Code", 1, 0, 'C')
            pdf.cell(100, 10, "Course Name", 1, 1, 'C')

            pdf.set_font("Arial", "", 12)
            for item in course_items:
                courseCode, courseName = self.course_table.item(item)['values']
                pdf.cell(50, 10, str(courseCode), 1, 0, 'C')
                pdf.cell(100, 10, str(courseName), 1, 1, 'C')

            pdf.ln(15)

            # Student Signature
            pdf.set_font("Arial", "", 12)
            pdf.cell(100, 10, "Student Signature:", ln=False, align='L')
            pdf.line(45, pdf.get_y() + 8, 100, pdf.get_y() + 8)

            # HOD Signature with image
            sign_path = "C:/Users/chinn/OneDrive/Desktop/Automated Attendance/College Images/sign.jpg"
            pdf.image(sign_path, x=160, y=pdf.get_y()+10, w=40)
            pdf.set_xy(150, pdf.get_y() + 22)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Head of Department", ln=True, align='R')

            # Save File
            filename = os.path.join(folder_path, f"HallTicket_{studentID}.pdf")
            pdf.output(filename)
            messagebox.showinfo("Success", f"Hall Ticket saved in '{folder_path}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate hall ticket.\n{e}")


    

    def open_selected_pdf(self, event):
        region = self.generated_table.identify("region", event.x, event.y)
        column = self.generated_table.identify_column(event.x)

        if region != "cell" or column != "#2":  # "#2" refers to the second column = 'view'
            return  # Do nothing if not clicking in 'Hall Ticket' column

        selected_item = self.generated_table.focus()
        if not selected_item:
            return

        values = self.generated_table.item(selected_item, 'values')
        if len(values) != 2:
            return

        filename = values[1]
        filepath = os.path.join("generated_HallTickets", filename)
        if os.path.exists(filepath):
            webbrowser.open_new(filepath)
        else:
            messagebox.showerror("Error", f"File not found: {filename}")


    def load_generated_pdfs(self):
        self.generated_table.delete(*self.generated_table.get_children())  # Clear old entries
        folder_path = "generated_HallTickets"
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf") and filename.startswith("HallTicket_"):
                    student_id = filename.split("_")[1].split(".")[0]
                    self.generated_table.insert("", "end", values=(student_id, filename))



if __name__ == "__main__":
    root = Tk()
    obj = Result(root)
    obj.load_generated_pdfs()

    root.mainloop()
    