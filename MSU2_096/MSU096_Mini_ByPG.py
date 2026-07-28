# -*- coding: UTF-8 -*-
import serial  # Import serial library (requires additional installation)
import serial.tools.list_ports
import time  # Import delay library
import threading  # Import timed callback library
import psutil  # Import psutil to get device information (requires additional installation)
import os  # Used for reading files
import pyautogui  # Used for screenshots (requires additional installation of pillow)
from datetime import datetime  # Used to get current time
import tkinter as tk
from tkinter import *  # Import UI library
import tkinter.filedialog  # Used to get file path
from PIL import Image  # Import PIL library for image processing
import sys  # Used to close the program


# import numpy as np  # Use numpy to accelerate data processing


class MSN_Device:  # Define a structure
    def __init__(self, com, version):
        self.com = com  # Register COM port location
        self.version = version  # Register MSN version
        self.name = 'MSN'  # Register device name
        self.baud_rate = 19200  # Register baud rate


My_MSN_Device = []  # Create an empty structure array


class MSN_Data:  # Define a structure
    def __init__(self, name, unit, family, data):
        self.name = name
        self.unit = unit
        self.family = family
        self.data = data


My_MSN_Data = []  # Create an empty structure array

# RGB565 color codes
RED = 0xf800
GREEN = 0x07e0
BLUE = 0x001f
WHITE = 0xffff
BLACK = 0x0000
YELLOW = 0xFFE0
GRAY0 = 0xEF7D
GRAY1 = 0x8410
GRAY2 = 0x4208

hex_code = b''

G_screnn0 = bytearray()  # Empty array
G_screnn1 = bytearray()  # Empty array
Img_data_use = bytearray()  # Empty array
G_screnn0_OK = 0
G_screnn1_OK = 0
size_USE_X1 = 0
size_USE_Y1 = 0

# Parameter definitions
Show_W = 565  # Display width
Show_H = 350  # Canvas height


# Button function definitions
def Get_Photo_Path1():  # Get file path
    global photo_path1, Label3
    photo_path1 = tk.filedialog.askopenfilename(title="Select File",
                                                filetypes=[('Image file', '*.jpg'), ('Image file', '*.jpeg'),
                                                           ('Image file', '*.png'), ('Image file', '*.bmp')])
    Label3.config(text=photo_path1[-20:])


def Get_Photo_Path2():  # Get file path
    global photo_path2, Label4
    photo_path2 = tk.filedialog.askopenfilename(title="Select File", filetypes=[('Bin file', '*.bin')])
    Label4.config(text=photo_path2[-20:])
    photo_path2 = photo_path2[:-4]


def Get_Photo_Path3():  # Get file path
    global photo_path3, Label5  # Supports JPG, PNG, BMP image formats
    photo_path3 = tk.filedialog.askopenfilename(title="Select File",
                                                filetypes=[('Image file', '*.jpg'), ('Image file', '*.jpeg'),
                                                           ('Image file', '*.png'), ('Image file', '*.bmp')])
    Label5.config(text=photo_path3[-20:])


def Get_Photo_Path4():  # Get file path
    global photo_path4, Label6
    photo_path4 = tk.filedialog.askopenfilename(title="Select File",
                                                filetypes=[('Image file', '*.jpg'), ('Image file', '*.jpeg'),
                                                           ('Image file', '*.png'), ('Image file', '*.bmp')])
    Label6.config(text=photo_path4[-20:])


def Writet_Photo_Path1():  # Write file
    global photo_path1, write_path1, Text1, Img_data_use
    if write_path1 == 0:  # Ensure previous write is completed
        Text1.delete(1.0, END)  # Clear text box
        Text1.insert(END, 'Converting image format...\n')  # Insert at the beginning of text box
        im1 = Image.open(photo_path1)
        if im1.width >= (im1.height * 2):  # Image aspect ratio exceeds 2:1
            im2 = im1.resize((int(80 * im1.width / im1.height), 80))
            Img_m = int(im2.width / 2)
            box = ((Img_m - 80, 0, Img_m + 80, 80))  # Define crop area
            im2 = im2.crop(box)
        else:
            im2 = im1.resize((160, int(160 * im1.height / im1.width)))
            Img_m = int(im2.height / 2)
            box = ((0, Img_m - 40, 160, Img_m + 40))  # Define crop area
            im2 = im2.crop(box)
        im2 = im2.convert('RGB')  # Convert to RGB format
        Img_data_use = bytearray()  # Empty array
        for y in range(0, 80):  # Parse encoding pixel by pixel
            for x in range(0, 160):  # Parse encoding pixel by pixel
                r, g, b = im2.getpixel((x, y))
                Img_data_use.append(((r >> 3) << 3) | (g >> 5))
                Img_data_use.append((((g % 32) >> 2) << 5) | (b >> 3))
        write_path1 = 1


def Writet_Photo_Path2():  # Write file
    global photo_path2, write_path2, Text1
    if write_path2 == 0:  # Ensure previous write is completed
        write_path2 = 1
        Text1.delete(1.0, END)  # Clear text box
        Text1.insert(END, 'Preparing to burn Flash firmware...\n')


def Writet_Photo_Path3():  # Write file
    global photo_path3, write_path3, Text1, Img_data_use
    if write_path3 == 0:  # Ensure previous write is completed
        Text1.delete(1.0, END)  # Clear text box
        Text1.insert(END, 'Converting image format...\n')

        im1 = Image.open(photo_path3)
        if im1.width >= (im1.height * 2):  # Image aspect ratio exceeds 2:1
            im2 = im1.resize((int(80 * im1.width / im1.height), 80))
            Img_m = int(im2.width / 2)
            box = ((Img_m - 80, 0, Img_m + 80, 80))  # Define crop area
            im2 = im2.crop(box)
        else:
            im2 = im1.resize((160, int(160 * im1.height / im1.width)))
            Img_m = int(im2.height / 2)
            box = ((0, Img_m - 40, 160, Img_m + 40))  # Define crop area
            im2 = im2.crop(box)
        im2 = im2.convert('RGB')  # Convert to RGB format
        Img_data_use = bytearray()  # Empty array
        for y in range(0, 80):  # Parse encoding pixel by pixel
            for x in range(0, 160):  # Parse encoding pixel by pixel
                r, g, b = im2.getpixel((x, y))
                Img_data_use.append(((r >> 3) << 3) | (g >> 5))
                Img_data_use.append((((g % 32) >> 2) << 5) | (b >> 3))
        write_path3 = 1


def Writet_Photo_Path4():  # Write file
    global photo_path4, write_path4, Text1, Img_data_use
    if write_path4 == 0:  # Ensure previous write is completed
        Text1.delete(1.0, END)  # Clear text box
        Text1.insert(END, 'Converting animated image format...\n')
        time.sleep(0.1)
        Path_use = photo_path4
        if Path_use[-4] == '.':  #
            write_path4 = Path_use[-4:]
            Path_use = Path_use[:-5]

        elif Path_use[-5] == '.':
            write_path4 = Path_use[-5:]
            Path_use = Path_use[:-6]
        else:
            Text1.insert(END, 'Animated image name does not meet requirements!\n')
        Img_data_use = bytearray()
        u_time = time.time()
        for i in range(0, 36):  # Convert 36 images sequentially
            im1 = Image.open(Path_use + str(i) + write_path4)
            if im1.width >= (im1.height * 2):  # Image aspect ratio exceeds 2:1
                im2 = im1.resize((int(80 * im1.width / im1.height), 80))
                Img_m = int(im2.width / 2)
                box = ((Img_m - 80, 0, Img_m + 80, 80))  # Define crop area
                im2 = im2.crop(box)
            else:
                im2 = im1.resize((160, int(160 * im1.height / im1.width)))
                Img_m = int(im2.height / 2)
                box = ((0, Img_m - 40, 160, Img_m + 40))  # Define crop area
                im2 = im2.crop(box)
            im2 = im2.convert('RGB')  # Convert to RGB format
            for y in range(0, 80):  # Parse encoding pixel by pixel
                for x in range(0, 160):  # Parse encoding pixel by pixel
                    r, g, b = im2.getpixel((x, y))
                    Img_data_use.append(((r >> 3) << 3) | (g >> 5))
                    Img_data_use.append((((g % 32) >> 2) << 5) | (b >> 3))
        u_time = time.time() - u_time
        u_time = int(u_time * 1000)
        Text1.insert(END, 'Conversion completed, time taken ' + str(u_time) + 'ms\n')
        write_path4 = 1


def Page_UP():  # Previous page
    global State_change, State_machine
    State_machine = State_machine + 1
    State_change = 1
    if State_machine > 5:
        State_machine = 0


def Page_Down():  # Next page
    global State_change, State_machine
    State_machine = State_machine - 1
    State_change = 1
    if State_machine < 0:
        State_machine = 5


def LCD_Change():  # Switch display orientation
    global LCD_Change_use
    LCD_Change_use = LCD_Change_use + 1
    if LCD_Change_use > 1:  # Limit switching modes
        LCD_Change_use = 0


def SER_Write(Data_U0):
    global Device_State
    # print('Sending data...')
    try:  # Attempt to send command - two cases where sending fails: 1. Device removed, send error; 2. Device in MSN connection state, slow response to computer commands
        # Timeout detection
        # u_time=time.time()
        if (False == ser.is_open):
            Device_State = 0  # Revert to disconnected state
        ser.write(Data_U0)
        # print(Data_U0)
        # u_time=time.time()-u_time
        # if u_time>2:
        # print('Send timeout');
        # Device_State=0 # Revert to disconnected state
        # ser.close() # Close serial port to prevent failure on next open
        # else:
        # print('Send completed');
    except:  # Exception occurred
        # print('Send exception');
        Device_State = 0
        ser.close()  # Close serial port to prevent failure on next open


def SER_Read():
    global Device_State
    # print('Receiving data...');
    try:  # Attempt to get data
        Data_U1 = ser.read(ser.in_waiting)
        return Data_U1
    except:  # Exception occurred
        # print('Receive exception');
        Device_State = 0
        ser.close()  # Close serial port to prevent failure on next open
        return 0


def Read_M_u8(add):  # Read host u8 register (MSC device code, Add)
    hex_use = bytearray()  # Empty array
    hex_use.append(0)  # Send to host
    hex_use.append(48)  # Identified as SFR command
    hex_use.append(0 * 32)  # Identified as 8bit SFR read
    hex_use.append(add // 256)  # High address
    hex_use.append(add % 256)  # Low address
    hex_use.append(0)  # Value
    SER_Write(hex_use)  # Send command

    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("byte") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            return recv[5]


def Read_M_u16(add):  # Read host u16 register (MSC device code, Add)
    hex_use = bytearray()  # Empty array
    hex_use.append(0)  # Send to host
    hex_use.append(48)  # Identified as SFR command
    hex_use.append(1 * 32)  # Identified as 16bit SFR read
    hex_use.append(add % 256)  # Address
    hex_use.append(0)  # High byte value
    hex_use.append(0)  # Low byte value
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("gbk") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            return recv[4] * 256 + recv[5]


def Write_M_u8(add, data_w):  # Write host u8 register (MSC device code, Add)
    hex_use = bytearray()  # Empty array
    hex_use.append(0)  # Send to host
    hex_use.append(48)  # Identified as SFR command
    hex_use.append(4 * 32)  # Identified as 8bit SFR write
    hex_use.append(add // 256)  # High address
    hex_use.append(add % 256)  # Low address
    hex_use.append(data_w % 256)  # Value
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            break
            # return recv[5]


def Write_M_u16(add, data_w):  # Write host u16 register (MSC device code, Add)
    hex_use = bytearray()  # Empty array
    hex_use.append(0)  # Send to host
    hex_use.append(48)  # Identified as SFR command
    hex_use.append(1 * 32)  # Identified as 16bit SFR write
    hex_use.append(add % 256)  # Address
    hex_use.append(data_w // 256)  # High byte value
    hex_use.append(data_w % 256)  # Low byte value
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("gbk") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            break


def Read_ADC_CH(ch):  # Read host ADC register value (ADC channel)
    hex_use = bytearray()  # Empty array
    hex_use.append(8)  # Read ADC
    hex_use.append(ch)  # Channel
    hex_use.append(0)
    hex_use.append(0)
    hex_use.append(0)
    hex_use.append(0)
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("gbk") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            return recv[4] * 256 + recv[5]


def Read_M_SFR_Data(add):  # Get SFR description from u8 area
    SFR_data = bytearray()  # Empty array
    for i in range(0, 256):  # Parse encoding in 128-byte units
        SFR_data.append(Read_M_u8(add + i))  # Read encoded data
    data_type = 0  # Cycle through types based on whether value is 0
    data_num = 0
    data_len = 0
    data_use = bytearray()  # Empty array
    data_name = b''
    data_unit = b''
    data_family = b''
    data_data = b''
    for i in range(0, 256):  # Parse encoding in 128-byte units
        if (SFR_data[i] != 0 and data_type < 3):
            data_use.append(SFR_data[i])  # Merge non-zero data together
        elif (data_type < 3):  # Detected 0 and not out of range
            if (len(data_use) == 0):  # Received 00 when no data received
                break  # Detected 0 and collected data is empty, determine as end
            if (data_type == 0):
                data_name = data_use  # Name
                data_type = 1
            elif (data_type == 1):
                data_unit = data_use  # Unit
                data_type = 2
            elif (data_type == 2):
                data_family = data_use  # Type
                data_type = 3
                if (int(ord(data_use) // 32) == 0):  # u8 data 2B add
                    data_len = 2
                elif (int(ord(data_use) // 32) == 1):  # u16 data 1B add
                    data_len = 1
                elif (int(ord(data_use) // 32) == 2):  # u32 data 2B add
                    data_len = 2
                elif (int(ord(data_use) // 32) == 3):  # u8 Text XB data
                    data_len = data_family[0] % 32  # Calculate data length
            data_use = bytearray()  # Empty array
            continue  # Continue to next loop
        if (data_len > 0 and data_type == 3):  # Valid data
            data_use.append(SFR_data[i])  # Merge non-zero data together
            data_len = data_len - 1
        if (data_len == 0 and data_type == 3):  # Collect remaining data
            data_data = data_use
            data_type = 0  # Reset type
            My_MSN_Data.append(MSN_Data(data_name, data_unit, data_family, data_data))  # Register data
            data_use = bytearray()  # Empty array


def Print_MSN_Data():
    num = len(My_MSN_Data)
    data_str = ''
    print('Total MSN data count: ' + str(num))
    # Parse data
    for i in range(0, num):  # Print all data
        data_str = data_str + 'Index: ' + str(i) + '    Name: ' + str(My_MSN_Data[i].name) + '    Unit: ' + str(
            My_MSN_Data[i].unit)
        if (ord(My_MSN_Data[i].family) // 32 == 0):  # Data type is u8 address (16bit)
            data_str = data_str + '    Type: u8_SFR_address, length ' + str(ord(My_MSN_Data[i].family) % 32)
            data_str = data_str + '    Address: ' + str(int(My_MSN_Data[i].data[0]) * 256 + int(My_MSN_Data[i].data[1]))
        elif (ord(My_MSN_Data[i].family) // 32 == 1):  # Data type is u16 address (8bit)
            data_str = data_str + '    Type: u16_SFR_address, length ' + str(ord(My_MSN_Data[i].family) % 32)
            data_str = data_str + '    Address: ' + str(int(My_MSN_Data[i].data[0]))
        elif (ord(My_MSN_Data[i].family) // 32 == 2):  # Data type is u32 address (16bit)
            data_str = data_str + '    Type: u32_SFR_address, length: ' + str(ord(My_MSN_Data[i].family) % 32)
            data_str = data_str + '    Address: ' + str(int(My_MSN_Data[i].data[0]) * 256 + int(My_MSN_Data[i].data[1]))
        elif (ord(My_MSN_Data[i].family) // 32 == 3):  # Data type is u8 string
            data_str = data_str + '    Type: string, length ' + str(ord(My_MSN_Data[i].family) % 32)
            data_str = data_str + '    Data: ' + str(My_MSN_Data[i].data)
        elif (ord(My_MSN_Data[i].family) // 32 == 4):  # Data type is u8 array
            data_str = data_str + '    Type: u8 array data, length ' + str(int(My_MSN_Data[i].family) % 32)
            data_str = data_str + '    Data: ' + str(My_MSN_Data[i].data)
        print(data_str)
        data_str = ''


def Read_MSN_Data(name_use):  # Read data from MSN_data
    num = len(My_MSN_Data)
    use_data = []  # Create an empty list
    for i in range(0, num):  # Search through all data
        if (My_MSN_Data[i].name == name_use):
            if (ord(My_MSN_Data[i].family) // 32 == 0):  # Data type is u8 address (16bit)
                sfr_add = int(My_MSN_Data[i].data[0]) * 256 + int(My_MSN_Data[i].data[1])
                for n in range(0, ord(My_MSN_Data[i].family) % 32):
                    use_data.append(Read_M_u8(sfr_add + n))
            elif (ord(My_MSN_Data[i].family) // 32 == 1):  # Data type is u16 address (8bit)
                use_data = Read_M_u16(int(My_MSN_Data[i].data[0]))
            elif (ord(My_MSN_Data[i].family) // 32 == 3):  # Data type is u8 string
                use_data = My_MSN_Data[i].data
            elif (ord(My_MSN_Data[i].family) // 32 == 4):  # Data type is u8 array
                use_data = My_MSN_Data[i].data
            print(str(My_MSN_Data[i].name) + '=' + str(use_data))
            return use_data
    if name_use != 0:
        print('"' + name_use + '"' + ' does not exist, please check if the name is correct')
    return 0


def Write_MSN_Data(name_use, data_w):  # Write data to MSN_data
    num = len(My_MSN_Data)
    for i in range(0, num):  # Search through all data
        if (My_MSN_Data[i].name == name_use):
            if (int(My_MSN_Data[i].family) // 32 == 0):  # Data type is u8 address (16bit)
                Write_M_u8(int(My_MSN_Data[i].data[0]) * 256 + int(My_MSN_Data[i].data[1]), data_w)
                print('"' + name_use + '"' + ' write ' + str(data_w) + ' completed')
                return 0
            elif (int(My_MSN_Data[i].family) // 32 == 1):  # Data type is u16 address (8bit)
                Write_M_u16(int(My_MSN_Data[i].data[0]), data_w)
                print('"' + name_use + '"' + ' write ' + str(data_w) + ' completed')
                return 0
    print('"' + name_use + '"' + ' does not exist, please check if the name is correct')


def Write_Flash_Page(Page_add, data_w, Page_num):  # Write 256B data to specified Flash page
    # First complete data transfer
    hex_use = bytearray()  # Empty array
    for i in range(0, 64):  # 256 bytes divided into 64 commands
        hex_use.append(4)  # Multiple writes to Flash
        hex_use.append(i)  # Low address
        hex_use.append(data_w[i * 4 + 0])  # Data0
        hex_use.append(data_w[i * 4 + 1])  # Data1
        hex_use.append(data_w[i * 4 + 2])  # Data2
        hex_use.append(data_w[i * 4 + 3])  # Data3
        SER_Write(hex_use)  # Send command
    hex_use = bytearray()  # Empty array
    hex_use.append(3)  # Flash operation
    hex_use.append(1)  # Write Flash
    hex_use.append(Page_add // (65536))  # Data0
    hex_use.append((Page_add % 65536) // 256)  # Data1
    hex_use.append((Page_add % 65536) % 256)  # Data2
    hex_use.append(Page_num % 256)  # Data3
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            break


def Write_Flash_Page_fast(Page_add, data_w,
                          Page_num):  # Without erasing, directly write 256B data to specified Flash page
    # First complete data transfer
    hex_use = b''
    for i in range(0, 64):  # 256 bytes divided into 64 commands
        hex_use = hex_use + int(4).to_bytes(1, byteorder="little")  # Multiple writes to Flash
        hex_use = hex_use + int(i).to_bytes(1, byteorder="little")  # Low address
        hex_use = hex_use + data_w[i * 4 + 0].to_bytes(1, byteorder="little")  # Data0
        hex_use = hex_use + data_w[i * 4 + 1].to_bytes(1, byteorder="little")  # Data1
        hex_use = hex_use + data_w[i * 4 + 2].to_bytes(1, byteorder="little")  # Data2
        hex_use = hex_use + data_w[i * 4 + 3].to_bytes(1, byteorder="little")  # Data3
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Flash operation
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # After erasing, write Flash
    hex_use = hex_use + int(Page_add // (256 * 256)).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int((Page_add % 65536) // 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int((Page_add % 65536) % 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(Page_num).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            break


def Erase_Flash_page(add, size):  # Clear specified memory area
    hex_use = bytearray()  # Empty array
    hex_use.append(3)  # Flash operation
    hex_use.append(2)  # Clear specified memory area
    hex_use.append((add % 65536) // 256)  # Data1
    hex_use.append((add % 65536) % 256)  # Data2
    hex_use.append((size % 65536) // 256)  # Data1
    hex_use.append((size % 65536) % 256)  # Data2
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            break


def Read_Flash_byte(add):  # Read value at specified address
    hex_use = bytearray()  # Empty array
    hex_use.append(3)  # Flash operation
    hex_use.append(0)  # Read Flash
    hex_use.append(add // (256 * 256))  # Data0
    hex_use.append((add % 65536) // 256)  # Data1
    hex_use.append((add % 65536) % 256)  # Data2
    hex_use.append(0)  # Data3
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            print(recv[5])
            return recv[5]


def Write_Flash_Photo_fast(Page_add, Photo_name):  # Write Bin format photo to Flash
    global Text1
    filepath = Photo_name + '.bin'  # Compose file name
    try:  # Attempt to open bin file
        binfile = open(filepath, 'rb')  # Open in read-only mode
    except:  # Exception occurred
        print('Cannot find "' + filepath + '" file, please check if it is located in the current directory')
        # Text1.delete(1.0, END) # Clear text box
        Text1.insert(END, 'File path or format error!\n')
        return 0
    Fsize = os.path.getsize(filepath)
    print('Found "' + filepath + '" file, size: ' + str(Fsize) + ' B')
    Text1.insert(END, 'Size ' + str(Fsize) + 'B, burning...\n')
    u_time = time.time()
    # Perform erase
    if (Fsize % 256 != 0):
        Erase_Flash_page(Page_add, Fsize // 256 + 1)  # Clear specified memory area
    else:
        Erase_Flash_page(Page_add, Fsize // 256)  # Clear specified memory area

    for i in range(0, Fsize // 256):  # Write one Page at a time
        Fdata = binfile.read(256)
        Write_Flash_Page_fast(Page_add + i, Fdata, 1)  # (page, data, size)
    if (Fsize % 256 != 0):  # There is remaining data to write
        Fdata = binfile.read(Fsize % 256)  # Read remaining data
        for i in range(Fsize % 256, 256):
            Fdata = Fdata + int(255).to_bytes(1, byteorder="little")  # Fill insufficient positions with 0xFF
        Write_Flash_Page_fast(Page_add + Fsize // 256, Fdata, 1)  # (page, data, size)
    u_time = time.time() - u_time
    print(filepath + ' burning completed, time taken ' + str(u_time) + ' seconds')
    Text1.insert(END, 'Burning completed, time taken ' + str(int(u_time * 1000)) + 'ms\n')


def Write_Flash_hex_fast(Page_add, img_use):  # Write hex data to Flash
    Fsize = len(img_use)
    Text1.insert(END, 'Size ' + str(Fsize) + 'B, burning...\n')
    u_time = time.time()
    # Perform erase
    if (Fsize % 256 != 0):
        Erase_Flash_page(Page_add, Fsize // 256 + 1)  # Clear specified memory area
    else:
        Erase_Flash_page(Page_add, Fsize // 256)  # Clear specified memory area
    for i in range(0, Fsize // 256):  # Write one Page at a time
        Fdata = img_use[:256]  # Take first 256 bytes
        img_use = img_use[256:]  # Take remaining bytes
        Write_Flash_Page_fast(Page_add + i, Fdata, 1)  # (page, data, size)
    if (Fsize % 256 != 0):  # There is remaining data to write
        Fdata = img_use  # Read remaining data
        for i in range(Fsize % 256, 256):
            Fdata = Fdata + int(255).to_bytes(1, byteorder="little")  # Fill insufficient positions with 0xFF
        Write_Flash_Page_fast(Page_add + Fsize // 256, Fdata, 1)  # (page, data, size)
    u_time = time.time() - u_time
    Text1.insert(END, 'Burning completed, time taken ' + str(int(u_time * 1000)) + 'ms\n')


def Write_Flash_ZK(Page_add, ZK_name):  # Write Bin format font library to Flash
    filepath = ZK_name + '.bin'  # Compose file name
    try:  # Attempt to open bin file
        binfile = open(filepath, 'rb')  # Open in read-only mode
    except:  # Exception occurred
        print('Cannot find "' + filepath + '" file, please check if it is located in the current directory')
        return 0
    Fsize = os.path.getsize(filepath) - 6  # Last six bytes of font file are not dot matrix data
    print('Found "' + filepath + '" file, size: ' + str(Fsize) + ' B')
    for i in range(0, Fsize // 256):  # Write one Page at a time
        Fdata = binfile.read(256)
        Write_Flash_Page(Page_add + i, Fdata, 1)  # (page, data, size)
    if (Fsize % 256 != 0):  # There is remaining data to write
        Fdata = binfile.read(Fsize % 256)  # Read remaining data
        for i in range(Fsize % 256, 256):
            Fdata = Fdata + int(255).to_bytes(1, byteorder="little")  # Fill insufficient positions with 0xFF
        Write_Flash_Page(Page_add + Fsize // 256, Fdata, 1)  # (page, data, size)
    print(filepath + ' burning completed')


def LCD_Set_XY(LCD_D0, LCD_D1):  # Set starting position
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")  # Set starting position
    hex_use = hex_use + int(LCD_D0 // 256).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int(LCD_D0 % 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int(LCD_D1 // 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(LCD_D1 % 256).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command


def LCD_Set_Size(LCD_D0, LCD_D1):  # Set size
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(1).to_bytes(1, byteorder="little")  # Set size
    hex_use = hex_use + int(LCD_D0 // 256).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int(LCD_D0 % 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int(LCD_D1 // 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(LCD_D1 % 256).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command


def LCD_Set_Color(LCD_D0, LCD_D1):  # Set color (FC, BC)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(2).to_bytes(1, byteorder="little")  # Set color
    hex_use = hex_use + int(LCD_D0 // 256).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int(LCD_D0 % 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int(LCD_D1 // 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(LCD_D1 % 256).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command


def LCD_Photo(LCD_X, LCD_Y, LCD_X_Size, LCD_Y_Size, Page_Add):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Size(LCD_X_Size, LCD_Y_Size)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")  # Display color image
    hex_use = hex_use + int(Page_Add // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Page_Add % 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_ADD(LCD_X, LCD_Y, LCD_X_Size, LCD_Y_Size):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Size(LCD_X_Size, LCD_Y_Size)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(7).to_bytes(1, byteorder="little")  # Load address
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_State(LCD_S):  #
    global Device_State
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(10).to_bytes(1, byteorder="little")  # Load address
    hex_use = hex_use + int(LCD_S).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_DATA(data_w, size):  # Write data of specified size to LCD
    # First complete data transfer
    hex_use = b''
    for i in range(0, 64):  # 256 bytes divided into 64 commands
        hex_use = hex_use + int(4).to_bytes(1, byteorder="little")  # Multiple writes to Flash
        hex_use = hex_use + int(i).to_bytes(1, byteorder="little")  # Low address
        hex_use = hex_use + data_w[i * 4 + 0].to_bytes(1, byteorder="little")  # Data0
        hex_use = hex_use + data_w[i * 4 + 1].to_bytes(1, byteorder="little")  # Data1
        hex_use = hex_use + data_w[i * 4 + 2].to_bytes(1, byteorder="little")  # Data2
        hex_use = hex_use + data_w[i * 4 + 3].to_bytes(1, byteorder="little")  # Data3
    hex_use = hex_use + int(2).to_bytes(1, byteorder="little")  # Flash operation
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # After erasing, write Flash
    hex_use = hex_use + int(8).to_bytes(1, byteorder="little")  # Data0
    hex_use = hex_use + int(size // 256).to_bytes(1, byteorder="little")  # Data1
    hex_use = hex_use + int(size % 256).to_bytes(1, byteorder="little")  # Data2
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")  # Data3
    SER_Write(hex_use)  # Send command


def Write_LCD_Photo_fast(x_star, y_star, x_size, y_size, Photo_name):  # Write Bin format photo to Flash
    filepath = Photo_name + '.bin'  # Compose file name
    try:  # Attempt to open bin file
        binfile = open(filepath, 'rb')  # Open in read-only mode
    except:  # Exception occurred
        print('Cannot find "' + filepath + '" file, please check if it is located in the current directory')
        return 0
    Fsize = os.path.getsize(filepath)
    print('Found "' + filepath + '" file, size: ' + str(Fsize) + ' B')
    u_time = time.time()
    # Write address
    LCD_ADD(x_star, y_star, x_size, y_size)
    for i in range(0, Fsize // 256):  # Write one Page at a time
        Fdata = binfile.read(256)
        LCD_DATA(Fdata, 256)  # (page, data, size)
    if (Fsize % 256 != 0):  # There is remaining data to write
        Fdata = binfile.read(Fsize % 256)  # Read remaining data
        for i in range(Fsize % 256, 256):
            Fdata = Fdata + int(255).to_bytes(1, byteorder="little")  # Fill insufficient positions with 0xFF
        LCD_DATA(Fdata, Fsize % 256)  # (page, data, size)
    u_time = time.time() - u_time
    print(filepath + ' display completed, time taken ' + str(u_time) + ' seconds')


def Write_LCD_Photo_fast1(x_star, y_star, x_size, y_size, Photo_name):  # Write Bin format photo to Flash
    filepath = Photo_name + '.bin'  # Compose file name
    try:  # Attempt to open bin file
        binfile = open(filepath, 'rb')  # Open in read-only mode
    except:  # Exception occurred
        print('Cannot find "' + filepath + '" file, please check if it is located in the current directory')
        return 0
    Fsize = os.path.getsize(filepath)
    print('Found "' + filepath + '" file, size: ' + str(Fsize) + ' B')
    u_time = time.time()
    # Write address
    LCD_ADD(x_star, y_star, x_size, y_size)
    hex_use = bytearray()  # Empty array
    for j in range(0, Fsize // 256):  # Write one Page at a time
        data_w = binfile.read(256)
        # First convert data format
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            hex_use.append(4)
            hex_use.append(i)
            hex_use.append(data_w[i * 4 + 0])
            hex_use.append(data_w[i * 4 + 1])
            hex_use.append(data_w[i * 4 + 2])
            hex_use.append(data_w[i * 4 + 3])
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(1)
        hex_use.append(0)
        hex_use.append(0)
    if (Fsize % 256 != 0):  # There is remaining data to write
        data_w = binfile.read(Fsize % 256)  # Read remaining data
        for i in range(Fsize % 256, 256):
            data_w = data_w + int(255).to_bytes(1, byteorder="little")  # Fill insufficient positions with 0xFF
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            hex_use.append(4)
            hex_use.append(i)
            hex_use.append(data_w[i * 4 + 0])
            hex_use.append(data_w[i * 4 + 1])
            hex_use.append(data_w[i * 4 + 2])
            hex_use.append(data_w[i * 4 + 3])
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(0)
        hex_use.append(Fsize % 256)
        hex_use.append(0)
    hex_use.append(2)
    hex_use.append(3)
    hex_use.append(9)
    hex_use.append(0)
    hex_use.append(0)
    hex_use.append(0)
    SER_Write(hex_use)  # Send command
    u_time = time.time() - u_time
    print(filepath + ' display completed, time taken ' + str(u_time) + ' seconds')


def Write_LCD_Screen_fast(x_star, y_star, x_size, y_size, Photo_data):  # Write Bin format photo to Flash
    LCD_ADD(x_star, y_star, x_size, y_size)
    Photo_data_use = Photo_data
    hex_use = bytearray()  # Empty array
    for j in range(0, x_size * y_size * 2 // 256):  # Write one Page at a time
        data_w = Photo_data_use[:256]
        Photo_data_use = Photo_data_use[256:]
        cmp_use = []  # Empty array
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            cmp_use.append(
                data_w[i * 4 + 0] * 256 * 256 * 256 + data_w[i * 4 + 1] * 256 * 256 + data_w[i * 4 + 2] * 256 + data_w[
                    i * 4 + 3])
        result = max(set(cmp_use), key=cmp_use.count)  # Find the most frequent data
        hex_use.append(2)
        hex_use.append(4)
        color_ram = result
        hex_use.append(color_ram // (256 * 256 * 256))
        color_ram = color_ram % (256 * 256 * 256)
        hex_use.append(color_ram // (256 * 256))
        color_ram = color_ram % (256 * 256)
        hex_use.append(color_ram // 256)
        hex_use.append(color_ram % 256)
        # First convert data format
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            if ((data_w[i * 4 + 0] * 256 * 256 * 256 + data_w[i * 4 + 1] * 256 * 256 + data_w[i * 4 + 2] * 256 + data_w[
                i * 4 + 3]) != result):  #
                hex_use.append(4)
                hex_use.append(i)
                hex_use.append(data_w[i * 4 + 0])
                hex_use.append(data_w[i * 4 + 1])
                hex_use.append(data_w[i * 4 + 2])
                hex_use.append(data_w[i * 4 + 3])
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(1)
        hex_use.append(0)
        hex_use.append(0)
    if (x_size * y_size * 2 % 256 != 0):  # There is remaining data to write
        data_w = Photo_data_use  # Read remaining data
        for i in range(x_size * y_size * 2 % 256, 256):
            data_w.append(0xff)  # Fill insufficient positions with 0xFF
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            hex_use.append(4)
            hex_use.append(i)
            hex_use.append(data_w[i * 4 + 0])
            hex_use.append(data_w[i * 4 + 1])
            hex_use.append(data_w[i * 4 + 2])
            hex_use.append(data_w[i * 4 + 3])
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(0)
        hex_use.append(x_size * y_size * 2 % 256)
        hex_use.append(0)
    SER_Write(hex_use)  # Send command


# Encode and analyze sent data to shorten data commands
def Write_LCD_Screen_fast1(x_star, y_star, x_size, y_size, Photo_data):  # Write Bin format photo to Flash
    LCD_ADD(x_star, y_star, x_size, y_size)
    Photo_data_use = Photo_data
    hex_use = bytearray()  # Empty array
    for j in range(0, x_size * y_size * 2 // 256):  # Write one Page at a time
        data_w = Photo_data_use[:256]
        Photo_data_use = Photo_data_use[256:]
        # First convert data format
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            hex_use.append(4)
            hex_use.append(i)
            hex_use.append(data_w[i * 4 + 0])
            hex_use.append(data_w[i * 4 + 1])
            hex_use.append(data_w[i * 4 + 2])
            hex_use.append(data_w[i * 4 + 3])
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(1)
        hex_use.append(0)
        hex_use.append(0)
    if (x_size * y_size * 2 % 256 != 0):  # There is remaining data to write
        data_w = Photo_data_use  # Read remaining data
        for i in range(x_size * y_size * 2 % 256, 256):
            data_w.append(0xff)  # Fill insufficient positions with 0xFF
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            hex_use.append(4)
            hex_use.append(i)
            hex_use.append(data_w[i * 4 + 0])
            hex_use.append(data_w[i * 4 + 1])
            hex_use.append(data_w[i * 4 + 2])
            hex_use.append(data_w[i * 4 + 3])
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(0)
        hex_use.append(x_size * y_size * 2 % 256)
        hex_use.append(0)
    # Wait for transfer to complete
    hex_use.append(2)
    hex_use.append(3)
    hex_use.append(9)
    hex_use.append(0)
    hex_use.append(0)
    hex_use.append(0)
    SER_Write(hex_use)  # Send command


def LCD_Photo_wb(LCD_X, LCD_Y, LCD_X_Size, LCD_Y_Size, Page_Add, LCD_FC, LCD_BC):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Size(LCD_X_Size, LCD_Y_Size)
    LCD_Set_Color(LCD_FC, LCD_BC)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(1).to_bytes(1, byteorder="little")  # Display monochrome image
    hex_use = hex_use + int(Page_Add // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Page_Add % 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):  # Need to verify returned data to ensure device status can be accurately identified
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_ASCII_32X64(LCD_X, LCD_Y, Txt, LCD_FC, LCD_BC, Num_Page):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Color(LCD_FC, LCD_BC)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(2).to_bytes(1, byteorder="little")  # Display ASCII
    hex_use = hex_use + int(ord(Txt)).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Num_Page // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Num_Page % 256).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_GB2312_16X16(LCD_X, LCD_Y, Txt, LCD_FC, LCD_BC):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Color(LCD_FC, LCD_BC)
    Txt_Data = Txt.encode('gb2312')
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Display color image
    hex_use = hex_use + int(Txt_Data[0]).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Txt_Data[1]).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_Photo_wb_MIX(LCD_X, LCD_Y, LCD_X_Size, LCD_Y_Size, Page_Add, LCD_FC, BG_Page):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Size(LCD_X_Size, LCD_Y_Size)
    LCD_Set_Color(LCD_FC, BG_Page)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(4).to_bytes(1, byteorder="little")  # Display monochrome image
    hex_use = hex_use + int(Page_Add // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Page_Add % 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_ASCII_32X64_MIX(LCD_X, LCD_Y, Txt, LCD_FC, BG_Page, Num_Page):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Color(LCD_FC, BG_Page)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(5).to_bytes(1, byteorder="little")  # Display ASCII
    hex_use = hex_use + int(ord(Txt)).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Num_Page // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Num_Page % 256).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        # time.sleep(0.5)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_GB2312_16X16_MIX(LCD_X, LCD_Y, Txt, LCD_FC, BG_Page):  #
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Color(LCD_FC, BG_Page)
    Txt_Data = Txt.encode('gb2312')
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(6).to_bytes(1, byteorder="little")  # Display color image
    hex_use = hex_use + int(Txt_Data[0]).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(Txt_Data[1]).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.2)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def LCD_Color_set(LCD_X, LCD_Y, LCD_X_Size, LCD_Y_Size, F_Color):  # Fill specified area with color
    global Device_State
    LCD_Set_XY(LCD_X, LCD_Y)
    LCD_Set_Size(LCD_X_Size, LCD_Y_Size)
    hex_use = int(2).to_bytes(1, byteorder="little")  # Multiple writes to LCD
    hex_use = hex_use + int(3).to_bytes(1, byteorder="little")  # Set command
    hex_use = hex_use + int(11).to_bytes(1, byteorder="little")  # Display color image
    hex_use = hex_use + int(F_Color // 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(F_Color % 256).to_bytes(1, byteorder="little")
    hex_use = hex_use + int(0).to_bytes(1, byteorder="little")
    SER_Write(hex_use)  # Send command
    # Wait for response
    while (1):
        time.sleep(0.001)
        recv = SER_Read()  # .decode("UTF-8") # Get serial data
        if (recv == 0):
            return 0
        elif (len(recv) != 0):
            if ((recv[0] != hex_use[0]) or (recv[1] != hex_use[1])):
                Device_State = 0  # Receive error
            break


def TIM1():  # Receive data
    global timer1, time_out
    time_out = 1
    timer1 = threading.Timer(0.2, TIM1)  # Create timer, delay 1 second
    timer1.start()


def show_gif():  # Display GIF animation
    global State_change, gif_num
    if (State_change == 1):
        State_change = 0
        gif_num = 0
    if (State_change == 0):
        LCD_Photo(0, 0, 160, 80, gif_num * 100)
        gif_num = gif_num + 1
        if (gif_num > 35):
            gif_num = 0

    time.sleep(0.05)
    # LCD_Color_set(40,0,80,80,RED)


def show_PC_state(FC, BC):  # Display PC status
    global State_change
    photo_add = 4038
    num_add = 4026
    if (State_change == 1):
        State_change = 0
        LCD_Photo_wb(0, 0, 160, 80, photo_add, FC, BC)  # Place background
    if (State_change == 0):
        CPU = int(psutil.cpu_percent(interval=0.5))
        mem = psutil.virtual_memory()
        RAM = int(mem.percent)

        battery = psutil.sensors_battery()
        if battery != None:
            BAT = int(battery.percent)
        else:
            BAT = 100
        FRQ = int(psutil.disk_usage('/').used * 100 / psutil.disk_usage('/').total)
        if (CPU >= 100):
            LCD_Photo_wb(24, 0, 8, 33, 10 + num_add, FC, BC)
            CPU = CPU % 100
        else:
            LCD_Photo_wb(24, 0, 8, 33, 11 + num_add, FC, BC)
        LCD_Photo_wb(32, 0, 24, 33, (CPU // 10) + num_add, FC, BC)
        LCD_Photo_wb(56, 0, 24, 33, (CPU % 10) + num_add, FC, BC)
        if (RAM >= 100):
            LCD_Photo_wb(104, 0, 8, 33, 10 + num_add, FC, BC)
            RAM = RAM % 100
        else:
            LCD_Photo_wb(104, 0, 8, 33, 11 + num_add, FC, BC)
        LCD_Photo_wb(112, 0, 24, 33, (RAM // 10) + num_add, FC, BC)
        LCD_Photo_wb(136, 0, 24, 33, (RAM % 10) + num_add, FC, BC)
        if (BAT >= 100):
            LCD_Photo_wb(104, 47, 8, 33, 10 + num_add, FC, BC)
            BAT = BAT % 100
        else:
            LCD_Photo_wb(104, 47, 8, 33, 11 + num_add, FC, BC)
        LCD_Photo_wb(112, 47, 24, 33, (BAT // 10) + num_add, FC, BC)
        LCD_Photo_wb(136, 47, 24, 33, (BAT % 10) + num_add, FC, BC)

        if (FRQ >= 100):
            LCD_Photo_wb(24, 47, 8, 33, 10 + num_add, FC, BC)
            FRQ = FRQ % 100
        else:
            LCD_Photo_wb(24, 47, 8, 33, 11 + num_add, FC, BC)
        LCD_Photo_wb(32, 47, 24, 33, (FRQ // 10) + num_add, FC, BC)
        LCD_Photo_wb(56, 47, 24, 33, (FRQ % 10) + num_add, FC, BC)


def show_Photo1():  # Display photo
    global State_change
    FC = BLUE
    BC = BLACK
    if (State_change == 1):
        State_change = 0
        LCD_Photo(0, 0, 160, 80, 3926)  # Place background
    if (State_change == 0):
        time.sleep(0.2)


def show_PC_time():
    global State_change
    FC = YELLOW
    photo_add = 3826
    num_add = 3651
    if (State_change == 1):
        State_change = 0
        LCD_Photo(0, 0, 160, 80, photo_add)  # Place background
        # while(1):
        #    time.sleep(1)
        LCD_ASCII_32X64_MIX(56 + 8, 8, ':', FC, photo_add, num_add)
        # LCD_ASCII_32X64_MIX(136+8,32,':',FC,photo_add,num_add)
    if (State_change == 0):
        time_h = int(datetime.now().hour)
        time_m = int(datetime.now().minute)
        time_S = int(datetime.now().second)
        LCD_ASCII_32X64_MIX(0 + 8, 8, chr((time_h // 10) + 48), FC, photo_add, num_add)
        LCD_ASCII_32X64_MIX(32 + 8, 8, chr((time_h % 10) + 48), FC, photo_add, num_add)
        LCD_ASCII_32X64_MIX(80 + 8, 8, chr((time_m // 10) + 48), FC, photo_add, num_add)
        LCD_ASCII_32X64_MIX(112 + 8, 8, chr((time_m % 10) + 48), FC, photo_add, num_add)
        # LCD_ASCII_32X64_MIX(160+8,8,chr((time_S//10)+48),FC,photo_add,num_add)
        # LCD_ASCII_32X64_MIX(192+8,8,chr((time_S%10)+48),FC,photo_add,num_add)
        time.sleep(0.2)


def Screen_Date_Process(Photo_data):  # Convert and process data
    Photo_data_use = Photo_data
    hex_use = bytearray()  # Empty array
    for j in range(0, size_USE_X1 * size_USE_Y1 // 128):  # Write one Page at a time
        data_w = Photo_data_use[:128]
        Photo_data_use = Photo_data_use[128:]
        cmp_use = []  # Empty array
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            cmp_use.append(data_w[i * 2 + 0] * 65536 + data_w[i * 2 + 1])
        result = max(set(cmp_use), key=cmp_use.count)  # Find the most frequent data
        hex_use.append(2)
        hex_use.append(4)
        color_ram = result
        hex_use.append(color_ram >> 24)
        color_ram = color_ram % 16777216
        hex_use.append(color_ram >> 16)
        color_ram = color_ram % 65536
        hex_use.append(color_ram >> 8)
        hex_use.append(color_ram % 256)
        # First convert data format
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            if ((data_w[i * 2 + 0] * 65536 + data_w[i * 2 + 1]) != result):
                hex_use.append(4)
                hex_use.append(i)
                hex_use.append(data_w[i * 2 + 0] >> 8)
                hex_use.append(data_w[i * 2 + 0] % 256)
                hex_use.append(data_w[i * 2 + 1] >> 8)
                hex_use.append(data_w[i * 2 + 1] % 256)
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(1)
        hex_use.append(0)
        hex_use.append(0)
    if (size_USE_X1 * size_USE_Y1 * 2 % 256 != 0):  # There is remaining data to write
        data_w = Photo_data_use  # Read remaining data
        for i in range(size_USE_X1 * size_USE_Y1 * 2 % 256, 256):
            data_w.append(0xffff)  # Fill insufficient positions with 0xFFFF
        for i in range(0, 64):  # 256 bytes divided into 64 commands
            hex_use.append(4)
            hex_use.append(i)
            hex_use.append(data_w[i * 2 + 0] >> 8)
            hex_use.append(data_w[i * 2 + 0] % 256)
            hex_use.append(data_w[i * 2 + 1] >> 8)
            hex_use.append(data_w[i * 2 + 1] % 256)
        hex_use.append(2)
        hex_use.append(3)
        hex_use.append(8)
        hex_use.append(0)
        hex_use.append(size_USE_X1 * size_USE_Y1 * 2 % 256)
        hex_use.append(0)
    return hex_use


# Create two data buffers to prevent conflicts
def Screen_Date_get():  # Create dedicated function to capture screen and process data
    global G_screnn0_OK, G_screnn1_OK, G_screnn0, G_screnn1, size_USE_X1, size_USE_Y1
    print("Screenshot thread created successfully")
    size_PC = pyautogui.size()
    size_mode = 0
    if (size_mode == 0):  # Horizontal fill
        if (size_PC.width >= size_PC.height * 2):  # Ultra-wide screen
            size_USE_X1 = 160
            size_USE_Y1 = 160 * size_PC.height // size_PC.width
        else:
            size_USE_X1 = 160
            size_USE_Y1 = 80
    elif (size_mode == 1):  # Vertical fill
        if (size_PC.height * 2 >= size_PC.width):
            size_USE_X1 = 80 * size_PC.width // size_PC.height
            size_USE_Y1 = 80
        else:
            size_USE_X1 = 160
            size_USE_Y1 = 80
    elif (size_mode == 2):  # Stretch fill
        size_USE_X1 = 160
        size_USE_Y1 = 80
    while (1):
        if (G_screnn0_OK == 0 or G_screnn1_OK == 0):
            u_time1 = time.time()
            hex_16RGB = []  # bytearray()
            im = pyautogui.screenshot()  # Screenshot takes ~110ms too slow # Screenshot ~45ms, crop ~18ms, format conversion 24ms
            if (size_mode == 0):  # Horizontal fill
                if (size_PC.width >= size_PC.height * 2):
                    im1 = im.resize((size_USE_X1, size_USE_Y1))  # Scale
                else:
                    im1 = im.resize((160, 160 * size_PC.height // size_PC.width))  # Scale
                    im1 = im1.crop((0, (160 * size_PC.height // size_PC.width - 80) // 2, 160,
                                    (160 * size_PC.height // size_PC.width - 80) // 2 + 80))  # Center crop
            elif (size_mode == 1):  # Vertical fill
                if (size_PC.height * 2 >= size_PC.width):
                    im1 = im.resize((size_USE_X1, size_USE_Y1))  # Scale
                else:
                    im1 = im.resize((80 * size_PC.width // size_PC.height, 80))  # Scale
                    im1 = im1.crop(((80 * size_PC.width // size_PC.height - 160) // 2, 0,
                                    (80 * size_PC.width // size_PC.height - 160) // 2 + 160, 80))  # Center crop
            elif (size_mode == 2):  # Stretch fill
                im1 = im.resize((size_USE_X1, size_USE_Y1))  # Scale
            im2 = im1.load()  # Load memory array directly for processing

            for y in range(0, size_USE_Y1):
                for x in range(0, size_USE_X1):
                    hex_16RGB.append(((im2[x, y][0] >> 3) << 11) | ((im2[x, y][1] >> 2) << 5) | (
                                im2[x, y][2] >> 3))  # First directly add 16bit array
                    # hex_16RGB.append(Color_16bit>>8)
                    # hex_16RGB.append(Color_16bit%256)
                    # hex_16RGB.append((im2[x,y][0]>>3)*8+im2[x,y][1]//32)
                    # hex_16RGB.append(((im2[x,y][1]%32)//4)*32+im2[x,y][2]//8)

            if (G_screnn0_OK == 0):
                G_screnn0 = Screen_Date_Process(hex_16RGB)
                G_screnn0_OK = 1
            elif (G_screnn1_OK == 0):
                G_screnn1 = Screen_Date_Process(hex_16RGB)
                G_screnn1_OK = 1
            u_time1 = time.time() - u_time1
            print("Screenshot time taken " + str(u_time1))
        time.sleep(0.001)


def show_PC_Screen():  # Display photo
    global State_change, Screen_Error, Device_State, Thread1
    global G_screnn0_OK, G_screnn1_OK, G_screnn0, G_screnn1, size_USE_X1, size_USE_Y1
    if (State_change == 1):
        State_change = 0
        Screen_Error = 0
        LCD_ADD((160 - size_USE_X1) // 2, (80 - size_USE_Y1) // 2, size_USE_X1, size_USE_Y1)
    if (State_change == 0):

        if (G_screnn0_OK == 1 or G_screnn1_OK == 1):
            # print("Transmitting screen...")
            u_time = time.time()
            if (G_screnn0_OK == 1):
                # LCD_ADD((240-size_USE_X1)//2,(240-size_USE_Y1)//2,size_USE_X1,size_USE_Y1)
                SER_Write(G_screnn0)
                G_screnn0_OK = 0
            elif (G_screnn1_OK == 1):
                # LCD_ADD((240-size_USE_X1)//2,(240-size_USE_Y1)//2,size_USE_X1,size_USE_Y1)
                SER_Write(G_screnn1)
                G_screnn1_OK = 0
            u_time = time.time() - u_time
            # print("Transmission time taken "+str(u_time))
            Screen_Error = 0
        else:
            Screen_Error = Screen_Error + 1
            if Screen_Error > 1000:
                Device_State = 0
                try:  # Attempt to create screenshot thread
                    Thread1.stop()
                except:
                    print("Warning, unable to stop screenshot thread")
                try:  # Attempt to create screenshot thread
                    Thread1.start()
                except:
                    print("Warning, unable to create screenshot thread")
            # print("No screen to transmit")
        time.sleep(0.001)


def UI_Page():  # Display GUI
    global Label1, root, s1, s2, s3, Label2, Label3, Label4, Label5, Label6, Text1
    # Create main window
    root = tk.Tk()  # Instantiate main window
    root.title("USB Screen Assistant V1.0")  # Set title
    size_show = pyautogui.size()
    Show_X = int(size_show.width / 2) - int(Show_W / 2)
    Show_Y = int(size_show.height / 2) - int(Show_H / 2)
    root.geometry(str(Show_W) + "x" + str(Show_H) + "+" + str(Show_X) + "+" + str(
        Show_Y))  # Main window size and position on display
    # Create buttons
    btn1 = tk.Button(root, text="Previous Page", height=1, width=12)
    btn1.place(x=290, y=275, anchor="w")  # Set position and alignment
    btn1.config(command=Page_UP)  # Connect button trigger event

    btn2 = tk.Button(root, text="Next Page", height=1, width=12)
    btn2.place(x=430, y=275, anchor="w")  # Set position and alignment
    btn2.config(command=Page_Down)  # Connect button trigger event

    btn3 = tk.Button(root, text="Select Background Image", height=1, width=20)
    btn3.place(x=250, y=75, anchor="w")  # Set position and alignment
    btn3.config(command=Get_Photo_Path1)  # Connect button trigger event

    btn4 = tk.Button(root, text="Select Flash Firmware", height=1, width=20)
    btn4.place(x=250, y=125, anchor="w")  # Set position and alignment
    btn4.config(command=Get_Photo_Path2)  # Connect button trigger event

    btn5 = tk.Button(root, text="Burn", height=1, width=8)
    btn5.place(x=470, y=75, anchor="w")  # Set position and alignment
    btn5.config(command=Writet_Photo_Path1)  # Connect button trigger event

    btn6 = tk.Button(root, text="Burn", height=1, width=8)
    btn6.place(x=470, y=125, anchor="w")  # Set position and alignment
    btn6.config(command=Writet_Photo_Path2)  # Connect button trigger event

    btn7 = tk.Button(root, text="Switch Display Orientation", height=1, width=28)
    btn7.place(x=290, y=325, anchor="w")  # Set position and alignment
    btn7.config(command=LCD_Change)  # Connect button trigger event

    btn8 = tk.Button(root, text="Burn", height=1, width=8)
    btn8.place(x=470, y=175, anchor="w")  # Set position and alignment
    btn8.config(command=Writet_Photo_Path3)  # Connect button trigger event

    btn9 = tk.Button(root, text="Burn", height=1, width=8)
    btn9.place(x=470, y=225, anchor="w")  # Set position and alignment
    btn9.config(command=Writet_Photo_Path4)  # Connect button trigger event

    btn10 = tk.Button(root, text="Select Album Image", height=1, width=20)
    btn10.place(x=250, y=175, anchor="w")  # Set position and alignment
    btn10.config(command=Get_Photo_Path3)  # Connect button trigger event

    btn11 = tk.Button(root, text="Select Animated Image", height=1, width=20)
    btn11.place(x=250, y=225, anchor="w")  # Set position and alignment
    btn11.config(command=Get_Photo_Path4)  # Connect button trigger event

    # Create sliders
    s1 = Scale(root, from_=0, to=31, resolution=1, troughcolor='Red',
               orient=HORIZONTAL)  # orient=HORIZONTAL horizontal, default vertical
    s1.place(x=250, y=25, anchor="w")  # W.get()
    s1.set(31)
    s2 = Scale(root, from_=0, to=63, resolution=1, troughcolor='Green',
               orient=HORIZONTAL)  # orient=HORIZONTAL horizontal, default vertical
    s2.place(x=355, y=25, anchor="w")  # W.get() can get slider value
    s2.set(0)
    s3 = Scale(root, from_=0, to=31, resolution=1, troughcolor='Blue',
               orient=HORIZONTAL)  # orient=HORIZONTAL horizontal, default vertical
    s3.place(x=460, y=25, anchor="w")  # W.get() can get slider value
    s3.set(0)
    # Create labels
    Label1 = tk.Label(root, text="Device Not Connected", bg="Red")
    Label1.place(x=5, y=25, anchor="w")  # Set position and alignment

    Label2 = tk.Label(root, bg="Red", width=2)
    Label2.place(x=220, y=25, anchor="w")  # Set position and alignment

    Label3 = tk.Label(root, bg="white", width=21)
    Label3.place(x=5, y=75, anchor="w")  # Set position and alignment

    Label4 = tk.Label(root, bg="white", width=21)
    Label4.place(x=5, y=125, anchor="w")  # Set position and alignment

    Label5 = tk.Label(root, bg="white", width=21)
    Label5.place(x=5, y=175, anchor="w")  # Set position and alignment

    Label6 = tk.Label(root, bg="white", width=21)
    Label6.place(x=5, y=225, anchor="w")  # Set position and alignment

    # Text_Show=tk.StringVar()
    # Text_Show.set(0)
    # Create text box
    Text1 = tk.Text(root, width=23, height=4)
    Text1.place(x=5, y=300, anchor="w")  # Set position and alignment
    # Text1.delete(0,END)
    # Text1.insert(END,'content one') # Insert "content one" at beginning of text box
    Text1.delete(1.0, END)  # Clear text box

    # Enter message loop
    root.mainloop()


def Get_MSN_Device():  # Attempt to find MSN device
    global Device_State, ADC_det, Thread1, ser, State_change, State_machine, My_MSN_Device, My_MSN_Data, Screen_Error, Label1, LCD_Change_now, Text1
    port_list = list(serial.tools.list_ports.comports())  # Query all serial ports
    Thread1 = threading.Thread(target=Screen_Date_get)
    if len(port_list) == 0:
        print('No serial port detected, please ensure device is connected to computer')
        # Label1.config(text="Device Connected",bg="GREEN")
        time.sleep(1)
        Label1.config(text="Device Not Connected", bg="RED")
        Device_State = 0  # Unable to connect
        try:  # Attempt to create screenshot thread
            Thread1.stop()
        except:
            print("Warning, unable to stop screenshot thread")
    else:  # Monitor serial ports to ensure it is an MSN device
        My_MSN_Device = []
        My_MSN_Data = []
        for i in range(0, len(port_list)):
            try:  # Attempt to open serial port
                ser = serial.Serial(port_list[i].name, 19200, timeout=2)  # Initialize serial connection, initial use
            except:  # Exception occurred
                print(port_list[
                          i].name + ' cannot be opened, please check if it is being used by another program')  # Display MSN device count
                # ser.close() # Close serial port to prevent failure on next open
                time.sleep(0.1)
                continue  # Continue to next loop
            time.sleep(
                0.25)  # In theory, MSN device sends " MSN01" every 100ms, should receive at least once within 250ms
            recv = SER_Read()
            if (recv == 0):
                break  # Exit current for loop
            else:
                recv = recv.decode("gbk")  # Get serial data
            if (len(recv) > 5):  # Only parse when receiving 6 or more characters
                for n in range(0, len(recv) - 5):  # Parse encoding character by character
                    if (ord(recv[n]) == 0):  # Parse when current byte is 0
                        if ((recv[n + 1] == 'M') and (recv[n + 2] == 'S') and (
                                recv[n + 3] == 'N')):  # Ensure it is an MSN device
                            if ((recv[n + 4] >= '0') and (recv[n + 4] <= '9') and (recv[n + 5] >= '0') and (
                                    recv[n + 5] <= '9')):  # Ensure version number is ASCII digit
                                My_MSN_Device.append(MSN_Device((port_list[i].name), (ord(recv[4]) - 48) * 10 + (
                                            ord(recv[5]) - 48)))  # Register MSN device
                                hex_code = int(0).to_bytes(1, byteorder="little")  # Can add to array one by one
                                hex_code = hex_code + b'MSNCN'
                                SER_Write(hex_code)  # Return message
                                # Wait for response to confirm connection
                                time.sleep(
                                    0.25)  # In theory, MSN device sends " MSN01" every 100ms, should receive at least once within 250ms
                                recv = SER_Read().decode("gbk")  # Get serial data
                                if ((ord(recv[0]) == 0) and (recv[1] == 'M') and (recv[2] == 'S') and (
                                        recv[3] == 'N') and (recv[4] == 'C') and (
                                        recv[5] == 'N')):  # Ensure it is an MSN device
                                    print('MSN device ' + str(len(My_MSN_Device)) + ' — ' + port_list[
                                        i].name + ' connection completed')  # Display MSN device count
                                else:
                                    print('MSN device ' + str(
                                        len(My_MSN_Device)) + ' cannot connect, please check connection')  # Display MSN device count
                                break  # Exit current for loop
        print('Number of MSN devices: ' + str(len(My_MSN_Device)) + '')  # Display MSN device count
        if (len(My_MSN_Device) >= 1):
            Device_State = 1  # Can connect normally
            State_change = 1  # State changed
            # State_machine=5 # Define initial state (keep previous state)
            Screen_Error = 0
            Read_M_SFR_Data(256)  # Read 128 bytes after u8 at 0x0100
            Print_MSN_Data()  # Parse data format in bytes
            Read_MSN_Data(b'MSN_Status')
            UID = Read_MSN_Data(b'MSN_UID')
            try:  # Attempt to create screenshot thread
                Thread1.start()
            except:
                try:  # Attempt to create screenshot thread
                    Thread1.stop()
                except:
                    print("Warning, unable to stop screenshot thread")
                print("Warning, unable to create screenshot thread")
            # Get button status
            # LCD_State(1) # Configure display orientation
            ADC_det = Read_ADC_CH(9)
            ADC_det = (ADC_det + Read_ADC_CH(9)) / 2
            ADC_det = ADC_det - 125  # Determine if pressed based on threshold of 125
            Label1.config(text="Device Connected", bg="GREEN")
            LCD_Change_now = 0
            Text1.delete(1.0, END)  # Clear text box
            # Text1.insert(END,'Device ID:') # Insert at beginning of text box

            # Label1=tk.Label(root,text="Device Connected",bg="GREEN")

            # for i in range(1,37):
            #   Write_Flash_Photo_fast(100*(i-1),str(i)) #160*80 resolution color image, occupies 100 Pages

            # Write_Flash_Photo_fast(3600,'Demo1') #240*240 monochrome image, occupies 29 Pages
            # Write_Flash_Photo_fast(3629,'N48X66P') #48*66 resolution digital tube image, occupies 22 Pages

            # Write_Flash_ZK(3651,'ASC64') #32*64 resolution ASCII table, occupies 128 Pages

            # Write_Flash_Photo_fast(3779,'logo') #240*102 monochrome LOGO, occupies 12 Pages
            # Write_Flash_Photo_fast(3791,'J1') #240*240 monochrome image, occupies 29 Pages

            # Write_Flash_Photo_fast(3820,'MLOGO') #160*68 monochrome image, occupies 6 Pages
            # Write_Flash_Photo_fast(3826,'CLK_BG') #160*80 color image, occupies 100 Pages
            # Write_Flash_Photo_fast(3926,'PH1') #160*80 color image, occupies 100 Pages
            # Write_Flash_Photo_fast(4026,'N24X33P') #24*33 resolution digital tube image, occupies 12 Pages
            # Write_Flash_Photo_fast(4038,'MP1') #160*80 monochrome image, occupies 7 Pages

        else:
            Device_State = 0  # Cannot connect normally
            # try: # Attempt to stop screenshot thread
            #    Thread1.stop()
            # except:
            #    print("Warning, unable to stop screenshot thread")


def MSN_Device_1_State_machine():  # Loop state machine for MSN device 1
    global State_machine, time_out, key_eff, key_on, State_change, s1, s2, s3, color_use, Label2, photo_path1, photo_path2, write_path1, write_path2, LCD_Change_use, LCD_Change_now, write_path3, write_path4, Img_data_use
    # print("State_machine"+str(State_machine))
    # if write_path1==1:
    if LCD_Change_now != LCD_Change_use:  # Display orientation doesn't match setting
        LCD_Change_now = LCD_Change_use
        LCD_State(LCD_Change_now)  # Configure display orientation
        State_change = 1

    color_La = '#{:02x}{:02x}{:02x}'.format(int(s1.get()) * 8, int(s2.get()) * 4, int(s3.get()) * 8)
    Label2.config(bg=color_La)
    if (write_path1 == 1):
        Write_Flash_hex_fast(3826, Img_data_use)
        write_path1 = 0
        State_change = 1
    if (write_path2 == 1):
        Write_Flash_Photo_fast(0, photo_path2)
        write_path2 = 0
        State_change = 1

    if (write_path3 == 1):
        Write_Flash_hex_fast(3926, Img_data_use)
        write_path3 = 0
        State_change = 1

    if (write_path4 == 1):
        Write_Flash_hex_fast(0, Img_data_use)
        write_path4 = 0
        State_change = 1

    if (time_out == 1):
        time_out = 0
        if (Read_ADC_CH(9) < ADC_det):  # Button pressed
            key_on = 1
        elif (key_on == 1):
            key_eff = 1
            key_on = 0
        else:
            key_on = 0
        if (key_eff == 1):
            key_eff = 0
            State_machine = State_machine + 1
            if (State_machine > 5):
                State_machine = 0
            State_change = 1
    elif (State_machine == 0):
        show_gif()
    elif (State_machine == 1):
        show_PC_state(BLUE, BLACK)
    elif (State_machine == 2):
        color_now = int(s1.get()) * 2048 + int(s2.get()) * 32 + int(s3.get())
        if color_now != color_use:
            color_use = color_now
            State_change = 1

        show_PC_state(color_use, BLACK)
    elif (State_machine == 3):
        show_Photo1()
    elif (State_machine == 4):
        show_PC_time()
    elif (State_machine == 5):
        show_PC_Screen()


def Device_Loop():
    global D
    while (1):
        D = D + 1
        if (Device_State == 0):
            Get_MSN_Device()
        elif (Device_State == 1):
            MSN_Device_1_State_machine()
        if not threading.main_thread().is_alive():
            break


print("This device has " + str(psutil.cpu_count(logical=False)) + " cores and " + str(
    psutil.cpu_count()) + " logical processors")
print("This CPU has a base frequency of " + str(round((psutil.cpu_freq().current / 1000), 1)) + " GHZ")
print("Current CPU usage: " + str(psutil.cpu_percent()) + "%")  # Not entirely accurate
mem = psutil.virtual_memory()
print("This device has " + str(round(mem.total / (1024 * 1024 * 1024))) + " GB of RAM")
print("Current memory usage: " + str(mem.percent) + "%")
print("System started at " + datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
battery = psutil.sensors_battery()

if battery != None:
    print("Battery remaining: " + str(battery.percent) + "%")
# if battery.power_plugged:
#   print("Connected to power adapter")
# else:
#   print("Disconnected from power adapter")

# Create timer, delay 0.2 seconds
D = 0
# while(1):
#    D=D+1
#    print(D)
#    time.sleep(0.5)

timer1 = threading.Timer(0.2, TIM1)
time_out = 0
CPU = 0
FC = BLUE
BC = BLACK
key_on = 0
key_eff = 0
State_change = 1  # State changed
gif_num = 0
State_machine = 5  # Define initial state
Device_State = 0  # Initially disconnected
LCD_Change_use = 0  # Initial display orientation
LCD_Change_now = 0
color_use = RED
write_path1 = 0
write_path2 = 0
write_path3 = 0
write_path4 = 0
photo_path1 = ""
photo_path2 = ""
photo_path3 = ""
photo_path4 = ""

Thread1 = threading.Thread(target=Screen_Date_get)
Thread2 = threading.Thread(target=UI_Page)

timer1.start()  # Start timer

try:  # Attempt to create user interface
    # Thread2.start()

    Thread2 = threading.Thread(target=Device_Loop, daemon=True)
    Thread2.start()
    UI_Page()  # run Tk on the main thread — this blocks until the window closes
    sys.exit()
except:
    print("Warning, unable to create user interface")

while (1):
    D = D + 1
    # print(D)
    # print(Thread2.is_alive())

    if Thread2.is_alive() == False:  # User interface detected as closed
        try:  # Attempt to stop screenshot thread
            Thread1.stop()
        except:
            print("Warning, unable to stop screenshot thread")
        try:  # Attempt to stop screenshot thread
            Thread2.stop()
        except:
            print("Warning, unable to stop screenshot thread")
        sys.exit()  # Exit program
        break
    else:
        if (Device_State == 0):  # Device not detected
            Get_MSN_Device()  # Attempt to find MSN device
        # print("Waiting")
        elif (Device_State == 1):  # Device detected
            MSN_Device_1_State_machine()

            # time.sleep(10)
        # print("OK")