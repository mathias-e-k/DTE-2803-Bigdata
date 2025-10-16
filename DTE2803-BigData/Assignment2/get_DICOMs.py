from os import listdir
from os.path import isdir, join, normpath

def get_sequences():
    sequences = []
    PATH = normpath("DTE2803-BigData\\Assignment2\\DICOMS\\DICOM-Paket1\\1")
    unchecked_dirs = [join(PATH, f) for f in listdir(PATH)]
    while unchecked_dirs:
        current_path = unchecked_dirs.pop(0)
        files = listdir(current_path)
        if isdir(join(current_path, files[0])):
            unchecked_dirs.extend([join(current_path, f) for f in files])
        else:
            sequences.append(current_path)
    return sequences


if __name__ == "__main__":
    seq = get_sequences()
    print(seq)
    print(len(seq))