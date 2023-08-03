import customtkinter as ctk
import serial
import json
from opcua import Server
# Global variables
machineState, remoteState, alarmdesc = "startup", "", ""
id, newid, sentid = 0, "", ""
changecmd, cmd = "", ""
limitLO, limitHI, measure_res, measure_stat = "", "", "", ""
# OPC UA Server setup
server = Server()
url = "opc.tcp://10.108.133.57:4840"
server.set_endpoint(url)
name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)
node = server.get_objects_node()
Param = node.add_object(addspace, "Parameters")
opcua_machineState = Param.add_variable(addspace, "appState", machineState)
opcua_cmd = Param.add_variable(addspace, "cmd", "")
opcua_cmd.set_writable()
opcua_id = Param.add_variable(addspace, "id", "")
opcua_id.set_writable()
opcua_changecmd = Param.add_variable(addspace, "change", "")
opcua_changecmd.set_writable()
opcua_remoteState = Param.add_variable(addspace, "remoteState", remoteState)
opcua_remoteState.set_writable()
opc_sentid = Param.add_variable(addspace, "ID FROM ACTION: ", sentid)
opc_sentid.set_writable()
opcmeasure_res = Param.add_variable(addspace, "voltage:", measure_res)
opcmeasure_res.set_writable()
opcmeasure_stat = Param.add_variable(addspace, "measure stat:", measure_stat)
opcmeasure_stat.set_writable()
opclimitHI = Param.add_variable(addspace, "high limit:", limitHI)
opclimitHI.set_writable()
opclimitLO = Param.add_variable(addspace, "low limit:", limitLO)
opclimitLO.set_writable()
opcalarmdesc = Param.add_variable(addspace, "alarm desc: ", alarmdesc)
server.start()
("OPC UA server started at {}".format(url))
#declaration + creatig server in the uaexpert

def open_new_window():
    global check
    check = "n"
    #this check will be needed later in the code, lines around 440
    global machineState
    def on_main():
        global machineState, alarmdesc, id, opcua_machineState, opcua_cmd, cmd, stat
        cmd = ""
        #declarations :D
        opcua_machineState.set_value(machineState)
        opcalarmdesc.set_value(alarmdesc)
        cmd = opcua_cmd.get_value()
        statcmd = ctk.CTkLabel(
            master=new_window,
            text=cmd,
            font=("Garamond", 20, "bold")
        )
        statcmd.pack()
        statcmd.place(x=90, y=320)
        #the cmd is a value that use can type from uaexpert and it willbe shown here
        print(cmd)
        print(machineState)
        statc = ctk.CTkLabel(
            master=new_window,
            text="           ",
            font=("Garamond", 20, "bold")
        )
        statc.pack()
        statc.place(x=90, y=110)
        stat = ctk.CTkLabel(
            master=new_window,
            text=machineState + " " + alarmdesc,
            font=("Garamond", 20, "bold")
        )
        stat.pack()
        stat.place(x=90, y=110)
        new_window.after(100, on_main)
    global new_window
    new_window = ctk.CTk()
    new_window.geometry("600x700")
    new_window.title("Julia's app")
    new_window.configure(bg="#303030")
    #creating a window for the app
    sleeplab = ctk.CTkLabel(
        master=new_window,
        text="SLEEP TIME:",
        font=("Arial", 14),
    )
    sleeplab.pack(pady=10)
    sleeplab.place(x=10, y=280)
    timecycle_var = ctk.StringVar(master=new_window)
    timecycle = ctk.CTkEntry(
        master=new_window,
        placeholder_text="5.00",
        textvariable=timecycle_var,
    )
    timecycle.pack(pady=10)
    timecycle.place(x=180, y=280)
    typelab = ctk.CTkLabel(
        master=new_window,
        text="PICK THE TYPE:",
        font=("Arial", 14)
    )
    typelab.pack(pady=10)
    typelab.place(x=10, y=210)
    combobox = ctk.CTkComboBox(master=new_window,
)
    combobox.set("pick the option")
    combobox.pack(pady=10)
    combobox.place(x=180, y=210)
    buttons = ctk.CTkButton(
        master=new_window,
        text="Start",
        bg_color="transparent",
        fg_color="transparent",
        height=40,
        width=120,
        font=("Arial", 18, "bold"),
        border_width=0
    )
    buttons.place(x=450, y=55)
    timecycle.configure(state="disabled")
    combobox.configure(state="disabled")
    buttons.configure(state="disabled")
    global resetbut
    def resetbut():
        #function for button which will reset the window
        global alarmdesc, machineState
        machineState = "startup"
        alarmdesc = " "
        new_window.destroy()
        open_new_window()

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
    #reset button
    res = ctk.CTkLabel(
        master=new_window,
        text="RESULT:",
        font=("Garamond", 20, "bold")
    )
    res.pack()
    res.place(x=20, y=25)
    try:
        #here is checking if the file limity.txty exists and more declarations :')
        global checkfile
        file_path = 'limity.txt'
        with open(file_path, 'r') as file:
            lines = file.readlines()
        global port, mode ,configs, limitHI_list, limitLO_list
        file_path = 'limity.txt'
        with open(file_path, 'r') as file:
            lines = file.readlines()

        configs = []
        port = ""
        limitHI_list = []
        limitLO_list = []
        mode = ""

        for line in lines:
            #check each line of the code and sorts by its name to diffrent arrays
            if line.startswith("portName"):
                port = line.split("=")[1].strip()
            elif line.startswith("[config"):
                config = line.strip()[1:-1]
                configs.append(config)
            elif "limitHI" in line:
                limitHI = line.split("=")[1].strip()
                limitHI_list.append(limitHI)
            elif "limitLO" in line:
                limitLO = line.split("=")[1].strip()
                limitLO_list.append(limitLO)
            elif line.startswith("mode"):
                mode = line.split("=")[1].strip()

        print("Configs:", configs)
        print("limitHI:", limitHI_list)
        print("limitLO:", limitLO_list)
        print("Port:", port)
        print("Mode:", mode)
        #prints are for checking if everything went smoothly in the console
        checkfile = "yes"
    except:
        machineState = "alarm"
        global alarmdesc
        alarmdesc = "couldnt find the limity.txt file"
        checkfile = "no"
    def checktheidle():
        #this if the stateofmach function connected with the device then doidle gets the vlue yes
        global doidle, machineState, alarmdesc
        if doidle == "yes":
            machineState = "idle"
            alarmdesc = "         "
            if mode != "remote":
                #in the remote mode combobx, sleep time, start button are supposed to be disabled
                combobox.configure(state="normal")
                combobox.configure(command=combobox_callback)
                combobox.configure(values=configs)
                machineState = "idle"
                alarmdesc = "        "
        else:
            machineState = "alarm"
            alarmdesc = "couldnt connect with the device"
    def stateofmach():
        global machineState, doidle, alarmdesc
        def send_command(arduino, command):
            arduino.write(command)
        try:
            arduino = serial.Serial(port, 115200, timeout=5)
            command1 = b'{"cmd":"smDis","val":"0.000000","ID":"0"}\n'
            send_command(arduino, command1)
            response = arduino.readline().strip().decode()
            arduino.close()
            print("Arduino response:", response)
            response_dict = json.loads(response)
            if "ack" in response_dict and response_dict["ack"] == "OK" and response_dict.get("ID") == "0":
                # this if basically means, "if the response for command1 was same as it was supposed to be"
                doidle = "yes"
                checktheidle()
            else:
                doidle = "no"
                machineState = "alarm"
                alarmdesc = "the device did not answer correctly"
                checktheidle()
        except:
            doidle = "no"
            machineState = "alarm"
            alarmdesc = "couldnt connect with the device"
            checktheidle()
        print(doidle)

    def measure_power():
        global machineState
        def send_command(arduino, command):
            arduino.write(command)

        def check_arduino_voltage():

            def voltch():
                global response, timecycle_var, alarmdesc, machineState, arduino
                arduino = serial.Serial(port, 115200, timeout=5)
                machineState = "busy"
                alarmdesc = "  "
                command1 = b'{"cmd":"smDis","val":"0.000000","ID":"0"}\n'
                command2 = b'{"cmd":"readV","val":"0.000000","ID":"3"}\n'
                send_command(arduino, command1)
                response = arduino.readline().strip().decode()
                try:
                    response_dict = json.loads(response)
                    if "ack" in response_dict and response_dict["ack"] == "OK" and response_dict.get("ID") == "0":
                        send_command(arduino, command2)
                        machineState = "busy"
                        alarmdesc = "   "
                        response = arduino.readline().strip().decode()
                        print("Arduino response:", response)
                        response_dict = json.loads(response)
                        if "ack" in response_dict and response_dict["ack"] == "OK" and response_dict.get("ID") == "3":
                            voltage_str = response_dict.get("val", "Unknown")
                            voltage = float(voltage_str)
                            arduino.close()
                            machineState = "ready"
                            return voltage
                        else:
                            machineState = "alarm"
                            alarmdesc = "not able to get the V value"
                            arduino.close()
                            return "No acknowledgment received for command2 or incorrect ID."
                    else:
                        machineState = "alarm"
                        alarmdesc = "wrong response recieved"
                        arduino.close()
                        return "No acknowledgment received for command1 or incorrect ID."
                except (json.JSONDecodeError, ValueError):
                    machineState = "alarm"
                    alarmdesc = "json decode error or value error"
                    return "Invalid response received."
            global timecycle_var, machineState
            return voltch()
        voltage = check_arduino_voltage()
        return voltage
    ctk.set_appearance_mode("System")

    def startsit():
        #function after clickingthe start button
        global machineState, timecycle_var, alarmdesc
        machineState = "busy"
        alarmdesc = "  "
        print(machineState)
        try:
            voltage = measure_power()
            if voltage is not None:
                opcmeasure_res.set_value(voltage)
                if float(voltage) < float(lowval) or float(voltage) > float(highval):
                    opcmeasure_stat.set_value("failed")
                    result_text = ctk.CTkLabel(
                        master=new_window,
                        text=f"Battery Voltage: {voltage} V \n failed",
                        font=("Arial", 14),
                        bg_color="#DE3C4B",
                        fg_color="#DE3C4B",
                    )
                    result_text.place(x=40, y=75)
                else:
                    opcmeasure_stat.set_value("passed")
                    result_text = ctk.CTkLabel(
                        master=new_window,
                        text=f"Battery Voltage: {voltage} V \n passed",
                        font=("Arial", 14),
                        bg_color="#58BC82",
                        fg_color="#58BC82",
                    )
                    result_text.place(x=40, y=75)
            else:
                result_text = ctk.CTkLabel(
                    master=new_window,
                    text="Failed to measure battery voltage.",
                    font=("Arial", 14),
                )
                result_text.place(x=40, y=75)
            # new_window.mainloop()
        except Exception as e:
            machineState = "alarm"
            alarmdesc = str(e)
            print(alarmdesc)
    def asd():
        #function if someone types sleep time
        global machineState, timecycle_var
        machineState = "busy"
        stat.configure(text=machineState)
        print(machineState, "NEWFUN")
        try:
            timec = int(timecycle_var.get())
            new_window.after(timec, startsit)
        except:
            print(timecycle_var.get())
            print("EXCEPT FOUND")
            new_window.after(0, startsit)
    def combobox_callback(choice):
        #fucntion after picking any choice from the combobox
        global indx, lowval, highval, mode, machineState, timecycle_var
        machineState = "ready"
        indx = configs.index(choice)
        print(indx)
        lowval = float(limitLO_list[indx])
        highval = float(limitHI_list[indx])
        print(choice, lowval, highval)
        lowvaluetext = ctk.CTkLabel(
            master=new_window,
            text="low value:  " + str(lowval),
            font=("Arial", 14),
        )
        lowvaluetext.place(x=20, y=140)
        opclimitLO.set_value(lowval)
        opclimitHI.set_value(highval)
        highvaluetext = ctk.CTkLabel(
            master=new_window,
            text="high value:  " + str(highval),
            font=("Arial", 14),
        )
        highvaluetext.place(x=20, y=160)
        if mode != "remote":
            global timecycle_var
            timecycle_var = ctk.StringVar()
            timecycle.configure(state="normal")
            timecycle.configure(textvariable=timecycle_var)
            buttons.configure(state="normal")
            buttons.configure(command=asd)
    def opcfunc():
        #function for the remote mode
        global remoteState, mode, id, opcua_id, opcua_changecmd, changecmd, oldid, choice, counter, newid, opcua_remoteState, remoteState, opc_sentid, check
        id = opcua_id.get_value()
        if mode == "remote":
            if id != "":
                #before user types the id into the ua expert it is  string without anything
                    if newid != id:
                        newid = id
                        changecmd = opcua_changecmd.get_value()
                        if changecmd == "cfg1" or changecmd == "cfg2" or changecmd == "cfg3" or changecmd == "measure" or changecmd == "reset":
                            #checking if the command that user typed is correct
                            remoteState = "ok"
                            opcua_remoteState.set_value(remoteState)
                            opc_sentid.set_value(id)
                            if changecmd == "measure":
                                if check == "y":
                                    startsit()
                                else:
                                    global machineState, alarmdesc
                                    remoteState = "error"
                                    opcua_remoteState.set_value(remoteState)
                                    alarmdesc = "you have configure the device first!"
                            else:
                                alarmdesc = "                                                      "
                                if changecmd == "cfg1":
                                    choice = "config0"
                                    check = "y"
                                    combobox_callback(choice)
                                elif changecmd == "cfg2":
                                    choice = "config1"
                                    check = "y"
                                    combobox_callback(choice)
                                elif changecmd == "cfg3":
                                    choice = "config2"
                                    check = "y"
                                    combobox_callback(choice)
                                elif changecmd == "reset":
                                    resetbut()
                        else:
                            remoteState = "error"
                            opcua_remoteState.set_value(remoteState)
                            opc_sentid.set_value(id)
        new_window.after(100, opcfunc)
    new_window.after(100, on_main)
    new_window.after(100, opcfunc)
    if checkfile == "yes":
        new_window.after(3000, stateofmach)
    new_window.mainloop()
    server.stop()
    print("OPC UA server stopped")
open_new_window()
