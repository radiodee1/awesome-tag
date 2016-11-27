#!/usr/bin/python

from os.path import expanduser
import os

class Dotfolder():
    
    def __init__(self) :
        self.FOLDER_NAME = ".atagpy"
        self.FOLDER_HOME = expanduser("~")
        self.FOLDER_FULL_DOTFOLDER = self.FOLDER_HOME + os.sep + self.FOLDER_NAME
        self.FOLDER_BASE_NAME = "base_name"
        self.FOLDER_CSV_FILE_SECOND = "csv_file_second"
        self.FOLDER_CSV_FILE_SINGLE = "csv_file_single"
        self.FOLDER_IMAGE_NAME = "image_name"
        self.FOLDER_LOCAL_DATABASE = "local_database"
        self.FOLDER_MY_CSV_NAME = "my_csv_name"
        self.FOLDER_ROOT_DATABASE = "root_database"
        self.FOLDER_SAVED_CURSOR = "saved_cursor"
        self.FOLDER_SAVED_SPLIT = "saved_split"
        self.FOLDER_SPLIT_CURRENT = "split_current"
        self.FOLDER_SPLIT_END = "split_end"
        self.FOLDER_SPLIT_FOLDER_NAME = "split_folder_name"
        self.FOLDER_SPLIT_START = "split_start"
        
        self.VAR_BASE_NAME = os.sep
        self.VAR_CSV_FILE_SECOND = 0
        self.VAR_CSV_FILE_SINGLE = 0
        self.VAR_IMAGE_NAME = "name.png"
        self.VAR_LOCAL_DATABASE = os.sep
        self.VAR_MY_CSV_NAME = "name"
        self.VAR_ROOT_DATABASE = os.sep
        self.VAR_SAVED_CURSOR = 0
        self.VAR_SAVED_SPLIT = 0
        self.VAR_SPLIT_CURRENT = 0
        self.VAR_SPLIT_END = 0
        self.VAR_SPLIT_FOLDER_NAME = "folder"
        self.VAR_SPLIT_START = 0
        
        """ initialize tasks """
        self.dotfolder_exists()
        self.load_vars()
        
    def dotfolder_exists(self):
        if not os.path.isdir(self.FOLDER_FULL_DOTFOLDER):
            os.makedirs(self.FOLDER_FULL_DOTFOLDER)
            
    def dot_read(self, name, default = ""):
        if os.path.isfile(self.FOLDER_FULL_DOTFOLDER + os.sep + name) :
            f = open( self.FOLDER_FULL_DOTFOLDER + os.sep + name , 'r')
            default = f.readline()
        print default
        return default
        
    def dot_write(self, name, value):
        f = open( self.FOLDER_FULL_DOTFOLDER + os.sep + name , 'w')
        f.write(value+"\n")
        print value

    def load_vars(self):
        self.VAR_BASE_NAME = self.dot_read(self.FOLDER_BASE_NAME)
        self.VAR_CSV_FILE_SECOND = self.dot_read(self.FOLDER_CSV_FILE_SECOND)
        self.VAR_CSV_FILE_SINGLE = self.dot_read(self.FOLDER_CSV_FILE_SINGLE)
        self.VAR_IMAGE_NAME = self.dot_read(self.FOLDER_IMAGE_NAME)
        self.VAR_LOCAL_DATABASE = self.dot_read(self.FOLDER_LOCAL_DATABASE)
        self.VAR_MY_CSV_NAME = self.dot_read(self.FOLDER_MY_CSV_NAME)
        self.VAR_ROOT_DATABASE = self.dot_read(self.FOLDER_ROOT_DATABASE)
        self.VAR_SAVED_CURSOR = self.dot_read(self.FOLDER_SAVED_CURSOR)
        self.VAR_SAVED_SPLIT = self.dot_read(self.FOLDER_SAVED_SPLIT)
        self.VAR_SPLIT_CURRENT = self.dot_read(self.FOLDER_SPLIT_CURRENT)
        self.VAR_SPLIT_END = self.dot_read(self.FOLDER_SPLIT_END)
        self.VAR_SPLIT_FOLDER_NAME = self.dot_read(self.FOLDER_SPLIT_FOLDER_NAME)
        self.VAR_SPLIT_START = self.dot_read(self.FOLDER_SPLIT_START)

    def save_vars(self):
        self.dot_write(self.FOLDER_BASE_NAME, self.VAR_BASE_NAME)
        self.dot_write(self.FOLDER_CSV_FILE_SECOND, self.VAR_CSV_FILE_SECOND)
        self.dot_write(self.FOLDER_CSV_FILE_SINGLE, self.VAR_CSV_FILE_SINGLE)
        self.dot_write(self.FOLDER_IMAGE_NAME, self.VAR_IMAGE_NAME)
        self.dot_write(self.FOLDER_LOCAL_DATABASE, self.VAR_LOCAL_DATABASE)
        self.dot_write(self.FOLDER_MY_CSV_NAME, self.VAR_MY_CSV_NAME)
        self.dot_write(self.FOLDER_ROOT_DATABASE, self.VAR_ROOT_DATABASE)
        self.dot_write(self.FOLDER_SAVED_CURSOR, self.VAR_SAVED_CURSOR)
        self.dot_write(self.FOLDER_SAVED_SPLIT, self.VAR_SAVED_SPLIT)
        self.dot_write(self.FOLDER_SPLIT_CURRENT, self.VAR_SPLIT_CURRENT)
        self.dot_write(self.FOLDER_SPLIT_END, self.VAR_SPLIT_END)
        self.dot_write(self.FOLDER_SPLIT_FOLDER_NAME, self.VAR_SPLIT_FOLDER_NAME)
        self.dot_write(self.FOLDER_SPLIT_START, self.VAR_SPLIT_START)

if __name__ == '__main__': 
    d = Dotfolder()
    d.dot_write(d.FOLDER_IMAGE_NAME, "/home/dave/image.png")
    print (d.dot_read(d.FOLDER_IMAGE_NAME))
    d.VAR_IMAGE_NAME = d.dot_read(d.FOLDER_IMAGE_NAME)
    print d.VAR_IMAGE_NAME
    print("done")
