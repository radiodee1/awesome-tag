import os
import atag_csv as enum
import nn_loader as loader
import atag_dotfolder as aa
import nn_model as model

'''
Here we read the csv file that we made and train the models
'''

class Read( enum.Enum) :
    def __init__(self, atag):
        enum.Enum.__init__(self)

        self.a = atag
        '''
        self.csvnum = atag.VAR_SPLIT_CURRENT
        self.csvfolder = atag.VAR_SPLIT_FOLDER_NAME
        self.csvname = 'train_'
        self.csvend = '.csv'

        self.csvfolder = self.csvfolder[: -1]
        if self.csvfolder.endswith('1') : self.csvfolder = self.csvfolder[: -1]

        self.csv_input = self.csvfolder + self.csvnum + os.sep + self.csvname + self.csvnum + self.csvend
        print self.csv_input + '\n'
        '''
        self.run_mnist()

    def run_mnist(self):
        print
        ll = loader.Load(self.a)
        train, test = ll.get_mnist_dat()
        nn = model.NN(self.a)
        nn.set_mnist_train_test(train,test)
        nn.color_setup()

if __name__ == '__main__':
    a = aa.Dotfolder()
    r = Read(a)


    #d.dot_write(d.FOLDER_IMAGE_NAME, "/home/dave/image.png")
    #print (d.dot_read(d.FOLDER_IMAGE_NAME))
    #d.VAR_IMAGE_NAME = d.dot_read(d.FOLDER_IMAGE_NAME)
    #print d.VAR_IMAGE_NAME
    print("done")