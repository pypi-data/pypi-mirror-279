import ctypes  # to call id
import os
import shlex  # pour faire des split qui respectent les ""
import sys
import json
from os.path import expanduser
import shutil


if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.utils import shared_variables,windows_utils
else:
    from orangecontrib.AAIT.utils import shared_variables


def force_save(self_instance):
    """
    This function forces the save of the currently opened Orange document.
    It utilizes the ctypes library to invoke the save_scheme function of the document.
    It checks if the save is successful and displays an error message if it fails.
    """

    # Initialize the canvas ID to a default value
    canvas_id = -666

    # Iterate through the shared variables to find the document's canvas ID
    for shared_variable in shared_variables.vect_doc_ptr:
        if self_instance.current_ows == shared_variable[0]:
            canvas_id = shared_variable[1]

    # Check if the canvas ID is still the default value, indicating failure to find the document
    if canvas_id == -666:
        print("Unable to save. Document not found.")
        return

    # Use ctypes to invoke the save_scheme function of the document
    save_result = ctypes.cast(canvas_id, ctypes.py_object).value.save_scheme()

    # Check the result of the save operation
    if save_result != 1:
        self_instance.error("Error: You need to save your document.")
        return

    # Clear any previous error messages
    self_instance.error("")


def force_save_as(self_instance, target_canvas_id=None):
    """
    This function forces the save of the currently opened Orange document with a new name. It loops until the save is successful.
    """
    save_result = 0

    # Loop until the save operation is successful
    while save_result != 1:
        self_instance.error("You need to save your document to use AAIT widgets")
        print("You need to save your document to use AAIT widgets")

        # Use ctypes to invoke the save_scheme function of the document
        save_result = ctypes.cast(target_canvas_id, ctypes.py_object).value.save_scheme()

    # Clear any previous error messages
    self_instance.error("")


def replaceAll(file_path, search_exp, replace_exp):
    """
    This function searches and replaces all occurrences of search_exp with replace_exp in a specified file.
    """
    try:
        modified_lines = []  # Create an empty list to store modified lines
        with open(file_path, "r") as file:
            lines = file.readlines()  # Read all lines from the file

        for line in lines:
            if search_exp in line:  # Check if the search expression is present in the line
                line = line.replace(search_exp,
                                    replace_exp)  # Replace the search expression with the replacement expression
            modified_lines.append(line)  # Append the modified line to the list

        print(modified_lines)  # Print the modified lines to the console

        with open(file_path, 'w') as file:
            file.writelines(modified_lines)  # Write the modified lines back to the file

    except Exception as e:
        print(e, file=sys.stderr)  # Print the exception details to standard error
        print("Error in modifying file:", file_path, file=sys.stderr)  # Print an error message to standard error
        return ""  # Return an empty string if there is an error


def current_met_directory(argself):
    """
    This function returns the current save directory for the current Orange document.
    It ensures that the document has been saved and that a save directory exists.
    """
    # Check if the current document is not saved or has an empty name
    if argself.current_ows == "toto" or argself.current_ows == "":
        print("Error: OWS file needs to be saved before using AAIT modules!", file=sys.stderr)

        # Force save the document with a new name
        force_save_as(argself)

        # Update the current document variable
        argself.current_ows = shared_variables.get_current_ows()

        # Recursive call to ensure a valid met directory is obtained
        return current_met_directory(argself)

    # Build the met directory path based on the current document path
    met_dir = argself.current_ows[:-3] + "metdir"

    # Check if the directory already exists
    if os.path.isdir(met_dir):
        return met_dir

    # Try creating the directory
    try:
        os.mkdir(met_dir)
    except Exception as e:
        print(e, file=sys.stderr)
        print("Error in creating directory:", met_dir, file=sys.stderr)
        return ""

    return met_dir


def write_met_file(self_arg, extra_arg_title=[], extra_arg_value=[]):
    """
    This function writes a file in "met" format (configuration) with specified titles and values.
    It checks for consistency between the lists of titles and values.
    """
    # Check for inconsistency in the length of title and value lists
    if len(extra_arg_title) != len(extra_arg_value):
        print("Error: Mismatch in length of arguments [title][value]", file=sys.stderr)
        return 1  # Return 1 to indicate an error

    # Get the current met directory
    met_dir = current_met_directory(self_arg)

    # Check if the met directory is not available
    if met_dir == "":
        # Show a save file window and call the function again
        print("Here, display a save file window and recall the function")
        return 1  # Return 1 to indicate an error

    # Construct the file name using the met directory and the caption title of self_arg
    file_name = met_dir + "/" + self_arg.captionTitle + ".met"

    try:
        with open(file_name, 'w') as file:
            # Write caption, name, and id to the file
            file.write("Caption ")
            file.write('"' + str(self_arg.captionTitle) + '"\n')
            file.write("Name ")
            file.write('"' + str(self_arg.name) + '"\n')
            file.write("Id ")
            file.write('"' + str(id(self_arg)) + '"')

            # Write additional titles and values to the file
            for i in range(len(extra_arg_title)):
                file.write("\n")
                file.write('"' + str(extra_arg_title[i]) + '" "')
                file.write(str(extra_arg_value[i]) + '"')

    except Exception as e:
        print(e, file=sys.stderr)
        print("Error in writing file:", file_name, file=sys.stderr)
        return 1  # Return 1 to indicate an error

    return 0  # Return 0 to indicate success


# 0 ok 1 erreur
def read_met_file_from_caption(self_instance, caption, out_title_list, out_value_list):
    """
    This function reads a "met" file based on a specified caption, extracts titles and values,
    and then stores them in the lists out_title_list and out_value_list.
    """
    # Get the current met directory
    met_directory = current_met_directory(self_instance)

    # Check if the met directory is not valid
    if met_directory == "":
        force_save_as(self_instance)
        # print("End of the attempt")

        # Update the current document variable
        self_instance.current_ows = shared_variables.get_current_ows()

        # Recursive call to ensure a valid met directory is obtained
        return read_met_file_from_caption(self_instance, caption, out_title_list, out_value_list)

    # Build the absolute path to the met file based on the caption
    absolute_path = met_directory + "/" + caption + ".met"

    # Call the function to read the met file from the absolute path
    return read_met_file_from_absolute_path(absolute_path, out_title_list, out_value_list)


def read_met_file_from_absolute_path(file_path, title_list, value_list):
    """
    This function reads a "met" file from its absolute path (file_path), extracts titles and values,
    and then stores them in the lists title_list and value_list.
    """
    lines_to_process = []
    del title_list[:]
    del value_list[:]

    try:
        with open(file_path, 'r') as file:
            lines_to_process = file.readlines()
    except Exception as e:
        print("Error in reading:", file_path, file=sys.stderr)
        print(e)
        return 1

    for i in range(0, len(lines_to_process)):
        cleaned_line = lines_to_process[i].strip()
        split_line = shlex.split(cleaned_line)

        if len(split_line) != 2:
            print("Line not expected:", lines_to_process[i], file=sys.stderr)
            return 1

        title_list.append(split_line[0])

        if len(split_line[1]) > 2:
            if (split_line[1][0] == '"' and split_line[1][-1] == '"'):
                split_line[1] = split_line[1][1:]
                split_line[1] = split_line[1][:-1]

        value_list.append(split_line[1])

    if len(title_list) != len(value_list):
        print("Error: Met file truncated size")
        return 1

    if len(title_list) < 3:
        print("Error: Met file truncated, less than 3 elements")
        return 1

    if title_list[0] != "Caption":
        print("Error: Caption not found in Met file at index 0")
        return 1

    if title_list[1] != "Name":
        print("Error: Name not found in Met file at index 1")
        return 1

    if title_list[2] != "Id":
        print("Error: Id not found in Met file at index 2")
        return 1

    return 0


def get_all_captions(self_instance, include_dict_variable=False):
    """
    This function returns the list of all caption names for "met" files in the current save directory.
    It allows including or excluding "dict_variable" files based on the include_dict_variable parameter.
    """
    # Get the current metm directory
    met_directory = current_met_directory(self_instance)

    # Check if the met directory is not valid
    if met_directory == "":
        print("Put a save file window here and call the function again")
        return 1

    # List to store file captions
    captions_list = []

    # Iterate through the directory
    for file_name in os.listdir(met_directory):
        # Check if the file is a "met" file
        if file_name.endswith('.met'):
            # Check if excluding "dict_variable" files and skip if necessary
            if not include_dict_variable and file_name[:-4] == "dict_variable":
                continue

            # Append the caption name to the list
            captions_list.append(file_name[:-4])

    return captions_list


def get_all_captions_with_specific_class(self_instance, class_name):
    """
    This function returns a list of caption names for "met" files that have a specified class (class_name).
    """
    # Get the list of all captions
    captions_to_study = get_all_captions(self_instance)

    # Check for an error in getting the list of captions
    if type(captions_to_study) is int:
        return []

    result_list = []

    # Check if the list of captions is empty
    if len(captions_to_study) == 0:
        return result_list

    # Iterate through the list of captions
    for caption_element in captions_to_study:
        title_list = []
        value_list = []

        # Read the "met" file and check for errors
        if 0 != read_met_file_from_caption(self_instance, caption_element, title_list, value_list):
            print("Error reading ", caption_element, file=sys.stderr)
            return []

        # Check if the class of the file matches the specified class_name
        if value_list[1] == class_name:
            result_list.append(caption_element)

    return result_list


def get_all_captions_from_specific_ows(ows_path, include_dict_variable=False):
    """
    This function returns the list of all caption names for "met" files in the save directory associated with a specified OWS document.
    """
    # Build the met directory path based on the OWS document path
    met_directory = ows_path[:-3] + "metdir"

    # List to store file captions
    captions_list = []

    # Iterate through the directory
    for file_name in os.listdir(met_directory):
        # Check if the file is a "met" file
        if file_name.endswith('.met'):
            # Check if excluding "dict_variable" files and skip if necessary
            if not include_dict_variable and file_name[:-4] == "dict_variable":
                continue

            # Append the caption name to the list
            captions_list.append(file_name[:-4])

    return captions_list


def get_all_captions_with_specific_class_from_specific_ows(class_name, ows_path):
    """
    This function returns a list of caption names for "met" files that have a specified class (class_name) in the save directory associated with a specified OWS document.
    """
    # Get the list of all captions for the specific OWS document
    captions_to_study = get_all_captions_from_specific_ows(ows_path)

    # Check for an error in getting the list of captions
    if type(captions_to_study) is int:
        return []

    result_list = []

    # Check if the list of captions is empty
    if len(captions_to_study) == 0:
        return result_list

    # Build the met directory path based on the OWS document path
    met_directory = ows_path[:-3] + "metdir"

    # Iterate through the list of captions
    for caption_element in captions_to_study:
        title_list = []
        value_list = []

        # Build the absolute path to the "met" file
        absolute_path = met_directory + "/" + caption_element + ".met"

        # Read the "met" file and check for errors
        if 0 != read_met_file_from_absolute_path(absolute_path, title_list, value_list):
            print("Error reading ", absolute_path, file=sys.stderr)
            return []

        # Check if the class of the file matches the specified class_name
        if value_list[1] == class_name:
            result_list.append(caption_element)

    return result_list


def is_caption_file_exist(self_arg, caption):
    """
    This function checks if a "met" file with a specific caption exists in the current save directory.
    """
    met_dir = current_met_directory(self_arg)

    # Check if the met_dir directory is not available
    if met_dir == "":
        # print("Here, display a save file window and recall the function")
        return 1  # Return 1 to indicate an error

    # Construct the absolute path using the met directory and the caption
    absolute_path = met_dir + "/" + caption + ".met"

    # Check if the file exists at the constructed absolute path
    return os.path.isfile(absolute_path)


def write_local_current_version():
    """"
    This function write local current version
    """
    version="0.0.0.0"# to be changed at each new version
    store_ia_path = expanduser("~")
    store_ia_path=store_ia_path.replace("\\","/")
    store_ia_path+="/ia_store/Parameters"
    version_file=store_ia_path+"/Store_IA.txt"
    try:
        os.makedirs(store_ia_path, exist_ok=True)
        with open(version_file, 'w') as f:
            f.write(version)
            pass
    except:
        raise Exception("error impossible to write file :", version_file)



def get_local_store_path():
    """
    This function return the IA Store path stocked locally on user computer
    create folder if not exist
    """
    store_ia_path = expanduser("~")
    store_ia_path = store_ia_path.replace("\\", "/")
    store_ia_path += "/ia_store/"

    if not os.path.exists(store_ia_path):
        # Create a new directory because it does not exist
        os.makedirs(store_ia_path,exist_ok=True)
        # create blanck file with future remote path
        try:
            with open(store_ia_path + '/remote_ressources_path.txt', 'w') as fp:
                pass
        except:
            raise Exception("error impossible to write file :", store_ia_path)
    return store_ia_path


def set_ia_store_remote_ressources_path(ressource_path):
    """
    Set up remote ressources path of store IA
    """
    if len(ressource_path) == 0:
        return
    ressource_path.replace("\\", "/")
    if ressource_path[-1] != "/":
        ressource_path += "/"
    # check if proposed directory is valid
    try:
        version = get_ia_store_remote_version(ressource_path)
        print("current remote version", version)
    except:
        raise Exception(ressource_path, "is not a valid remote ressource path")
    store_ia_path = get_local_store_path()
    # writinf local file with directory path
    try:
        with open(store_ia_path + '/remote_ressources_path.txt', 'w') as fp:
            fp.write(ressource_path)
            pass
    except:
        raise Exception("error impossible to write file :", store_ia_path + '/remote_ressources_path.txt')


def get_ia_store_remote_version(ressource_path):
    """
    Return current remote version of store IA
    """
    version_file = ressource_path + "Parameters/Store_IA.txt"
    version = ""
    try:
        with open(version_file, 'r') as f:
            line = f.readline()
            version = line.split(" ")[-1]
            pass
    except:
        raise Exception("error impossible to read file :", version_file)
    return version


def get_ia_store_remote_ressources_path():
    """
    Get remote ressources path of store IA
    """
    try:
        local_ia_store_path = get_local_store_path()
    except Exception:
        raise Exception("Impossible to open local ia store path")

    path_to_read = local_ia_store_path + "remote_ressources_path.txt"
    output_path = ""
    try:
        with open(path_to_read, 'r') as f:
            output_path = f.readline()
            pass
    except:
        raise Exception("error impossible to read file :", path_to_read)
    return output_path


def get_ia_store_requirements_json():
    """
    Return the dictionnary of requierment
    """
    try:
        ia_store_remote = get_ia_store_remote_ressources_path()
    except:
        raise Exception("no acces to ia store ressource path")
    json_path = ia_store_remote + "Parameters/requirements.json"
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data
    except:
        raise Exception("unable to read", json_path)


def download_ia_store_file_or_directory(file_or_directory):
    if file_or_directory == "":
        return

    print("file_or_directory ->",file_or_directory)
    input=get_ia_store_remote_ressources_path()+file_or_directory

    output=get_local_store_path()+file_or_directory

    if already_downloaded(input,output):
        print(output, "already downloaded -> skip")
        return

    os.makedirs(os.path.dirname(output),exist_ok=True)
    if os.name=='nt':
        windows_utils.win32_shellcopy(input,output)
    else:
        try:
            shutil.copyfile(input, output)
        except:
            raise Exception("erreur then copy",input)

def get_size(path):
    """
    Returns the size of the specified file or directory in bytes.

    :param path: Path to the file or directory.
    :return: Size in bytes.
    """
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        return get_dir_size(path)
    else:
        raise Exception("The specified path is neither a file nor a directory")

def get_dir_size(directory):
    """
    Returns the total size of all files in a directory in bytes.

    :param directory: Path to the directory.
    :return: Size in bytes.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Ignore symbolic links
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def delete_path(path):
    """
    Deletes the specified file or directory.

    :param path: Path to the file or directory to be deleted.
    """
    try:
        if os.path.isfile(path):
            os.remove(path)  # Remove the file
            print(f"File '{path}' has been deleted.")
        elif os.path.isdir(path):
            shutil.rmtree(path)  # Remove the directory and all its contents
            print(f"Directory '{path}' and all its contents have been deleted.")
        else:
            print(f"The path '{path}' does not exist.")
    except Exception as e:
        raise("An error occurred while deleting "+path+"\""+e)

def already_downloaded(input,output):
    """
    Check if a file need to be downloaded or downloaded again
    based on file size
    remove file if necessary
    """
    # file or directory doesn't exist -> we need to download it

    if not os.path.exists(output):
        return False
    if get_size(input)==get_size(output):
        return True
    # remove output
    print("remove")
    delete_path(output)
    return False


def GetFromRemote(name_to_download):
    """
    Get files form store ia
    """
    write_local_current_version()
    if get_ia_store_remote_version(get_ia_store_remote_ressources_path())!=get_ia_store_remote_version(get_local_store_path()):
        raise Exception("you need to update your ia store add on!")
    try:
        requirements = get_ia_store_requirements_json()
    except:
        raise Exception("unable to read  ia store containt")
    for element in requirements:
        if element['name'] != name_to_download:
            continue
        for element2 in element['workflows']:
            download_ia_store_file_or_directory(element2)
        for element2 in element['extra_datas']:
            download_ia_store_file_or_directory(element2)






if __name__ == "__main__":
    # avant faire un bouton
    # set_ia_store_remote_ressources_path(ressource_path)

    ia_store_remote = get_ia_store_remote_ressources_path()
    ia_store_local = get_local_store_path()

    print(ia_store_remote)
    print(ia_store_local)
    get_ia_store_requirements_json()
    ia_store_content = get_ia_store_requirements_json()
    print(ia_store_content)
    GetFromRemote("all store IA")
