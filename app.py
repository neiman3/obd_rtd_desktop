import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import arduino_serial
import helper_funcs
from main import *


class CANFrame:

    def __init__(self):
        self.id = 0x7df
        self.length = 8
        self.data = (0, 0, 0, 0, 0, 0, 0, 0)

    def setData(self, data, pos=-1):
        if pos == -1:
            for index in range(len(data)):
                self.data = data[index]
        else:
            self.data[pos] = data

    def getData(self, pos=-1):
        if pos == -1:
            return self.data
        else:
            return self.data[pos]

    def reset(self):
        self.id = 0x7df
        self.length = 8
        self.data = (0, 0, 0, 0, 0, 0, 0, 0)


log_file_name = []

device_address = "/dev/cu.wchusbserial1441310"
arduino = None
outgoing_frame = CANFrame()

light_bg_color = "#eeeeee"
dark_bg_color = "#3f3d3f"

light_label_color = "#7a7a7a"


def errorBox(title, message):
    messagebox.showerror(title=title, message=message)


def createNewLogFile():
    new_log_file_name = filedialog.asksaveasfilename(initialdir="~/Documents", title="Create empty text file",
                                                     defaultextension="log")
    if new_log_file_name != '':
        open(new_log_file_name, 'a').close()
        logFileLabel.config(text=helper_funcs.shortenStringToFit(new_log_file_name, 55))
        log_file_name.append(new_log_file_name)
        writeToConsole("Created new log file at " + new_log_file_name)


def openLogFile():
    filename = filedialog.askopenfilename(initialdir="~/Documents", title="Choose an existing text file")
    if filename != '':
        logFileLabel.config(text=helper_funcs.shortenStringToFit(filename, 55))
        log_file_name.append(filename)


def deviceConnectionHandler():
    global arduino
    connectButton.config(text="Connecting...")
    root.update()

    arduino = arduino_serial.connect_device(device_address)
    sleep(0.25)

    if arduino is not None and arduino_serial.clean_string(arduino.readline()) == '0xA455':  # Device status is ready
        device_info = arduino_serial.receive_all_waiting_data(arduino)
        writeDeviceInfoTextLabels(device_info[0], device_info[1], device_info[2], device_info[3], device_info[4],
                                  device_info[5])
        arduino.flushInput()
        arduino.flushOutput()
        root.after(100, serial_monitor)
        writeToConsole("%s is connected." % device_info[0])
    else:
        writeToConsole("Failed to connect to USB device.")
        for widget in deviceStatusTableFrame.grid_slaves():
            widget.destroy()
        tk.Label(deviceStatusTableFrame, text="Device is not connected", bg=light_bg_color).grid()
        messagebox.showerror(title="Unable to connect to device", message="The device could not be found. Please"
                                                                          "troubleshoot your connection and try again.")
        connectButton.config(text="Connect to Device")
    root.update()
    root.minsize(max(root.winfo_width(), 600), max(root.winfo_height(), 400))
    connectButton.config(text="Connect to Device")


def writeDeviceInfoTextLabels(device_name, firmware_version, firmware_build, hardware_version, serial_number, mfg_date):
    for widget in deviceStatusTableFrame.grid_slaves():
        widget.destroy()
    tk.Label(deviceStatusTableFrame, text="Device name:", bg=light_bg_color).grid(row=0, column=0, sticky='e')
    tk.Label(deviceStatusTableFrame, text=device_name, bg=light_bg_color).grid(row=0, column=1, sticky='w')
    tk.Label(deviceStatusTableFrame, text="Firmware:", bg=light_bg_color).grid(row=1, column=0, sticky='e')
    tk.Label(deviceStatusTableFrame, text=firmware_version + " (b" + firmware_build + ")",
             bg=light_bg_color).grid(row=1, column=1, sticky='w')
    tk.Label(deviceStatusTableFrame, text="Hardware:", bg=light_bg_color).grid(row=2, column=0, sticky='e')
    tk.Label(deviceStatusTableFrame, text=hardware_version, bg=light_bg_color).grid(row=2, column=1, sticky='w')
    tk.Label(deviceStatusTableFrame, text="Serial number:", bg=light_bg_color).grid(row=3, column=0, sticky='e')
    tk.Label(deviceStatusTableFrame, text=serial_number, bg=light_bg_color).grid(row=3, column=1, sticky='w')
    tk.Label(deviceStatusTableFrame, text="Date of manufacture:", bg=light_bg_color).grid(row=4, column=0, sticky='e')
    tk.Label(deviceStatusTableFrame, text=mfg_date, bg=light_bg_color).grid(row=4, column=1, sticky='w')


def writeToConsole(string_to_write):
    string_to_write_2 = helper_funcs.timeNowString() + ': ' + string_to_write
    if log_file_name:
        try:
            file_obj = open(log_file_name[-1], 'a')
            file_obj.write(string_to_write_2 + '\n')
            file_obj.close()
        except:
            messagebox.showerror(title="Unable to write to log file", message="An error occured while writing to the "
                                                                              "log file.")
    consoleText.config(state='normal')
    if string_to_write != 'Session started.':
        consoleText.insert('end', '\n')
    consoleText.insert('end', string_to_write_2)
    consoleText.see("end")
    consoleText.config(state='disabled')


def sendOutgoingCANFrame():
    if arduino is None:
        writeToConsole("Could not send frame. There is no device connected.")
        return

    arduino.write(b'\x00')
    writeToConsole("Sent empty serial message.")


def updateOutgoingMessageSettings():
    return


def launchHelp():
    import webbrowser, os
    fn = os.path.realpath("help.html")
    webbrowser.open("file://" + fn, new=2)


def serial_monitor():
    global arduino
    if monitorEnabled.get() == 1:
        if arduino.inWaiting():
            msg = arduino_serial.clean_string(arduino.readline())
            writeToConsole('Arduino says \'%s\'' % msg)
            root.update()
    else:
        arduino.flushInput()
        arduino.flushOutput()
    root.after(100, serial_monitor)


root = tk.Tk()
root.config(bg=light_bg_color)
root.title("Neiman Diagnostics Utility")
root.rowconfigure(0, weight=4)
root.rowconfigure(1, weight=4)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
# root.geometry("700x500")
# root.resizable(False, False)


# Device status frame
deviceStatusFrame = tk.Frame(root, bg=light_bg_color)
deviceStatusFrame.grid(row=0, column=0, sticky="ew")
deviceStatusFrameLabel = tk.Label(deviceStatusFrame, text="Device info", fg=light_label_color, bg=light_bg_color)
deviceStatusFrameLabel.pack(side="top")
deviceStatusTableFrame = tk.Frame(deviceStatusFrame, bg=light_bg_color, padx=10, pady=10)
tk.Label(deviceStatusTableFrame, text="Device is not connected", bg=light_bg_color).grid()
deviceStatusTableFrame.pack()

# outgoingMessageFrame frame
outgoingMessageFrame = tk.Frame(root, bg="#FFFFFF")
tk.Label(outgoingMessageFrame, text="Send", fg=light_label_color).grid(row=0, sticky='w', padx=10, pady=10)

outgoingMessageContentsFrame = tk.Frame(outgoingMessageFrame)
outgoingMessageContentsFrame.grid(row=1, sticky='w', padx=10, pady=0)

tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=0)
outgoingMessageContentCANID = tk.StringVar()
outgoingMessageEntryCANID = tk.Entry(outgoingMessageContentsFrame, width=3, textvariable=outgoingMessageContentCANID)
outgoingMessageContentCANID.set("7DF")
outgoingMessageEntryCANID.grid(row=0, column=1)

outgoingMessageEntryFrameLength = tk.Entry(outgoingMessageContentsFrame, width=1, text="8")
outgoingMessageEntryFrameLength.grid(row=0, column=2)
outgoingMessageEntryFrameLength.insert(0, '8')
outgoingMessageEntryFrameLength.config(state='disabled')

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=3)
outgoingMessageContentByte1 = tk.StringVar()
outgoingMessageEntryByte1 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte1)
outgoingMessageContentByte1.set("02")
outgoingMessageEntryByte1.grid(row=0, column=4)

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=5)
outgoingMessageContentByte2 = tk.StringVar()
outgoingMessageEntryByte2 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte2)
outgoingMessageContentByte2.set("01")
outgoingMessageEntryByte2.grid(row=0, column=6)

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=7)
outgoingMessageContentByte3 = tk.StringVar()
outgoingMessageEntryByte3 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte3)
outgoingMessageContentByte3.set("PID")
outgoingMessageEntryByte3.grid(row=0, column=8)

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=9)
outgoingMessageContentByte4 = tk.StringVar()
outgoingMessageEntryByte4 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte4)
outgoingMessageContentByte4.set("00")
outgoingMessageEntryByte4.grid(row=0, column=10)

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=11)
outgoingMessageContentByte5 = tk.StringVar()
outgoingMessageEntryByte5 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte5)
outgoingMessageContentByte5.set("00")
outgoingMessageEntryByte5.grid(row=0, column=12)

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=13)
outgoingMessageContentByte6 = tk.StringVar()
outgoingMessageEntryByte6 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte6)
outgoingMessageContentByte6.set("00")
outgoingMessageEntryByte6.grid(row=0, column=14)

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=15)
outgoingMessageContentByte7 = tk.StringVar()
outgoingMessageEntryByte7 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte7)
outgoingMessageContentByte7.set("00")
outgoingMessageEntryByte7.grid(row=0, column=16)

# tk.Label(outgoingMessageContentsFrame, text="0x", padx=0, pady=0).grid(row=0, column=17)
outgoingMessageContentByte8 = tk.StringVar()
outgoingMessageEntryByte8 = tk.Entry(outgoingMessageContentsFrame, width=2, textvariable=outgoingMessageContentByte8)
outgoingMessageContentByte8.set("00")
outgoingMessageEntryByte8.grid(row=0, column=18)
outgoingMessageSendButton = tk.Button(outgoingMessageFrame,
                                      text="Send Frame",
                                      padx=10, pady=5, fg="black", bg="#263D42",
                                      command=sendOutgoingCANFrame)
outgoingMessageSendButton.grid(row=2, sticky='e', padx=10, pady=(3, 10))

tk.Label(outgoingMessageFrame, text="Receive", fg=light_label_color).grid(row=3, sticky='w', padx=10, pady=0)
monitorEnabled = tk.IntVar()
monitorEnabledCheckbox = tk.Checkbutton(outgoingMessageFrame, text="Enable monitor", variable=monitorEnabled, onvalue=1,
                                        offvalue=0, command=updateOutgoingMessageSettings)
monitorEnabledCheckbox.grid(row=4, sticky='w', padx=10, pady=(10, 3))
monitorEnabledCheckbox.select()
filterByCANID = tk.IntVar()
filterByCANIDCheckbox = tk.Checkbutton(outgoingMessageFrame, text="Filter incoming frames", variable=filterByCANID,
                                       onvalue=1, offvalue=0, command=updateOutgoingMessageSettings)
filterByCANIDCheckbox.grid(row=5, sticky='w', padx=10, pady=(0, 3))
filterSelectionFrame = tk.Frame(outgoingMessageFrame)
filterSelectionFrame.grid(row=6, sticky='e', padx=10, pady=0)
tk.Label(filterSelectionFrame, text="Filter by Frame ID: ").grid(row=0, column=0)
filterValue = tk.StringVar()
filterValueEntry = tk.Entry(filterSelectionFrame, width=5, textvariable=filterValue)
filterValueEntry.grid(row=0, column=1)

outgoingMessageContentsFrame.grid(row=1)
outgoingMessageFrame.grid(row=1, column=0, sticky='wens')

# Console log frame
consoleFrame = tk.Frame(root, padx=5, pady=5, bg=dark_bg_color)
consoleText = tk.Text(consoleFrame, bg=dark_bg_color, fg='white', borderwidth=10, wrap=tk.WORD)
consoleText.config(state='disabled')
# consoleText.grid(row=0, column=0, sticky='news')
consoleText.pack(expand=True, fill='both')
consoleFrame.grid(row=0, column=1, rowspan=2, sticky="news")

# Control button frame
controlButtonFrame = tk.Frame(root, padx=5, pady=5, bg=light_bg_color)
connectButton = tk.Button(controlButtonFrame,
                          text="Connect to Device",
                          padx=10, pady=5, fg="black", bg="#263D42",
                          command=deviceConnectionHandler)
# connectButton.pack(side="left")
connectButton.grid(row=0, column=0)
logFileButton = tk.Button(controlButtonFrame,
                          text="Choose Log File",
                          padx=10, pady=5, fg="black", bg="#263D42",
                          command=openLogFile)
# logFileButton.pack(side="left")
logFileButton.grid(row=0, column=1)
newLogFileButton = tk.Button(controlButtonFrame,
                             text="Create Log File",
                             padx=10, pady=5, fg="black", bg="#263D42",
                             command=createNewLogFile)
newLogFileButton.grid(row=0, column=2)

tk.Button(controlButtonFrame,
          text="Help",
          padx=10, pady=5, fg="black", bg="#263D42",
          command=launchHelp).grid(row=0, column=3, sticky='e')

logFileLabel = tk.Label(controlButtonFrame, text="No log file selected", bg=light_bg_color)
# logFileLabel.pack(side="left")
logFileLabel.grid(row=0, column=4)

controlButtonFrame.grid(row=2, column=0, columnspan=2, sticky='ew')

writeToConsole("Session started.")

root.update()
root.minsize(max(root.winfo_width(), 600), max(root.winfo_height(), 400))

root.mainloop()
