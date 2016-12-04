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
        self.run_mnist()

    def run_mnist(self):
        print
        ll = loader.Load(self.a)
        #train, test = ll.get_mnist_dat()

        nn = model.NN(self.a)
        nn.load_ckpt = True
        nn.save_ckpt = True
        nn.train = True
        nn.test = True
        nn.set_loader(ll)

        nn.set_vars(len(ll.dat), 100)
        nn.mnist_setup()

        #nn.set_vars(len(ll.dat), 50)
        #nn.conv_setup()

if __name__ == '__main__':
    a = aa.Dotfolder()
    r = Read(a)


    #d.dot_write(d.FOLDER_IMAGE_NAME, "/home/dave/image.png")
    #print (d.dot_read(d.FOLDER_IMAGE_NAME))
    #d.VAR_IMAGE_NAME = d.dot_read(d.FOLDER_IMAGE_NAME)
    #print d.VAR_IMAGE_NAME
    print("done")