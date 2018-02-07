#!/usr/bin/python
##Writen By Lynton Brown
##This File will add a GUI for Temp Reading
import os
import time
from Tkinter import *

lock = 0
class GUI(object):
    
    def __init__(self, master):
        self.master = master
        master.title ("Temp")
        master.resizable(width=False, height=False)
        master.geometry('200x30')
        temp=Label(master, text= 'Temp', font= 'bold', justify='center')
        temp.grid()
        self.temp = temp
        self.update(lock)

    def exitFunctions(self):
        print "Exiting"
        lock = 1
        return self.update(lock)

    def read_temp(self):
        device_file = '/sys/bus/w1/devices/28-000008ab6b92/w1_slave'
        f = open(device_file, 'r')
        lines=f.readlines()
        f.close()
        equals_pos=lines[1].find('t=')
        if equals_pos !=-1:
            temp_string=lines[1][equals_pos+2:]
            temp_f=float(temp_string)/1000.0*(9.0/5.0)+32.0
            temp_c=float(temp_string)/1000.0
            time.sleep(0.01)
            return ('%.2f' %(temp_f)) ##Change to 'temp_c' if Celsius is Preferred

    def update(self, lock):
        if lock == 0:
            temp_f = self.read_temp()
            if (temp_f <= 72):
                self.temp.configure(text = temp_f, foreground='green')
            if (temp_f > 72):
                self.temp.configure(text = temp_f, foreground='red')
            if (temp_f <= 64):
                self.temp.configure(text = temp_f, foreground='blue')
            self.temp.update_idletasks()
            root.update()
            time.sleep(0.01)
            lock = 0
            return self.update(lock)
        elif lock == 1:
            root.destroy()
            exit()

def SystemCheck():
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')
    def WriteFile():
        menuItem = '/home/pi/.TempReading.py'
        if os.path.isfile(menuItem):
            print"File Present"
            return -1
        else:
            print"Writing File"
            with open('./.TempReading.py', 'r') as src, open ('/home/pi/.TempReading.py', 'w') as dst:
                    dst.write(src.read())
            with open('/home/pi/.local/share/applications/TempReading.desktop', 'w') as dsktp:
                dsktp.writelines('[Desktop Entry] \nComment=Display Temp'+
                                  '\nTerminal=false \nName=Temp\nExec=/home/pi/.TempReading.py'+
                                  '\nType=Application\nIcon=preferences-desktop-display\nNoDisplay=false\nCategories=System')
            os.system('chmod +x /home/pi/.TempReading.py')
            return -1
    if os.path.isdir('/home/pi'):
        print os.name
        WriteFile()
        return -1
    else:
        exit()
        return -1

SystemCheck()
root=Tk()
TempSensor=GUI(root)
root.protocol("WM_DELETE_WINDOW", TempSensor.exitFunctions)
root.mainloop()
