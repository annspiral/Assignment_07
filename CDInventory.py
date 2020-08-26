#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AAllen, 2020-Aug-15, Added function get_new_entry() in IO
# AAllen, 2020-Aug-15, Added functions add_CD(), delete_CD() in DataProcessor
# AAllen, 2020-Aug-15, Added function write_file() in FileProcessor
# AAllen, 2020-Aug-15, updated function comments, added get_sorted_values_list()
# AAllen, 2020-Aug-15, added error checking in get_new_entry() for ID
# AAllen, 2020-Aug-17, cleaned up some docstrings
# AAllen, 2020-Aug-18, moved call to DataProcessor.get_sorted_values_list()
#                       out of IO.get_new_entry()
# AAllen, 2020-Aug-20, removed pass calls
# AAllen, 2020-Aug-22, replaced code to in get_new_entry() to find the next
#                       available ID
# AAllen, 2020-Aug-22, updated FileProcessor.read_file() and write_file()
#                       to use a pickled binary data format
# AAllen, 2020-Aug-22, added structured error handling for IO.get_new_entry()
# AAllen, 2020-Aug-22, create IO.get_ID() to get valid ID to delete
# AAllen, 2020-Aug-23, added try-except blocks throughout code
# AAllen, 2020-Aug-26, removed try-except around simple input lines
# AAllen, 2020-Aug-26, added general Exception case catches to try-except blocks
#------------------------------------------#

# -- DATA -- #
import pickle

strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def add_CD(tplEntry, table):
        """Function to add a CD dictionary entry to the table/inventory
        
        Takes a tuple of entry strings (ID, Title, Artist) and creates a 
        dictionary collection {'ID':num, 'Title':string, 'Artist':string}
        that is added to the full inventory table, which is a list of dictionaries
        
        Args:
            tplEntry: a tuple of strings containing values to be added into
            dictionary collection and table - expected order of ID, Title, Artist.
            table (list of dict): 2D data structure (list of dicts) that holds
            the data during runtime
        
        Returns:
            Boolean: True if row could be added, False if it could not.
        
        """
        # convert tuple values into dictionary item
        
        try:
            dicRow = {'ID': int(tplEntry[0]),
                      'Title': tplEntry[1],
                      'Artist': tplEntry[2]}
            table.append(dicRow)
            return True
        except ValueError:
            print('\n! Unable to add new CD to table. ID is not an integer.\n')
            return False
        except IndexError:
            print('\nUnable to add new CD to table. Did not have the correct' +
                  ' number of data fields for new CD entry.\n')
            return False
        except AttributeError:
            print('\n! Unable to add new CD to table. Could not append to table.\n')
        except Exception as e:
            print('Unable to add new CD to table.', e,'\n')
            return False


    @staticmethod
    def delete_CD(intDelID, table):
        """Function to delete a CD dictionary entry from the table/inventory
        
        Deletes the row identified by the ID value from the inventory table.
        The row is a dictionary entry that represents each CD.
        
        Args:
            intDelID: ID value for the dictionary collection in the list that
            will be deleted
            table (list of dict): 2D data structure (list of dicts) that holds
            the CD inventory data during runtime
        
        Returns:
            Boolean: True if row was deleted. False if not.
        
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            try:
                # if value of 'ID' for this row matches ID to delete, delete
                # row and set flag to true that row is deleted
                if row['ID'] == intDelID:
                    del table[intRowNr]
                    blnCDRemoved = True
                    break
            except KeyError:
                print('Inventory table does not have expected key value.\n')
            except IndexError:
                print('Error deleting expected row from inventory. Index out of range.\n')
            except Exception as e:
                print('Error deleting row from inventory.', e, '\n')

        if blnCDRemoved:
            print('The CD was removed\n')
            return True
        else:
            print('! Unable to delete CD. Could not find CD with ID = ',
                  intDelID, '.\n')
            return False
            
      
        
    @staticmethod
    def get_sorted_values_list(table, key='ID'):
        """Function to get all values of the specified key from a list of
        dictionaries
        
        Creates a sorted list of all the values for the key provided that are
        currently in the inventory table (2D list of dictionaries)
        
        Args:
            table: expects a 2D table that is a list of dictionaries
            key: key for which values are retrieved from the dictionaries,
            defaults to look for a key name 'ID'
        
        Returns:
            List: sorted list of all values with the provided key that are
            in the 2D table. List is set to None if unable to get list.
            False: if unable to retrieve list of IDs
        
        """
        # start with an empty list of IDs
        lstIDsUsed = []
        
        # if the inventory table is empty, return an empty list of IDs as
        # valid return value
        try:
            if len(table) == 0:
                return lstIDsUsed
        except TypeError:
            print("Error getting length of Inventory table. Table set to none.\n")
            return False
        
        # if the inventory table is not empty get current IDs
        try:
            #get a list of all values for the key parameter
            for row in table:
                lstIDsUsed.append(row.get(key))
            lstIDsUsed.sort()
        except TypeError:
            # if lstIDsUsed is still empty after getting IDs, .sort() will
            # cause a TypeError. Catch this error and return False so 
            # duplicate IDs are not created
            print('TypeError getting list of IDs from table.\n')
            lstIDsUsed = False
            return lstIDsUsed
        except Exception as e:
                print('Error getting list of IDs from table.', e, '\n')
                lstIDsUsed = False
        else:
            return lstIDsUsed
        


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one 
        dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds
            the data during runtime

        Returns:
            Boolean: True if file loaded. False if not loaded.
        """
        # clear table to load with file contents
        table.clear()
        try:
            # open file to read binary
            objFile = open(file_name, 'rb')
        except FileNotFoundError as e:
            print('! FileNotFoundError reading file: ', e ,'\n')
            return False
        except PermissionError as e:
            print('! PermissionError reading file: ', e ,'\n')
            return False 
        except Exception as e:
            print('! Error reading file: ', e ,'\n')
            return False 
        else:
            try:
                # copy contents of file into table
                table[:] = pickle.load(objFile)[:]
            except AttributeError as e:
                print('! Error unpickling data file: ', file_name,', ', e ,'\n',
                      'Recommended to check data file for corruption.')
                return False
            except pickle.UnpicklingError as e:
                print('! Error unpickling data file: ', file_name,', ', e ,'\n',
                      'Recommended to check data file for corruption.')
                return False
            except EOFError as e:
                print('! Error unpickling data file: ', file_name,', ', e ,'\n',
                      'Recommended to check data file for corruption.')
                return False
            except Exception as e:
                print('! Error unpickling data file: ', file_name,', ', e ,'\n',
                      'Recommended to check data file for corruption.')
                return False
            objFile.close()
            return True
        


    @staticmethod
    def write_file(file_name, table):
        """Function to write updated inventory list of dictionaries to file

        Writes the data in table to the file identified by file_name. Table is
        a list of dictionaries. Each dictionary item is written to a line in 
        the file, with a newline ending. The dictionary is written as the 
        value from each key/value pair separated by a comma

        Args:
            file_name (string): name of file used to save to
            table (list of dict): 2D data structure (list of dicts) that holds 
            the data during runtime

        Returns:
            Boolean: True if file could be updated. False if file could not
            be updated.
        """

        try:
            # open file to write binary
            objFile = open(file_name, 'wb')
        except PermissionError as e:
            print('! PermissionError reading file: ', e ,'\n')
            return False 
        except Exception as e:
            print('! Error reading file: ', e ,'\n')
            return False 
        else:
            try: 
                # add table data to file
                pickle.dump(table, objFile)
            except AttributeError as e:
                print('! Error pickling data file: ', e, '\n')
                return False
            except pickle.PicklingError as e:
                print('! Error pickling data file: ', e ,'\n')
                return False
            except Exception as e:
                print('! Error pickling data file: ', e ,'\n')
                return False
            objFile.close()
            return True


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nCD Inventory Menu\n\n[l] load Inventory from file\n[a] add CD\n[i] display Current Inventory')
        print('[d] delete CD from Inventory\n[s] save Inventory to file\n[x] exit\n')


    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        
        choice = ' '
        try:
            # request user menu choice and check for valid option
            while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        except:
            print('Error getting new menu option.\n')
        
        print()  # Add extra space for layout
        return choice


    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that
            holds the data during runtime.

        Returns:
            None.

        """
        try:
            print('======= The Current Inventory: =======')
            print('ID\tCD Title (by: Artist)\n')
            for row in table:
                print('{}\t{} (by:{})'.format(*row.values()))
            print('======================================')
        except:
            print("Error displaying Inventory menu.\n")


    @staticmethod
    def get_new_entry(lstTestIDs):
        """Requests the new entry values, ID, Title, Artist
            
         Args:
            lstTestIDs: a list containing IDs currently in use in the table

        Returns:
            tplNewEntry: a tuple of three strings with the user's input for the
            (ID, Title, Artist) for a new CD entry
    
        """
        # Get a unique entry ID
        entryID = '' # create empty default ID
        validID = False # Flag to indicate valid ID identified
        # request an ID number from user
        entryID = input('Enter ID number: ').strip()
        
        # verify ID number and re-ask as needed
        while not validID:
            try:
                int(entryID)
            except ValueError:
                # if the user does not enter an ID, find one and assign it
                # if the list of current IDs is empty, start with ID 0
                if entryID == '' and ((lstTestIDs == []) or (lstTestIDs == None)):
                    entryID = 0
                    break
                # assign a CD ID, by finding the next available, unique ID to use
                # code curtesy of Doug Klos
                elif entryID == '':
                    entryID = 0
                    while True:
                         if entryID in lstTestIDs:
                            entryID += 1
                         else:
                             break
                # if they ID was not a valid int and not blank, ask again     
                else:
                    entryID = input('Please enter a numerical, non-decimal ID number: ').strip()
            # if an ID was passed in that was not a string or hits another error, try again
            except:
                entryID = input('Unable to assign ID.\n' +
                                'Please choose a different ID or press [enter] to' +
                                ' assign one automatically: ').strip()
            else:
                # if entry is a valid int and not a duplicate, use the ID
                if  int(entryID) in lstTestIDs:
                    entryID = input('ID =' + entryID + ' is already being used.\n' +
                                     'Please choose a different ID or [enter] to' +
                                     ' assign one automatically: ').strip()
                elif int(entryID) < 0:
                    entryID = input('Please choose a positive value ID or [enter] to' +
                                     ' assign one automatically: ').strip()
                else:
                    validID = True
                            
        # get the entry title and artist, these can be blank                 

        entryTitle = input('What is the CD\'s title? ').strip()
        entryArtist = input('What is the Artist\'s name? ').strip()
        
        # create new entry tuple with ID, Title and Artist
        tplNewEntry = (entryID, entryTitle, entryArtist)
        return tplNewEntry
    
    
    @staticmethod
    def get_ID():
        """Requests a positive, integer ID value from the user to delete
            
         Args:
            none

        Returns:
            Integer: integer value greater than 0 for ID to delete
    
        """  
        while True:
            try:
                # request ID from user
                intIDDel = int(input('Which ID would you like to delete? ').strip())
            except ValueError:
                # catch alpha/symbol error entries that do not convert to int
                print('\nPlease enter an integer ID value greater than zero.')
            else:
                # Check to see if the integer is a positive value
                if intIDDel >= 0:
                    break
                else:
                    print('\nPlease enter an integer ID greater than 0.')
        return intIDDel


# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')       
        strYesNo = input('Type \'yes\' to continue and reload from file. Otherwise reload will be canceled: ')
        try:
            if strYesNo.lower() == 'yes':
                print('reloading...')
                FileProcessor.read_file(strFileName, lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
        except:
            print('Error loading data from file.\n')
        else:
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.0 get the sorted list of IDs currently in use
        lstTestIDs = DataProcessor.get_sorted_values_list(lstTbl)
        # 3.3.1 Check to see if there is a valid list of IDs to check against
        if lstTestIDs == False:
            print('Unable to add a new entry without a confirming current IDs in use.\n')
        # 3.3.2 Ask user for new ID, CD Title and Artist
        else:
            #3.3.2.1 Get values for the new entry
            tplUserEntry = IO.get_new_entry(lstTestIDs)
            # 3.3.2.2 Add item with users values to the table
            DataProcessor.add_CD(tplUserEntry, lstTbl)
        # 3.3.3 Display inventory to user to confirm CD added
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = IO.get_ID()
        # 3.5.2 search thru table and delete CD
        # 3.5.2.1 delete CD with requested ID
        DataProcessor.delete_CD(intIDDel, lstTbl)
        # 3.5.2.2 display inventory to user after delete for confirmation
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
            print('Error confirming save cancelation with user.\n')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




