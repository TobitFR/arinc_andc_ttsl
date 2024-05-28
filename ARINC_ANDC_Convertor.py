#Made by TSK on May 28th 2024
#Version 1.6 - Developped on https://replit.com/@sinackt/ARINC-ANDC-Convertor#main.py
#Python 3.12.2

import time  # Used for the compilation timing
import PySimpleGUI as sg # Used to create the GUI
import os.path # Used to get the file path
import sys

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
    [sg.Text("Print Log")],
    [sg.Multiline(size=(60, 20), key="-LOG-", autoscroll=True, reroute_stdout=True, reroute_stderr=True)],
    [sg.Checkbox('Modif ATIS', default=True, key="-ATIS-")],
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
            # Start of time to beat ARE
            start_time = time.time()

            #Filename of AIRAC File
            filename_airac_file = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            #Filename of Airport List
            filename_airport_list = os.path.join(
                    values["-FOLDER2-"], values["-FILE LIST2-"][0]
                )

            # Get the AIRAC cycle of the filename
            AIRACcycle = filename_airac_file[-7:-3]

            # Opening of the ARINC file
            with open(filename_airac_file, 'r') as file:
                print('Reading of ' + filename_airac_file + ' file...')
                # Reading of the 4 first row of simaero.pc and making it the header
                header_content = file.readline() + file.readline() + file.readline() + file.readline()
                print('Reading and conversion of header...')

            # Reading of the footer

                    #WARNING TEMPORARY : 
                     
            #with open('footer.txt', 'r') as footer_file:
            #    footer_content = footer_file.read()
            footer_content = 'SEURP EDDFEDGRW36    1131231770 N49595460E008313470               00325000050148      0000                                 151992307\nSEURP EDDFEDGRW36    2S                            35963Y        L00325                                                    152002307'
            print('Reading of footer.txt file...')



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
                    # All lines containing K1/2... as country code
                    with open(filename_airac_file, 'r') as file:
                        filtered_lines_USA_airports = [line for line in file if line[10:12] in USA_country_list_data]
                        # All lines containing wanted USA airport
                        filtered_lines_USA_airports = [line for line in filtered_lines_USA_airports if
                                                       any(code in line[6:10] for code in country_list_data_USA)]
                        filtered_lines_USA_airports = [line[10:12] for line in filtered_lines_USA_airports]
                        # Filter to remove duplicates
                        filtered_lines_USA_airports = list(set(filtered_lines_USA_airports))
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

                with open(filename_airac_file, 'r') as file:

                    # If the country_list_data contains "ALL" then show all the VOR DME NDB of all the world
                    if "ALL" in country_list_data:
                        filtered_lines_radnav = [line for line in file if line[4:5] == 'D' or line[4:6] == 'DB']
                        print('Export ALL countries VOR DME NDB')
                    else:
                        # Use the country list to filter for the data only country
                        filtered_lines_radnav = [line for line in file if line[19:21] in country_list_data]
                        # Filtering the data the VOR, DME and NDB
                        filtered_lines_radnav = [line for line in filtered_lines_radnav if
                                                 line[4:5] == 'D' or line[4:6] == 'DB']

                # ------------------------------------------------------------------------------------------

                # Reopening of the ARINC, because without it won't work and I don't know why :(
                with open(filename_airac_file, 'r') as file:
                    # Reading of the airport_list.txt file
                    with open(filename_airport_list, 'r') as airport_list_file:
                        airport_list_data = airport_list_file.read().splitlines()
                        # Do not take in account the first row
                        airport_list_data = airport_list_data[1:]
                        # Sorting airport by alphabetic order
                        airport_list_data.sort()
                        print('Airport list reading...')
                        print(airport_list_data)
                        print(f"Number of airport : {len(airport_list_data)}")

                    # Use the airport list to filter for the data only airport
                    filtered_lines_airport = [line for line in file if line[6:10] in airport_list_data]
                    # Filter only A|G|I|M|VATI data
                    filtered_lines_airport = [line for line in filtered_lines_airport if
                                              line[12:13] == 'A' or line[12:13] == 'G' or line[12:13] == 'I' or line[
                                                  12:13] == 'M' or line[12:16] == 'VATI']
                    if values["-ATIS-"] == True:
                        # Replace 8.33kHz to 25kHz frequency on ATIS - If character 22 is a 1 it become a 0 and so on
                        filtered_lines_airport = [line[:22] + '0' + line[23:] if line[22] == '1' and line[12:16] == 'VATI' else line for line in
                                                filtered_lines_airport]  # XXX.X10 -> XXX.X00
                        filtered_lines_airport = [line[:22] + '2' + line[23:] if line[22] == '3' and line[12:16] == 'VATI' else line for line in
                                                filtered_lines_airport]  # XXX.X30 -> XXX.X25
                        filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '4' and line[12:16] == 'VATI' else line for line in
                                                filtered_lines_airport]  # XXX.X40 -> XXX.X50
                        filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '6' and line[12:16] == 'VATI' else line for line in
                                                filtered_lines_airport]  # XXX.X60 -> XXX.X50
                        filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '8' and line[12:16] == 'VATI' else line for line in
                                                filtered_lines_airport]  # XXX.X80 -> XXX.X75
                        filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '9' and line[12:16] == 'VATI' else line for line in
                                                filtered_lines_airport]  # XXX.X90 -> XXX.X75
                        print('ATIS 8.33kHz to 25kHz conversion...')
                    else:
                        print('ATIS 8.33kHz to 25kHz conversion... skipped')

                # ------------------------------------------------------------------------------------------

                # Output
                if filtered_lines_airport:
                    # Writing of the list in the file
                    with open('export_' + AIRACcycle + '.txt', 'w') as output_file:
                        # Addition of the header
                        output_file.write(header_content)
                        # Addition of the radnav data
                        output_file.writelines(filtered_lines_radnav)
                        print(
                            f"Number of radionav lines exported : {len(filtered_lines_radnav)}")
                        # Addition of the airport data
                        output_file.writelines(filtered_lines_airport)
                        print(
                            f"Number of airport lines exported : {len(filtered_lines_airport)}")
                        # Addition of the footer
                        output_file.write(footer_content)
                        # Counting the number of lines in the export.txt file
                    with open('export_' + AIRACcycle + '.txt', 'r') as export_file:
                        num_lines = sum(1 for line in export_file)
                        print('Number of lines in export_' + AIRACcycle + '.txt: ', end='')
                        print(num_lines)
                        print(
                            "All files have been generated in %s seconds, you may now close the script."
                            % (time.time() - start_time))
                else:
                    print("Error in filtering the lines")
                    print("--- %s seconds ---" % (time.time() - start_time))

        except:
            pass

window.close()
