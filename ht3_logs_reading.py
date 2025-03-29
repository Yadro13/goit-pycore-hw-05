import sys
from pathlib import Path

USAGE = "Usage: python ht3_logs_reading.py path/to/logfile.log [LEVEL: 'info', 'debug', 'warning' or 'error']"

LEVELS = ["INFO", "DEBUG", "ERROR", "WARNING"]

# Parsing log line
def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 3) # stripping log line
    if len(parts) < 4:
        return {}
    date, time, level, message = parts # assign parts to variables
    return {"date": date, "time": time, "level": level.upper(), "message": message}

# Loading logs from file
def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r') as file:
            logs = [parsed for line in file if (parsed := parse_log_line(line))]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the log file: {e}")
        sys.exit(1)
    return logs

# Filtering logs by level
def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log['level'] == level.upper(), logs))

# Counting logs by level
def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts

# Displaying log count table
def display_log_counts(counts: dict):
    print("\nLogging level | Quantity")
    print("--------------|----------")
    for level in LEVELS:
        print(f"{level:<14}| {counts.get(level, 0)}")

# Displaying filtered logs
def display_filtered_logs(logs: list, level: str):
    print(f"\nLog details for level '{level.upper()}':")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")

# Main program
def main():
    
    # Check arguments q-ty
    if len(sys.argv) != 2:
        print(USAGE) # pring helper usage message
        sys.exit(1)

    # Get filepath as 1st argument
    file_path = sys.argv[1]
    # Get level as 2nd argument
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path) # load logs from file
    counts = count_logs_by_level(logs) # count log lines by levels
    display_log_counts(counts) # call display function

    # Check if levels are in LEVELS list
    if level_filter.upper() in LEVELS:
        filtered = filter_logs_by_level(logs, level_filter) # call filtered function
        display_filtered_logs(filtered, level_filter) # call display function
    else:
        print(USAGE) # pring helper usage message

if __name__ == "__main__":
    main()