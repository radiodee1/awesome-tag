import atag_dotfolder as aa

class Dimension(object) :
    def __init__(self):

        self.a = aa.Dotfolder()

        if self.a.VAR_DIM_CONFIG == "":
            print "reset dim_config"
            self.a.dot_write(self.a.FOLDER_DIM_CONFIG, "4")
        self.key = int(self.a.VAR_DIM_CONFIG)

        self.ENUM_LOAD_ALL_GRADIENT = 0
        self.ENUM_LOAD_DOT_ONLY = 1
        self.ENUM_LOAD_CONV_CUTOFF = 2
        self.ENUM_LOAD_CONV_GRADIENT = 3

        self.ENUM_PIPELINE_1 = 0
        self.ENUM_PIPELINE_2 = 1
        self.ENUM_PIPELINE_3 = 2
        self.ENUM_PIPELINE_4 = 3

        self.COLUMN_LOADTYPE = 0
        self.COLUMN_NAME = 1
        self.COLUMN_DESCRIPTION = 2
        self.COLUMN_MID_DOT = 3
        self.COLUMN_IN_OUT_DOT = 4
        self.COLUMN_IN_OUT_CONV = 5
        self.COLUMN_XY_CONV = 6
        self.COLUMN_CWEIGHT_1 = 7
        self.COLUMN_CBIAS_1 = 8
        self.COLUMN_CWEIGHT_2 = 9
        self.COLUMN_CBIAS_2 = 10
        self.COLUMN_RESHAPE_1 = 11
        self.COLUMN_RESHAPE_2 = 12
        self.COLUMN_FULL_CONNECTED_W1 = 13
        self.COLUMN_FULL_CONNECTED_B1 = 14
        self.COLUMN_FULL_CONNECTED_W2 = 15
        self.COLUMN_FULL_CONNECTED_B2 = 16
        self.COLUMN_ENUM_PIPELINE = 17
        self.COLUMN_LOAD_DOT_CONV = 18

        self.ROW_NAME_ORIGINAL_28 = 0
        self.ROW_NAME_LARGER_XY = 1
        self.ROW_NAME_PIPELINE_EXPERIMENT = 2
        self.ROW_NAME_PIPELINE_LARGEST_XY = 3
        self.ROW_NAME_PIPELINE_3_WORKING = 4
        self.ROW_NAME_PIPELINE_4_EYE = 5

        #self.key = self.ROW_NAME_ORIGINAL_28 #
        #self.key =  self.ROW_NAME_LARGER_XY
        #self.key = self.ROW_NAME_PIPELINE_EXPERIMENT
        #self.key = self.ROW_NAME_PIPELINE_LARGEST_XY
        self.dim_default = self.ROW_NAME_PIPELINE_4_EYE

        def dim_xy(w, h):
            return [w , h]

        def dim_abcd(a,b,c,d):
            return [a,b,c,d]

        def dim_ab(a,b):
            return [a,b]

        def dim_bias(b):
            return [b]

        def dim_load_dot_conv(load_dot=True, load_conv=True):
            return [load_dot, load_conv]

        convdim = 9  # try 11
        basedim = 13 # try 13

        ''' set both to False for multi-graph version to work '''
        load_dot = False
        load_conv = False

        name_string = ""
        if load_dot: name_string = name_string + "_dot"
        if load_conv: name_string = name_string + "_conv"

        self.DIMENSIONS = [
            [
                self.ENUM_LOAD_ALL_GRADIENT,
                'load_all',
                'load all as default',
                0,
                dim_ab(4 * 3, 2),
                dim_ab(28 * 28 * 3 , 2),
                dim_xy(28, 28),
                dim_abcd(5,5,3,32),
                dim_bias(32),
                dim_abcd( 5, 5, 32, 64),
                dim_bias(64),
                dim_abcd(-1, 28, 28, 3),
                dim_ab(-1, 7 * 7 * 64), # -1, 3136
                dim_ab(7 * 7 * 64, 1024), # 3136, 1024
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2),
                self.ENUM_PIPELINE_1,
                dim_load_dot_conv()

            ],
            [
                self.ENUM_LOAD_ALL_GRADIENT,
                'big_input',
                'load all as big input',
                0,
                dim_ab(4 * 3, 2), # in out dot
                dim_ab(40 * 40 * 3, 2), # in out conv 4800, 2
                dim_xy(40, 40), # x y
                dim_abcd(5, 5, 3, 44), # conv weight 1
                dim_bias(44), # conv bias 1
                dim_abcd(5, 5, 44, 88), # conv weight 2
                dim_bias(88),
                dim_abcd(-1, 40, 40, 3),
                dim_ab(-1, 10 * 10 * 88), # -1, 8800
                dim_ab(10 * 10 * 88, 1024), # 8800 , 1024
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2),
                self.ENUM_PIPELINE_1,
                dim_load_dot_conv()
            ],
            [
                self.ENUM_LOAD_ALL_GRADIENT,
                'big_input_pipeline',
                'load all as big input, experiment with pipeline',
                6,
                dim_ab(4 * 3, 2),  # in out dot
                dim_ab(40 * 40 * 3, 2),  # in out conv 4800, 2
                dim_xy(40, 40),  # x y
                dim_abcd(5, 5, 3, 44),  # conv weight 1
                dim_bias(44),  # conv bias 1
                dim_abcd(5, 5, 44, 88),  # conv weight 2
                dim_bias(88),
                dim_abcd(-1, 40, 40, 3),
                dim_ab(-1, 10 * 10 * 88),  # -1, 8800
                dim_ab(10 * 10 * 88, 1024),  # 8800 , 1024
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2),
                self.ENUM_PIPELINE_2,
                dim_load_dot_conv()
            ],
            [
                self.ENUM_LOAD_ALL_GRADIENT,
                'pipeline_2_biggest_input_' + str(basedim * 4) +"_" + str(convdim) ,
                'load all as big input, experiment with pipeline',
                6,
                dim_ab(4 * 3, 2),  # in out dot
                dim_ab(basedim * 4 * basedim * 4 * 3, 2),  # in out conv 4800, 2
                dim_xy(basedim * 4, basedim * 4),  # x y
                dim_abcd(convdim, convdim, 3, basedim * 4 + convdim - 1),  # conv weight 1
                dim_bias(basedim * 4 + convdim - 1),  # conv bias 1
                dim_abcd(convdim, convdim, basedim * 4 + convdim - 1, 2 * (basedim * 4 + convdim -1)),  # conv weight 2
                dim_bias( 2 * (basedim * 4 + convdim - 1) ),
                dim_abcd(-1, basedim * 4, basedim * 4, 3),
                dim_ab(-1, basedim * basedim * 2 * (basedim * 4 + convdim - 1) ),  # -1, 8800
                dim_ab( basedim * basedim * 2 * (basedim * 4 + convdim - 1) , 1024),   # 8800 , 1024
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2),
                self.ENUM_PIPELINE_2,
                dim_load_dot_conv()
            ],
            [
                self.ENUM_LOAD_ALL_GRADIENT,
                'pipeline_3_multi_graph_' + str(basedim * 4) + "_" + str(convdim) + name_string ,
                'save graph in two parts, experiment with pipeline',
                6,
                dim_ab(4 * 3, 2),  # in out dot
                dim_ab(basedim * 4 * basedim * 4 * 3, 2),  # in out conv 4800, 2
                dim_xy(basedim * 4, basedim * 4),  # x y
                dim_abcd(convdim, convdim, 3, basedim * 4 + convdim - 1),  # conv weight 1
                dim_bias(basedim * 4 + convdim - 1),  # conv bias 1
                dim_abcd(convdim, convdim, basedim * 4 + convdim - 1, 2 * (basedim * 4 + convdim -1)),  # conv weight 2
                dim_bias( 2 * (basedim * 4 + convdim - 1) ),
                dim_abcd(-1, basedim * 4, basedim * 4, 3),
                dim_ab(-1, basedim * basedim * 2 * (basedim * 4 + convdim - 1) ),  # -1, 8800
                dim_ab( basedim * basedim * 2 * (basedim * 4 + convdim - 1) , 1024),   # 8800 , 1024
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2),
                self.ENUM_PIPELINE_3,
                dim_load_dot_conv(load_dot=load_dot, load_conv=load_conv)
            ],
            [
                self.ENUM_LOAD_ALL_GRADIENT,
                'pipeline_3_multi_graph_' + str(basedim * 4) + "_" + str(convdim) + name_string,
                'save graph in two parts, experiment with pipeline',
                6,
                dim_ab(4 * 3, 2),  # in out dot
                dim_ab(basedim * 4 * basedim * 4 * 3, 2),  # in out conv 4800, 2
                dim_xy(basedim * 4, basedim * 4),  # x y
                dim_abcd(convdim, convdim, 3, basedim * 4 + convdim - 1),  # conv weight 1
                dim_bias(basedim * 4 + convdim - 1),  # conv bias 1
                dim_abcd(convdim, convdim, basedim * 4 + convdim - 1, 2 * (basedim * 4 + convdim - 1)),  # conv weight 2
                dim_bias(2 * (basedim * 4 + convdim - 1)),
                dim_abcd(-1, basedim * 4, basedim * 4, 3),
                dim_ab(-1, basedim * basedim * 2 * (basedim * 4 + convdim - 1)),  # -1, 8800
                dim_ab(basedim * basedim * 2 * (basedim * 4 + convdim - 1), 1024),  # 8800 , 1024
                dim_bias(1024),
                dim_ab(1024, 2),
                dim_bias(2),
                self.ENUM_PIPELINE_4,
                dim_load_dot_conv(load_dot=load_dot, load_conv=load_conv)
            ]

        ]

        #print self.DIMENSIONS[self.key]