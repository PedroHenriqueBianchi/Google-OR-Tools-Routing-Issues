from os import getcwd
from os.path import dirname

if __name__ == '__main__':
    char_to_be_removed = '.'
    fileName = 'rio_claro_2000'

    local_file_path = r"{}\utils\files\{}_with_commas.txt".format(
        dirname(getcwd()),
        fileName
    )

    new_local_file_path = r"{}\utils\files\{}.txt".format(
        dirname(getcwd()),
        fileName
    )

    file_with_char_to_be_removed = open(file=local_file_path, mode='r')

    same_file_without_char = open(file=new_local_file_path, mode='a+')

    for line in file_with_char_to_be_removed:
        new_line = line.replace(char_to_be_removed, '')
        same_file_without_char.write(new_line)

    same_file_without_char.close()
    file_with_char_to_be_removed.close()
