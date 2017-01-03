

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