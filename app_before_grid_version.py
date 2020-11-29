
import tkinter as tk
import helper_funcs
from tkinter import filedialog
from tkinter import messagebox
from main import *
from datetime import datetime

log_file_name = []


def timeNowString():
    return datetime.now().today()


def openLogFile():
    filename = filedialog.askopenfilename(initialdir="~/Documents", title="Select text file")
    logFileLabel.config(text=helper_funcs.shortenStringToFit(filename, 55))
    log_file_name.append(filename)


def deviceConnectionHandler():
    deviceStatusMainText.set("Connecting to device...")
    result = connectToDeviceProcess()
    if result:
        deviceStatusMainText.set(helper_funcs.shortenStringToFit(str(result), 18, 1) + " is connected")
    else:
        deviceStatusMainText.set('Device is not connected!')
        messagebox.showerror(title="Unable to connect to device", message="The device could not be found. Please"
                                                                          "troubleshoot your connection and try again.")


root = tk.Tk()
root.title("Scan Gauge Utility")
# root.geometry("700x500")
root.resizable(False, False)

canvas = tk.Canvas(root, height=500, width=700)
canvas.pack()

# Device status frame
deviceStatusFrame = tk.Frame(root, bg=light_bg_color)
deviceStatusFrame.place(relwidth=0.5, relheight=0.25)
deviceStatusFrameLabel = tk.Label(deviceStatusFrame, text="Device info", fg="#7a7a7a", bg=light_bg_color)
deviceStatusFrameLabel.pack(side="top")
deviceStatusMainText = tk.StringVar()
deviceStatusMainText.set("Device is not connected")
# deviceStatusMainTextLabel = tk.Label(deviceStatusFrame, text="Device is not connected", bg=light_bg_color)
deviceStatusMainTextLabel = tk.Label(deviceStatusFrame, textvariable=deviceStatusMainText, bg=light_bg_color)
deviceStatusMainTextLabel.pack()

# outgoingMessageFrame frame
# outgoingMessageFrame = tk.Frame(root, bg="#FF0000")
# outgoingMessageFrame.place(relwidth="0.5", relheight="0.75")

# Console log frame


# Control button frame
controlButtonFrame = tk.Frame(root, padx=5, pady=5, bg=light_bg_color)
connectButton = tk.Button(controlButtonFrame,
                          text="Connect to Device",
                          padx=10, pady=5, fg="black", bg="#263D42",
                          command=deviceConnectionHandler)
connectButton.pack(side="left")
logFileButton = tk.Button(controlButtonFrame,
                          text="Choose Log File",
                          padx=10, pady=5, fg="black", bg="#263D42",
                          command=openLogFile)
logFileButton.pack(side="left")
logFileLabel = tk.Label(controlButtonFrame, text="No log file selected", bg=light_bg_color)
logFileLabel.pack(side="left")
controlButtonFrame.pack(side="left")

root.mainloop()
