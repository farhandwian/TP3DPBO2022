from ast import excepthandler
from tkinter import *
from PIL import ImageTk, Image
from typing import final
import mysql.connector

# koneksi ke database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpw",
    database="dpbo"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)

    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(
        row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    # Input 3
    input_jk = StringVar(root)
    input_jk.set("0")
    values = {"Laki-Laki": "Laki-Laki",
              "Perempuan": "Perempuan"}

    label3 = Label(dframe, text="Jenis Kelamin").grid(
        row=2, column=0, sticky="w")
    i = 20
    for (text, value) in values.items():
        input3 = Radiobutton(dframe, text=text, variable=input_jk, value=value)
        input3.grid(row=2, column=1, padx=i, pady=10, sticky="w")
        i += 100

    # input 4
    options = ["Filsafat Meme", "Sastra Mesin",
               "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=3, column=0, sticky="w")
    dropdown = OptionMenu(dframe, input_jurusan, *options)
    dropdown.grid(row=3, column=1, padx=20, pady=10, sticky='w')

    # input 5
    # function checked value from checbox input
    def isChecked():
        hobby_value = []
        if(input_hobi1.get() == 1):
            hobby_value.append("Main Game")
        if(input_hobi2.get() == 1):
            hobby_value.append("Bernyanyi")
        if(input_hobi3.get() == 1):
            hobby_value.append("Jalan-Jalan")

        return hobby_value

    input_hobi1 = IntVar()
    input_hobi2 = IntVar()
    input_hobi3 = IntVar()

    label5 = Label(dframe, text="hobby").grid(row=4, column=0, sticky='w')

    # checbox form
    checkme = Checkbutton(dframe, text='Main Game',
                          variable=input_hobi1, onvalue=1, offvalue=0)
    checkme.grid(row=4, column=1, padx=20, pady=10, sticky='w')
    checkme = Checkbutton(dframe, text='Bernyanyi',
                          variable=input_hobi2, onvalue=1, offvalue=0)
    checkme.grid(row=4, column=1, padx=120, pady=10, sticky='w')
    checkme = Checkbutton(dframe, text='Jalan-Jalan',
                          variable=input_hobi3, onvalue=1, offvalue=0)
    checkme.grid(row=4, column=1, padx=220, pady=10, sticky='w')

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda: [insertData(
        top, input_nama, input_nim, input_jk, input_jurusan, isChecked()), top.withdraw()])
    btn_submit.grid(row=4, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Back", anchor="s",
                        command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=4, column=1, padx=10)

# Untuk memasukan data


def insertData(parent, p_nama, p_nim, p_gender, p_jurusan, p_hobby):
    flag_vld = 1
    top = Toplevel()

    # Get data
    hobby = ",".join(p_hobby)
    nama = p_nama.get()
    nim = p_nim.get()
    jurusan = p_jurusan.get()
    gender = p_gender.get()

    # validation form
    if((nama == "") or (nim == "") or (jurusan == "") or (gender == "0")):
        Label(top, text="Input Not Valid!", anchor="s",
              bg='yellow', fg='red').pack(padx=10, pady=10)
        btn_back = Button(top, text="Back", anchor="s", command=lambda: [
                          top.destroy(), parent.deiconify()])
        btn_back.pack(padx=10, pady=10)
    else:
        # Input data disini
        try:
            sql = "INSERT INTO mahasiswa (nim, nama, gender, jurusan, hobby) VALUES (%s, %s, %s, %s, %s)"
            val = (nim, nama, gender, jurusan, hobby)
            dbcursor.execute(sql, val)
            mydb.commit()

            Label(top, text="Insert success",
                  anchor="s", fg='green').pack(padx=10, pady=10)
            btn_ok = Button(top, text="Syap!", anchor="s", command=lambda: [
                            top.destroy(), root.deiconify()])
            btn_ok.pack(padx=10, pady=10)
        except mysql.connector.Error as err:
            # if query err
            Label(top, text="Insert Failed{}".format(
                err), anchor="s", fg='red').pack(padx=10, pady=10)
            btn_back = Button(top, text="Back", anchor="s", command=lambda: [
                              top.destroy(), parent.deiconify()])
            btn_back.pack(padx=10, pady=10)


# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()

    # Cancel Button
    btn_cancel = Button(frame, text="Back", anchor="w",
                        command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column=0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1,
                   relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1,
                   relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1,
                   relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1,
                   relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jurusan", borderwidth=1,
                   relief="solid", width=20, padx=5).grid(row=0, column=4)
    title5 = Label(tableFrame, text="hobby", borderwidth=1,
                   relief="solid", width=30, padx=5).grid(row=0, column=5)

    # Print content dari database ke dalam table
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1,
                       relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid",
                       height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid",
                       height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid",
                       height=2, width=20, padx=5).grid(row=i+1, column=3)
        label4 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid",
                       height=2, width=20, padx=5).grid(row=i+1, column=4)
        label4 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid",
                       height=2, width=30, padx=5).grid(row=i+1, column=5)
        i += 1


def viewFacility():
    global root
    root.withdraw()
    top = Toplevel()
    top.title("Semua Fasilitas Kampus")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()

    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w",
                        command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Fasilitas Kampus")
    head.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column=0, columnspan=2)

    current_value = IntVar(root)

    # titles
    titles = ["Lab Komputer", "Musholla", "Perpustakaan", "Ruang Kelas"]

    # images path
    images = ["project/labkomputer.jpg", "project/musholla.jpg",
              "project/perpustakaan.jpg", "project/ruangkelas.jpg"]

    def imageSlider():
        index = current_value.get()
        title = Label(frame, text=titles[index-1]
                      ).grid(row=2, column=0, columnspan=5)
        img = Image.open(images[index-1])
        img = img.resize((500, 500))
        img = ImageTk.PhotoImage(img)

        img_frame = Label(frame, image=img).grid(row=3, column=0, columnspan=5)
        img_frame.image = img

        horizontal = Scale(frame, from_=1, to=4, orient=HORIZONTAL,
                           variable=current_value).grid(row=4, column=0, columnspan=5)
        confirm_btn = Button(frame, text="Ganti Fasilitas", command=imageSlider).grid(
            row=5, column=0, columnspan=5)

    horizontal = Scale(frame, from_=1, to=4, orient=HORIZONTAL,
                       variable=current_value).grid(row=4, column=0, columnspan=5)
    confirm_btn = Button(frame, text="Ganti Fasilitas", command=imageSlider).grid(
        row=5, column=0, columnspan=5)

    title = Label(frame, text=titles[0]).grid(row=2, column=0, columnspan=5)
    img = Image.open(images[0])
    img = img.resize((500, 500))
    img = ImageTk.PhotoImage(img)

    img_frame = Label(frame, image=img).grid(row=3, column=0, columnspan=5)
    img_frame.image = img


# Dialog konfirmasi hapus semua data


def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)

    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green",
                     fg="white", command=lambda: [top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red",
                    fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI


def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)

    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white",
                     command=lambda: [top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white",
                    command=lambda: [top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)


def delAll():
    top = Toplevel()

    # Delete data disini
    try:
        dbcursor.execute("DELETE FROM mahasiswa")
        mydb.commit()

        Label(top, text="delete success",
              anchor="s", fg='green').pack(padx=10, pady=10)
        btn_ok = Button(top, text="OK!", command=top.destroy)
        btn_ok.pack(pady=20)
    except mysql.connector.Error as err:
        Label(top, text="delete fail {}".format(
            err), anchor="s", fg='red').pack(padx=10, pady=10)
        btn_ok = Button(top, text="Back", command=top.destroy)
        btn_ok.pack(pady=20)


# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa",
               command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa",
               command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa",
                 command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# View facility btn
b_facility = Button(buttonGroup, text="Semua Fasilitas Kampus",
                    command=viewFacility, width=30)
b_facility.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()
