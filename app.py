import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import os
from tkcalendar import DateEntry  # ใช้ DateEntry สำหรับเลือกวันที่
import time

def connect_db():
    for i in range(5):
        try:
            conn = sqlite3.connect('concerts_1.db', timeout=10)
            return conn
        except sqlite3.OperationalError:
            time.sleep(1)
    raise Exception("Database is locked, please try again later.")

def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                birthday TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT,
                image TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                concert_id INTEGER,
                ticket_type TEXT,
                quantity INTEGER,
                total_price INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(concert_id) REFERENCES concerts(id)
            )
        ''')
        conn.commit()

class ConcertBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Concert Booking App")
        self.root.geometry("1024x768")
        self.root.configure(bg="#1c1c1c")
        self.user_id = None

        self.concerts = [
        ("หงส์ทอง เฟี้ยวติวัล", "2024-11-23", "Khonkaen", "HT.jpg"),
        ("ติดเศร้าคอนเสิร์ต Don't Cry Alone @ศรีราชา", "2024-11-16", "Chonburi", "dca.jpg"),
        ("Big Mountain Music Festival", "2024-12-07", "Nakhon Ratchasima", "bmmf.jpg"),
        ("In The Mood Music Fest for the Bakerian", "2024-12-14", "Chonburi", "itmm.png"),
        ("เต้ย Freshtival", "2025-01-05", "Khonkaen", "TF.jpg"),
        ("ภูผาม่านเฟสติวัล", "2025-01-24", "Khonkaen", "ph.jpg"),
        ("เฉียงเหนือเฟส 2", "2025-02-01", "Khonkaen", "CN.jpg"),
        ("Maroon 5", "2025-02-03", "Bangkok", "maroon_5.png"),
    ]
        self.ticket_prices = {
            "หงส์ทอง เฟี้ยวติวัล": 1200,
            "ติดเศร้าคอนเสิร์ต Don't Cry Alone": 800,
            "Big Mountain Music Festival": 1500,
            "In The Mood Music Fest for the Bakerian": 1000,
            "เต้ย Freshtival": 1300,
            "ภูผาม่านเฟสติวัล": 1100,
            "เฉียงเหนือเฟส 2": 950,
            "Maroon 5": 1800,
        }

        self.init_ui()

    def create_menu(self):
        menu_frame = tk.Frame(self.frame, bg="#333")
        menu_frame.pack(fill='x')

        home_button = tk.Button(menu_frame, text="🏠 Home", command=self.home_page, bg="#333", fg="white", font=("Helvetica", 12, "bold"), borderwidth=0)
        home_button.pack(side='left', padx=10, pady=5)

        profile_button = tk.Button(menu_frame, text="👤 Profile", command=self.profile_page, bg="#333", fg="white", font=("Helvetica", 12, "bold"), borderwidth=0)
        profile_button.pack(side='right', padx=10, pady=5)

        logout_button = tk.Button(menu_frame, text="🚪 Logout", command=self.logout, bg="#333", fg="white", font=("Helvetica", 12, "bold"), borderwidth=0)
        logout_button.pack(side='right', padx=10, pady=5)

    def init_ui(self):
        self.frame = tk.Frame(self.root, bg="#1c1c1c")
        self.frame.place(relwidth=1, relheight=1)
        self.login_frame()

    def login_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Login", font=("Helvetica", 20, "bold"), bg="#1c1c1c", fg="white").pack(pady=20)

        tk.Label(self.frame, text="Username", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.username_entry.pack()

        tk.Label(self.frame, text="Password", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', font=("Helvetica", 14), bg="#333", fg="white")
        self.password_entry.pack()

        tk.Button(self.frame, text="Login", command=self.login, bg="#e91e63", fg="white", font=("Helvetica", 14, "bold"), width=15).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()

        if user:
            self.user_id = user[0]
            self.home_page()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def login_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # กำหนดพื้นหลังพร้อมตกแต่ง
        tk.Label(self.frame, text="Concert Booking App", font=("Helvetica", 30, "bold"), bg="#1c1c1c", fg="#e91e63").pack(pady=30)

        login_box = tk.Frame(self.frame, bg="#333", padx=20, pady=20)
        login_box.pack(pady=20)

        # ตกแต่งข้อความส่วนหัว
        tk.Label(login_box, text="Login", font=("Helvetica", 20, "bold"), bg="#333", fg="white").pack(pady=10)

        # เพิ่มการตกแต่งช่องกรอกข้อมูล
        tk.Label(login_box, text="Username", bg="#333", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.username_entry = tk.Entry(login_box, font=("Helvetica", 14), bg="#555", fg="white", bd=0, relief="solid", width=20)
        self.username_entry.pack(pady=(0, 10))

        tk.Label(login_box, text="Password", bg="#333", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.password_entry = tk.Entry(login_box, show='*', font=("Helvetica", 14), bg="#555", fg="white", bd=0, relief="solid", width=20)
        self.password_entry.pack(pady=(0, 20))

        # ปุ่ม login พร้อมการตกแต่งเพิ่มเติม
        tk.Button(login_box, text="Login", command=self.login, bg="#e91e63", fg="white", font=("Helvetica", 14, "bold"), width=15, relief="flat").pack(pady=(0, 10))
        tk.Button(login_box, text="Register", command=self.register_frame, bg="#333", fg="#e91e63", font=("Helvetica", 12, "underline"), borderwidth=0).pack(pady=5)
        tk.Button(login_box, text="Forgot Password", command=self.forgot_password, bg="#333", fg="#e91e63", font=("Helvetica", 12, "underline"), borderwidth=0).pack()



    def forgot_password(self):
        email = simpledialog.askstring("Forgot Password", "Enter your email:")
        if email:
            messagebox.showinfo("OTP Sent", "An OTP has been sent to your email.")

    def home_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_menu()

        tk.Label(self.frame, text="Welcome to the Concert Booking App!", font=("Helvetica", 24, "bold"), bg="#1c1c1c", fg="#e91e63").pack(pady=20)

        concert_frame = tk.Frame(self.frame, bg="#1c1c1c")
        concert_frame.pack(pady=20)
        
        concerts = [
            ("หงส์ทอง เฟี้ยวติวัล", "2024-11-23", "Khonkaen", "HT.jpg"),
            ("ติดเศร้าคอนเสิร์ต Don't Cry Alone @ศรีราชา", "2024-11-16", "Chonburi", "dca.jpg"),
            ("Big Mountain Music Festival", "2024-12-07","-","2025-12-08" "Nakhon Ratchasima", "bmmf.jpg"),
            ("In The Mood Music Fest for the Bakerian", "2024-12-14", "Chonburi", "itmm.png"),
            ("เต้ย Freshtival", "2025-01-05", "Khonkaen", "TF.jpg"),
            ("ภูผาม่านเฟสติวัล", "2025-01-24","-","2025-01-25", "Khonkaen", "ph.jpg"),
            ("เฉียงเหนือเฟส 2", "2025-02-01", "Khonkaen", "CN.jpg"),
            ("Maroon 5", "2025-02-03", "Bangkok", "maroon_5.png"),
        ]
        
        rows = 2
        cols = 4
        for i, concert in enumerate(concerts):
            concert_name, concert_date, concert_location, concert_image = concert

            frame = tk.Frame(concert_frame, bg="#1c1c1c", padx=10, pady=10)
            frame.grid(row=i // cols, column=i % cols, padx=10, pady=10)

            tk.Label(frame, text=f"{concert_name}\n{concert_date}\n{concert_location}", font=("Helvetica", 12), bg="#1c1c1c", fg="white").pack(pady=5)

            if os.path.exists(concert_image):
                img = tk.PhotoImage(file=concert_image)
                img_label = tk.Label(frame, image=img, bg="#1c1c1c")
                img_label.image = img
                img_label.pack(pady=5)
            else:
                tk.Label(frame, text="(Image not available)", bg="#1c1c1c", fg="grey").pack(pady=5)

            tk.Button(frame, text="Book Ticket", command=lambda c=concert: self.book_ticket(c), bg="#e91e63", fg="white", font=("Helvetica", 12), width=10).pack(pady=5)

    def register_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Register", font=("Helvetica", 20, "bold"), bg="#1c1c1c", fg="white").pack(pady=20)

        tk.Label(self.frame, text="Username", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.username_entry.pack()

        tk.Label(self.frame, text="First Name", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.first_name_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.first_name_entry.pack()

        tk.Label(self.frame, text="Last Name", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.last_name_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.last_name_entry.pack()

        tk.Label(self.frame, text="Phone", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.phone_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.phone_entry.pack()

        tk.Label(self.frame, text="Email", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.email_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.email_entry.pack()

        tk.Label(self.frame, text="Password", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', font=("Helvetica", 14), bg="#333", fg="white")
        self.password_entry.pack()

        tk.Button(self.frame, text="Register", command=self.register, bg="#e91e63", fg="white", font=("Helvetica", 14, "bold"), width=15).pack(pady=10)
        tk.Button(self.frame, text="Back to Login", command=self.login_frame, bg="#1c1c1c", fg="#e91e63", font=("Helvetica", 12), borderwidth=0).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not (username and first_name and last_name and phone and email and password):
            messagebox.showerror("Error", "All fields are required.")
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, first_name, last_name, phone, email, password) VALUES (?, ?, ?, ?, ?, ?)',
                               (username, first_name, last_name, phone, email, password))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful.")
                self.login_frame()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username or Email already exists.")

    def home_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_menu()

        tk.Label(self.frame, text="Welcome to the Concert Booking App!", font=("Helvetica", 24, "bold"), bg="#1c1c1c", fg="#e91e63").pack(pady=20)

        concert_frame = tk.Frame(self.frame, bg="#1c1c1c")
        concert_frame.pack(pady=20)
        
        concerts = [
            ("หงส์ทอง เฟี้ยวติวัล", "2024-11-23", "Khonkaen", "HT.jpg"),
            ("ติดเศร้าคอนเสิร์ต Don't Cry Alone @ศรีราชา", "2024-11-16", "Chonburi", "dca.jpg"),
            ("Big Mountain Music Festival", "2024-12-07","-","2025-12-08" "Nakhon Ratchasima", "bmmf.jpg"),
            ("In The Mood Music Fest for the Bakerian", "2024-12-14", "Chonburi", "itmm.png"),
            ("เต้ย Freshtival", "2025-01-05", "Khonkaen", "TF.jpg"),
            ("ภูผาม่านเฟสติวัล", "2025-01-24","-","2025-01-25", "Khonkaen", "ph.jpg"),
            ("เฉียงเหนือเฟส 2", "2025-02-01", "Khonkaen", "CN.jpg"),
            ("Maroon 5", "2025-02-03", "Bangkok", "maroon_5.png"),
        ]
        
        rows = 2
        cols = 4
        for i, concert in enumerate(concerts):
            concert_name, concert_date, concert_location, concert_image = concert

            frame = tk.Frame(concert_frame, bg="#1c1c1c", padx=10, pady=10)
            frame.grid(row=i // cols, column=i % cols, padx=10, pady=10)

            tk.Label(frame, text=f"{concert_name}\n{concert_date}\n{concert_location}", font=("Helvetica", 12), bg="#1c1c1c", fg="white").pack(pady=5)

            if os.path.exists(concert_image):
                img = tk.PhotoImage(file=concert_image)
                img_label = tk.Label(frame, image=img, bg="#1c1c1c")
                img_label.image = img
                img_label.pack(pady=5)
            else:
                tk.Label(frame, text="(Image not available)", bg="#1c1c1c", fg="grey").pack(pady=5)

            tk.Button(frame, text="Book Ticket", command=lambda c=concert: self.book_ticket(c), bg="#e91e63", fg="white", font=("Helvetica", 12), width=10).pack(pady=5)

    def register_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Register", font=("Helvetica", 20, "bold"), bg="#1c1c1c", fg="white").pack(pady=20)

        tk.Label(self.frame, text="Username", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.username_entry.pack()

        tk.Label(self.frame, text="First Name", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.first_name_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.first_name_entry.pack()

        tk.Label(self.frame, text="Last Name", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.last_name_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.last_name_entry.pack()

        tk.Label(self.frame, text="Phone", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.phone_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.phone_entry.pack()

        tk.Label(self.frame, text="Email", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.email_entry = tk.Entry(self.frame, font=("Helvetica", 14), bg="#333", fg="white")
        self.email_entry.pack()

        tk.Label(self.frame, text="Password", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', font=("Helvetica", 14), bg="#333", fg="white")
        self.password_entry.pack()

        tk.Button(self.frame, text="Register", command=self.register, bg="#e91e63", fg="white", font=("Helvetica", 14, "bold"), width=15).pack(pady=10)
        tk.Button(self.frame, text="Back to Login", command=self.login_frame, bg="#1c1c1c", fg="#e91e63", font=("Helvetica", 12), borderwidth=0).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not (username and first_name and last_name and phone and email and password):
            messagebox.showerror("Error", "All fields are required.")
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, first_name, last_name, phone, email, password) VALUES (?, ?, ?, ?, ?, ?)',
                               (username, first_name, last_name, phone, email, password))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful.")
                self.login_frame()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username or Email already exists.")

    def home_page(self):
        # เคลียร์หน้าจอเก่า
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_menu()

        tk.Label(self.frame, text="Welcome to the Concert Booking App!", font=("Helvetica", 24, "bold"), bg="#1c1c1c", fg="#e91e63").pack(pady=20)

        concert_frame = tk.Frame(self.frame, bg="#1c1c1c")
        concert_frame.pack(pady=20)

        rows = 2
        cols = 4
        for i, concert in enumerate(self.concerts):
            concert_name, concert_date, concert_location, concert_image = concert

            frame = tk.Frame(concert_frame, bg="#1c1c1c", padx=10, pady=10)
            frame.grid(row=i // cols, column=i % cols, padx=10, pady=10)

            tk.Label(frame, text=f"{concert_name}\n{concert_date}\n{concert_location}", font=("Helvetica", 12), bg="#1c1c1c", fg="white").pack(pady=5)

            if os.path.exists(concert_image):
                img = tk.PhotoImage(file=concert_image)
                img_label = tk.Label(frame, image=img, bg="#1c1c1c")
                img_label.image = img
                img_label.pack(pady=5)
            else:
                tk.Label(frame, text="(Image not available)", bg="#1c1c1c", fg="grey").pack(pady=5)

            tk.Button(frame, text="Book Ticket", command=lambda c=concert: self.book_ticket(c), bg="#e91e63", fg="white", font=("Helvetica", 12), width=10).pack(pady=5)

    def book_ticket(self, concert):
        print(f"Booking ticket for: {concert}")  # ตรวจสอบว่าฟังก์ชันทำงาน
        if len(concert) < 5:
            concert = concert + ({'Standard': 1000, 'VIP': 2000},)  # กำหนด ticket_prices ค่าเริ่มต้นหากขาดไป

        concert_name, concert_date, concert_location, concert_image, ticket_prices = concert

        # เปิดหน้าต่างการจอง
        top = tk.Toplevel(self.root)
        top.title(f"Book Ticket for {concert_name}")
        top.geometry("400x300")
        top.configure(bg="#1c1c1c")
        
        # แสดงข้อมูลคอนเสิร์ต
        tk.Label(top, text=f"{concert_name}", font=("Helvetica", 18, "bold"), bg="#1c1c1c", fg="white").pack(pady=10)
        tk.Label(top, text=f"{concert_date}\n{concert_location}", font=("Helvetica", 12), bg="#1c1c1c", fg="white").pack(pady=5)
        
        # แสดงตัวเลือกตั๋วและจำนวน
        tk.Label(top, text="Select Ticket Type:", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=10)
        ticket_type_var = tk.StringVar(value="Standard")
        tk.OptionMenu(top, ticket_type_var, *ticket_prices.keys()).pack()

        tk.Label(top, text="Select Quantity:", bg="#1c1c1c", fg="white", font=("Helvetica", 14)).pack(pady=10)
        quantity_var = tk.IntVar(value=1)
        tk.Spinbox(top, from_=1, to=10, textvariable=quantity_var).pack()

        total_cost_label = tk.Label(top, text="Total: 0 Baht", font=("Helvetica", 16, "bold"), bg="#1c1c1c", fg="white")
        total_cost_label.pack(pady=15)
        def update_total():
                ticket_type = ticket_type_var.get()
                quantity = quantity_var.get()
                total_cost = ticket_prices[ticket_type] * quantity
                total_cost_label.config(text=f"Total: {total_cost} Baht")

        ticket_type_var.trace("w", lambda *args: update_total())
        quantity_var.trace("w", lambda *args: update_total())

        # เรียก update_total() หนึ่งครั้งเพื่อแสดงค่าเริ่มต้น
        update_total()

        def confirm_booking():
            print(f"Booking confirmed for: {concert_name} - {ticket_type_var.get()} x {quantity_var.get()}")  # ตรวจสอบการจอง
            ticket_type = ticket_type_var.get()
            quantity = quantity_var.get()
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO bookings (user_id, concert_id, ticket_type, quantity) VALUES (?, ?, ?, ?)',
                            (self.user_id, self.concerts.index(concert) + 1, ticket_type, quantity))
                conn.commit()
            messagebox.showinfo("Success", "Ticket booked successfully!")
            top.destroy()

        tk.Button(top, text="Confirm Booking", command=confirm_booking, bg="#e91e63", fg="white", font=("Helvetica", 12, "bold"), width=15).pack(pady=20)
    
    def profile_page(self):
        if not self.user_id:
            messagebox.showerror("Error", "กรุณาเข้าสู่ระบบก่อน.")
            return

        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_menu()

        # ส่วนหัวของโปรไฟล์
        tk.Label(self.frame, text="YOUR TICKETS", font=("Helvetica", 24, "bold"), bg="#1c1c1c", fg="white").pack(pady=20)

        # แสดงตั๋วคอนเสิร์ต
        show_tickets(self.frame, self.user_id)

        # สร้าง frame สำหรับโปรไฟล์
        profile_frame = tk.Frame(self.frame, bg="#e91e63", width=300, height=400)
        profile_frame.pack(pady=20, padx=20, side="right")
        profile_frame.pack_propagate(False)

        # โหลดรูปโปรไฟล์หรือแสดงรูปพื้นฐาน
        load_profile_image(profile_frame)

        # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (self.user_id,))
            user = cursor.fetchone()

        if user:
            tk.Label(profile_frame, text=f"{user[1]}", font=("Helvetica", 14, "bold"), bg="#e91e63", fg="white").pack(pady=10)
            tk.Label(profile_frame, text=f"{user[2]} {user[3]}", font=("Helvetica", 12), bg="#e91e63", fg="white").pack(pady=5)

            # ปุ่ม Edit Profile
            tk.Button(profile_frame, text="Edit Profile", font=("Helvetica", 12, "bold"), bg="white", fg="#e91e63",
                      command=lambda: edit_profile(self.frame, self.user_id)).pack(pady=10)
        else:
            messagebox.showerror("Error", "ไม่สามารถโหลดโปรไฟล์ได้.")
            return

    def book_ticket(self, concert):
        # รหัสนี้ถูกต้องแล้วในโค้ดที่แก้ไขด้านบน
        pass  # รหัสนี้ถูกย้ายไปในโค้ดที่แก้ไขแล้ว

    def logout(self):
        self.user_id = None
        self.login_frame()

def show_tickets(parent, user_id):
    # ตรวจสอบว่าผู้ใช้ได้เข้าสู่ระบบหรือยัง
    if not user_id:
        messagebox.showerror("Error", "กรุณาเข้าสู่ระบบก่อน.")
        return

    # สร้าง frame สำหรับแสดงตั๋ว
    tickets_frame = tk.Frame(parent, bg="#1c1c1c")
    tickets_frame.pack(pady=10, padx=10, fill='both', expand=True)

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT concerts.name, bookings.ticket_type, bookings.quantity, concerts.date, concerts.location
            FROM bookings
            JOIN concerts ON bookings.concert_id = concerts.id
            WHERE bookings.user_id = ?
        ''', (user_id,))
        bookings = cursor.fetchall()

    if not bookings:
        tk.Label(tickets_frame, text="คุณยังไม่มีการจองตั๋ว.", font=("Helvetica", 16), fg="red", bg="#1c1c1c").pack(pady=20)
    else:
        for booking in bookings:
            concert_name, ticket_type, quantity, concert_date, concert_location = booking
            ticket_info = f"{concert_name} ({concert_date}) - {concert_location}\nType: {ticket_type}, Quantity: {quantity}"
            tk.Label(tickets_frame, text=ticket_info, font=("Helvetica", 12), fg="white", bg="#1c1c1c", justify="left").pack(pady=10, anchor='w')

def load_profile_image(profile_frame):
    profile_image_path = "profile_image_path.txt"  # บันทึกที่อยู่ของรูปภาพในไฟล์นี้

    # ตรวจสอบว่ามีไฟล์บันทึกตำแหน่งรูปภาพอยู่หรือไม่
    if os.path.exists(profile_image_path):
        with open(profile_image_path, "r") as file:
            image_path = file.read().strip()
            if os.path.exists(image_path):
                profile_img = Image.open(image_path).resize((100, 100))
            else:
                profile_img = Image.new("RGB", (100, 100), "grey")
    else:
        profile_img = Image.new("RGB", (100, 100), "grey")

    img = ImageTk.PhotoImage(profile_img)
    profile_img_label = tk.Label(profile_frame, image=img, bg="#e91e63")
    profile_img_label.image = img
    profile_img_label.pack(pady=10)

    upload_button = tk.Button(profile_frame, text="Upload Image", font=("Helvetica", 10), bg="white", fg="#e91e63",
                              command=lambda: upload_profile_image(profile_frame, profile_image_path))
    upload_button.pack(pady=5)

def upload_profile_image(profile_frame, profile_image_path):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        profile_image = Image.open(file_path).resize((100, 100))
        img = ImageTk.PhotoImage(profile_image)

        # อัปเดตรูปภาพโปรไฟล์ในโปรแกรม
        for widget in profile_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(image=img)
                widget.image = img
                break

        # บันทึกที่อยู่ของรูปภาพลงไฟล์
        with open(profile_image_path, "w") as file:
            file.write(file_path)
        messagebox.showinfo("Success", "รูปภาพถูกบันทึกเรียบร้อยแล้ว.")

def edit_profile(parent, user_id):
    edit_window = tk.Toplevel(parent)
    edit_window.title("Edit Profile")
    edit_window.geometry("400x500")
    edit_window.config(bg="#1c1c1c")

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

    if not user:
        messagebox.showerror("Error", "ไม่สามารถโหลดข้อมูลผู้ใช้ได้.")
        edit_window.destroy()
        return

    tk.Label(edit_window, text="Edit Profile", font=("Helvetica", 16, "bold"), bg="#1c1c1c", fg="white").pack(pady=10)

    fields = ["Username", "First Name", "Last Name", "Phone", "Email", "Birthday"]
    entries = {}
    for i, field in enumerate(fields):
        tk.Label(edit_window, text=f"{field}:", font=("Helvetica", 12), bg="#1c1c1c", fg="white").pack(pady=5)
        entry = tk.Entry(edit_window, font=("Helvetica", 12), bg="#555", fg="white", bd=0, relief="solid", width=30)
        entry.pack(pady=5)
        if field == "Username":
            entry.insert(0, user[1])
        elif field == "First Name":
            entry.insert(0, user[2])
        elif field == "Last Name":
            entry.insert(0, user[3])
        elif field == "Phone":
            entry.insert(0, user[4])
        elif field == "Email":
            entry.insert(0, user[5])
        elif field == "Birthday":
            entry.insert(0, user[7] if user[7] else "")
        entries[field.lower().replace(" ", "_")] = entry

    # ปุ่มบันทึกการเปลี่ยนแปลง
    save_button = tk.Button(edit_window, text="Save Changes", font=("Helvetica", 12), bg="#e91e63", fg="white",
                            command=lambda: save_profile(entries, user_id, edit_window))
    save_button.pack(pady=10)

    # ปุ่มปิดหน้าต่าง
    close_button = tk.Button(edit_window, text="Close", font=("Helvetica", 12), bg="#555", fg="white",
                             command=edit_window.destroy)
    close_button.pack(pady=10)

def save_profile(entries, user_id, edit_window):
    username = entries["username"].get()
    first_name = entries["first_name"].get()
    last_name = entries["last_name"].get()
    phone = entries["phone"].get()
    email = entries["email"].get()
    birthday = entries["birthday"].get()

    if not (username and first_name and last_name and phone and email):
        messagebox.showerror("Error", "กรุณากรอกข้อมูลทุกช่องที่จำเป็น.")
        return

    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE users
                SET username = ?, first_name = ?, last_name = ?, phone = ?, email = ?, birthday = ?
                WHERE id = ?
            ''', (username, first_name, last_name, phone, email, birthday, user_id))
            conn.commit()
            messagebox.showinfo("Success", "อัปเดตโปรไฟล์สำเร็จ.")
            edit_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "ชื่อผู้ใช้หรืออีเมลนี้มีอยู่แล้ว.")

# เริ่มการทำงานของแอปพลิเคชัน
init_db()
root = tk.Tk()
app = ConcertBookingApp(root)
root.mainloop()