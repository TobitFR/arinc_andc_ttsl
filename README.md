
# ARINC ANDC Convertor

This Python script converts the ARINC 424 world file (assuming it follows the schema described in ARINC 424-17) into a restricted file for importing only the desired data into the ANDC of a TTSL simulator.


## Authors

- [@TobitFR](https://www.github.com/TobitFR)


## Features

- Airport selection (using airport_list.txt).
- Country VOR, DME & NDB selection (country_list.txt).
- Automatic conversion of 8.33kHz ATIS frequency to 25kHz compliant frequency (V1.1).
- Possibility to add a footer, to add manually add line to exported file (such as RWY36 for EDDF).
- A script timer to show to ARE how VB is obsolete ;)

## How to use

- Install Python version 3+ if not already installed. (3.8 maximum for Windows 7)
- Place the simaero_XXXX.pc file in the folder.
- Check that both airports_list.txt are up to date with your need.
- Execute the main.py file.
- A new file named export_XXXX.txt containing only the airports set on airport_list.txt, VOR, DME & NDB will be added for the whole country based on the aiports countries (the whole country is added of the is an airport set for the country) and footer if used, will be created.
  
## Changelog
Version 1.4 (April 15th 2024)
 - HotFix : ATIS function was modifying all 22th caracters regardless if it's ATIS or not causing VHF frequency to become unusable (009.90 io 109.90)

Version 1.3 (April 13th 2024)
 - Removal of the country_list.txt, country_list will be created using the airports ICAO, if there is USA airport, the ICAO will be converted to the right KX.

Version 1.2 (April 10th 2024)
- Addition of possibility of taking the whole world for the VOR DME NDB part.

Version 1.1 (April 8th 2024)
- Addition of automatic conversion of 8.33kHz ATIS frequency to 25kHz compliant frequency.
- Removed the need of renaming the filename from "simaero_XXXX.pc" to "simaero.pc". The script automatically take the latest file with ".pc" extension. Be carefull to not leave the older files - just in case ;)
- Addition of the AIRAC cycle on the export filename.

Version 1.0 (April 8th 2024)
- Initial Release
