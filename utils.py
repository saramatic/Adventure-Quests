# utils.py

def format_location(location):
    """Format a location tuple as a string."""
    return f"({location[0]}, {location[1]})"

def validate_input(prompt, options):
    """Prompt the user until a valid input is provided."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print(f"Invalid choice. Options are: {', '.join(options)}")

def calculate_distance(loc1, loc2):
    """Calculate the Manhattan distance between two locations."""
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
