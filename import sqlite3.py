import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox,ttk,PhotoImage,filedialog
from PIL import Image, ImageTk
import sqlite3,qrcode



# การเชื่อมต่อฐานข้อมูล SQLite
conn = sqlite3.connect("concert.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS concerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    price REAL NOT NULL,x
    image TEXT
)
''')

# สร้างฐานข้อมูล
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    birthdate  DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    concert_name TEXT,
    ticket_type TEXT,
    quantity INTEGER,
    price REAL,
    qr_code TEXT
)
''')
conn = sqlite3.connect("concert.db")
cursor = conn.cursor()


def main_window():
    root = tk.Tk()
    root.title("Concert Ticket Booking")
    root.geometry("1920x1080")
    root.configure(bg="black")

    # ฟังก์ชันเคลียร์หน้าจอ
    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()

            
    def show_frame(frame):
        frame.tkraise()

    # Function to load the background image
    def load_background_image(frame, image_path):
        try:
            from PIL import Image, ImageTk
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((1600, 800))
            bg = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(frame, image=bg)
            bg_label.image = bg
            bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print("Error loading background image:", e)


    # Admin Panel
    def create_admin_panel(root):
    # ลบเฟรมเดิมออกก่อน
        if hasattr(root, 'current_frame'):
            root.current_frame.destroy()
        
        
        admin_frame = tk.Frame(root, bg="black")
        admin_frame.place(relwidth=1, relheight=1)
        root.current_frame = admin_frame 

        load_background_image(admin_frame, "admin_bg.png")

        # Admin Panel Content
        title = tk.Label(admin_frame, text="Admin Panel", font=("Arial", 32), bg="black", fg="white")
        title.place(relx=0.5, rely=0.1, anchor="center")

        admin_frame_button = tk.Button(admin_frame, text="logout", font=("Arial", 14), bg="dark red", fg="white", command=logout)
        admin_frame_button.place(relx=0.85, rely=0.1, anchor="center", width=200, height=50)

        # Database connection
        conn = sqlite3.connect("concert.db")
        cursor = conn.cursor()

        def add_concert():
            add_concert = tk.Frame(root, bg="black")
            add_concert.place(relwidth=1, relheight=1)

            title = tk.Label(add_concert, text="Add Concert", font=("Arial", 32), bg="black", fg="white")
            title.place(relx=0.5, rely=0.05, anchor="center")

            # ✅ Concert Name
            name_label = tk.Label(add_concert, text="Concert Name:", font=("Arial", 14), bg="black", fg="white")
            name_label.place(relx=0.3, rely=0.2, anchor="w")
            name_entry = tk.Entry(add_concert, font=("Arial", 14), width=30)
            name_entry.place(relx=0.5, rely=0.2, anchor="w")

            # ✅ Date
            date_label = tk.Label(add_concert, text="Date (YYYY-MM-DD):", font=("Arial", 14), bg="black", fg="white")
            date_label.place(relx=0.3, rely=0.3, anchor="w")
            date_entry = tk.Entry(add_concert, font=("Arial", 14), width=30)
            date_entry.place(relx=0.5, rely=0.3, anchor="w")

            # ✅ Location (แก้บั๊กให้ขึ้น)
            location_label = tk.Label(add_concert, text="Location:", font=("Arial", 14), bg="black", fg="white")
            location_label.place(relx=0.3, rely=0.4, anchor="w")  
            location_entry = tk.Entry(add_concert, font=("Arial", 14), width=30)
            location_entry.place(relx=0.5, rely=0.4, anchor="w")  

            # ✅ Price
            price_label = tk.Label(add_concert, text="Price:", font=("Arial", 14), bg="black", fg="white")
            price_label.place(relx=0.3, rely=0.5, anchor="w")  # ✅ เลื่อนลงมา
            price_entry = tk.Entry(add_concert, font=("Arial", 14), width=30)
            price_entry.place(relx=0.5, rely=0.5, anchor="w")  # ✅ ตำแหน่งใหม่ (ไม่ชนกับ Location)

            # ✅ Select Image
            image_label = tk.Label(add_concert, text="Concert Image:", font=("Arial", 14), bg="black", fg="white")
            image_label.place(relx=0.3, rely=0.6, anchor="w")
            image_button = tk.Button(add_concert, text="Select Image", command=lambda: select_image(add_concert))
            image_button.place(relx=0.5, rely=0.6, anchor="w")

            add_concert_button = tk.Button(add_concert, text="Cancel", command=lambda: create_admin_panel(root), bg="#f44336", fg="white", font=("Arial", 14, "bold"))
            add_concert_button.place(relx=0.5, rely=0.8, anchor="center", width=200, height=50)  # ✅ ใช้ place อย่างเดียว

            image_path = None  # Variable to store selected image path

            def select_image(frame):
                nonlocal image_path
                image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
                if image_path:
                    img = Image.open(image_path)
                    img = img.resize((100, 100))  # Resize for display purposes
                    img = ImageTk.PhotoImage(img)
                    image_preview = tk.Label(frame, image=img)
                    image_preview.image = img
                    image_preview.place(relx=0.7, rely=0.5, anchor="w")

            def submit_concert():
                name = name_entry.get()
                date = date_entry.get()
                location = location_entry.get()
                price = price_entry.get()

                if not name or not date or not price or not location or not image_path:
                    messagebox.showerror("Error", "Please fill all fields and select an image.")
                    return

                conn = sqlite3.connect("concert.db")
                cursor = conn.cursor()

                try:
                    cursor.execute('''INSERT INTO concerts (name, date, location, price, image)
                                    VALUES (?, ?, ?, ?, ?)''',
                                (name, date, location, price, image_path))
                    conn.commit()
                    messagebox.showinfo("Success", "Concert added successfully!")
                    conn.close()

                    create_admin_panel(root)  # อัปเดตหน้าโฮมเพจ
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                    conn.close()

            # ✅ Submit Button
            submit_button = tk.Button(add_concert, text="Add Concert", font=("Arial", 14), bg="green", fg="white", command=submit_concert)
            submit_button.place(relx=0.5, rely=0.7, anchor="center", width=200, height=50)

            return add_concert

        def edit_concert():
            # สร้าง frame สำหรับแก้ไขคอนเสิร์ต
            edit_concert_frame = tk.Frame(root, bg="black")
            edit_concert_frame.place(relwidth=1, relheight=1)

            title = tk.Label(edit_concert_frame, text="Edit Concert", font=("Arial", 32), bg="black", fg="white")
            title.place(relx=0.5, rely=0.05, anchor="center")

            # ดึงข้อมูลคอนเสิร์ตจากฐานข้อมูล
            conn = sqlite3.connect("concert.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM concerts")
            concerts = cursor.fetchall()
            conn.close()

            # Listbox สำหรับเลือกคอนเสิร์ตที่ต้องการแก้ไข
            concert_listbox = tk.Listbox(edit_concert_frame, font=("Arial", 14), height=5, width=40)
            for concert in concerts:
                concert_listbox.insert(tk.END, concert[1])  # ใส่ชื่อคอนเสิร์ต
            concert_listbox.place(relx=0.5, rely=0.2, anchor="center")

            # ช่องกรอกข้อมูลคอนเสิร์ตที่ต้องการแก้ไข
            name_label = tk.Label(edit_concert_frame, text="Concert Name:", font=("Arial", 14), bg="black", fg="white")
            name_label.place(relx=0.3, rely=0.4, anchor="w")
            name_entry = tk.Entry(edit_concert_frame, font=("Arial", 14), width=30)
            name_entry.place(relx=0.5, rely=0.4, anchor="w")

            date_label = tk.Label(edit_concert_frame, text="Date (YYYY-MM-DD):", font=("Arial", 14), bg="black", fg="white")
            date_label.place(relx=0.3, rely=0.5, anchor="w")
            date_entry = tk.Entry(edit_concert_frame, font=("Arial", 14), width=30)
            date_entry.place(relx=0.5, rely=0.5, anchor="w")

            price_label = tk.Label(edit_concert_frame, text="Price:", font=("Arial", 14), bg="black", fg="white")
            price_label.place(relx=0.3, rely=0.6, anchor="w")
            price_entry = tk.Entry(edit_concert_frame, font=("Arial", 14), width=30)
            price_entry.place(relx=0.5, rely=0.6, anchor="w")

            image_label = tk.Label(edit_concert_frame, text="Concert Image:", font=("Arial", 14), bg="black", fg="white")
            image_label.place(relx=0.3, rely=0.7, anchor="w")

            image_preview = tk.Label(edit_concert_frame, bg="black")  # สำหรับแสดงภาพตัวอย่าง
            image_preview.place(relx=0.7, rely=0.7, anchor="w")

            edit_concert_button = tk.Button(edit_concert_frame, text="Cancel", command=lambda: create_admin_panel(root), bg="#f44336", fg="white", font=("Arial", 14, "bold"))
            edit_concert_button.place(relx=0.42, rely=0.88, anchor="center", width=200, height=50)
  # ✅ ใช้ place อย่างเดียว

            image_path = None  # ตัวแปรสำหรับเก็บ path ของภาพที่เลือก

            # ฟังก์ชันสำหรับดึงข้อมูลคอนเสิร์ตที่เลือกและแสดงในฟอร์ม
            def populate_fields():
                selected_concert_index = concert_listbox.curselection()
                if selected_concert_index:
                    selected_concert_id = concerts[selected_concert_index[0]][0]  # ดึง ID คอนเสิร์ต
                    conn = sqlite3.connect("concert.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT name, date, price, image FROM concerts WHERE id=?", (selected_concert_id,))
                    concert = cursor.fetchone()
                    conn.close()

                    # ใส่ค่าที่ดึงมาในช่องกรอกข้อมูล
                    name_entry.delete(0, tk.END)
                    name_entry.insert(0, concert[0])
                    date_entry.delete(0, tk.END)
                    date_entry.insert(0, concert[1])
                    price_entry.delete(0, tk.END)
                    formatted_price = f"{int(concert[2]):,}"  # แปลงเป็น int แล้วใส่คอมม่า
                    price_entry.insert(0, formatted_price)

                    # แสดงภาพที่เลือก
                    nonlocal image_path
                    image_path = concert[3]  # เก็บ path ของภาพ
                    if image_path:
                        img = Image.open(image_path)
                        img = img.resize((100, 100))  # ปรับขนาดภาพ
                        img = ImageTk.PhotoImage(img)
                        image_preview.configure(image=img)
                        image_preview.image = img

            # ปุ่มสำหรับเลือกคอนเสิร์ตที่จะแก้ไข
            select_button = tk.Button(edit_concert_frame, text="Select Concert", font=("Arial", 14), bg="blue", fg="white", command=populate_fields)
            select_button.place(relx=0.58, rely=0.8, anchor="center", width=200, height=50)

            # ฟังก์ชันสำหรับเลือกภาพใหม่
            def select_image(frame):
                nonlocal image_path
                image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
                if image_path:
                    img = Image.open(image_path)
                    img = img.resize((100, 100))  # ปรับขนาดภาพ
                    img = ImageTk.PhotoImage(img)
                    image_preview.configure(image=img)
                    image_preview.image = img

            # ปุ่มสำหรับเลือกภาพใหม่
            select_image_button = tk.Button(edit_concert_frame, text="Select New Image", font=("Arial", 14), bg="orange", fg="white", command=lambda: select_image(edit_concert_frame))
            select_image_button.place(relx=0.42, rely=0.8, anchor="center", width=200, height=50)

            # ฟังก์ชันสำหรับอัพเดตข้อมูลคอนเสิร์ต
            def update_concert():
                selected_concert_index = concert_listbox.curselection()
                if not selected_concert_index:
                    messagebox.showerror("Error", "Please select a concert to edit.")
                    return

                selected_concert_id = concerts[selected_concert_index[0]][0]  # ดึง ID คอนเสิร์ต
                name = name_entry.get()
                date = date_entry.get()
                price = price_entry.get()

                if not name or not date or not price:
                    messagebox.showerror("Error", "Please fill all fields.")
                    return

                conn = sqlite3.connect("concert.db")
                cursor = conn.cursor()
                try:
                    # แปลงราคาหากเกินพันให้มีคอมม่าและไม่มีทศนิยม
                    formatted_price = "{:,}".format(int(price))  # ลบทศนิยมออกและเพิ่มคอมม่า

                    cursor.execute('''UPDATE concerts SET name=?, date=?, price=?, image=? WHERE id=?''',
                                (name, date, formatted_price, image_path, selected_concert_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Concert updated successfully!")
                    conn.close()

                    # รีเฟรชหน้าจอหลังจากอัพเดต
                    edit_concert_frame.destroy()  # ลบหน้าจอเก่า
                    edit_concert()  # สร้างหน้าจอใหม่

                except Exception as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                    conn.close()

            # ปุ่มสำหรับอัพเดตคอนเสิร์ต
            update_button = tk.Button(edit_concert_frame, text="Update Concert", font=("Arial", 14), bg="green", fg="white", command=update_concert)
            update_button.place(relx=0.58, rely=0.88, anchor="center", width=200, height=50)

            return edit_concert_frame


        def delete_concert():
            # สร้าง frame สำหรับลบคอนเสิร์ต
            delete_concert_frame = tk.Frame(root, bg="black")
            delete_concert_frame.place(relwidth=1, relheight=1)

            title = tk.Label(delete_concert_frame, text="Delete Concert", font=("Arial", 32), bg="black", fg="white")
            title.place(relx=0.5, rely=0.05, anchor="center")

            # ดึงข้อมูลคอนเสิร์ตจากฐานข้อมูลทั้งหมด
            conn = sqlite3.connect("concert.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM concerts")  # ดึงข้อมูล ID และ ชื่อคอนเสิร์ต
            concerts = cursor.fetchall()  # ดึงข้อมูลทั้งหมด
            conn.close()

            # Listbox สำหรับเลือกคอนเสิร์ตที่ต้องการลบ
            concert_listbox = tk.Listbox(delete_concert_frame, font=("Arial", 14), height=5, width=40)
            for concert in concerts:
                concert_listbox.insert(tk.END, concert[1])  # ใส่ชื่อคอนเสิร์ตที่ดึงมา
            concert_listbox.place(relx=0.5, rely=0.2, anchor="center")

            # ฟังก์ชันสำหรับลบคอนเสิร์ต
            def delete_selected_concert():
                selected_concert_index = concert_listbox.curselection()  # เลือกคอนเสิร์ต
                if not selected_concert_index:
                    messagebox.showerror("Error", "Please select a concert to delete.")
                    return

                selected_concert_id = concerts[selected_concert_index[0]][0]  # ดึง ID ของคอนเสิร์ตที่เลือก
                conn = sqlite3.connect("concert.db")
                cursor = conn.cursor()
                try:
                    # ลบคอนเสิร์ตจากฐานข้อมูล
                    cursor.execute("DELETE FROM concerts WHERE id=?", (selected_concert_id,))
                    conn.commit()  # บันทึกการเปลี่ยนแปลง
                    messagebox.showinfo("Success", "Concert deleted successfully!")  # แจ้งผลสำเร็จ
                    conn.close()

                    # รีเฟรชหน้าจอหลังจากลบ
                    delete_concert_frame.destroy()  # ลบหน้าจอเก่า
                    delete_concert()  # สร้างหน้าจอใหม่

                except Exception as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                    conn.close()

            # ปุ่มสำหรับลบคอนเสิร์ต
            delete_button = tk.Button(delete_concert_frame, text="Delete Concert", font=("Arial", 14), bg="dark red", fg="white", command=delete_selected_concert)
            delete_button.place(relx=0.5, rely=0.7, anchor="center", width=200, height=50)

            delete_concert_button = tk.Button(delete_concert_frame, text="Cancel", command=lambda: create_admin_panel(root), bg="#f44336", fg="white", font=("Arial", 14, "bold"))
            delete_concert_button.place(relx=0.5, rely=0.8, anchor="center", width=200, height=50)

            return delete_concert_frame
        
        def show_sales_summary():
            conn = sqlite3.connect("concert.db")
            cursor = conn.cursor()
            
            # ดึงข้อมูลยอดขายจากฐานข้อมูล
            cursor.execute("""
                SELECT concert_name, SUM(quantity) as total_tickets, SUM(price) as total_sales
                FROM tickets
                GROUP BY concert_name
            """)
            sales_data = cursor.fetchall()
            conn.close()
            
            # สร้าง popup สำหรับแสดงยอดขาย
            sales_summary = tk.Toplevel()
            sales_summary.title("Sales Summary")
            sales_summary.geometry("500x300")
            
            tk.Label(sales_summary, text="สรุปยอดขายคอนเสิร์ต", font=("Arial", 16, "bold")).pack(pady=10)
            
            if not sales_data:
                tk.Label(sales_summary, text="ยังไม่มีข้อมูลการขาย", font=("Arial", 14)).pack()
            else:
                # สร้างตาราง
                columns = ("concert_name", "total_tickets", "total_sales")
                tree = ttk.Treeview(sales_summary, columns=columns, show="headings", height=8)
                
                # กำหนดหัวตาราง
                tree.heading("concert_name", text="ชื่อคอนเสิร์ต", anchor="center")
                tree.heading("total_tickets", text="จำนวนตั๋ว", anchor="center")
                tree.heading("total_sales", text="รายได้รวม (บาท)", anchor="center")
                
                # กำหนดขนาดคอลัมน์
                tree.column("concert_name", width=200, anchor="center")
                tree.column("total_tickets", width=100, anchor="center")
                tree.column("total_sales", width=150, anchor="center")
                
                # เพิ่มข้อมูลลงในตาราง
                for concert, tickets, revenue in sales_data:
                    tree.insert("", "end", values=(concert, tickets, f"{revenue:,.0f}"))
                
                tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Buttons for Admin tasks
        add_button = tk.Button(admin_frame, text="🎵\n\nAdd Concert", font=("Arial", 15), bg="green", fg="white", command=add_concert)
        add_button.place(relx=0.2, rely=0.5, anchor="center", width=200, height=200)

        edit_button = tk.Button(admin_frame, text="✏️\n\nEdit Concert", font=("Arial", 15), bg="orange", fg="white", command=edit_concert)
        edit_button.place(relx=0.4, rely=0.5, anchor="center", width=200, height=200)

        delete_button = tk.Button(admin_frame, text="❌\n\nDelete Concert", font=("Arial", 15), bg="red", fg="white", command=delete_concert)
        delete_button.place(relx=0.6, rely=0.5, anchor="center", width=200, height=200)
        
        sales_button = tk.Button(admin_frame, text="📊\n\nSales Summary", font=("Arial", 15), bg="blue", fg="white", command=show_sales_summary)
        sales_button.place(relx=0.8, rely=0.5, anchor="center", width=200, height=200)

        return admin_frame

    # Verify admin login function
    def verify_admin_login(username, password):
        if username == "admingp" and password == "13911464":
            return True
        return False

    # เมนูบาร์
    def create_menu(user):  # รับค่า user เป็นพารามิเตอร์
        menu_frame = tk.Frame(root, bg="gray")
        menu_frame.pack(side='top', fill='x')

        home_button = tk.Button(menu_frame, text="🏠 Home", command=lambda: home_page_screen(user), bg="gray", fg="black", font=("Helvetica", 12, "bold"), borderwidth=0)
        home_button.pack(side='left', padx=10, pady=5)

        profile_button = tk.Button(menu_frame, text="👤 Profile", command=lambda: profile_screen(user), bg="gray", fg="black", font=("Helvetica", 12, "bold"), borderwidth=0)
        profile_button.pack(side='left', padx=10, pady=5)

        aboutus_button = tk.Button(menu_frame, text="ℹ️ About Us", command=lambda: about_us_screen(user), bg="gray", fg="black", font=("Helvetica", 12, "bold"), borderwidth=0)
        aboutus_button.pack(side='right', padx=10, pady=5)

        logout_button = tk.Button(menu_frame, text="🚪 Logout", command=logout, bg="gray", fg="black", font=("Helvetica", 12, "bold"), borderwidth=0)
        logout_button.pack(side='right', padx=10, pady=5)

        
    def about_us_screen(user):  
        clear_frame()  # ล้างหน้าจอเพื่อแสดงหน้าสำหรับ About Us
        create_menu(user)  # ส่ง user ไปยัง create_menu()

        # สร้าง Frame สำหรับ About Us
        about_us_frame = tk.Frame(root, bg="black", width=400, height=600)
        about_us_frame.pack(fill='both', expand=True)

        # กำหนดขนาดของรูปภาพที่ต้องการ
        image_width = 1200  # กำหนดความกว้างของภาพที่ต้องการ
        image_height = 700  # กำหนดความสูงของภาพที่ต้องการ

        # โหลดรูปภาพพื้นหลัง (ใช้ไฟล์ของคุณเอง)
        img = Image.open("ab.png")  # ใช้ไฟล์ ab.png
        img = img.resize((image_width, image_height), Image.Resampling.LANCZOS)  # ปรับขนาดภาพตามที่กำหนด
        img = ImageTk.PhotoImage(img)  # แปลงภาพให้สามารถใช้ใน Tkinter

        # แสดงภาพใน Label
        background_label = tk.Label(about_us_frame, image=img)
        background_label.place(relx=0.5, rely=0.5, anchor="center")  # วางรูปภาพในตำแหน่งกลางของ Frame

        # ให้ `img` ใช้งานได้จนจบฟังก์ชัน (ป้องกันการเก็บค่าเป็น garbage collection)
        about_us_frame.img = img

    # ฟังก์ชัน Logout
    def logout():
        clear_frame()
        root.config(menu="")
        create_login_frame()


    def create_login_frame():
        login_frame = tk.Frame(root, bg="black")
        login_frame.place(relwidth=1, relheight=1)

        load_background_image(login_frame, "1.png")

        username_entry = tk.Entry(login_frame, width=25, font=("Arial", 22))
        username_entry.place(relx=0.15, rely=0.47, anchor=tk.W)

        password_entry = tk.Entry(login_frame, show="*", width=25, font=("Arial", 22))
        password_entry.place(relx=0.15, rely=0.6, anchor=tk.W)

        show_icon = PhotoImage(file="eye_open.png").subsample(10, 10)  # ไอคอนตาเปิด
        hide_icon = PhotoImage(file="eye_closed.png").subsample(10, 10)  # ไอคอนตาปิด

        def toggle_password():
            if password_entry.cget("show") == "*":
                password_entry.config(show="")
                toggle_button.config(image=hide_icon)
            else:
                password_entry.config(show="*")
                toggle_button.config(image=show_icon)

                 # เพิ่มปุ่ม Show/Hide Password
        toggle_button = tk.Button(login_frame, image=show_icon,  bd=0, command=toggle_password)
        toggle_button.image = show_icon  # ป้องกันภาพถูกลบโดย garbage collector
        toggle_button.place(relx=0.392, rely=0.6, anchor="w", width=30, height=30)

        def login():
            username = username_entry.get()
            password = password_entry.get()

            # Check if the user is an admin
            if verify_admin_login(username, password):
                messagebox.showinfo("Login Success", "Welcome Admin")
                admin_panel = create_admin_panel(root)  # Admin Panel
                show_frame(admin_panel)  # Show the Admin Panel
            else:
                # Check if it's a regular user
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Login Success", "Welcome back, " + username)
                    print(f"User {username} logged in successfully")
                    home_page_screen(user)  
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")



        login_button = tk.Button(login_frame, text="LOGIN", font=("Arial", 14), bg="red", fg="white", width=25, height=2, command=login)
        login_button.place(relx=0.28, rely=0.75, anchor=tk.CENTER)

        register_button = tk.Button(login_frame, text="REGISTER", font=("Arial", 14), fg="black", bg="white", width=25, height=2, command=lambda: create_register_frame())
        register_button.place(relx=0.70, rely=0.72, anchor=tk.CENTER)

        return login_frame

    # หน้าจอ Register
    def create_register_frame():
        register_frame = tk.Frame(root, bg="black")
        register_frame.place(relwidth=1, relheight=1)

        load_background_image(register_frame, "2.png")

        fields = ["USERNAME", "PASSWORD", "FIRSTNAME", "LASTNAME"]
        entries = {}

        for idx, field in enumerate(fields):
            entry = tk.Entry(register_frame, width=20, font=("Arial", 22))
            entry.place(relx=0.6, rely=0.348 + idx * 0.1, anchor=tk.W)
            entries[field] = entry

        birthdate_entry = DateEntry(
            register_frame,
            width=20,
            background="darkblue",
            foreground="white",
            font=("Arial", 20),
            justify="center",
            selectmode="day",
            state="readonly",
        )

        # ปรับตำแหน่ง DateEntry
        birthdate_entry.place(relx=0.6, rely=0.748, anchor=tk.W)

        # ตั้งค่า popup calendar ให้แสดงด้านบน
        def adjust_popup(*args):
            # ตรวจสอบว่าปฏิทินเปิดอยู่หรือไม่
            popup_widget = birthdate_entry._top_cal
            if popup_widget:
                # คำนวณตำแหน่งใหม่ให้อยู่ด้านบน
                x = birthdate_entry.winfo_rootx()
                y = birthdate_entry.winfo_rooty() - popup_widget.winfo_reqheight()  # ย้ายปฏิทินขึ้นไปด้านบน
                popup_widget.geometry(f"+{x}+{y}")

        # เชื่อมฟังก์ชัน adjust_popup กับการเปิดปฏิทิน
        birthdate_entry.bind("<<DateEntrySelected>>", adjust_popup)
        birthdate_entry.bind("<FocusIn>", adjust_popup)  # ปรับตำแหน่งทุกครั้งเมื่อโฟกัส

        def register():
            username = entries["USERNAME"].get()
            password = entries["PASSWORD"].get()
            firstname = entries["FIRSTNAME"].get()
            lastname = entries["LASTNAME"].get()
            birthdate = birthdate_entry.get()  # ได้ค่าเป็น "YYYY-MM-DD"

            # เช็คว่ามีข้อมูลครบหรือไม่
            if not username or not password or not firstname or not lastname or not birthdate:
                messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
                return

            # ตรวจสอบความยาวของรหัสผ่าน
            if len(password) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters")
                return

            # ตรวจสอบว่ามี username อยู่แล้วหรือไม่
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "Username already exists")
                return

            # เพิ่มข้อมูลลงในฐานข้อมูล
            try:
                cursor.execute(
                    "INSERT INTO users (username, password, firstname, lastname, birthdate) VALUES (?, ?, ?, ?, ?)",
                    (username, password, firstname, lastname, birthdate)
                )
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                show_frame(login_frame)  # กลับไปหน้า login
            except Exception as e:
                messagebox.showerror("Database Error", f"เกิดข้อผิดพลาด: {e}")

        # ปุ่มลงทะเบียน
        register_button = tk.Button(register_frame, text="REGISTER", font=("Arial", 14), bg="red", fg="white", width=25, height=2, command=register)
        register_button.place(relx=0.7, rely=0.82, anchor=tk.CENTER)

        back_to_login_button = tk.Button(register_frame, text="BACK TO LOGIN", font=("Arial", 14), bg="red", fg="white", width=25, height=2, command=lambda: show_frame(login_frame))
        back_to_login_button.place(relx=0.28, rely=0.75, anchor=tk.CENTER)



        return register_frame
        
    # ลิสต์คอนเสิร์ตตัวอย่าง
    list_con = [
    {"name": "Maroon 5", "date": "2026-02-03", "location": "Bangkok", "price": [6_500, 5_500, 4_500, 3_500, 2_500], "image": "maroon_5.png", "Map": "Maroon_5_map.png"},
    {"name": "2025 YUGYEOM TOUR [TRUSTY] ENCORE IN BANGKOK", "date": "2026-03-15", "location": "Bangkok", "price": [4_900, 3_900, 2_900], "image": "YUGYEOM_TOUR.jpg", "Map": "YUGYEOM_TOUR_map.png"},
    {"name": "keshi : REQUIEM TOUR IN BANGKOK", "date": "2026-02-26", "location": "Bangkok", "price": [3_800, 3_300, 2_800], "image": "keshi.png", "Map": "keshi_map.png"},
    {"name": "JO1 WORLD TOUR JO1DER SHOW 2025 'WHEREVER WE ARE' IN BANGKOK", "date": "2025-12-07", "location": "Bangkok", "price": [4_000, 3_500, 3_000], "image": "jo1_world_tour.jpg", "Map": "JO1_WORLD_TOUR_map.png"},
    {"name": "bodyslam Power of The B-Side Concert", "date": "2026-04-04", "location": "Bangkok", "price": [6_500, 5_000, 4_500, 4_000, 3_500, 2_500], "image": "bodyslam.jpg", "Map": "bodyslam_map.jpg"},
    {"name": "กาลครั้ง 8 หนีกรุง INFUNITY", "date": "2026-03-01", "location": "Chonburi", "price": [1_800, 950], "image": "gaanlakrang_neekrung.png", "Map": "gaanlakrang_neekrung_map.png"},
    {"name": "Bodyslam Live At Omar's Tent Club", "date": "2026-03-06", "location": "Krabi", "price": [1_100, 22_000, 25_000], "image": "bodyslam_live_at.png", "Map": "bodyslam_live_at_map.png"},
]


    def home_page_screen(user):
        clear_frame()  # ลบเฟรมเก่าทั้งหมด
        create_menu(user)

        # ดึงข้อมูลจากฐานข้อมูล
        conn = sqlite3.connect("concert.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, date, location, price, image FROM concerts")
        db_concerts = [dict(zip(["name", "date", "location", "price", "image"], row)) for row in cursor.fetchall()]
        conn.close()

        all_concerts = list_con + db_concerts  # ใช้ list_con ที่อัปเดตล่าสุด

        tk.Label(root, text="BOOKING TICKETS!!!", font=("Arial", 26, "bold"), bg="black", fg="red").pack(pady=8)

        # ✅ Scrollable Frame
        frame_container = tk.Frame(root, bg="black")
        frame_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame_container, bg="black", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)

        canvas.configure(yscrollcommand=scrollbar.set)  # ต้องมาก่อน create_window
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content_frame = tk.Frame(canvas, bg="black")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # ตั้งค่าให้เฟรมอยู่ตรงกลาง
        COLUMNS = 3
        for i in range(COLUMNS):
            content_frame.columnconfigure(i, weight=1)

        FRAME_WIDTH = root.winfo_width() // COLUMNS - 30  # ปรับขนาดตามหน้าต่าง
        FRAME_HEIGHT = 520  # กำหนดความสูงให้พอดี
        IMAGE_SIZE = (220, 220)

        row, col = 0, 0
        concert_widgets = []

        # เพิ่มการเช็คข้อมูลใหม่หลังจากแอดมินเพิ่มคอนเสิร์ต
        for concert in all_concerts:
            concert_frame = tk.Frame(content_frame, padx=10, pady=10, relief=tk.RIDGE, bd=2, bg="black", width=FRAME_WIDTH, height=FRAME_HEIGHT)
            concert_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            concert_frame.columnconfigure(0, weight=1)
            concert_frame.rowconfigure(0, minsize=60)   # ชื่อคอนเสิร์ต
            concert_frame.rowconfigure(1, minsize=220)  # รูปภาพ
            concert_frame.rowconfigure(2, minsize=90)   # รายละเอียด
            concert_frame.rowconfigure(3, minsize=110)  # ปุ่มกด

            name_label = tk.Label(concert_frame, text=concert["name"], font=("Arial", 15, "bold"), bg="black", fg="red", wraplength=FRAME_WIDTH, justify="center")
            name_label.grid(row=0, column=0, pady=5, sticky="nsew")

            if concert["image"]:
                try:
                    img = Image.open(concert["image"])
                    img.thumbnail(IMAGE_SIZE)
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(concert_frame, image=photo, bg="black")
                    img_label.image = photo
                    img_label.grid(row=1, column=0, pady=5, sticky="nsew")
                    img_label.bind("<Button-1>", lambda event, c=concert: book_ticket_screen(user, c))
                except:
                    tk.Label(concert_frame, text="Image not available", fg="red", bg="black").grid(row=1, column=0, pady=5, sticky="nsew")

            price_text = ""
            if isinstance(concert["price"], float):
                price_text = f"💰 : {concert['price']:,.0f} THB"  
            elif isinstance(concert["price"], int):
                price_text = f"💰 : {concert['price']:,.0f} THB"
            elif isinstance(concert["price"], list) or isinstance(concert["price"], tuple):
                # ถ้าราคาเป็น range (list หรือ tuple) แสดงช่วงราคา
                price_text = f"💰 : {min(concert['price']):,.0f} - {max(concert['price']):,.0f} THB"

            detail_text = f"📅 {concert['date']}\n📍 {concert['location']}\n{price_text}"
            detail_label = tk.Label(concert_frame, text=detail_text, font=("Arial", 13), bg="black", fg="white", justify="center")
            detail_label.grid(row=2, column=0, pady=5, sticky="nsew")

            book_button = tk.Button(concert_frame, text="🎟️ Book Now", bg="red", fg="white", font=("Arial", 14, "bold"), width=18, height=2, command=lambda c=concert: book_ticket_screen(user, c))
            book_button.grid(row=3, column=0, pady=10, sticky="s")

            concert_widgets.append(concert_frame)

            col += 1
            if col >= COLUMNS:
                col = 0
                row += 1

        # ลดแลคโดยอัปเดต Scrollable frame แบบประหยัดทรัพยากร
        content_frame.update_idletasks()
        canvas.update_idletasks()
        root.update_idletasks()  # บังคับอัปเดตขนาด UI
        canvas.config(scrollregion=canvas.bbox("all"))

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))  # อัปเดต scrollregion ใหม่

        content_frame.bind("<Configure>", update_scroll_region)

        root.after(100, update_scroll_region)

        def on_mouse_wheel(event):
            if root.winfo_exists():
                if event.delta:  # Windows
                    canvas.yview_scroll(-1 * (event.delta // 120), "units")
                elif event.num == 4:  # Mac scroll up
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:  # Mac scroll down
                    canvas.yview_scroll(1, "units")

        canvas.bind("<MouseWheel>", on_mouse_wheel)  # Windows
        canvas.bind("<Button-4>", on_mouse_wheel)  # Mac scroll up
        canvas.bind("<Button-5>", on_mouse_wheel)  # Mac scroll down


    def book_ticket_screen(user, concert):
        if user is None or concert is None:
            messagebox.showerror("Error", "Invalid user or concert details.")
            return

        # ตรวจสอบค่าของ user และ concert
        print(f"user: {user}")
        print(f"concert: {concert}")

        clear_frame()
        create_menu(user)

        booking_frame = tk.Frame(root, bg="black", bd=5, relief="solid")
        booking_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(booking_frame, text="BOOKING TICKETS!!!", font=("Arial", 26, "bold"), bg="black", fg="red").pack(pady=20)
        tk.Label(booking_frame, text=f"Concert: {concert['name']}", font=("Arial", 16), bg="black", fg="white").pack()

        # เช็คว่าเป็นคอนเสิร์ตที่มีแผนผังที่นั่งหรือไม่
        try:
            if 'Map' in concert:  # ถ้ามีแผนผังที่นั่ง
                img = Image.open(concert['Map'])
            else:
                img = Image.open(concert['image'])

            # กำหนดขนาดสูงสุดที่ต้องการ (เช่น กว้าง 200px สูง 250px)
            max_width = 300
            max_height = 300

            # คำนวณอัตราส่วน
            width, height = img.size
            aspect_ratio = width / height

            # คำนวณขนาดใหม่ที่รักษาอัตราส่วน
            if width > height:
                new_width = max_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(new_height * aspect_ratio)

            # ปรับขนาดภาพ
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(booking_frame, image=img, bg="black")
            img_label.image = img  # เก็บการอ้างอิงของภาพไว้
            img_label.pack(pady=10)

        except Exception as e:
            print(f"Error loading image: {e}")
            tk.Label(booking_frame, text="No Image Available", font=("Arial", 12), bg="black", fg="white").pack()


        price = concert['price']
        if isinstance(price, list):  # ถ้าราคาเป็นลิสต์
            formatted_prices = [f"{price:,.0f}" for price in concert['price']]
            price_var = tk.StringVar(value=formatted_prices[0])  # ตั้งค่าเริ่มต้นเป็นราคาตัวแรกในลิสต์
            price_menu = tk.OptionMenu(booking_frame, price_var, *formatted_prices)
            price_menu.config(bg="black", fg="white", font=("Arial", 12))
            price_menu.pack()
        else:
            price_var = tk.StringVar(value=str(concert['price']))

        quantity_frame = tk.Frame(booking_frame, bg="black")
        quantity_frame.pack(pady=10)

        quantity_var = tk.IntVar(value=1)
        quantity_entry = tk.Entry(quantity_frame, textvariable=quantity_var, width=5, font=("Arial", 14))
        quantity_entry.pack(side="left", padx=10)

        decrease_button = tk.Button(quantity_frame, text="-", command=lambda: quantity_var.set(quantity_var.get() - 1) if quantity_var.get() > 1 else None, bg="#f44336", fg="white", font=("Arial", 14, "bold"))
        decrease_button.pack(side="left", padx=10)

        increase_button = tk.Button(quantity_frame, text="+", command=lambda: quantity_var.set(quantity_var.get() + 1), bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
        increase_button.pack(side="right", padx=10)

        total_price_label = tk.Label(booking_frame, text="Total Price: ", font=("Arial", 16), bg="black", fg="white")
        total_price_label.pack(pady=10)

        def update_total_price(*args):
            try:
                # ลบคอมม่าออกจากราคาที่เลือก
                price_str = price_var.get().replace(',', '')  
                price = float(price_str)  # ใช้ float เพื่อจัดการกับราคาที่เป็นทศนิยม
                quantity = quantity_var.get()
                total_price = price * quantity
                # แปลงราคาทั้งหมดเป็นจำนวนเต็มและใส่คอมม่า
                formatted_total_price = "{:,.0f}".format(total_price)  # ไม่มีทศนิยมและคอมม่า
                total_price_label.config(text=f"Total Price: {formatted_total_price} THB")
                print(f"Total Price: {formatted_total_price}")  # แสดงราคาทั้งหมดที่คำนวณได้
            except ValueError:
                messagebox.showerror("Invalid Input", "Please select a valid price and quantity.")


        price_var.trace_add("write", update_total_price)
        quantity_var.trace_add("write", update_total_price)

        def book_ticket():
            try:
                quantity = quantity_var.get()
                if quantity <= 0:
                    messagebox.showerror("Invalid Input", "Quantity must be greater than 0.")
                    return

                price_str = price_var.get().replace(',', '')  # ลบคอมม่า
                price = float(price_str)  # ใช้ float เพื่อจัดการกับราคาที่เป็นทศนิยม
                total_price = price * quantity
                formatted_total_price = "{:,.0f}".format(total_price)

                confirm = messagebox.askyesno("Confirm Booking", 
                                            f"Are you sure you want to book {quantity} ticket(s) for {concert['name']}?\nTotal price: {formatted_total_price} THB")

                if confirm:
                    try:
                        # ตรวจสอบว่า concert['name'] หรือ user[0] เป็น None หรือไม่
                        if user[0] is None or concert['name'] is None:
                            messagebox.showerror("Error", "Invalid user or concert details.")
                            return

                        qr_code_path = f"qr_{user[0]}_{concert['name'].replace(' ', '_')}.png"
                        qr_data = f"Payment for {concert['name']} - {quantity} ticket(s) - {formatted_total_price} THB"
                        qr = qrcode.QRCode(version=1, box_size=10, border=4)
                        qr.add_data(qr_data)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill="black", back_color="white")
                        qr_img.save(qr_code_path)
                        print(f"QR Code saved at: {qr_code_path}")  # แสดงเส้นทางการบันทึกคิวอาร์โค้ด
                    except Exception as e:
                        messagebox.showerror("QR Code Error", f"Error generating QR code: {e}")
                        print(f"Error generating QR code: {e}")
                        return

                    try:
                        # บันทึกข้อมูลลงในฐานข้อมูล
                        cursor.execute("""INSERT INTO tickets (user_id, concert_name, ticket_type, quantity, price, qr_code)
                                        VALUES (?, ?, ?, ?, ?, ?)""", 
                                        (user[0], concert['name'], "Regular", quantity, total_price, qr_code_path))
                        conn.commit()
                        print("Data inserted into database successfully")  # ข้อมูลถูกบันทึกสำเร็จ
                    except Exception as e:
                        messagebox.showerror("Database Error", f"Error inserting data into database: {e}")
                        print(f"Database error: {e}")
                        return

                    # เปลี่ยนไปหน้าจอการชำระเงิน
                    payment_screen(user, concert, quantity, total_price, qr_code_path)

            except ValueError as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                print(f"An error occurred: {str(e)}")

        tk.Button(booking_frame, text="Confirm Booking", command=book_ticket, bg="#4CAF50", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(booking_frame, text="Cancel", command=lambda: home_page_screen(user), bg="#f44336", fg="white", font=("Arial", 14, "bold")).pack()

        def payment_screen(user, concert, quantity, total_price, qr_code_path):
                clear_frame()
                create_menu(user)  # เพิ่มเมนูในหน้าจอชำระเงิน
                tk.Label(root, text="PAYMENT", font=("Arial", 26, "bold"), bg="white").pack(pady=20)

                tk.Label(root, text=f"Concert: {concert['name']}", font=("Arial", 16), bg="white").pack()
                tk.Label(root, text=f"Tickets: {quantity}", bg="white").pack()
                formatted_price = "{:,}".format(total_price)
                tk.Label(root, text=f"Total Price: {formatted_price} THB", bg="white").pack(pady=10)

                # แสดง QR Code
                qr_img = Image.open(qr_code_path)
                qr_img = qr_img.resize((300, 300))  # ปรับขนาดรูป QR Code
                qr_img = ImageTk.PhotoImage(qr_img)
                qr_label = tk.Label(root, image=qr_img, bg="white")
                qr_label.image = qr_img
                qr_label.pack(pady=20)

                # ฟังก์ชันยืนยันการชำระเงิน
                def confirm_payment():
                    messagebox.showinfo("Payment Successful", "Your payment has been processed successfully!")
                    profile_screen(user)  # กลับไปที่หน้าโปรไฟล์

                tk.Button(root, text="Confirm Payment", command=confirm_payment, bg="#4CAF50", fg="white").pack(pady=10)
                tk.Button(root, text="Cancel", command=lambda: home_page_screen(user), bg="#f44336", fg="white").pack()

    def show_concert_details(concert_name, qr_code_path, user):
                top = tk.Toplevel()
                top.title(f"{concert_name} Details")
                
                # ขนาดของหน้าต่าง
                top.geometry("300x400")

                # แสดงชื่อคอนเสิร์ต
                tk.Label(top, text=concert_name, font=("Arial", 18, "bold")).pack(pady=20)

                # แสดงชื่อผู้ใช้
                tk.Label(top, text=f"User: {user[3]} {user[4]}", font=("Arial", 12), fg="black").pack(pady=10)

                # แสดง QR Code
                try:
                    qr_img = Image.open(qr_code_path)  # ใช้ path ของ QR Code ที่เก็บไว้ใน database
                    qr_img = qr_img.resize((150, 150))  # ขนาด QR Code
                    qr_img = ImageTk.PhotoImage(qr_img)
                    qr_label = tk.Label(top, image=qr_img)
                    qr_label.image = qr_img
                    qr_label.pack(pady=20)
                except FileNotFoundError:
                    tk.Label(top, text="QR Code Not Found", fg="red").pack()

                top.mainloop()

        # ฟังก์ชันโปรไฟล์
    def profile_screen(user): 
        clear_frame()
        create_menu(user)  # สร้างเมนูด้านบน

        tk.Label(root, text="YOUR PROFILE", font=("Arial", 26, "bold"), bg="black", fg="red").pack(pady=20)

        scrollable_frame = tk.Frame(root, bg="black")
        scrollable_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(scrollable_frame, bg="black", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        profile_content = tk.Frame(canvas, bg="black")
        canvas.create_window((0, 0), window=profile_content, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        profile_content.bind("<Configure>", on_frame_configure)

        profile_frame = tk.Frame(profile_content, bg="red", width=400, height=300)
        profile_frame.pack(pady=20)

        try:
            img = Image.open("profile_placeholder.png")  
            img = img.resize((150, 150))  
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(profile_frame, image=img, bg="red")
            img_label.image = img
            img_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(profile_frame, text="Image not found", bg="red", fg="white").pack()

        tk.Label(profile_frame, text=f"{user[3]} {user[4]}", font=("Arial", 18, "bold"), bg="red", fg="white").pack()
        tk.Label(profile_frame, text=f"Username: {user[1]}", font=("Arial", 12), bg="red", fg="white").pack()

        tk.Button(profile_frame, text="Edit Profile", command=lambda: edit_profile_screen(user), bg="white", fg="black").pack(pady=10)

        tk.Label(profile_content, text="YOUR TICKETS", font=("Arial", 16, "bold"), bg="black", fg="white").pack(pady=10)

        conn = sqlite3.connect("concert.db")
        cursor = conn.cursor()
        cursor.execute("SELECT concert_name, ticket_type, quantity, price, qr_code FROM tickets WHERE user_id=?", (user[0],))
        tickets = cursor.fetchall()

        cursor.execute("SELECT name, image FROM concerts")
        concerts_data = cursor.fetchall()
        all_concerts = {concert[0]: concert[1] for concert in concerts_data}
        conn.close()
        
        # อ่านจาก list_con ด้วย
        for concert in list_con:
            concert_name = concert["name"]
            concert_image = concert["image"]
            # ถ้า database ไม่มีคอนเสิร์ตนี้ ให้เพิ่มจาก list_con
            if concert_name not in all_concerts:
                all_concerts[concert_name] = concert_image

        if tickets:
            for ticket in tickets:
                ticket_frame = tk.Frame(profile_content, bg="white", padx=10, pady=5)
                ticket_frame.pack(fill="x", pady=5)

                concert_name, ticket_type, quantity, price, qr_code_path = ticket
                concert_img_label = tk.Label(ticket_frame, bg="white")
                concert_img_label.grid(row=0, column=0, rowspan=3, padx=10)

                if concert_name in all_concerts:
                    concert_img_path = all_concerts[concert_name]
                    try:
                        concert_img = Image.open(concert_img_path)
                        concert_img = concert_img.resize((100, 100))
                        concert_img = ImageTk.PhotoImage(concert_img)
                        concert_img_label.config(image=concert_img)
                        concert_img_label.image = concert_img
                    except FileNotFoundError:
                        concert_img_label.config(text="Image Not Found", fg="red")

                formatted_price = f"{int(price):,}"

                tk.Label(ticket_frame, text=f"{concert_name}", font=("Arial", 14, "bold"), bg="white", fg="black").grid(row=0, column=1, sticky="w")
                tk.Label(ticket_frame, text=f" Quantity: {quantity} | Total: {formatted_price} THB", bg="white", fg="black").grid(row=1, column=1, sticky="w")

                qr_code_label = tk.Label(ticket_frame, bg="white")
                qr_code_label.grid(row=0, column=2, rowspan=3, padx=10)

                if qr_code_path:
                    try:
                        qr_img = Image.open(qr_code_path)
                        qr_img = qr_img.resize((100, 100))
                        qr_img = ImageTk.PhotoImage(qr_img)
                        qr_code_label.config(image=qr_img)
                        qr_code_label.image = qr_img
                    except FileNotFoundError:
                        qr_code_label.config(text="QR Not Found", fg="red")

                tk.Button(ticket_frame, text="View Details", command=lambda c=concert_name, qr=qr_code_path, u=user: show_concert_details(c, qr, u), bg="#FF4D4D", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3, activebackground="#FF6666", activeforeground="white").grid(row=2, column=1, pady=5)
        else:
            tk.Label(profile_content, text="No tickets booked yet.", font=("Arial", 14, "italic"), bg="black", fg="white").pack()

        # ฟังก์ชันแก้ไขโปรไฟล์
    def edit_profile_screen(user):
            clear_frame()
            create_menu(user)
            tk.Label(root, text="EDIT PROFILE", font=("Arial", 26, "bold"), bg="black", fg="red").pack(pady=20)

            tk.Label(root, text="Firstname", bg="black", fg="white").pack()
            firstname_entry = tk.Entry(root, fg="black", bg="white")
            firstname_entry.insert(0, user[3])
            firstname_entry.pack()

            tk.Label(root, text="Lastname", bg="black", fg="white").pack()
            lastname_entry = tk.Entry(root, fg="black", bg="white")
            lastname_entry.insert(0, user[4])
            lastname_entry.pack()

            def save_profile():
                conn = sqlite3.connect("concert.db")
                cursor = conn.cursor()
                firstname = firstname_entry.get()
                lastname = lastname_entry.get()

                cursor.execute("UPDATE users SET firstname=?, lastname=? WHERE id=?", (firstname, lastname, user[0]))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Profile updated!")
                profile_screen(user)

            tk.Button(root, text="Save", command=save_profile, bg="#4CAF50", fg="white").pack(pady=10)
            tk.Button(root, text="Cancel", command=lambda: profile_screen(user), bg="red", fg="white").pack(pady=10)


    login_frame = create_login_frame()

    show_frame(login_frame)

    root.mainloop()

main_window()