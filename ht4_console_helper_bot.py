from pathlib import Path
import json
from colorama import Fore, Style, init

init(autoreset=True)
PHONEBOOK = 'contacts.json'
json_path = Path(PHONEBOOK)

# Error messages for ValueError
FUNC_LIST_VALUE_ERROR = {
    "add_contact": "To add a record please use: add [name] [phone]",
    "change_contact": "To change a record please use: change [name] [new phone]",
    "delete_contact": "To delete a record please use: delete [name]",
    "show_contact": "To show a record please use: show [name]",
}

# Error messages for KeyError
FUNC_LIST_KEY_ERROR = {
    "add_contact": "Key Error ADD", # Cannot imagine this case
    "change_contact": "Contact is not found in the phonebook. Can't change",
    "delete_contact": "Contact is not found in the phonebook. Can't delete",
    "show_contact": "Contact is not found in the phonebook. Can't show",
}

# Error messages for IndexError
FUNC_LIST_INDEX_ERROR = {
    "add_contact": "Index Error ADD", # Cannot imagine this case
    "change_contact": "Index Error CHANGE", # Cannot imagine this case
    "delete_contact": "To delete a record please use: delete [name]",
    "show_contact": "To show a record please use: show [name]",
}

# Text for 'help' command
HELP_TEXT = "Available commands:\n" \
"'hello' - Greets you, sir \n" \
"'add' - Adds new record to your phonebook " \
"Usage: 'add [name] [phone]'\n" \
"'change' - Changes existing record or adds new record (if none) to your phonebook " \
"Usage: 'change [name] [phone]'\n" \
"'show' - Shows existing record from your phonebook " \
"Usage: 'show [name]'\n" \
"'delete' - Deletes existing record from your phonebook " \
"Usage: 'delete [name]'\n" \
"'all' - Shows your phonebook \n" \
"'close', 'exit' or 'quit' - Exits this program :(\n" \
"'help' - Shows this text \n"

# Helper function to match function name for decorator
def func_name(func_name: str, error: str) -> str:
    
    # Check error value to select correct dictionary
    match error:
            case "Value_Error":
                list = FUNC_LIST_VALUE_ERROR
            case "Key_Error":
                list = FUNC_LIST_KEY_ERROR
            case "Index_Error":
                list = FUNC_LIST_INDEX_ERROR
    
    # Match function name to a dictionary key to get correct error message
    matched = next(filter(lambda k: k == func_name, list), None)
    
    if matched:
        return list[matched]

    return "Unknown command"

# Decorator function to catch errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return dir_file_color('WARN', func_name(func.__name__, "Value_Error"))
        except KeyError:
            return dir_file_color('WARN', func_name(func.__name__, "Key_Error"))
        except IndexError:
            return dir_file_color('WARN', func_name(func.__name__, "Index_Error"))
        
    return inner

# Function to print filenames and directories in different colors
def dir_file_color(lvl: str, message: str):
    # Dictionary for different colors (c) S. Kodenko ;)
    COLORS={
        'CHANGE'    :Fore.BLUE,
        'ADD'       :Fore.GREEN,
        'DELETE'    :Fore.RED,
        'WARN'      :Fore.YELLOW
    }
    if lvl in COLORS.keys():
        return f"{COLORS[lvl]} {message} {Style.RESET_ALL}"
    else:
        return f"{Fore.WHITE} {message} {Style.RESET_ALL}"
    
# Function to parse input commands
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Decorated add contact function
@input_error
def add_contact(args, contacts) -> str:
    name, phone = args
    contacts[name] = phone
    return dir_file_color('ADD', f"Contact {name} added.")

# Decorated change contact function
@input_error
def change_contact(args, contacts) -> str:
    name, phone = args
    contacts[name] = phone
    return dir_file_color('CHANGE', f"Contact {name} changed.")

# Decorated delete contact function
@input_error
def delete_contact(args, contacts) -> str:
    if not args:
        raise IndexError("No name provided")
    name = args[0]
    del contacts[name]
    return dir_file_color('DELETE', f"Contact {name} deleted")

# Decorated show contact function
@input_error    
def show_contact(args, contacts):
    if not args:
        raise IndexError("No name provided")
    name = args[0]
    print(f"1. {Fore.WHITE} {name}: \t {Fore.MAGENTA} {contacts[name]} {Style.RESET_ALL}") 

# Print phonebook function    
def print_contacts(contacts: dict):
     print("Your existing contacts, sir:")
     i = 0
     for key, value in contacts.items():
        i += 1
        print(f"{i}. {Fore.WHITE} {key}: \t {Fore.MAGENTA} {value} {Style.RESET_ALL}")  

# Show help for 'help' command
def show_help():
    print(HELP_TEXT)

# Main program
def main():
    
    # Read saved phonebook (.json file version)
    if json_path.exists():
        with open(PHONEBOOK, "r") as json_file:
            contacts = json.load(json_file)
            print_contacts(contacts)
    else:
        contacts = {}

    # Welcome message
    print("Welcome to the assistant bot!")
    print("Please use 'help' command for more information")
    print()

    # Endless cycle to await commands
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # Command execution block
        if command in ["close", "exit", "quit"]:
            sorted_contacts = {k: contacts[k] for k in sorted(contacts)}
            with open(PHONEBOOK, "w") as json_file:
                json.dump(sorted_contacts, json_file, indent=4)
                print("Phonebook is saved. Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "delete":
            print(delete_contact(args, contacts))
        elif command == "show":
            print(show_contact(args, contacts))   
        elif command == "all":
            print_contacts(contacts)
        elif command == "help":
            show_help()    
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

