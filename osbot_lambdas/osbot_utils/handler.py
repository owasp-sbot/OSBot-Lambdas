from osbot_utils.utils.Files import files_list, current_temp_folder, temp_file


def run(event, context=None):
    temp_file(contents='an_temp_file', extension='.txt')
    return files_list(current_temp_folder())