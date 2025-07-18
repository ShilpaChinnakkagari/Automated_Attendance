# manage_updates.py
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

class UpdateManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Faculty Update Management")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")
        self.root.state('zoomed')
        
        # Initialize database
        self.initialize_db()
        
        # Main container
        main_frame = Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = Frame(main_frame, bg="#2c3e50", height=80)
        header_frame.pack(fill=X, pady=(0,20))
        
        Label(header_frame, 
             text="Faculty Update Management System",
             font=("Arial", 16, "bold"), 
             bg="#2c3e50", fg="white"
             ).pack(side=LEFT, padx=20)
        
        # Content area
        content_frame = Frame(main_frame, bg="white", bd=2, relief=GROOVE)
        content_frame.pack(fill=BOTH, expand=True)
        
        # Form frame
        form_frame = Frame(content_frame, bg="white", padx=20, pady=20)
        form_frame.pack(fill=X)
        
        # Update type
        Label(form_frame, text="Update Type:", bg="white").grid(row=0, column=0, sticky=W, pady=5)
        self.update_type = ttk.Combobox(form_frame, values=[
            "Course", "Workshop", "Hackathon", "Internship", 
            "Campus Drive", "Resource", "Other"
        ], state="readonly")
        self.update_type.grid(row=0, column=1, sticky=EW, pady=5, padx=5)
        
        # Title
        Label(form_frame, text="Title:", bg="white").grid(row=1, column=0, sticky=W, pady=5)
        self.title_entry = Entry(form_frame, width=50)
        self.title_entry.grid(row=1, column=1, sticky=EW, pady=5, padx=5)
        
        # Description
        Label(form_frame, text="Description:", bg="white").grid(row=2, column=0, sticky=NW, pady=5)
        self.desc_text = Text(form_frame, width=50, height=5)
        self.desc_text.grid(row=2, column=1, sticky=EW, pady=5, padx=5)
        
        # Date
        Label(form_frame, text="Date/Deadline:", bg="white").grid(row=3, column=0, sticky=W, pady=5)
        self.date_entry = Entry(form_frame, width=50)
        self.date_entry.grid(row=3, column=1, sticky=EW, pady=5, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Link
        Label(form_frame, text="Link (optional):", bg="white").grid(row=4, column=0, sticky=W, pady=5)
        self.link_entry = Entry(form_frame, width=50)
        self.link_entry.grid(row=4, column=1, sticky=EW, pady=5, padx=5)
        
        # Submit button
        submit_btn = Button(form_frame, text="Post Update", command=self.post_update,
                           bg="#27ae60", fg="white", font=("Arial", 12))
        submit_btn.grid(row=5, column=1, sticky=E, pady=10)
        
        # Separator
        ttk.Separator(content_frame, orient=HORIZONTAL).pack(fill=X, padx=20, pady=10)
        
        # Existing updates frame
        updates_frame = Frame(content_frame, bg="white")
        updates_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Treeview for existing updates
        self.updates_tree = ttk.Treeview(updates_frame, columns=("id", "type", "title", "date"), show="headings")
        self.updates_tree.heading("id", text="ID")
        self.updates_tree.heading("type", text="Type")
        self.updates_tree.heading("title", text="Title")
        self.updates_tree.heading("date", text="Date")
        self.updates_tree.column("id", width=50)
        self.updates_tree.column("type", width=100)
        self.updates_tree.column("title", width=300)
        self.updates_tree.column("date", width=100)
        
        scrollbar = ttk.Scrollbar(updates_frame, orient=VERTICAL, command=self.updates_tree.yview)
        self.updates_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.updates_tree.pack(fill=BOTH, expand=True)
        
        # Delete button
        delete_btn = Button(updates_frame, text="Delete Selected", command=self.delete_update,
                          bg="#e74c3c", fg="white", font=("Arial", 10))
        delete_btn.pack(side=LEFT, pady=5)
        
        # Load existing updates
        self.load_updates()
        
    def initialize_db(self):
        """Initialize the SQLite database"""
        self.conn = sqlite3.connect("college_updates.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                link TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def post_update(self):
        """Post a new update to the database"""
        update_type = self.update_type.get()
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", END).strip()
        date = self.date_entry.get()
        link = self.link_entry.get()
        
        if not all([update_type, title, description, date]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
            
        try:
            self.cursor.execute("""
                INSERT INTO updates (type, title, description, date, link)
                VALUES (?, ?, ?, ?, ?)
            """, (update_type, title, description, date, link))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Update posted successfully!")
            self.clear_form()
            self.load_updates()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to post update:\n{str(e)}")
    
    def clear_form(self):
        """Clear the form fields"""
        self.update_type.set('')
        self.title_entry.delete(0, END)
        self.desc_text.delete("1.0", END)
        self.date_entry.delete(0, END)
        self.link_entry.delete(0, END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    def load_updates(self):
        """Load existing updates from database"""
        for item in self.updates_tree.get_children():
            self.updates_tree.delete(item)
            
        self.cursor.execute("SELECT id, type, title, date FROM updates ORDER BY date DESC")
        for row in self.cursor.fetchall():
            self.updates_tree.insert("", END, values=row)
    
    def delete_update(self):
        """Delete selected update"""
        selected = self.updates_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an update to delete")
            return
            
        update_id = self.updates_tree.item(selected[0])['values'][0]
        
        try:
            self.cursor.execute("DELETE FROM updates WHERE id = ?", (update_id,))
            self.conn.commit()
            self.load_updates()
            messagebox.showinfo("Success", "Update deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete update:\n{str(e)}")
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def launch_update_manager():
    root = Tk()
    UpdateManager(root)
    root.mainloop()

if __name__ == "__main__":
    launch_update_manager()