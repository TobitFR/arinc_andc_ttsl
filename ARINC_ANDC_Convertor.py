# Made by TSK on May 28th 2024
# Version 1.6.2 - Developped on https://replit.com/@sinackt/ARINC-ANDC-Convertor#main.py
# Python 3.12.2

import time  # Used for the compilation timing
import PySimpleGUI as sg  # Used to create the GUI
import os.path  # Used to get the file path

# First the window layout in 3 columns

file_list_column = [
    [
        sg.Text("AIRAC File Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

second_file_list_column = [
    [
        sg.Text("Airport List Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER2-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST2-"
        )
    ],
]

# For now will only show the print log
text_viewer_column = [
    [sg.Text("Compilation log")],
    [sg.Multiline(size=(60, 20), key="-LOG-", autoscroll=True, reroute_stdout=True, reroute_stderr=True)],
    [sg.Checkbox('ATIS 8.33kHz -> 25kHz Conversion', default=True, key="-ATIS-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(second_file_list_column),
        sg.VSeperator(),
        sg.Column(text_viewer_column),
    ]
]

window = sg.Window("AIRAC Convertor - TSK", layout)

# Function to read the entire file content once
def read_file_content(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = sorted(os.listdir(folder))
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".pc"))
        ]
        window["-FILE LIST-"].update(fnames)

    elif event == "-FOLDER2-":
        folder2 = values["-FOLDER2-"]
        try:
            file_list2 = sorted(os.listdir(folder2))
        except:
            file_list2 = []

        fnames2 = [
            f
            for f in file_list2
            if os.path.isfile(os.path.join(folder2, f))
            and f.lower().endswith((".txt"))
        ]
        window["-FILE LIST2-"].update(fnames2)

    elif event == "-FILE LIST2-":  # A file was chosen from the listbox
        try:
            #Verifing that the AIRAC file has been defined
            try:
                fnames
            except NameError:
                sg.popup_auto_close("No AIRAC File Selected")

            # Start of time to beat ARE
            start_time = time.time()

            # Filename of AIRAC File
            filename_airac_file = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            # Filename of Airport List
            filename_airport_list = os.path.join(
                values["-FOLDER2-"], values["-FILE LIST2-"][0]
            )

            # Get the AIRAC cycle of the filename
            AIRACcycle = filename_airac_file[-7:-3]

            # Reading the AIRAC file and the Airport List file
            airac_file_content = read_file_content(filename_airac_file)
            airport_list_content = read_file_content(filename_airport_list)

            # Reading the header (first 4 lines) and footer
            header_content = ''.join(airac_file_content[:4])
            footer_content = 'SEURP EDDFEDGRW36    1131231770 N49595460E008313470               00325000050148      0000                                 151992307\nSEURP EDDFEDGRW36    2S                            35963Y        L00325                                                    152002307'
            print('Reading of header and footer...')

            # ------------------------------------------------------------------------------------------
            # Reading of the country_list.txt file
            with open(filename_airport_list, 'r') as country_list_file:
                country_list_data = country_list_file.read().splitlines()
                # Do not take in account the first row
                country_list_data = country_list_data[1:]    

                # Filtering for USA airports
                country_list_data_USA = [line for line in country_list_data if line.startswith('K')]
                # Filter USA airports only if they are in the list
                if len(country_list_data_USA) != 0:
                    print('USA airport(s) detected, proceeding to auto filtering')
                    # Removing the wrong USA airport from country list
                    country_list_data = [line for line in country_list_data if line not in country_list_data_USA]
                    # Search of USA's airport local ICAO code
                    USA_country_list_data = ['K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7']
                    # Filter lines containing K1/2... as country code and wanted USA airports
                    filtered_lines_USA_airports = [line[10:12] for line in airac_file_content if line[10:12] in USA_country_list_data and any(code in line[6:10] for code in country_list_data_USA)]
                # Take only the first 2 characters
                country_list_data = [line[:2] for line in country_list_data]
                # Filter USA airports only if they are in the list
                if len(country_list_data_USA) != 0:
                    # Merging the two lists
                    country_list_data = country_list_data + filtered_lines_USA_airports
                # Filter to remove duplicates
                country_list_data = list(set(country_list_data))
                # Sorting country by alphabetic order
                country_list_data.sort()
                print('Country list reading...')
                print(country_list_data)
                print(f"Number of country : {len(country_list_data)}")

            if "ALL" in country_list_data:
                filtered_lines_radnav = [line for line in airac_file_content if line[4:5] == 'D' or line[4:6] == 'DB']
                print('Export ALL countries VOR DME NDB')
            else:
                filtered_lines_radnav = [line for line in airac_file_content if line[19:21] in country_list_data and (line[4:5] == 'D' or line[4:6] == 'DB')]

            airport_list_data = sorted([line[:4] for line in airport_list_content[1:]])  # Sorting airport list alphabetically
            print(airport_list_data)
            filtered_lines_airport = [line for line in airac_file_content if line[6:10] in airport_list_data and (line[12:13] in 'AGIM' or line[12:16] == 'VATI')]
            if values["-ATIS-"]:
                filtered_lines_airport = [line[:22] + '0' + line[23:] if line[22] == '1' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]  # XXX.X10 -> XXX.X00
                filtered_lines_airport = [line[:22] + '2' + line[23:] if line[22] == '3' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]  # XXX.X30 -> XXX.X25
                filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '4' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]  # XXX.X40 -> XXX.X50
                filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '6' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]  # XXX.X60 -> XXX.X50
                filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '8' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]  # XXX.X80 -> XXX.X75
                filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '9' and line[12:16] == 'VATI' else line for line in filtered_lines_airport]  # XXX.X90 -> XXX.X75
                print('ATIS 8.33kHz to 25kHz conversion...')
            else:
                print('ATIS 8.33kHz to 25kHz conversion... skipped')

            if filtered_lines_airport:
                output_filename = os.path.join(folder, 'export_' + AIRACcycle + '.txt')
                with open(output_filename, 'w') as output_file:
                    output_file.write(header_content)
                    output_file.writelines(filtered_lines_radnav)
                    print(f"Number of radionav lines exported : {len(filtered_lines_radnav)}")
                    output_file.writelines(filtered_lines_airport)
                    print(f"Number of airport lines exported : {len(filtered_lines_airport)}")
                    output_file.write(footer_content)
                with open(output_filename, 'r') as export_file:
                    num_lines = sum(1 for line in export_file)
                    print(f'Number of lines in {output_filename}: {num_lines}')
                    #print(f"All files have been generated in {time.time() - start_time} seconds, you may now close the script.")
                    #sg.popup_auto_close(f"All files have been generated in {time.time() - start_time} seconds, you may now close the script.")
                    ch = sg.popup_auto_close(f"All files have been generated in {time.time() - start_time} seconds, you may now close the script.","Press OK to proceed",  title="AIRAC Convertor - TSK", keep_on_top=True)
            else:
                print("Error in filtering the lines")
                print(f"--- {time.time() - start_time} seconds ---")

        except Exception as e:
            print(f"An error occurred: {e}")

window.close()
