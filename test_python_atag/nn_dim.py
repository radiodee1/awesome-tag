

class Enum(object) :
    def __init__(self):
        self.ENUM_LOAD_ALL_CUTOFF = 0
        self.ENUM_LOAD_DOT_ONLY = 1
        self.ENUM_LOAD_CONV_CUTOFF = 2
        self.ENUM_LOAD_CONV_GRADIENT = 3

        self.COLUMN_LOADTYPE = 0
        self.COLUMN_NAME = 1
        self.COLUMN_DESCRIPTION = 2
        self.COLUMN_IN_OUT_DOT = 3
        self.COLUMN_IN_OUT_CONV = 4
        self.COLUMN_XY_CONV = 5
        self.COLUMN_CWEIGHT_1 = 6
        self.COLUMN_CBIAS_1 = 7
        self.COLUMN_CWEIGHT_2 = 8
        self.COLUMN_CBIAS_2 = 9
        self.COLUMN_RESHAPE_1 = 10
        self.COLUMN_RESHAPE_2 = 11
        self.COLUMN_FULL_CONNECTED_W1 = 12
        self.COLUMN_FULL_CONNECTED_B1 = 13
        self.COLUMN_FULL_CONNECTED_W2 = 14
        self.COLUMN_FULL_CONNECTED_B2 = 15

        self.ROW_NAME_ORIGINAL_28 = 0
        self.ROW_NAME_LARGER_XY = 1
        self.ROW_NAME_LARGER_OUT = 2

        def dim_xy(w, h):
            return [w , h]

        def dim_abcd(a,b,c,d):
            return [a,b,c,d]

        def dim_ab(a,b):
            return [a,b]

        def dim_bias(b):
            return [b]


        self.DIMENSIONS = [
            [
                self.ENUM_LOAD_ALL_CUTOFF,
                'load_all',
                'load all as default',
                dim_ab(4 * 3, 2),
                dim_ab(28 * 28 * 3 , 2),
                dim_xy(28, 28),
                dim_abcd(5,5,3,32),
                dim_bias(32),
                dim_abcd( 5, 5, 32, 64),
                dim_bias(64),
                dim_abcd(-1, 28, 28, 3),
                dim_ab(-1, 7 * 7 * 64),
                dim_ab(7 * 7 * 64, 1024),
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2)

            ],
            [
                self.ENUM_LOAD_ALL_CUTOFF,
                'load_all',
                'load all as default',
                dim_ab(4 * 3, 2),
                dim_ab(28 * 28 * 3, 2),
                dim_xy(28, 28),
                dim_abcd(5, 5, 3, 32),
                dim_bias(32),
                dim_abcd(5, 5, 32, 64),
                dim_bias(64),
                dim_abcd(-1, 28, 28, 3),
                dim_ab(-1, 7 * 7 * 64),
                dim_ab(7 * 7 * 64, 1024),
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2)
            ],
            [
                self.ENUM_LOAD_ALL_CUTOFF,
                'load_all',
                'load all as default',
                dim_ab(4 * 3, 2),
                dim_ab(28 * 28 * 3, 2),
                dim_xy(28, 28),
                dim_abcd(5, 5, 3, 32),
                dim_bias(32),
                dim_abcd(5, 5, 32, 64),
                dim_bias(64),
                dim_abcd(-1, 28, 28, 3),
                dim_ab(-1, 7 * 7 * 64),
                dim_ab(7 * 7 * 64, 1024),
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2)
            ]

        ]

        print self.DIMENSIONS[self.ROW_NAME_ORIGINAL_28]