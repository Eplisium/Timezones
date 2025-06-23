import pytz
from datetime import datetime
import os

# Configuration for Home Time Zone (Change this to your preferred time zone)
HOME_TIMEZONE = "America/New_York"  # Example: You can set this to any valid time zone, e.g., "Europe/London"

# Optional Output Directory (Set to None or empty string to use the current directory)
OUTPUT_DIRECTORY = "./Timereports"  # Example: "C:/Users/Rue/Documents/TimeReports" or "./TimeReports"

# List of major time zones for comparison (can be customized)
MAJOR_TIMEZONES = [
    "America/Los_Angeles",  # Pacific Time (US)
    "America/Chicago",      # Central Time (US)
    "America/New_York",     # Eastern Time (US)
    "Europe/London",        # Greenwich Mean Time / British Summer Time
    "Europe/Paris",         # Central European Time
    "Asia/Dubai",           # Gulf Standard Time
    "Asia/Tokyo",           # Japan Standard Time
    "Australia/Sydney"      # Australian Eastern Time
]

def get_all_time_zones_times(home_tz):
    # Get the current UTC time
    utc_now = datetime.now(pytz.UTC)
    
    # List to store time zone information
    time_data = []
    home_data = None
    home_local_time = None
    
    # First, process the home time zone to get its local time for comparison
    try:
        home_timezone = pytz.timezone(home_tz)
        home_local_time = utc_now.astimezone(home_timezone)
        home_offset = home_local_time.utcoffset()
        if home_offset is not None:
            home_offset_seconds = home_offset.total_seconds()
            home_offset_hours = int(home_offset_seconds // 3600)
            home_offset_minutes = int((home_offset_seconds % 3600) // 60)
            home_offset_str = f"{home_offset_hours:+03d}:{abs(home_offset_minutes):02d}"
        else:
            home_offset_seconds = 0
            home_offset_hours = 0
            home_offset_minutes = 0
            home_offset_str = "+00:00"
        home_dst_active = "Yes" if home_local_time.dst() and home_local_time.dst().total_seconds() != 0 else "No"
        home_region = home_tz.split('/')[-1].replace('_', ' ') if '/' in home_tz else home_tz.replace('_', ' ')
        if '/' in home_tz and len(home_tz.split('/')) > 1:
            home_region = '/'.join(home_tz.split('/')[1:]).replace('_', ' ')
        home_data = {
            'timezone': home_tz,
            'time_24h': home_local_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'time_12h': home_local_time.strftime('%Y-%m-%d %I:%M:%S %p %Z'),
            'offset_str': home_offset_str,
            'offset_hours': home_offset_seconds / 3600 if home_offset else 0,
            'dst_active': home_dst_active,
            'region': home_region,
            'time_diff': "N/A (Home)"
        }
    except Exception as e:
        print(f"Error processing home timezone {home_tz}: {e}")
        home_data = None
    
    # Iterate over all time zones in pytz for the full list
    for tz in pytz.all_timezones:
        try:
            # Get the timezone object
            timezone = pytz.timezone(tz)
            # Convert UTC time to the local time of this timezone
            local_time = utc_now.astimezone(timezone)
            # Get the UTC offset in seconds and convert to hours and minutes
            offset = local_time.utcoffset()
            if offset is not None:
                offset_seconds = offset.total_seconds()
                offset_hours = int(offset_seconds // 3600)
                offset_minutes = int((offset_seconds % 3600) // 60)
                offset_str = f"{offset_hours:+03d}:{abs(offset_minutes):02d}"
            else:
                offset_seconds = 0
                offset_hours = 0
                offset_minutes = 0
                offset_str = "+00:00"
            # Check if DST is in effect
            dst_active = "Yes" if local_time.dst() and local_time.dst().total_seconds() != 0 else "No"
            # Format time in both 24-hour and 12-hour (AM/PM)
            time_24h = local_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            time_12h = local_time.strftime('%Y-%m-%d %I:%M:%S %p %Z')
            # Extract a simple region or description
            region = tz.split('/')[-1].replace('_', ' ') if '/' in tz else tz.replace('_', ' ')
            if '/' in tz and len(tz.split('/')) > 1:
                region = '/'.join(tz.split('/')[1:]).replace('_', ' ')
            # Calculate time difference from home (if home data exists and for major time zones)
            time_diff = "N/A"
            if home_local_time and tz in MAJOR_TIMEZONES:
                diff_seconds = offset_seconds - home_offset_seconds if home_offset else offset_seconds
                diff_hours = int(diff_seconds // 3600)
                diff_minutes = int((abs(diff_seconds) % 3600) // 60)
                time_diff = f"{diff_hours:+d}:{diff_minutes:02d}"
            # Store the data with offset for sorting
            time_data.append({
                'timezone': tz,
                'time_24h': time_24h,
                'time_12h': time_12h,
                'offset_str': offset_str,
                'offset_hours': offset_seconds / 3600 if offset else 0,
                'dst_active': dst_active,
                'region': region,
                'time_diff': time_diff
            })
        except Exception as e:
            print(f"Error processing timezone {tz}: {e}")
            continue
    
    # Sort the list by UTC offset (excluding home, which will be added at the top)
    time_data.sort(key=lambda x: x['offset_hours'])
    
    return home_data, time_data

def write_times_to_file(home_data, time_data, output_dir=""):
    # Create a filename with a timestamp to avoid overwriting
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"world_times_detailed_{timestamp}.txt"
    
    # If an output directory is specified, create it if it doesn't exist
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
        except Exception as e:
            print(f"Error creating output directory {output_dir}: {e}")
            print("Falling back to current directory.")
            output_path = filename
    else:
        output_path = filename
    
    # Write the data to a file with a nicely formatted table
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write a header
        f.write("World Times Detailed Report\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write("=" * 60 + "\n\n")
        f.write("This report includes current local times for all known time zones worldwide,\n")
        f.write("sorted by UTC offset (west to east). Times are shown in both 24-hour and 12-hour formats.\n")
        f.write(f"Home Time Zone: {HOME_TIMEZONE} (listed at top). Major time zones show time difference from Home.\n\n")
        
        # Write table header
        f.write(f"{'Time Zone':<35} {'Region/City':<25} {'24-Hour Time':<28} {'12-Hour Time':<28} {'UTC Offset':<12} {'DST Active':<12} {'Diff from Home':<15}\n")
        f.write("-" * 155 + "\n")
        
        # Write home time zone at the top if available
        if home_data:
            f.write(f"{home_data['timezone']:<35} {home_data['region']:<25} {home_data['time_24h']:<28} {home_data['time_12h']:<28} {home_data['offset_str']:<12} {home_data['dst_active']:<12} {home_data['time_diff']:<15}\n")
            f.write("-" * 155 + "\n")
        
        # Write data rows for all other time zones
        for entry in time_data:
            if entry['timezone'] != HOME_TIMEZONE:  # Avoid duplicating home entry
                f.write(f"{entry['timezone']:<35} {entry['region']:<25} {entry['time_24h']:<28} {entry['time_12h']:<28} {entry['offset_str']:<12} {entry['dst_active']:<12} {entry['time_diff']:<15}\n")
    
    print(f"Output written to {output_path}")

def main():
    print("Fetching current times for all time zones...")
    home_data, time_data = get_all_time_zones_times(HOME_TIMEZONE)
    print(f"Retrieved data for {len(time_data)} time zones.")
    write_times_to_file(home_data, time_data, OUTPUT_DIRECTORY)
    print("Done!")

if __name__ == "__main__":
    main()