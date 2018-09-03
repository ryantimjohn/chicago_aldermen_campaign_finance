from os import listdir
from shutil import copyfile

for file in listdir():
    ward = file.split()[0]
    copyfile(file, "Ward{}.json".format(ward))