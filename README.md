# Worldwide Time Zones Script

## Overview

This Python script retrieves and displays the current local times for all known time zones worldwide. It generates a detailed text report that includes time in both 24-hour and 12-hour formats, UTC offset, Daylight Saving Time (DST) status, and time differences from a configurable "home" time zone. The report is sorted by UTC offset for easy reference.

The script is designed to be simple, customizable, and useful for developers, travelers, or anyone needing a quick global time overview.

## Features

- Fetches current times for all time zones using the `pytz` library.
- Allows configuration of a home time zone for personalized time differences.
- Outputs a formatted text file with a table of time zone data.
- Supports customization of major time zones for which time differences are calculated.
- Handles DST and UTC offsets automatically.

## Prerequisites

- **Python Version**: Python 3.6 or higher.
- **Dependencies**:
  - `pytz`: A library for handling time zones. Install it using pip.

## Installation

1. Clone or download the script to your local machine.
2. Install the required dependencies by running the following command in your terminal or command prompt:

   ```
   pip install pytz
   ```

## Configuration

Before running the script, open `worldwide.py` and edit the configuration variables at the top of the file. These are clearly marked for easy modification:

- **HOME_TIMEZONE**: Set this to your preferred time zone string (e.g., `"America/New_York"`). This is used as the reference for calculating time differences in major time zones.
- **OUTPUT_DIRECTORY**: Specify a directory path for saving the output file (e.g., `"./Timereports"`). Set it to an empty string or `None` to save files in the current directory.
- **MAJOR_TIMEZONES**: A list of time zones for which the script calculates and displays the time difference from the home time zone. The default list includes common zones like `"America/Los_Angeles"`, `"Europe/London"`, etc. You can add or remove entries as needed.

Example configuration snippet from the script:

```python
HOME_TIMEZONE = "America/New_York"  # Change to your preferred time zone
OUTPUT_DIRECTORY = "./Timereports"  # Or set to an empty string for the current directory
MAJOR_TIMEZONES = [
    "America/Los_Angeles",
    "America/Chicago",
    "America/New_York",
    "Europe/London",
    "Europe/Paris",
    "Asia/Dubai",
    "Asia/Tokyo",
    "Australia/Sydney"
]
```

## Usage

To run the script, simply execute it from your terminal or command prompt:

```
python worldwide.py
```

- The script will fetch the current times, process the data, and generate a text file in the specified output directory.
- Output file name: Something like `world_times_detailed_YYYYMMDD_HHMMSS.txt` (e.g., `world_times_detailed_20231015_143020.txt`).
- The process may take a few seconds, as it handles all available time zones.

## Output Format

The generated text file contains a detailed report with the following structure:

- **Header**: Includes the generation timestamp and a brief description.
- **Table**: A formatted table with the following columns:
  - **Time Zone**: The full time zone string (e.g., "America/New_York").
  - **Region/City**: A simplified region or city name (e.g., "New York").
  - **24-Hour Time**: Current time in 24-hour format (e.g., "2023-10-15 14:30:00 EDT").
  - **12-Hour Time**: Current time in 12-hour format (e.g., "2023-10-15 02:30:00 PM EDT").
  - **UTC Offset**: The offset from UTC (e.g., "+05:00").
  - **DST Active**: "Yes" if Daylight Saving Time is in effect, otherwise "No".
  - **Diff from Home**: Time difference from the home time zone (only for major time zones, e.g., "+3:00").

Example snippet from the output file:

```
Time Zone                        Region/City                 24-Hour Time                  12-Hour Time                  UTC Offset   DST Active  Diff from Home
-----------------------------------------------------------------------------------------------
America/New_York                 New York                    2023-10-15 14:30:00 EDT      2023-10-15 02:30:00 PM EDT    -04:00       Yes         N/A (Home)
...
Europe/London                    London                      2023-10-15 19:30:00 BST      2023-10-15 07:30:00 PM BST    +01:00       Yes         +05:00
```

## Notes

- **Error Handling**: The script includes basic error handling for invalid time zones or directory creation issues. Any errors will be printed to the console.
- **Performance**: Processing all time zones can be resource-intensive, as there are hundreds of them. If you only need a subset, consider modifying the script to filter time zones.
- **Customization Ideas**: You could extend the script to add features like email notifications, CSV output, or integration with other tools.
- **License**: This script is provided as-is. Consider adding a license (e.g., MIT) if you plan to share it publicly.

## Contributing

If you'd like to improve this script, feel free to fork the repository (if it exists) and submit pull requests. For bugs or suggestions, please open an issue or contact the author.

Author: Rue  
Created: [12:46 AM 6/23/2025]

---
