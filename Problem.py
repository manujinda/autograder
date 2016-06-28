class Problem(object):
    """
        A class to represent a single problem or a Homework
    """
    
    def __init__(self, no):
        self.prob_no = no
        self.proj_desc = 'Problem description'
        self.files_provided = []
        self.files_submitted = []
        self.inp_outps = {} # A dictionalry that maps test inputs to anticipated outputs
        self.language = 'Programming language used'
        self.com_lin_opt = False
        self.stud_mak_fil = False
        self.mak_targs = []
        self.scores = []
