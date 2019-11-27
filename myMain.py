# import all modules
from tkinter import *
import sqlite3, datetime, math, os, random
from tkinter import messagebox
import threading


conn = sqlite3.connect("G:\mini3\store.db")
c = conn.cursor()
# date
# date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date = datetime.datetime.now().date()

# temporary lists .......
products_list = []
products_price = []
products_quantity = []
product_id = []

# list for labels....
label_lists = []

username = 'admin'


class Application:
    def __init__(self, master):
        self.master = master

        # creating the frames
        self.left = Frame(master, width =700, height =768, bg='white')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=666, height=768, bg='lightblue')
        self.right.pack(side=RIGHT)

        # components
        self.heading = Label(self.left, bg='white', text='Students Choice Stationary', font=('arial 40 bold'))
        self.heading.place(x=0, y=0)

        self.user = Label(self.right, text= 'Admin: ' + str(username), font='arial 16 bold', fg='white', bg='lightblue')
        self.user.place(x=200, y=0)

        self.logout = Button(self.right, text='Logout', cursor='hand2', width=22, height=2, bg='lightblue', fg='white', command=self.logout)
        self.logout.place(x=500, y=0)

        self.date_l = Label(self.right, text="Date: " + str(date), font='arial 16 italic', bg='lightblue', fg='white')
        self.date_l.place(x=0, y=0)

        # table invoice ......
        self.tproduct = Label(self.right, text= 'Products', font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tproduct.place(x=0, y=60)

        self.tquantity = Label(self.right, text='Quantity', font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tquantity.place(x=300, y=60)
        self.tquantity.focus()

        self.tamount = Label(self.right, text='Amount', font=('arial 18 bold'), bg='lightblue', fg='white')
        self.tamount.place(x=500, y=60)

        # entries.....
        self.enterid = Label(self.left, text="Enter Product's ID", font=('arial 18 bold'), bg='white')
        self.enterid.place(x=0, y=80)

        self.enterid_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.enterid_e.place(x=190, y=80)
        self.enterid_e.focus()

        # buttons......

        self.search_btn = Button(self.left, text='Search', cursor='hand2', width=22, height=2, bg='lightblue', command=self.ajax)
        self.search_btn.place(x=350, y=120)

        # fill later by function ajax...
        self.productname = Label(self.left, text='', font=('arial 18 bold'), bg='white', fg='steelblue')
        self.productname.place(x=0, y=250)

        self.pprice = Label(self.left, text='', font=('arial 18 bold'), bg='white', fg='steelblue')
        self.pprice.place(x=0, y=290)

        # total label.....
        self.total_l = Label(self.right, text='', font=('arial 40 bold'), bg='lightblue', fg='white')
        self.total_l.place(x=0, y=600)

    def logout(self):
        for i in root.winfo_children():
            i.destroy()
        Login(root)

    def ajax(self):
        self.get_id = self.enterid_e.get()
        # get the products info with that id and fill in the labels above....
        query = "SELECT * FROM inventory WHERE id=?"
        result = c.execute(query, (self.get_id, ))
        for self.r in result:
            self.get_id = self.r[0]
            self.get_name = self.r[1]
            self.get_price = self.r[4]
            self.get_stock = self.r[2]

        self.productname.configure(text="Product's Name: " + str(self.get_name))
        self.pprice.configure(text="Price: INR. " + str(self.get_price))

        # create the quantity and the discount label
        self.quantity_l = Label(self.left, text='Enter Quantity:', font=('arial 18 bold'), bg='white')
        self.quantity_l.place(x=0, y=370)

        self.quantity_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.quantity_e.place(x=190, y=370)
        self.quantity_e.focus()
        # discount ......
        self.discount_l = Label(self.left, text='Enter Discount:', font=('arial 18 bold'), bg='white')
        self.discount_l.place(x=0, y=410)

        self.discount_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.discount_e.place(x=190, y=410)
        self.discount_e.insert(END, 0)

        # add to cart
        self.add_to_cart_btn = Button(self.left, text='Add to Cart', cursor="hand2", width=22, height=2, bg='lightblue', command=self.add_cart)
        self.add_to_cart_btn.place(x=350, y=450)

        # generate bill and change
        self.change_1 = Label(self.left, text='Cash:', font=('arial 18 bold'), bg='white')
        self.change_1.place(x=0, y=550)

        self.change_e = Entry(self.left, width=25, font='arial 18 bold', bg='lightblue')
        self.change_e.place(x=190, y=550)

        # button change
        self.change_btn = Button(self.left, text='Calculate Change', cursor="hand2", width=22, height=2, bg='lightblue', command=self.change)
        self.change_btn.place(x=350, y=590)

        # generate bill button
        self.bill_btn = Button(self.left, text='Generate Bill',  cursor="hand2", font='arial 10 bold',  width=80, height=2, bg='lightblue', fg='black', command=self.generate_bill)
        self.bill_btn.place(x=30, y=640)

        # update database....
        self.update = Button(self.left, text='Update Products', cursor="hand2", font='arial 12 bold', width=25, height=2, bg='lightblue', fg='black', command=self.update_products)
        self.update.place(x=70, y=690)

        # add to database......
        self.add_db = Button(self.left, text='Add Products', width=25,  cursor="hand2", font='arial 12 bold', height=2, bg='lightblue', fg='black', command=self.add_products)
        self.add_db.place(x=350, y=690)


    def add_cart(self):
        # get the value from database
        self.quantity_value = int(self.quantity_e.get())
        if self.quantity_value > int(self.get_stock):
            messagebox.showinfo('Error', 'Not that many products in our inventory')

        else:
            # calculate final price
            self.final_price = float(self.quantity_value) * float(self.get_price) - float(str(self.discount_e.get()))

            products_list.append(self.get_name)
            products_price.append(self.final_price)
            products_quantity.append(self.quantity_value)
            product_id.append(self.get_id)

            # print(products_list)
            # print(products_price)
            # print(products_quantity)

            self.x_index = 300
            self.y_index = 100
            self.counter = 0
            for self.p in products_list:
                self.tempname = Label(self.right, text=str(products_list[self.counter]), font=('arial 18 bold'), bg='lightblue', fg='white')
                self.tempname.place(x=0, y=self.y_index)
                label_lists.append(self.tempname)

                self.tempqt = Label(self.right, text=str(products_quantity[self.counter]), font=('arial 18 bold'), bg='lightblue',
                                      fg='white')
                self.tempqt.place(x=300, y=self.y_index)
                label_lists.append(self.tempqt)

                self.tempprice = Label(self.right, text=str(products_price[self.counter]), font='arial 18 bold', bg='lightblue',
                                      fg='white')
                self.tempprice.place(x=500, y=self.y_index)
                label_lists.append(self.tempprice)

                self.y_index +=40
                self.counter += 1

                # total configuration
                self.total_l.configure(text='Total: INR. ' + str(sum(products_price)))

                # clear the window......
                # self.quantity_l.place_forget()
                # self.quantity_e.place_forget()
                # self.discount_l.place_forget()
                # self.discount_e.place_forget()
                # self.productname.configure(text='')
                # self.tempprice.configure(text='')
                # self.add_to_cart_btn.destroy()

                # autofocus to enter id .....
                self.enterid_e.focus()
                self.enterid_e.delete(0, END)

    def change(self):
        # get the amount given by the customer and the amount generated by the the computer
        self.amount_given = float(self.change_e.get())
        self.our_total = float(sum(products_price))

        self.to_give = self.amount_given - self.our_total

        # label change .....
        self.c_amount = Label(self.left, text="Change: INR. " + str(self.to_give), font=('arial 18 bold'), fg='red', bg='white')
        self.c_amount.place(x=0, y=600)

    def generate_bill(self):
        # create the bill before updating......
        directory = "G:/mini3/Invoice/" + str(date) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Templates for the bills
        company = "\t\t\t\tStudent Choice Stationary.\n"
        address = "\t\t\t\tShirpur, India.\n"
        phone = "\t\t\t\tMobile No: 9977842528.\n"
        sample = "\t\t\t\t\tInvoice.\n"
        dt = "\t\t\t\t" + str(date)
        table_header = "\n\n\t\t=====================================================\n\t\t\tSN.\tProducts\t\tQty\t\tAmount\n\t\t====================================================="
        final = company + address + phone + sample + dt + "\n" + table_header

        # open the file......
        file_name = str(directory) + str(random.randrange(5000, 10000)) + ".rtf"
        f = open(file_name, 'w')
        f.write(final)
        # fill the dynamic data.....
        r = 1
        i = 0
        for t in products_list:
            f.write("\n\t\t\t" + str(r) + "\t" + str(products_list[i] + ".......")[:7] + "\t\t" + str(products_quantity[i]) + "\t\t" + str(products_price[i]))
            i += 1
            r += 1
        teller = "Prasoon"
        f.write("\n\n\t\t\tTotal: INR. " + str(sum(products_price)))
        f.write("\n\n\t\t\tChange: INR. " + str(str(self.to_give)))
        f.write("\n\t\t\tThanks for shopping with us")
        f.write("\n\t\t\tYou served by " + teller)
        f.close()
        # decrease the stock......
        self.x = 0
        initial = "SELECT * FROM inventory WHERE id=?"
        result = c.execute(initial, (product_id[self.x], ))
        for i in products_list:
            for r in result:
                self.old_stock = r[2]
            self.new_stock = int(self.old_stock) - int(products_quantity[self.x])

            # updating the stock .......
            sql = "UPDATE inventory SET stock=? WHERE id=?"
            c.execute(sql, (self.new_stock, product_id[self.x]))
            conn.commit()

            # insert into trasanction table.......
            sql2 = "INSERT INTO transactions (product_name, quantity, amount, date)VALUES(?,?,?,?)"
            trans = (products_list[self.x], products_quantity[self.x], products_price[self.x], date)
            c.execute(sql2, trans)
            conn.commit()
            self.x += 1

        for a in label_lists:
            a.destroy()

        del(products_list[:])
        del (product_id[:])
        del (products_quantity[:])
        del (products_price[:])

        self.total_l.configure(text='')
        self.enterid_e.focus()
        self.enterid_e.delete(0, END)
        self.c_amount.configure(text='')
        self.change_e.delete(0, END)
        messagebox.showinfo('Success', 'Done everything')

    def add_products(self):
        for i in root.winfo_children():
            i.destroy()
        Database(root)

    def update_products(self):
        for i in root.winfo_children():
            i.destroy()
        UpdateProducts(root)


# update class......

result = c.execute("SELECT Max(id) FROM inventory")
for r in result:
    id = r[0]


class UpdateProducts:
    def __init__(self, master):
        self.master = master
        self.heading = Label(master, text='Update Products', font='arial 40 bold', fg='steelblue', bg='#d9d9d9')
        self.heading.place(x=400, y=0)

        # label and entry for id
        self.Id_l = Label(master, text="Enter Id", font='arial 18 bold', bg='#d9d9d9')
        self.Id_l.place(x=0, y=70)

        self.Id_e = Entry(master, font='arial 18 bold', width=10, bg='white')
        self.Id_e.place(x=380, y=70)

        self.btn_search = Button(master, text='Search', width=15, height=2, bg='lightblue', command=self.search)
        self.btn_search.place(x=550, y=70)

        # labels and entries for the window

        self.name_l = Label(master, text='Enter Product Name', font='arial 18 bold', bg='#d9d9d9')
        self.name_l.place(x=0, y=120)

        self.stock_l = Label(master, text='Enter Stock', font='arial 18 bold', bg='#d9d9d9')
        self.stock_l.place(x=0, y=170)

        self.cp_l = Label(master, text='Enter Cost Price', font='arial 18 bold', bg='#d9d9d9')
        self.cp_l.place(x=0, y=220)

        self.sp_l = Label(master, text='Enter Selling Price', font='arial 18 bold', bg='#d9d9d9')
        self.sp_l.place(x=0, y=270)

        self.totalcp_l = Label(master, text='Enter Total Cost Price', font='arial 18 bold', bg='#d9d9d9')
        self.totalcp_l.place(x=0, y=320)

        self.totalsp_l = Label(master, text='Enter Total Selling Price', font='arial 18 bold', bg='#d9d9d9')
        self.totalsp_l.place(x=0, y=370)

        self.vendor_l = Label(master, text='Enter Vendor Name', font='arial 18 bold', bg='#d9d9d9')
        self.vendor_l.place(x=0, y=420)

        self.vendor_phone_l = Label(master, text='Enter Vendor Phone Number', font='arial 18 bold', bg='#d9d9d9')
        self.vendor_phone_l.place(x=0, y=470)

        # entries for the label....
        self.name_e = Entry(master, width=25, font='arial 18 bold')
        self.name_e.place(x=380, y=120)

        self.stock_e = Entry(master, width=25, font='arial 18 bold')
        self.stock_e.place(x=380, y=170)

        self.cp_e = Entry(master, width=25, font='arial 18 bold')
        self.cp_e.place(x=380, y=220)

        self.sp_e = Entry(master, width=25, font='arial 18 bold')
        self.sp_e.place(x=380, y=270)

        self.totalcp_e = Entry(master, width=25, font='arial 18 bold')
        self.totalcp_e.place(x=380, y=320)

        self.totalsp_e = Entry(master, width=25, font='arial 18 bold')
        self.totalsp_e.place(x=380, y=370)

        self.vendor_e = Entry(master, width=25, font='arial 18 bold')
        self.vendor_e.place(x=380, y=420)

        self.vendor_phone_e = Entry(master, width=25, font='arial 18 bold')
        self.vendor_phone_e.place(x=380, y=470)

        # button to add to database
        self.btn_add = Button(master, text='Update Database', width=25, height=2, bg='steelblue', fg='white',  cursor="hand2", command=self.update)
        self.btn_add.place(x=520, y=520)

        # button to go back to main application..........
        def back_to_main():
            for i in root.winfo_children():
                i.destroy()
            Application(root)
        self.btn_add = Button(master, text='Back', width=50, height=2, bg='#d9d9d9', fg='#4d4d1a', cursor="hand2", command=back_to_main)
        self.btn_add.place(x=350, y=620)

        # text box
        self.tbox = Text(master, width=60, height=17)
        self.tbox.place(x=750, y=70)
        self.tbox.insert(END, 'ID has reached up to:' + str(id))

    def search(self):
        sql = "SELECT * FROM inventory WHERE id=?"
        result = c.execute(sql, (self.Id_e.get(),))
        for r in result:
            self.n1 = r[1]  # name
            self.n2 = r[2]  # stock
            self.n3 = r[3]  # cp
            self.n4 = r[4]  # sp
            self.n5 = r[5]  # totalcp
            self.n6 = r[6]  # totalsp
            self.n7 = r[7]  # assumed_profit
            self.n8 = r[8]  # vendor
            self.n9 = r[9]  # vendor_phone

        conn.commit()
        # insert into the entries to update
        self.name_e.delete(0, END)
        self.name_e.insert(0, str(self.n1))

        self.stock_e.delete(0, END)
        self.stock_e.insert(0, str(self.n2))

        self.cp_e.delete(0, END)
        self.cp_e.insert(0, str(self.n3))

        self.sp_e.delete(0, END)
        self.sp_e.insert(0, str(self.n4))

        self.totalcp_e.delete(0, END)
        self.totalcp_e.insert(0, str(self.n5))

        self.totalsp_e.delete(0, END)
        self.totalsp_e.insert(0, str(self.n6))

        self.vendor_e.delete(0, END)
        self.vendor_e.insert(0, str(self.n8))

        self.vendor_phone_e.delete(0, END)
        self.vendor_phone_e.insert(0, str(self.n9))

    def update(self):
        # get the update values
        self.u1 = self.name_e.get()
        self.u2 = self.stock_e.get()
        self.u3 = self.cp_e.get()
        self.u4 = self.sp_e.get()
        self.u5 = self.totalcp_e.get()
        self.u6 = self.totalsp_e.get()
        self.u7 = self.vendor_e.get()
        self.u8 = self.vendor_phone_e.get()

        query = "UPDATE inventory SET name=?, stock=?, cp=?, sp=?, totalcp=?, totalsp=?, vendor=?, vendor_phoneno=? WHERE id=?"
        values = (self.u1, self.u2, self.u3, self.u4, self.u5, self.u6, self.u7, self.u8, self.Id_e.get())
        c.execute(query, values)
        conn.commit()
        messagebox.showinfo('success', 'updated database')

# add to database class ........


result = c.execute("SELECT Max(id) FROM inventory")
for r in result:
    id = r[0]


class Database:
    def __init__(self, master):
        self.master = master
        self.heading = Label(master, text='Add to Database', font=('arial 40 bold'), fg='steelblue', bg='#d9d9d9')
        self.heading.place(x=400, y=0)


        # labels and entries for the window
        self.name_l = Label(master, text='Enter Product Name', font='arial 18 bold', bg='#d9d9d9')
        self.name_l.place(x=0, y=70)

        self.stock_l = Label(master, text='Enter Stock', font='arial 18 bold', bg='#d9d9d9')
        self.stock_l.place(x=0, y=120)

        self.cp_l = Label(master, text='Enter Cost Price', font='arial 18 bold',bg='#d9d9d9')
        self.cp_l.place(x=0, y=170)

        self.sp_l = Label(master, text='Enter Selling Price', font='arial 18 bold',bg='#d9d9d9')
        self.sp_l.place(x=0, y=220)

        self.vendor_l = Label(master, text='Enter Vendor Name', font='arial 18 bold', bg='#d9d9d9')
        self.vendor_l.place(x=0, y=270)

        self.vendor_phone_l = Label(master, text='Enter Vendor Phone Number', font='arial 18 bold', bg='#d9d9d9')
        self.vendor_phone_l.place(x=0, y=320)

        self.id_l = Label(master, text='Enter ID', font='arial 18 bold', bg='#d9d9d9')
        self.id_l.place(x=0, y=370)

        # entries for the label....
        self.name_e = Entry(master, width=25, font='arial 18 bold')
        self.name_e.place(x=380, y=70)

        self.stock_e = Entry(master, width=25, font='arial 18 bold')
        self.stock_e.place(x=380, y=120)

        self.cp_e = Entry(master, width=25, font='arial 18 bold')
        self.cp_e.place(x=380, y=170)

        self.sp_e = Entry(master, width=25, font='arial 18 bold')
        self.sp_e.place(x=380, y=220)

        self.vendor_e = Entry(master, width=25, font='arial 18 bold')
        self.vendor_e.place(x=380, y=270)

        self.vendor_phone_e = Entry(master, width=25, font='arial 18 bold')
        self.vendor_phone_e.place(x=380, y=320)

        self.id_e = Entry(master, width=25, font=('arial 18 bold'))
        self.id_e.place(x=380, y=370)

        # button to add to database
        self.btn_add = Button(master, text='Add To Database', width=25, cursor="hand2", height=2, bg='steelblue', fg='white', command=self.get_items)
        self.btn_add.place(x=520, y=420)

        self.btn_clear = Button(master, text='Clear All Fields', width=18, height=2, bg='lightgreen',
                                fg='white',  cursor="hand2", command=self.clear_all)
        self.btn_clear.place(x=350, y=420)

        # button to go back to main application..........
        def back_to_main():
            for i in root.winfo_children():
                i.destroy()
            Application(root)
        self.btn_add = Button(master, text='Back', width=50, height=2, bg='#d9d9d9', fg='#4d4d1a', cursor="hand2", command=back_to_main)
        self.btn_add.place(x=350, y=520)

        # text box
        self.tbox = Text(master, width=60, height=20)
        self.tbox.place(x=750, y=70)
        self.tbox.insert(END, 'ID has reached up to:' + str(id))

    def get_items(self):
        self.name = self.name_e.get()
        self.stock = self.stock_e.get()
        self.cp = self.cp_e.get()
        self.sp = self.sp_e.get()
        self.vendor = self.vendor_e.get()
        self.vendor_phone = self.vendor_phone_e.get()

        # dynamic entries...

        self.totalcp = float(self.cp) * float(self.stock)
        self.totalsp = float(self.sp) * float(self.stock)
        self.assumed_profit = float(self.totalsp-self.totalcp)
        if self.name == ' ' or self.stock == ' ' or self.cp == ' ' or self.sp == ' ':
            messagebox.showinfo('Error', 'Please fill all entries')
        else:
            sql = "INSERT INTO inventory (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phoneno)VALUES(?,?,?,?,?,?,?,?,?)"
            parameters = (self.name, self.stock, self.cp, self.sp, self.totalcp, self.totalsp, self.assumed_profit, self.vendor, self.vendor_phone)
            c.execute(sql, parameters)
            conn.commit()

            # textbox insert
            self.tbox.insert(END, "\n\nInserted\t" + str(self.name) + "\tinto the database with code.\t" + str(self.id_e.get()))
            messagebox.showinfo('success!!', 'Successfully added to the database')

    def clear_all(self):
        num = id + 1
        self.name_e.delete(0, END)
        self.stock_e.delete(0, END)
        self.cp_e.delete(0, END)
        self.sp_e.delete(0, END)
        self.vendor_e.delete(0, END)
        self.vendor_phone_e.delete(0, END)
        self.id_e.delete(0, END)


'''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9' # X11 color: 'gray85'
_ana1color = '#d9d9d9' # X11 color: 'gray85'
_ana2color = '#d9d9d9' # X11 color: 'gray85'
font10 = "-family {Courier New} -size 10 -weight normal -slant"  \
    " roman -underline 0 -overstrike 0"
font11 = "-family {Kristen ITC} -size 34 -weight normal -slant"  \
    " roman -underline 0 -overstrike 0"
font12 = "-family {Segoe UI} -size 18 -weight normal -slant "  \
    "italic -underline 0 -overstrike 0"
font13 = "-family {Segoe UI} -size 14 -weight normal -slant "  \
    "roman -underline 0 -overstrike 0"
font17 = "-family {Gill Sans MT Condensed} -size 14 -weight "  \
    "normal -slant italic -underline 0 -overstrike 0"
font18 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
    "italic -underline 0 -overstrike 0"

class Login:
    def __init__(self, master):

        self.Frame1 = Frame(master)
        self.Frame1.place(relx=-0.02, rely=-0.02, relheight=0.21, relwidth=1.04)
        self.Frame1.configure(relief=FLAT, borderwidth="2", background="#0066ff", width=625)

        self.Label1 = Label(self.Frame1)
        self.Label1.place(relx=0.23, rely=0.38, height=41, width=700)
        self.Label1.configure(background="#0066ff", borderwidth="0", disabledforeground="#a3a3a3", font=font11, foreground="#ffffff", text='''Students Choice Stationary''', width=200)

        self.loginLabel = Label(master)
        self.loginLabel.place(relx=0.43, rely=0.30, height=31, width=94)
        self.loginLabel.configure(background="#d9d9d9", disabledforeground="#a3a3a3", font='arial 18 bold', foreground="#000000", width=94)
        self.loginLabel.configure(text='''Log In''')

        self.user_l = Label(master)
        self.user_l.place(relx=0.25, rely=0.40, height=31, width=144)
        self.user_l.configure(activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font='arial 18 bold')
        self.user_l.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black")
        self.user_l.configure(text='''Username''')

        self.txtuser_e = Entry(master)
        self.txtuser_e.place(relx=0.4, rely=0.40, height=30, relwidth=0.15)
        self.txtuser_e.configure(background="white", borderwidth="0", disabledforeground="#a3a3a3", font='arial 18 bold', foreground="#000000", highlightbackground="#d9d9d9")
        self.txtuser_e.configure(highlightcolor="black", insertbackground="black", selectbackground="#c4c4c4", selectforeground="black")

        self.pass_l = Label(master)
        self.pass_l.place(relx=0.25, rely=0.50, height=31, width=144)
        self.pass_l.configure(activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font='arial 18 bold')
        self.pass_l.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black")
        self.pass_l.configure(text='''Password''')

        self.txtpass_e = Entry(master, show='*')
        self.txtpass_e.place(relx=0.4, rely=0.50, height=30, relwidth=0.15)
        self.txtpass_e.configure(background="white", borderwidth="0", disabledforeground="#a3a3a3", font='arial 18 bold', foreground="#000000", highlightbackground="#d9d9d9")
        self.txtpass_e.configure(highlightcolor="black", insertbackground="black", selectbackground="#c4c4c4", selectforeground="black")

        self.BtnLogin = Button(master)
        self.BtnLogin.place(relx=0.42, rely=0.60, height=34, width=150)
        self.BtnLogin.configure(activebackground="#d9d9d9", activeforeground="#000000", font='arial 10 bold', background="#d9d9d9", cursor="hand2", disabledforeground="#a3a3a3")
        self.BtnLogin.configure(foreground="black", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", width=100)
        self.BtnLogin.configure(text='''Login''', command=self.login)

    def login(self):
        if self.txtuser_e.get() == username and self.txtpass_e.get() == 'admin':
            for i in root.winfo_children():
                i.destroy()
            Application(root)
        else:
            messagebox.showerror('Invalid credentials', 'Try again with the correct credentials!!!!')


root = Tk()
Login(root)
root.title("Students Choice Stationary")
root.iconbitmap(r'studentschoice.icon')
root.configure(background="#d9d9d9")
root.resizable(False, False)
root.geometry("1366x768+0+0")
root.mainloop()


