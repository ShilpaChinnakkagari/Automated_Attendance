# study_portal.py
import webbrowser
import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime

class StudyPortal:
    def __init__(self, root, student_id):
        self.root = root
        self.student_id = student_id
        self.root.title(f"Study Portal - Student ID: {student_id}")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f2f5")
        self.root.state('zoomed')
        
        # Initialize database connection
        self.conn = sqlite3.connect("college_updates.db")
        self.cursor = self.conn.cursor()
        
        # Main container
        main_frame = Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = Frame(main_frame, bg="#2c3e50", height=80)
        header_frame.pack(fill=X, pady=(0,20))
        
        Label(header_frame, 
             text=f"Study & Opportunities Portal - Student ID: {self.student_id}",
             font=("Arial", 16, "bold"), 
             bg="#2c3e50", fg="white"
             ).pack(side=LEFT, padx=20)
        
        # Content area
        content_frame = Frame(main_frame, bg="white", bd=2, relief=GROOVE)
        content_frame.pack(fill=BOTH, expand=True)
        
        # Main content frame
        study_frame = Frame(content_frame, bg="white")
        study_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Website access button
        website_btn = Button(study_frame, 
                           text="🌐 Access Learning Website", 
                           font=("Arial", 14),
                           bg="#3498db", fg="white",
                           command=self.open_website,
                           padx=20, pady=10)
        website_btn.pack(pady=20)
        
        # Updates section
        Label(study_frame, 
             text="Current Opportunities & Resources",
             font=("Arial", 14, "bold"),
             bg="white").pack(anchor=W, pady=(20,10))
        
        # Create opportunity buttons
        opportunities = [
            ("📚 All Courses", "Course"),
            ("🚀 Hackathons", "Hackathon"),
            ("🔧 Workshops", "Workshop"),
            ("💼 Internships", "Internship"),
            ("🏢 Campus Drives", "Campus Drive"),
            ("📰 Resources & Others", "Resource,Other")
        ]
        
        for text, update_type in opportunities:
            btn = Button(study_frame,
                        text=text,
                        font=("Arial", 12),
                        bg="#ecf0f1",
                        command=lambda ut=update_type: self.show_updates(ut),
                        padx=15, pady=8,
                        wraplength=300,
                        justify=LEFT)
            btn.pack(fill=X, pady=5, ipadx=10)
        
        # Footer
        footer_frame = Frame(main_frame, bg="#2c3e50", height=40)
        footer_frame.pack(fill=X, pady=(20,0))
        
        Label(footer_frame, 
             text="© 2023 College Opportunities Portal",
             font=("Arial", 10), 
             bg="#2c3e50", fg="white"
             ).pack(pady=10)
    
    def open_website(self):
        """Open the learning website"""
        website_url = "http://20.0.121.215/"
        try:
            webbrowser.open_new(website_url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open website:\n{str(e)}")
    
    def show_updates(self, update_type):
        """Show updates of specific type"""
        if "," in update_type:
            types = update_type.split(",")
            placeholders = ",".join("?" * len(types))
            query = f"SELECT * FROM updates WHERE type IN ({placeholders}) ORDER BY date DESC"
            params = types
        else:
            query = "SELECT * FROM updates WHERE type = ? ORDER BY date DESC"
            params = (update_type,)
        
        self.cursor.execute(query, params)
        updates = self.cursor.fetchall()
        
        if not updates:
            messagebox.showinfo("Info", f"No {update_type} updates available")
            return
        
        top = Toplevel(self.root)
        top.title(f"{update_type} Updates")
        top.geometry("800x600")
        
        # Create a frame for the treeview
        tree_frame = Frame(top)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create a treeview with scrollbar
        tree = ttk.Treeview(tree_frame, columns=("type", "title", "date", "desc"), show="headings")
        
        # Define headings
        tree.heading("type", text="Type")
        tree.heading("title", text="Title")
        tree.heading("date", text="Date")
        tree.heading("desc", text="Description")
        
        # Define column widths
        tree.column("type", width=100)
        tree.column("title", width=200)
        tree.column("date", width=100)
        tree.column("desc", width=350)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree.pack(fill=BOTH, expand=True)
        
        # Insert data
        for update in updates:
            tree.insert("", END, values=(update[1], update[2], update[4], update[3]))
        
        # Add link button if available
        def open_link():
            selected = tree.focus()
            if selected:
                item = tree.item(selected)
                values = item['values']
                for update in updates:
                    if update[2] == values[1] and update[5]:  # Match title and check for link
                        webbrowser.open_new(update[5])
                        return
                messagebox.showinfo("Info", "No link available for this item")
        
        link_btn = Button(top, text="Open Link", command=open_link)
        link_btn.pack(pady=5)
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def launch_study_portal(student_id):
    root = Tk()
    StudyPortal(root, student_id)
    root.mainloop()

if __name__ == "__main__":
    launch_study_portal("12345")  # Test with sample ID