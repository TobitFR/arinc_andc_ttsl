#Made by TSK on April 10th 2024
#Version 1.2 - Developped on https://replit.com/@sinackt/ARINC-ANDC-Convertor#main.py
#Python 3.12.2

#Libraries
import time #Used for the compilation timing
import glob #Used to filter the AIRAC file to get last AIRAC file

#Start of time to beat ARE
start_time = time.time()

#Get all the files with a ".pc" extension
filename = glob.glob('./*.pc')#[-1]
#Sorting filename to get the latest ARINC file
filename = sorted(filename)
#Selecting the last one
filename = filename[-1]

#Get the AIRAC cycle of the filename
AIRACcycle = filename[10:14]


#Opening of the ARINC file
with open(filename, 'r') as file:
  print('Reading of ' + filename + ' file...')
  #Reading of the 4 first row of simaero.pc and making it the header
  header_content = file.readline() + file.readline() + file.readline() + file.readline()
  print('Reading and conversion of header...')

  #Reading of the footer
  with open('footer.txt', 'r') as footer_file:
    footer_content = footer_file.read()
    print('Reading of footer.txt file...')

  #Reading of the country_list.txt file
  with open('country_list.txt', 'r') as country_list_file:
      country_list_data = country_list_file.read().splitlines()
      #Do not take in account the first column
      country_list_data = country_list_data[1:]
      print('Country list reading...')
      print(country_list_data)
      print(f"Number of country : {len(country_list_data)}")

      #If the country_list_data contains "ALL" then show all the VOR DME NDB of all the world
      if "ALL" in country_list_data:
        print('Export ALL countries VOR DME NDB')
        filtered_lines_radnav = [line for line in file if line[4:5] == 'D' or line[4:6] == 'DB']
      else:
        #Use the country list to filter for the data only country
        filtered_lines_radnav = [line for line in file if line[19:21] in country_list_data]
        #Filtering the data the VOR, DME and NDB
        filtered_lines_radnav = [line for line in filtered_lines_radnav if line[4:5] == 'D' or line[4:6] == 'DB']

#Reopening of the ARINC, because without it won't work and I don't know why :(  
with open(filename, 'r') as file:
  #Reading of the airport_list.txt file
  with open('airport_list.txt', 'r') as airport_list_file:
      airport_list_data = airport_list_file.read().splitlines()
      #Do not take in account the first column
      airport_list_data = airport_list_data[1:]
      print('Airport list reading...')
      #print(airport_list_data)
      print(f"Number of airport : {len(airport_list_data)}")

  #Use the airport list to filter for the data only airport
  filtered_lines_airport = [line for line in file if line[6:10] in airport_list_data]
  #Filter only A|G|I|M|VATI data
  filtered_lines_airport = [line for line in filtered_lines_airport if line[12:13] == 'A' or line[12:13] == 'G' or line[12:13] == 'I' or line[12:13] == 'M' or line[12:16] == 'VATI']
  #Replace 8.33kHz to 25kHz frequency on ATIS - If character 22 is a 3 it become a 2 and so on
  filtered_lines_airport = [line[:22] + '0' + line[23:] if line[22] == '1' else line for line in filtered_lines_airport] #XXX.X10 -> XXX.X00
  filtered_lines_airport = [line[:22] + '2' + line[23:] if line[22] == '3' else line for line in filtered_lines_airport] #XXX.X30 -> XXX.X25
  filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '4' else line for line in filtered_lines_airport] #XXX.X40 -> XXX.X50
  filtered_lines_airport = [line[:22] + '5' + line[23:] if line[22] == '6' else line for line in filtered_lines_airport] #XXX.X60 -> XXX.X50
  filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '8' else line for line in filtered_lines_airport] #XXX.X80 -> XXX.X75
  filtered_lines_airport = [line[:22] + '7' + line[23:] if line[22] == '9' else line for line in filtered_lines_airport] #XXX.X90 -> XXX.X75
  print('ATIS 8.33kHz to 25kHz conversion...')


  #Output
  if filtered_lines_radnav:
      #Writing of the list in the file
      with open('export_' + AIRACcycle + '.txt', 'w') as output_file:
          #Addition of the header
          output_file.write(header_content)
          #Addition of the radnav data
          output_file.writelines(filtered_lines_radnav)
          print(f"Number of radionav lines exported : {len(filtered_lines_radnav)}")
          #Addition of the airport data
          output_file.writelines(filtered_lines_airport)
          print(f"Number of airport lines exported : {len(filtered_lines_airport)}")
          #Addition of the footer
          output_file.write(footer_content)
      # Counting the number of lines in the export.txt file
      with open('export_' + AIRACcycle + '.txt', 'r') as export_file:
          num_lines = sum(1 for line in export_file)
          print('Number of lines in export_' + AIRACcycle + '.txt: ', end='')
          print(num_lines)
          print("All files have been generated in %s seconds, you may now close the script." % (time.time() - start_time))

  else:
      print("Error RIP")
      print("--- %s seconds ---" % (time.time() - start_time))
