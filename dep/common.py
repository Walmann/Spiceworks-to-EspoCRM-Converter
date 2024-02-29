import json
import os


def checkForDev():
    if os.path.isfile("./DEVFILE"):
        return True
    else:
        return False

def questionYN(q):
    answer = input(q)
    try:
        answer = answer.lower()[0]
    except IndexError:
        answer = 0
    if answer == "y":
        return True
    elif answer == "n":
        return False
    else:
        print("Error in answer. Try again.")
        questionYN(q=q)


def formatStringForSQL(String):
    return String.replace("'", "")


def getUserSettings():
    if os.path.isfile("./userSettingsMine.txt"):
        settings = "./userSettingsMine.txt"
    else:
        settings = "./userSettings.txt"
    with open(settings, "r") as file:
        settings = json.loads(file.read())
        return settings
    raise FileNotFoundError("Settingsfile not found!")

def formatLastSQLQuery(SQLQuery):
    # Change the last query, replace "," with ";". SQL Syntax reasons
    lastQuery = SQLQuery[-1][:-1]+";" 
    SQLQuery.pop()
    SQLQuery.append(lastQuery)
    return SQLQuery

def createSQLOutputFile(input_list, entries_per_file=7500):
    filename_prefix = ""
    if input_list[0].startswith("INSERT INTO `user` "):
        filename_prefix = "users"
    elif input_list[0].startswith("INSERT INTO `case` "):
        filename_prefix = "case"
    elif input_list[0].startswith("INSERT INTO `note` "):
        filename_prefix = "note"

    total_entries = len(input_list)

    # Calculate the number of files needed
    total_files = -(-total_entries // entries_per_file)

    for file_number in range(total_files):
        first_line = True  # To prevent duplicate SQL header, but create header in all files

        start_index = file_number * entries_per_file
        end_index = min((file_number + 1) * entries_per_file, total_entries)

        file_name = f"./Outputfiles/{filename_prefix}_{file_number + 1}.txt"

        with open(file_name, "w+", encoding="UTF-8") as file:
            SQLheader = input_list[0]
            file.write(SQLheader + "\n")
            for i, entry in enumerate(input_list[start_index:end_index]):
                if first_line:
                    first_line = False
                    continue
                if i == end_index - start_index - 1:  # Check if it's the last line
                    if entry.endswith(","):
                        entry = entry[:-1] + ";"
                    else:
                        if entry.endswith(";"):
                            pass
                        else:
                            print(
                                f'Error: Last character of the last line in {file_name} is not ",".'
                            )

                file.write(entry + "\n")

        print(f"File {file_name} created with {end_index - start_index} entries.")

    # Example usage:
    # create_output_file([["INSERT INTO `user` (id, name, email),", "VALUES (1, 'John', 'john@example.com');"]], 1)
