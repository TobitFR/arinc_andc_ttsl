
# ARINC ANDC Convertor

This Python script converts the ARINC 424 world file (assuming it follows the schema described in ARINC 424-17) into a restricted file for importing only the desired data into the ANDC of a TTSL simulator.


## Authors

- [@TobitFR](https://www.github.com/TobitFR)


## Features

- Airport selection (using airport_list.txt).
- Automatic country VOR, DME & NDB selection using the airport selection (V1.3).
- Automatic conversion of 8.33kHz ATIS frequency to 25kHz compliant frequency (V1.1), possibility to disable this function (V1.6).
- Automatic conversion of American ICAO to the right region code, ie KLAX -> K2 (V1.3).
- A nice graphical user interface using PySimpleGUI (V1.6).
- Possibility to add a footer, to add manually add line to exported file (such as RWY36 for EDDF).
- A script timer to show to ARE how VB is obsolete ;)

## How to use

- Execute the ARINC_ANDC_Convertor.exe.
- On "AIRAC File Folder" select the folder containing the simaero_XXXX.pc file.
- Select the desired "simaero_XXXX.pc" file.
- Check or uncheck the "ATIS 8.33kHz -> 25kHz Conversion" depending of the simulator.
- On "Airport List Folder" select the folder containing the airport_list.txt file.
- Select the desired ".txt" file, the software will disregard the first line, for the next line only put one ICAO per line.
- Once the ".txt" file is selected, the software will compile data. The compilation log is shown on the right column.
- The compiled file is exported in the "AIRAC File Folder".
  
## Changelog

Version 1.6.2 (May 28th 2024)
 - Addition of a pop-up at the end the compilation.
 - Addition of a warning pop-up in case the AIRAC file was not selected.

Version 1.6.1 (May 28th 2024)
 - Various optimizations, mainly simaero_XXXX.pc is now opened once instead of three times. Execution for A330-340, v1.6 : 1,68s -> v1.7 : 1,38s. (Thanks to GPT-4o)

Version 1.6 (May 28th 2024)
 - Addition of Graphical User Interface using PySimpleGUI.
 - Addition of a checkbox enabling or disabling the ATIS 25kHz conversion.
 - Removal of the need to put all the files in the same folder.
 - Removal of the footer.txt, now incorporated in the code - this might change.

Version 1.5 (XX XX 2024)
 - Various fix

Version 1.4 (April 15th 2024)
 - HotFix : ATIS function was modifying all 22th caracters regardless if it's ATIS or not causing VHF frequency to become unusable (009.90 io 109.90)

Version 1.3 (April 13th 2024)
 - Removal of the country_list.txt, country_list will be created using the airports ICAO (if at least one airport on a counrty is selected the whole country VOR/DME/NDB will be added), if there is an american airport, the ICAO will be converted to the right region code (ie KX).

Version 1.2 (April 10th 2024)
- Addition of possibility of taking the whole world for the VOR DME NDB part.

Version 1.1 (April 8th 2024)
- Addition of automatic conversion of 8.33kHz ATIS frequency to 25kHz compliant frequency.
- Removed the need of renaming the filename from "simaero_XXXX.pc" to "simaero.pc". The script automatically take the latest file with ".pc" extension. Be carefull to not leave the older files - just in case ;)
- Addition of the AIRAC cycle on the export filename.

Version 1.0 (April 8th 2024)
- Initial Release
