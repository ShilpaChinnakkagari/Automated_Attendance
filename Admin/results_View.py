from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

class Report:
    def __init__(self, root):
        self.root = root
        self.root.title("View Student Results")
        self.root.geometry("1000x500+100+100")
        self.root.config(bg="white")
        self.root.state('zoomed')

        self.search = StringVar()

        # Title
        title = Label(self.root, text="View Student Results", 
                      font=("lucida", 20, "bold", "italic"), bg="orange", fg="black")
        title.pack(side=TOP, fill=X)

        # Search Section
        lbl_search = Label(self.root, text="Search by Roll No:", 
                           font=("times new roman", 14, "bold"), bg="white").place(x=50, y=60)
        text_search = Entry(self.root, textvariable=self.search, font=("times new roman", 14), bg="lightyellow").place(x=200, y=60, width=200)
        
        btn_search = Button(self.root, text="Search", command=self.search_name,
                            font=("times new roman", 12, "bold"), bg="skyblue", fg="white", cursor="hand2").place(x=440, y=60, width=100, height=30)
        btn_reset = Button(self.root, text="Reset", command=self.reset_fields, 
                           font=("times new roman", 12, "bold"), bg="red", fg="white", cursor="hand2").place(x=540, y=60, width=100, height=30)

        # Table Frame
        frame = Frame(self.root, bd=2, relief=RIDGE)
        frame.place(x=50, y=120, width=900, height=300)

        # Scrollbars
        scroll_x = Scrollbar(frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame, orient=VERTICAL)

        # Table
        self.result_table = ttk.Treeview(frame, columns=("courseCode", "marks", "fullmarks", "percentage"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.result_table.xview)
        scroll_y.config(command=self.result_table.yview)

        self.result_table.heading("courseCode", text="courseCode")
        self.result_table.heading("marks", text="Marks")
        self.result_table.heading("fullmarks", text="Full Marks")
        self.result_table.heading("percentage", text="Percentage")

        self.result_table["show"] = "headings"

        self.result_table.column("courseCode", width=150)
        self.result_table.column("marks", width=100)
        self.result_table.column("fullmarks", width=100)
        self.result_table.column("percentage", width=100)

        self.result_table.pack(fill=BOTH, expand=1)

        # Label for Overall Percentage
        self.overall_percentage = Label(self.root, text="Overall Percentage: N/A",
                                        font=("times new roman", 14, "bold"), bg="white", fg="black")
        self.overall_percentage.place(x=50, y=440)

    def search_name(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="vnsvb", database="face_recognition")
        my_cursor = conn.cursor()
        try:
            student_id = self.search.get().strip()
            if not student_id:
                messagebox.showerror("Error", "Please enter a Student ID")
                return

            # Fetch student results for all subjects
            query = "SELECT courseCode, marks, fullmarks FROM result WHERE studentID = %s"
            my_cursor.execute(query, (student_id,))
            rows = my_cursor.fetchall()

            if rows:
                self.result_table.delete(*self.result_table.get_children())  # Clear previous records
                total_marks = 0
                total_fullmarks = 0

                for row in rows:
                    courseCode, marks, fullmarks = row
                    percentage = (marks / fullmarks) * 100 if fullmarks > 0 else 0
                    self.result_table.insert("", "end", values=(courseCode, marks, fullmarks, f"{percentage:.2f}%"))

                    total_marks += marks
                    total_fullmarks += fullmarks

                # Calculate Overall Percentage
                overall_percentage = (total_marks / total_fullmarks) * 100 if total_fullmarks > 0 else 0
                self.overall_percentage.config(text=f"Overall Percentage: {overall_percentage:.2f}%")
            else:
                messagebox.showinfo("Result", "No student records found!")
                self.reset_fields()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        finally:
            conn.close()

    def reset_fields(self):
        self.search.set("")
        self.result_table.delete(*self.result_table.get_children())  # Clear table
        self.overall_percentage.config(text="Overall Percentage: N/A")


if __name__ == "__main__":
    root = Tk()
    obj = Report(root)
    root.mainloop()
