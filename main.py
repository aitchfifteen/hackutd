import csv

# Prompt the user to input the CSV file name
csv_file_name = input("Enter the name of your CSV file (e.g., 'example.csv'): ")

# Try to open the file in the current directory
try:
    with open(csv_file_name, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        raw_text = ""

        # Skip the header row
        headers = next(csvreader)

        # Process each row in the CSV file
        for row in csvreader:
            for col in row:
                if col.isdigit():  # If the value is an integer
                    raw_text += col + " "
                elif col.replace('.', '', 1).isdigit():  # If the value is a float
                    raw_text += col + " "
                else:  # If the value is a string or empty
                    raw_text += col + " "
            raw_text += "\n"

    # Output the processed text
    print(raw_text)

except FileNotFoundError:
    print(f"Error: '{csv_file_name}' was not found in the current folder. Please check the file name and try again.")
except Exception as e:
    print(f"An error occurred: {e}")

