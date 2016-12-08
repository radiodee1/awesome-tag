import os
import signal
import sys
import atag_csv as enum
import nn_loader as loader
import atag_dotfolder as aa
import nn_model as model


'''
Here we read the csv file that we made and train the models
'''

class Read( enum.Enum) :
    def __init__(self, atag, pic):
        enum.Enum.__init__(self)

        self.pic = pic

        self.a = atag
        self.run_mnist()
        self.nn = None

    def run_mnist(self):
        print
        ll = loader.Load(self.a, self.pic)
        self.nn = model.NN(self.a)

        signal.signal(signal.SIGINT, self.signal_handler)

        self.nn.load_ckpt = True
        self.nn.save_ckpt = True
        self.nn.train = False
        self.nn.test = True
        self.nn.set_loader(ll)

        #self.nn.predict_skintone = True
        #self.nn.set_vars(len(ll.dat), 100, "skin", 0)
        #self.nn.skintone_setup()

        self.nn.predict_softmax = False
        self.nn.set_vars(len(ll.dat), 100, "softmax", 0)
        self.nn.softmax_setup()

        #self.nn.predict_conv = False
        #self.nn.set_vars(len(ll.dat), 50, "conv", 0)
        #self.nn.conv_setup()

    def signal_handler(self, signum, frame):
        self.nn.save()
        sys.exit()

if __name__ == '__main__':

    pic = ""
    if len(sys.argv) > 1 : pic = str(sys.argv[1])
    print pic
    a = aa.Dotfolder()
    r = Read(a, pic)

    print("done")