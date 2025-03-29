import sys

def load_logs(file_path: str) -> list:
    pass

def parse_log_line(line: str) -> dict:
    pass

def filter_logs_by_level(logs: list, level: str) -> list:
    pass

def count_logs_by_level(logs: list) -> dict:
    pass

def display_log_counts(counts: dict):
    pass

if __name__ == "__main__":
    
    sent_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if sent_path.exists():
        load_logs(sent_path)
    else:
        print(f"Path {sent_path} does not exist")