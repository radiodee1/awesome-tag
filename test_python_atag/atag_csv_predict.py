
import atag_csv as enum

class PredictRead(enum.Enum):
    def __init__(self):
        enum.Enum.__init__(self)
        self.filename = ""
        self.pic_num = 0

    def read_predict_list(self):
        pass

    def predict_next(self, pic):
        return pic


    def predict_prev(self, pic):
        return pic


