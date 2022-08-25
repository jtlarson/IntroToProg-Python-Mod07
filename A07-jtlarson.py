# ----------------------------------------------#
# Title: Exceptional Pickle Handling
# Dev: jtlarson
# Date: August 20, 2022
# Changelog: (date,name,change)
# 2022-08-20,jtlarson,initial pseudo code
# 2022-08-22,jtlarson,filled in classes
# 2022-08-24,jtlarson,fixed bugs and refined output
# ----------------------------------------------#
import pickle # used for saving list
import os # used by read_data_from_file function
import io # used by fail_to_pickle function

#---------Data-----------#
BINARY_FILE_STR = 'ToGo'
sandwich_contents_lst = [] #the 'bread' of the sandwich
topping_str = '' #something that goes in a sandwich
menu_choice = '' #current menu choice

#add data to file for testing
# yesterdays_sandwich = ["bacon", "lettuce", "tomato"]
# sandwich_file = open(BINARY_FILE_STR, 'wb')
# pickle.dump(yesterdays_sandwich, sandwich_file)
# sandwich_file.close()

#---------Processing-----------#

class Processing: #class for processing data

    @staticmethod
    def read_data_from_file(binary_file_name, list_of_toppings): #pickle.load file using try, except with custom errors
        """ Reads data from a file into a list. Uses custom exception handling
        in multiple 'exception' blocks to trigger friendly user output.

        :param file_name: (string) with name of file
        :param list_of_rows: (list) you want filled with file data
        :return: (list) of toppings (items)
        """
        list_of_toppings.clear()  # clear current data
        try:     # Using 'try, except' to provide enhanced suggestions if loading any rows from file fails
            file = open(binary_file_name, "rb") #if it's there, read it
        except FileNotFoundError as e:
            IO.output_message(message="new_customer")
            try:  # Using 'try, except' to provide enhanced suggestions if loading any rows from file fails
                file = open(binary_file_name, "ab+") #Create it and read the contents
            except Exception as e:
                print(e)
                print(type(e))
                print(e.__doc__)
                print(e.__str__())
                IO.output_message(message="file_write_error", data=os.getcwd())
                exit()
        try:
            list_of_toppings = pickle.load(file)
            file.close()
        except EOFError as e: #This error is expected if the file doesn't have a list yet--just move on.
            file.close()
        except Exception as e:
            IO.output_message(message="unpickle_error")
            file.close()
        return list_of_toppings

    #function: append ingredients to sandwich
    @staticmethod
    def add_item_to_list(topping_name, list_of_toppings):
        """ Adds data to a list of dictionary rows

        :param topping_name: (string) with name of topping
        :param list_of_toppings: (list) list where item will be appended
        :return: (list) of sandwich toppings
        """
        # Append row dictionary to list of rows (table)
        list_of_toppings.append(topping_name)
        return list_of_toppings

    #function: remove all ingredients (eating / leave hungry)
    @staticmethod
    def remove_all_items(list_of_toppings):
        """ Removes all items from list

        :param list_of_toppings: (list) list that will be erased
        :return: (list) empty list
        """
        # remove all items from hand and bag
        list_of_toppings = []
        Processing.write_data_to_file(BINARY_FILE_STR,list_of_toppings)
        return list_of_toppings

    #function: open file handle (take it to go)
    @staticmethod
    def write_data_to_file(file_name, list_of_toppings):
        """ pickle topping list for later

        :param file_name: (string) with name of file
        :param list_of_toppings: (list) to write to file
        :return: (list) the 'pickled sandwich'
        """
        # Open the file and pickle the 'sandwich' list
        file = open(file_name, "wb")
        pickle.dump(list_of_toppings,file)
        file.close()
        return list_of_toppings

    #function: pickle current list with try, except
    @staticmethod
    def fail_to_pickle(file_name, list_of_toppings):
        """ Pickle operation designed to fail due to file opened in 'rb' mode
        This intentional fault is used as a functional part of the program by
        triggering a custom exception and message

        :param file_name: (string) with name of file
        :param list_of_toppings: (list) to write to file
        :return: (list) the 'pickled sandwich'
        """
        # Open the file in rb and fail to pickle the 'sandwich' list
        try:
            file = open(file_name, "rb") #if it's there, read it
            pickle.dump(list_of_toppings, file)
        except io.UnsupportedOperation as e:
            IO.output_message(message="dash")
            file.close()
        # remove all items from hand and bag
        list_of_toppings = []
        Processing.write_data_to_file(file_name=file_name,list_of_toppings=list_of_toppings)
        return list_of_toppings

#---------User IO-----------#

class IO: #create IO class

    @staticmethod
    def output_message(message, data = ''): #function to display comments: greeting, eating, take it to go, dash
        """  Messages for user
        :param message: (string) keyword of message to display
        :param data: (string) Optional additional data to display
        :return: Nothing
        """
        message_dict = {'welcome': "Welcome to Bracket's Sandwich Shop!",
                        'new_customer': "New Customer! (expected file not found)",
                        'sandwich_loaded': "It looks like you have a sandwich:",
                        'fresh_sandwich': "You look like you could use a fresh sandwich! (no list in file)",
                        'file_write_error': "Unknown error accessing/creating save file--verify write access to:",
                        'unpickle_error': "It looks like your sandwich got mangled! (can't unpickle file)",
                        'eating': "You eat every list bite of that sandwich.",
                        'togo': "Sure - I'll just put it in the ToGo bag (file) for you.",
                        'dash': "In your haste to leave without paying, you spill your sandwich all over the floor!",
                        'unknown': "I didn't understand that. Try again"
                        }
        print(message_dict[message], data)
        #print()

    @staticmethod
    def output_menu_tasks(): #function to display main menu
        """  Display a menu of choices to the user

        :return: nothing
        """
        print('''
        Menu of Options
        1) Add to sandwich
        2) Eat the sandwich
        3) Take your sandwich to go
        4) Dine and dash
        ''')
        #print()  # Add an extra line for looks

    @staticmethod
    def show_current_sandwich(toppings_list):
        """ Shows the current 'toppings' (items) in the sandwich (list)

        :param toppings_list: (list) sandwich items
        :return: nothing
        """
        if toppings_list: #if there are any toppings
            max_topping_chars_int = 0  # the length of the task name
            # Find the longest task name
            for item in toppings_list:
                if len(item) > max_topping_chars_int:
                    max_topping_chars_int = len(item)
            # Display sandwich contents between bread (===) sized to fit
            print(" " * 7, "=" * (max_topping_chars_int))
            for item in toppings_list:
                print(" " * 7, item)
            print(" " * 7, "=" * (max_topping_chars_int), end="") #position output above Menu
            print()

    @staticmethod
    def input_menu_choice(): #function: ask user for selection and return
        """ Gets the menu choice from a user

        :return: string
        """
        choice = str(input("Which option would you like to perform? [1 to 4] - ")).strip()
        #print()  # Add an extra line for looks
        return choice
    #function: ask user for ingredient (string) to add (try, except?)
    @staticmethod
    def input_topping():
        """ Ask the user for a topping

        :return: string
        """
        while True:
            choice = str(input("Type in a topping for your sandwich: ")).strip()
            #print()  # Add an extra line for looks
            if all(x.isalpha() or x.isspace() for x in choice):
                break
            else:
                print("I don't have that topping. What else can I add?")
        return choice

#------Main Code flow-------#

IO.output_message("welcome") #print welcome

sandwich_contents_lst = Processing.read_data_from_file(BINARY_FILE_STR, sandwich_contents_lst) #Open file and present contents if found

#While loop to display menu, add sandwich contents (append), eat the sandwich (erase), take it to go (try: pickle current list),
# or 'dine and dash' (except: pickle fails because file handle isn't open)
while True:
    if sandwich_contents_lst:
        IO.output_message(message="sandwich_loaded")
        IO.show_current_sandwich(toppings_list=sandwich_contents_lst)  # Show current data in the list/table
    else:
        IO.output_message(message="fresh_sandwich")
    IO.output_menu_tasks()
    menu_choice = IO.input_menu_choice()

    # Process user's menu choice
    if menu_choice == '1':  # add sandwich contents (append)
        topping_str = IO.input_topping()
        sandwich_contents_lst = Processing.add_item_to_list(topping_name=topping_str,list_of_toppings=sandwich_contents_lst)
        continue  # to show the menu

    elif menu_choice == '2':  # eat the sandwich (erase)
        IO.output_message('eating')
        sandwich_contents_lst = Processing.remove_all_items(list_of_toppings=sandwich_contents_lst)
        continue  # to show the menu

    elif menu_choice == '3':  # take it to go (try: pickle current list)
        if len(sandwich_contents_lst) == 0:
            continue
        else:
            IO.output_message('togo')
            sandwich_contents_lst = Processing.write_data_to_file(file_name=BINARY_FILE_STR,list_of_toppings=sandwich_contents_lst)
            break  # exit the program

    elif menu_choice == '4':  # 'dine and dash' - rb file mode will cause exception that triggers user message
        if len(sandwich_contents_lst) == 0:
            continue
        else:
            sandwich_contents_lst = Processing.fail_to_pickle(file_name=BINARY_FILE_STR,list_of_toppings=sandwich_contents_lst)
            break  # exit the program

    else:
        IO.output_message(message="unknown")
        continue
#exit