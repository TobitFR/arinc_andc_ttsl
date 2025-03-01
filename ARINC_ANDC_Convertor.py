# Made by TSK on March 1st 2025
# Version 1.9
# Python 3.13.2 = to install on W10 : py -m pip install auto-py-to-exe


import time  # Used for the compilation timing
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.constants import END  # Add explicit import of END constant

# Function to read the entire file content once
def read_file_content(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Function to extract AIRAC cycle from file
def extract_airac_cycle(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                return lines[1][35:39]  # Extract characters 36-40 (0-based index)
            return ""
    except:
        return ""

# Function to extract airport list from file
def extract_airport_list(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Skip header and get airport codes
            return [line.strip()[:4] for line in lines[1:] if line.strip()]
    except:
        return []

# Functions to browse files
def browse_airac_file():
    filename = filedialog.askopenfilename(filetypes=[('PC Files', '*.pc')])
    if filename:
        airac_file_path.set(filename)
        # Extract and display AIRAC cycle
        cycle = extract_airac_cycle(filename)
        airac_cycle_label.config(text=f"AIRAC Cycle: {cycle}")
        airac_cycle_var.set(cycle)

def browse_airport_file():
    filename = filedialog.askopenfilename(filetypes=[('TXT Files', '*.txt')])
    if filename:
        airport_file_path.set(filename)
        # Extract and display airport list
        airports = extract_airport_list(filename)
        airport_list_text.delete(1.0, END)
        # Format airports: 10 per line with fixed spacing
        sorted_airports = sorted(airports)
        formatted_lines = []
        for i in range(0, len(sorted_airports), 10):
            line_airports = sorted_airports[i:i+10]
            # Calculate padding for centering
            line_text = ' '.join(f"{airport:<4}" for airport in line_airports)
            padding = (49 - len(line_text)) // 2
            formatted_lines.append(' ' * padding + line_text)
        airport_list_text.insert(END, '\n'.join(formatted_lines))
        log_text.insert(END, f"Loaded {len(airports)} airports\n")

# Function to compile the data
def compile_files():
    if airac_file_path.get() and airport_file_path.get():
        filename_airac_file = airac_file_path.get()
        filename_airport_list = airport_file_path.get()
        folder = os.path.dirname(filename_airac_file)

        # Start of time measurement
        start_time = time.time()

        # Get the AIRAC cycle from the file content
        AIRACcycle = airac_cycle_var.get()

        # Reading the AIRAC file and the Airport List file
        airac_file_content = read_file_content(filename_airac_file)
        airport_list_content = read_file_content(filename_airport_list)

        # Reading the header (first 4 lines) and footer
        header_content = ''.join(airac_file_content[:4])
        footer_content = 'SEURP EDDFEDGRW36    1131231770 N49595460E008313470               00325000050148      0000                                 151992307\nSEURP EDDFEDGRW36    2S                            35963Y        L00325                                                    152002307'
        log_text.insert(END, 'Reading of header and footer...\n')

        # ------------------------------------------------------------------------------------------
        # Reading the country_list.txt file
        with open(filename_airport_list, 'r') as country_list_file:
            country_list_data = country_list_file.read().splitlines()
            # Skip the first row
            country_list_data = country_list_data[1:]
            # Filtering for USA airports
            country_list_data_USA = [line for line in country_list_data if line.startswith('K')]
            if country_list_data_USA:
                log_text.insert(END, 'USA airport(s) detected, proceeding to auto filtering\n')
                country_list_data = [line for line in country_list_data if line not in country_list_data_USA]
                USA_country_list_data = ['K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7']
                filtered_lines_USA_airports = [line[10:12] for line in airac_file_content if line[10:12] in USA_country_list_data and any(code in line[6:10] for code in country_list_data_USA)]
                country_list_data = [line[:2] for line in country_list_data]
                if country_list_data_USA:
                    country_list_data += filtered_lines_USA_airports
                country_list_data = list(set(country_list_data))
                country_list_data.sort()

                # Log country list with count
                log_text.insert(END, f'Country list reading... {country_list_data} (Number of countries: {len(country_list_data)})\n')

            filtered_lines_radnav = [line for line in airac_file_content if line[19:21] in country_list_data and (line[4:5] == 'D' or line[4:6] == 'DB')]

            airport_list_data = sorted([line[:4] for line in airport_list_content[1:]])  # Sorting airport list alphabetically
            log_text.insert(END, f"Airport list... {airport_list_data} (Number of airports: {len(airport_list_data)})\n")
            filtered_lines_airport = [line for line in airac_file_content if line[6:10] in airport_list_data and (line[12:13] in 'AGIM' or line[12:16] == 'VATI')]

            if atis_var.get():
                # Apply ATIS conversion
                log_text.insert(END, 'ATIS 8.33kHz to 25kHz conversion...\n')
                filtered_lines_airport = [line[:22] + '0' + line[23:] if line[22] == '1' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]
                filtered_lines_airport = [line[:22] + '2' + line[23:] if line[22] == '3' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]
                filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '4' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]
                filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '6' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]
                filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '8' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]
                filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '9' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]
            else:
                log_text.insert(END, 'ATIS 8.33kHz to 25kHz conversion... skipped\n')

            if filtered_lines_airport:
                output_filename = os.path.join(folder, 'export_' + AIRACcycle + '.txt')
                with open(output_filename, 'w') as output_file:
                    output_file.write(header_content)
                    output_file.writelines(filtered_lines_radnav)
                    log_text.insert(END, f"Number of radionav lines exported : {len(filtered_lines_radnav)}\n")
                    output_file.writelines(filtered_lines_airport)
                    log_text.insert(END, f"Number of airport lines exported : {len(filtered_lines_airport)}\n")
                    # Only add footer_content if EDDF is in the airport list
                    if 'EDDF' in airport_list_data:
                        output_file.write(footer_content)
                        log_text.insert(END, "Footer content added (EDDF found in airport list)\n")
                    else:
                        log_text.insert(END, "Footer content skipped (EDDF not in airport list)\n")
                with open(output_filename, 'r') as export_file:
                    num_lines = sum(1 for line in export_file)
                    log_text.insert(END, f'Number of lines in {output_filename}: {num_lines}\n')
                    messagebox.showinfo("AIRAC Convertor", f"All files have been generated in {time.time() - start_time} seconds.")
            else:
                log_text.insert(END, "Error in filtering the lines\n")
                log_text.insert(END, f"--- {time.time() - start_time} seconds ---\n")
    else:
        messagebox.showwarning("Input Error", "You need to choose both files!")

# Creating the Tkinter window
root = tk.Tk()
root.title("AIRAC Convertor - TSK x GPT - v1.9")
root.configure(bg='#f0f0f0')  # Light gray background

# Style configuration
style = ttk.Style()
style.configure('TButton', padding=5)
style.configure('TLabel', padding=2)

# Variables
airac_file_path = tk.StringVar()
airport_file_path = tk.StringVar()
atis_var = tk.BooleanVar(value=True)
airac_cycle_var = tk.StringVar()

# Main Layout Frame
frame_main = tk.Frame(root, bg='#f0f0f0')
frame_main.pack(padx=20, pady=20, fill='both', expand=True)

# Left frame for file inputs and buttons
frame_left = tk.Frame(frame_main, bg='#f0f0f0', relief='groove', borderwidth=2)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Title
title_label = tk.Label(frame_left, text="AIRAC Data Converter", font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#2c3e50')
title_label.grid(row=0, column=0, columnspan=3, pady=(10,20), sticky='ew')

# File selection section
file_frame = tk.Frame(frame_left, bg='#f0f0f0')
file_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=10)

tk.Label(file_frame, text="AIRAC File (.pc):", bg='#f0f0f0', fg='#2c3e50', font=('Arial', 10)).grid(row=0, column=0, sticky='w')
tk.Entry(file_frame, textvariable=airac_file_path, width=50, bg='white', relief='solid').grid(row=0, column=1, padx=5)
tk.Button(file_frame, text="Browse", command=browse_airac_file, relief='groove', bg='#3498db', fg='white', padx=10).grid(row=0, column=2)

# AIRAC Cycle display
airac_cycle_label = tk.Label(file_frame, text="AIRAC Cycle: ", font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#e74c3c')
airac_cycle_label.grid(row=1, column=0, columnspan=3, sticky='w', pady=(10,5))

tk.Label(file_frame, text="Airport List (.txt):", bg='#f0f0f0', fg='#2c3e50', font=('Arial', 10)).grid(row=2, column=0, sticky='w')
tk.Entry(file_frame, textvariable=airport_file_path, width=50, bg='white', relief='solid').grid(row=2, column=1, padx=5)
tk.Button(file_frame, text="Browse", command=browse_airport_file, relief='groove', bg='#3498db', fg='white', padx=10).grid(row=2, column=2)

# Airport List display section
airport_frame = tk.Frame(frame_left, bg='#f0f0f0')
airport_frame.grid(row=2, column=0, columnspan=3, sticky='ew', padx=10, pady=10)

tk.Label(airport_frame, text="Selected Airports:", font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(anchor='center')
airport_list_text = tk.Text(airport_frame, height=5, width=49, font=('Courier', 10), bg='white', relief='solid')
airport_list_text.pack(expand=True, pady=(5,5))

# Options and Buttons section
options_frame = tk.Frame(frame_left, bg='#f0f0f0')
options_frame.grid(row=3, column=0, columnspan=3, sticky='ew', padx=10, pady=10)

# Create a sub-frame for the checkbox to center it
checkbox_frame = tk.Frame(options_frame, bg='#f0f0f0')
checkbox_frame.pack(fill='x', pady=5)
tk.Checkbutton(checkbox_frame, text="ATIS 8.33kHz -> 25kHz Conversion", variable=atis_var, bg='#f0f0f0', fg='#2c3e50', selectcolor='#3498db').pack(expand=True)

# Create a sub-frame for buttons and align them to the right
button_frame = tk.Frame(options_frame, bg='#f0f0f0')
button_frame.pack(fill='x', pady=10)
button_frame.grid_columnconfigure(0, weight=1)  # This will push buttons to the right

tk.Button(button_frame, text="Compile", command=compile_files, relief='groove', bg='#2ecc71', fg='white', width=15, height=1, font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Exit", command=root.destroy, relief='groove', bg='#e74c3c', fg='white', width=15, height=1, font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5)

# Right frame for logs
frame_right = tk.Frame(frame_main, bg='#f0f0f0', relief='groove', borderwidth=2)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

tk.Label(frame_right, text="Compilation Log", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', padx=10, pady=10)
log_text = tk.Text(frame_right, height=20, width=80, font=('Consolas', 9), bg='white', relief='solid')
log_text.pack(fill='both', expand=True, padx=10, pady=(0,10))

# Adjust frames to expand when the window is resized
frame_main.grid_columnconfigure(1, weight=1)
frame_main.grid_rowconfigure(0, weight=1)
frame_right.grid_columnconfigure(0, weight=1)
frame_right.grid_rowconfigure(1, weight=1)

root.mainloop()
