from opcua import Client
import serial
import customtkinter as ctk

url = "opc.tcp://10.108.133.57:4840"
client = Client(url)
client.connect()
print("Client connected")

def opennew():
    global ids
    ids = 1
    def resetbut():
        global ids
        global measurebutton
        measurebutton.configure(state="disabled")
        changes.set_value("reset")
        sentid.set_value(ids)
        ids = ids + 1
    def takedat():
        global voltage, lowlimit, highlimit, remotestate, idfromaction, measurestate, appstate, alarmdescrip, changes, \
            sentid, check
        volt = client.get_node("ns=2; i=8")
        sentid = client.get_node("ns=2; i=4")
        changes = client.get_node("ns=2; i=5")
        lowli = client.get_node("ns=2; i=11")
        highli = client.get_node("ns=2; i=10")
        remotestat = client.get_node("ns=2; i=6")
        measurestat = client.get_node("ns=2; i=9")
        idfromact = client.get_node("ns=2; i=7")
        appstat = client.get_node("ns=2; i=2")
        alarmdesc = client.get_node("ns=2; i=12")
        voltage = volt.get_value()
        lowlimit = lowli.get_value()
        highlimit = highli.get_value()
        remotestate = remotestat.get_value()
        measurestate = measurestat.get_value()
        idfromaction = idfromact.get_value()
        appstate = appstat.get_value()
        alarmdescrip = alarmdesc.get_value()
        lowvaluetext = ctk.CTkLabel(
            master=new_window,
            text="low value:  " + str(lowlimit),
            font=("Arial", 14),
        )
        lowvaluetext.place(x=20, y=140)
        highvaluetext = ctk.CTkLabel(
            master=new_window,
            text="high value:  " + str(highlimit),
            font=("Arial", 14),
        )
        highvaluetext.place(x=20, y=160)
        global result_text
        if measurestate == "failed":
            result_text = ctk.CTkLabel(
                master=new_window,
                text=f"Battery Voltage: {voltage} V \n failed",
                font=("Arial", 14),
                bg_color="#DE3C4B",
                fg_color="#DE3C4B",
            )
            result_text.place(x=130, y=175)
        elif measurestate == "passed":
            result_text = ctk.CTkLabel(
                master=new_window,
                text=f"Battery Voltage: {voltage} V \n passed",
                font=("Arial", 14),
                bg_color="#58BC82",
                fg_color="#58BC82",
            )
            result_text.place(x=130, y=175)
        new_window.after(100, takedat)
    def cfg1s():
        measurebutton.configure(state="normal")
        global ids
        changes.set_value("cfg1")
        sentid.set_value(ids)
        ids = ids + 1
    def cfg2s():
        measurebutton.configure(state="normal")
        global ids
        changes.set_value("cfg2")
        sentid.set_value(ids)
        ids = ids + 1
    def cfg3s():
        measurebutton.configure(state="normal")
        global ids
        changes.set_value("cfg3")
        sentid.set_value(ids)
        ids = ids + 1
    def check():
        global ids
        changes.set_value("measure")
        sentid.set_value(ids)
        ids = ids + 1
    global new_window, cfg1, cfg2, measurebutton, cfg3
    new_window = ctk.CTk()
    new_window.geometry("600x700")
    new_window.title("Client app")
    new_window.configure(bg="#303030")
    cfg1 = ctk.CTkButton(
        master=new_window,
        text="cfg1",
        bg_color="transparent",
        fg_color="transparent",
        height=40,
        width=120,
        font=("Arial", 18, "bold"),
        border_width=0,
        command=cfg1s
    )
    cfg1.place(x=0, y=55)
    cfg1.configure(state="normal")
    cfg2 = ctk.CTkButton(
        master=new_window,
        text="cfg2",
        bg_color="transparent",
        fg_color="transparent",
        height=40,
        width=120,
        font=("Arial", 18, "bold"),
        border_width=0,
        command=cfg2s
    )
    cfg2.place(x=120, y=55)
    cfg2.configure(state="normal")
    cfg3 = ctk.CTkButton(
        master=new_window,
        text="cfg3",
        bg_color="transparent",
        fg_color="transparent",
        height=40,
        width=120,
        font=("Arial", 18, "bold"),
        border_width=0,
        command=cfg3s
    )
    cfg3.place(x=270, y=55)
    cfg3.configure(state="normal")
    measurebutton = ctk.CTkButton(
        master=new_window,
        text="measure",
        bg_color="transparent",
        fg_color="transparent",
        height=40,
        width=120,
        font=("Arial", 18, "bold"),
        border_width=0,
        command=check
    )
    measurebutton.place(x=450, y=55)
    measurebutton.configure(state="disabled")
    buttonr = ctk.CTkButton(
        master=new_window,
        text="Reset",
        command=resetbut,
        bg_color="transparent",
        fg_color="transparent",
        height=40,
        width=120,
        font=("Arial", 18, "bold"),
        border_width=0
    )
    buttonr.place(x=450, y=115)
    new_window.after(100, takedat)
    new_window.mainloop()
opennew()
