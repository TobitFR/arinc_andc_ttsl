
# ARINC ANDC Convertor

This Python script converts the ARINC 424 world file (assuming it follows the schema described in ARINC 424-17) into a restricted file for importing only the desired data into the ANDC of a TTSL simulator.


## Authors

- [@TobitFR](https://www.github.com/TobitFR)


## Features

- Airport selection (using airport_list.txt)
- Country VOR, DME & NDB selection (country_list.txt)
- Automatic conversion of 8.33kHz ATIS frequency to 25kHz compliant frequency (V1.1)
- Possibility to add a footer, to add manually add line to exported file (such as RWY36 for EDDF)
- A script timer to show to ARE how VB is obsolete ;)

## How to use

- Install Python version 3+ if not already installed. (3.8 maximum for Windows 7)
- Place the simaero_XXXX.pc file in the folder.
- Check that both airports_list.txt and country_list.txt are up to date with your need.
- Execute the main.py file.
- A new file named export.txt containing only the airports set on airport_list.txt, VOR, DME & NDB set on country_list.txt and footer if used will be created.
## Changelog
Version 1.1
- Addition of automatic conversion of 8.33kHz ATIS frequency to 25kHz compliant frequency
- Removed the need of renaming the filename from "simaero_XXXX.pc" to "simaero.pc". The script automatically take the latest file with ".pc" extension. Be carefull to not leave the older files - just in case ;)

Version 1.0
- Initial Release
