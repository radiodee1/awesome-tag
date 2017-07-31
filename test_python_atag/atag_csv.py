

class Enum(object) :
    def __init__(self):
        self.TEMPLATE_ID = 0
        self.SUBJECT_ID = 1
        self.FILE = 2
        self.MEDIA_ID = 3
        self.SIGHTING_ID = 4
        self.FRAME = 5
        self.FACE_X = 6
        self.FACE_Y = 7
        self.FACE_WIDTH = 8
        self.FACE_HEIGHT = 9

        # only in non-detection csv files
        self.FACE_YAW = 16

        self.COLOR = 10 # THIS IS MY COLOR
        self.IS_FACE = 11 # THIS IS MY BOOBLEAN
        self.ATAG_ID = 12
        self.TOTAL = 13
        self.TOTAL_READ = 10

        self.RED = "RED"
        self.GREEN = "GREEN"
        self.BLUE = "BLUE"

        self.CONST_ONE_CHANNEL = 1
        self.CONST_THREE_CHANNEL = 3
        self.CONST_DOT = 12

        self.AGGREGATE_START = -1
        self.AGGREGATE_TOUCHED = -5
        self.AGGREGATE_DELETE = -99

        # for gpu
        self.BIT_TOP = 0x0001
        self.BIT_BOTTOM = 0x0002
        self.BIT_LEFT = 0x0004
        self.BIT_RIGHT = 0x0008

        self.GPU_X = 0
        self.GPU_Y = 1
        self.GPU_W = 2
        self.GPU_H = 3
        self.GPU_NUM = 4
        self.GPU_BOX = 5
        self.GPU_TOT = 6