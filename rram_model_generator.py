import argparse
from num_interpreter import num_interpreter

parser = argparse.ArgumentParser(description='RRAM Model Generator')
parser.add_argument('--mode', default='cols', choices=['cols', 'all'],
                    help='Generation mode {cols, all} (default: cols)')
parser.add_argument('--row', type=int, metavar='N', default=256, choices=[256, 512, 1024, 2048],
                    help='Number of rows {256, 512, 1024, 2048} (default: 256)')
parser.add_argument('--col', type=int, metavar='N', default=256, choices=[256, 512, 1024, 2048],
                    help='Number of columns {256, 512, 1024, 2048} (default: 256)')
parser.add_argument('--gen_col', type=int, metavar='N', default=6,
                    help='Number of generated columns (default: 6)')
parser.add_argument('--pi', type=int, metavar='N', default=8,
                    help='Number of segments in Pi model (default: 8)')
parser.add_argument('--file', type=argparse.FileType('w'), metavar='FILE_NAME', default='array_model.sp',
                    help='Output file name (default: array_model.sp)')
args = parser.parse_args()

MODE = args.mode
NROW = args.row
NCOL = args.col
NSEG = args.pi
NUM_GEN_COL = args.gen_col

# Parameters for the Memristor
HRS = '20K'     # ohm
LRS = '2K'      # ohm

# Parameters for Transistor
MOS_MODEL = 'nch'   # device model name
MOS_W = '300n'      # meter
MOS_L = '40n'       # meter
CGTOT = '150a'      # farad

# Parameters for Parasitic RC
RW = '900m'     # ohm
RB = '300m'     # ohm
RS = '200m'     # ohm
CWS = '100a'    # farad
CBS = '100a'    # farad
CSS = '300a'    # farad

# Parameters for Coupling Capacitance
CWWC = '10a'    # farad
CBSC = '10a'    # farad
CBBC = '20a'    # farad

# Parameters for Pi Model
RPI_WL = str((NCOL - NUM_GEN_COL * 2) * num_interpreter(RW) / NSEG)
CPI_WL = str((NCOL - NUM_GEN_COL * 2) * (num_interpreter(CWS) + num_interpreter(CGTOT)) / (NSEG+1))

f = args.file

if MODE == 'cols':
    f.write(".subckt array")
    for i in range(NROW):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" WL_L<{:0d}>".format(i))
    f.write("\n+")
    for i in range(NROW):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" WL_R<{:0d}>".format(i))
    f.write("\n+")
    for i in range(NCOL):
        if (i >= 0 and i < NUM_GEN_COL) or (i >= NCOL - NUM_GEN_COL and i <= NCOL - 1):
            f.write(" BL_T<{:0d}>".format(i))
    for i in range(NCOL):
        if (i >= 0 and i < NUM_GEN_COL) or (i >= NCOL - NUM_GEN_COL and i <= NCOL - 1):
            f.write(" BL_B<{:0d}>".format(i))
    for i in range(int(NCOL/2)):
        if (i >= 0 and i < int(NUM_GEN_COL/2)) or (i >= int(NCOL/2) - int(NUM_GEN_COL/2) and i <= int(NCOL/2) - 1):
            f.write(" SL_T<{:0d}>".format(i))
    for i in range(int(NCOL/2)):
        if (i >= 0 and i < int(NUM_GEN_COL/2)) or (i >= int(NCOL/2) - int(NUM_GEN_COL/2) and i <= int(NCOL/2) - 1):
            f.write(" SL_B<{:0d}>".format(i))
    f.write(" VSS\n")
    
elif MODE == 'all':
    f.write(".subckt array")
    for i in range(NROW):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" WL_L<{:0d}>".format(i))
    f.write("\n+")
    for i in range(NROW):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" WL_R<{:0d}>".format(i))
    f.write("\n+")
    for i in range(NCOL):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" BL_T<{:0d}>".format(i))
    f.write("\n+")
    for i in range(NCOL):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" BL_B<{:0d}>".format(i))
    f.write("\n+")
    for i in range(int(NCOL/2)):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" SL_T<{:0d}>".format(i))
    f.write("\n+")
    for i in range(int(NCOL/2)):
        if i != 0 and i % 256 == 0:
            f.write("\n+")
        f.write(" SL_B<{:0d}>".format(i))
    f.write(" VSS\n")

if MODE == 'cols':
    # Create array and parasitic RC
    fweight = open('weight.txt', 'r')
    for i in range(NROW):
        w_tmp = int(fweight.readline())
        for j in range(int(NCOL/2)):
            if (j >= 0 and j < int(NUM_GEN_COL/2)) or (j >= int(NCOL/2) - int(NUM_GEN_COL/2) and j <= int(NCOL/2) - 1):
                if w_tmp == 1:
                    RL = num_interpreter(LRS)
                    RR = num_interpreter(HRS)
                elif w_tmp == -1:
                    RL = num_interpreter(HRS)
                    RR = num_interpreter(LRS)
                else:
                    RL = num_interpreter(HRS)
                    RR = num_interpreter(HRS)
                if i == NROW - 1:
                    f.write("X_{:0d}_{:0d}  BL_T<{:0d}>   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j, 2*j, i, 2*j, RL))
                    f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   SL_T<{:0d}>   VSS {}     w={}    l={}\n".format(i, 2*j, i, 2*j, i, 2*j, j, MOS_MODEL, MOS_W, MOS_L))
                    f.write("X_{:0d}_{:0d}  BL_T<{:0d}>   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j+1, 2*j+1, i, 2*j+1, RR))
                    f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   SL_T<{:0d}>   VSS {}     w={}    l={}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j, j, MOS_MODEL, MOS_W, MOS_L))
                else:
                    f.write("X_{:0d}_{:0d}  b_{:0d}_{:0d}   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j, i, 2*j, i, 2*j, RL))
                    f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   s_{:0d}_{:0d}   VSS {}     w={}    l={}\n".format(i, 2*j, i, 2*j, i, 2*j, i, j, MOS_MODEL, MOS_W, MOS_L))
                    f.write("X_{:0d}_{:0d}  b_{:0d}_{:0d}   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j+1, RR))
                    f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   s_{:0d}_{:0d}   VSS {}     w={}    l={}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j, i, j, MOS_MODEL, MOS_W, MOS_L))
                    
                if j == 0:
                    f.write("RW_{:0d}_{:0d} WL_L<{:0d}>       w_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i, i, 2*j, RW))
                else:
                    f.write("RW_{:0d}_{:0d} w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i, 2*j-1, i, 2*j, RW))
                    
                if j == int(NCOL/2) - 1:
                    f.write("RW_{:0d}_{:0d} WL_R<{:0d}>       w_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i, i, 2*j, RW))
                else:
                    f.write("RW_{:0d}_{:0d}     w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j, RW))
                    
                f.write("CWS_{:0d}_{:0d}    w_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j, i, 2*j, CWS))
                f.write("CWS_{:0d}_{:0d}    w_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j+1, i, 2*j, CWS))
                
                if i == 0:
                    f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_B<{:0d}>   {:s}\n".format(i, 2*j, i, 2*j, 2*j, RB))
                    f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_B<{:0d}>   {:s}\n".format(i, 2*j+1, i, 2*j+1, 2*j+1, RB))
                    f.write("CBS_{:0d}_{:0d}    BL_B<{:0d}>   VSS {:s}\n".format(i, 2*j, 2*j, CBS))
                    f.write("CBS_{:0d}_{:0d}    BL_B<{:0d}>   VSS {:s}\n".format(i, 2*j+1, 2*j+1, CBS))
                elif i == NROW - 1:
                    f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_T<{:0d}>   {:s}\n".format(i, 2*j, i-1, 2*j, 2*j, RB))
                    f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_T<{:0d}>   {:s}\n".format(i, 2*j+1, i-1, 2*j+1, 2*j+1, RB))
                    f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}       VSS {:s}\n".format(i, 2*j, i-1, 2*j, CBS))
                    f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}       VSS {:s}\n".format(i, 2*j+1, i-1, 2*j+1, CBS))
                else:
                    f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   b_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i-1, 2*j, i, 2*j, RB))
                    f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   b_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i-1, 2*j+1, i, 2*j+1, RB))
                    f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j, i-1, 2*j, CBS))
                    f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j+1, i-1, 2*j+1, CBS))
                
                if i == 0:
                    f.write("RS_{:0d}_{:0d}     s_{:0d}_{:0d}   SL_B<{:0d}>   {:s}\n".format(i, j, i, j, j, RS))
                    f.write("CSS_{:0d}_{:0d}    SL_B<{:0d}>   VSS         {:s}\n".format(i, j, j, CSS))
                elif i == NROW - 1:
                    f.write("RS_{:0d}_{:0d}     s_{:0d}_{:0d}   SL_T<{:0d}>   {:s}\n".format(i, j, i-1, j, j, RS))
                    f.write("CSS_{:0d}_{:0d}    s_{:0d}_{:0d}       VSS         {:s}\n".format(i, j, i-1, j, CSS))
                else:
                    f.write("RS_{:0d}_{:0d}     s_{:0d}_{:0d}   s_{:0d}_{:0d}   {:s}\n".format(i, j, i-1, j, i, j, RS))
                    f.write("CSS_{:0d}_{:0d}    s_{:0d}_{:0d}   VSS {:s}\n".format(i, j, i-1, j, CSS))
                    
        # Create Pi model on WL
        for k in range(NSEG):
            if k == 0:
                f.write("CPI_WL_{:0d}_{:0d}    w_{:0d}_{:0d}   VSS             {:s}\n".format(i, k, i, 15, CPI_WL))
                f.write("RPI_WL_{:0d}_{:0d}    w_{:0d}_{:0d}   kw_{:0d}_{:0d}   {:s}\n".format(i, k, i, 15, i, k, RPI_WL))
            elif k == NSEG - 1:
                f.write("CPI_WL_{:0d}_{:0d}    kw_{:0d}_{:0d}   VSS             {:s}\n".format(i, k, i, k-1, CPI_WL))
                f.write("RPI_WL_{:0d}_{:0d}    kw_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, k, i, k-1, i, NCOL-16, RPI_WL))
                f.write("CPI_WL_{:0d}_{:0d}    w_{:0d}_{:0d}   VSS             {:s}\n".format(i, k+1, i, NCOL-16, CPI_WL))
            else:
                f.write("CPI_WL_{:0d}_{:0d}    kw_{:0d}_{:0d}   VSS             {:s}\n".format(i, k, i, k-1, CPI_WL))
                f.write("RPI_WL_{:0d}_{:0d}    kw_{:0d}_{:0d}   kw_{:0d}_{:0d}   {:s}\n".format(i, k, i, k-1, i, k, RPI_WL))

    # Create coupling capacitance
    for i in range(NROW):
        for j in range(int(NCOL/2)):
            if (j >= 0 and j < int(NUM_GEN_COL/2)) or (j >= int(NCOL/2) - int(NUM_GEN_COL/2) and j <= int(NCOL/2) - 1):
                if i == 0:
                    f.write("CBSC_{:0d}_{:0d}   BL_B<{:0d}>   SL_B<{:0d}>   {:s}\n".format(i, 2*j, 2*j, j, CBSC))
                    f.write("CBSC_{:0d}_{:0d}   BL_B<{:0d}>   SL_B<{:0d}>   {:s}\n".format(i, 2*j+1, 2*j+1, j, CBSC))
                else:
                    f.write("CBSC_{:0d}_{:0d}   b_{:0d}_{:0d}   s_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i-1, 2*j, i-1, j, CBSC))
                    f.write("CBSC_{:0d}_{:0d}   b_{:0d}_{:0d}   s_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i-1, 2*j+1, i-1, j, CBSC))
                    
                if i != NROW - 1:
                    f.write("CWWC_{:0d}_{:0d}   w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i, 2*j, i+1, 2*j, CWWC))
                    f.write("CWWC_{:0d}_{:0d}   w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i, 2*j, i+1, 2*j, CWWC))
                    
            if (j >= 0 and j < int(NUM_GEN_COL/2) - 1) or (j >= int(NCOL/2) - int(NUM_GEN_COL/2) and j <= int(NCOL/2) - 2):
                if i == 0:
                    f.write("CBBC_{:0d}_{:0d}   BL_B<{:0d}>   BL_B<{:0d}>   {:s}\n".format(i, j, 2*j+1, 2*j+2, CBBC))
                else:
                    f.write("CBBC_{:0d}_{:0d}   b_{:0d}_{:0d}   b_{:0d}_{:0d}   {:s}\n".format(i, j, i-1, 2*j+1, i-1, 2*j+2, CBBC))

    fweight.close()
    
elif MODE == 'all':
    # Create array and parasitic RC
    fweight = open('weight.txt', 'r')
    for i in range(NROW):
        w_tmp = int(fweight.readline())
        for j in range(int(NCOL/2)):
            if w_tmp == 1:
                RL = num_interpreter(LRS)
                RR = num_interpreter(HRS)
            elif w_tmp == -1:
                RL = num_interpreter(HRS)
                RR = num_interpreter(LRS)
            else:
                RL = num_interpreter(HRS)
                RR = num_interpreter(HRS)
            if i == NROW - 1:
                f.write("X_{:0d}_{:0d}  BL_T<{:0d}>   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j, 2*j, i, 2*j, RL))
                f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   SL_T<{:0d}>   VSS {}     w={}    l={}\n".format(i, 2*j, i, 2*j, i, 2*j, j, MOS_MODEL, MOS_W, MOS_L))
                f.write("X_{:0d}_{:0d}  BL_T<{:0d}>   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j+1, 2*j+1, i, 2*j+1, RR))
                f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   SL_T<{:0d}>   VSS {}     w={}    l={}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j, j, MOS_MODEL, MOS_W, MOS_L))
            else:
                f.write("X_{:0d}_{:0d}  b_{:0d}_{:0d}   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j, i, 2*j, i, 2*j, RL))
                f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   s_{:0d}_{:0d}   VSS {}     w={}    l={}\n".format(i, 2*j, i, 2*j, i, 2*j, i, j, MOS_MODEL, MOS_W, MOS_L))
                f.write("X_{:0d}_{:0d}  b_{:0d}_{:0d}   n_{:0d}_{:0d}   cell     RM={:.1f}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j+1, RR))
                f.write("M_{:0d}_{:0d}  n_{:0d}_{:0d}   w_{:0d}_{:0d}   s_{:0d}_{:0d}   VSS {}     w={}    l={}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j, i, j, MOS_MODEL, MOS_W, MOS_L))
                
            if j == 0:
                f.write("RW_{:0d}_{:0d} WL_L<{:0d}>       w_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i, i, 2*j, RW))
            else:
                f.write("RW_{:0d}_{:0d} w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i, 2*j-1, i, 2*j, RW))
                
            if j == int(NCOL/2) - 1:
                f.write("RW_{:0d}_{:0d} WL_R<{:0d}>       w_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i, i, 2*j, RW))
            else:
                f.write("RW_{:0d}_{:0d}     w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i, 2*j+1, i, 2*j, RW))
                
            f.write("CWS_{:0d}_{:0d}    w_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j, i, 2*j, CWS))
            f.write("CWS_{:0d}_{:0d}    w_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j+1, i, 2*j, CWS))
            
            if i == 0:
                f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_B<{:0d}>   {:s}\n".format(i, 2*j, i, 2*j, 2*j, RB))
                f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_B<{:0d}>   {:s}\n".format(i, 2*j+1, i, 2*j+1, 2*j+1, RB))
                f.write("CBS_{:0d}_{:0d}    BL_B<{:0d}>   VSS {:s}\n".format(i, 2*j, 2*j, CBS))
                f.write("CBS_{:0d}_{:0d}    BL_B<{:0d}>   VSS {:s}\n".format(i, 2*j+1, 2*j+1, CBS))
            elif i == NROW - 1:
                f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_T<{:0d}>   {:s}\n".format(i, 2*j, i-1, 2*j, 2*j, RB))
                f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   BL_T<{:0d}>   {:s}\n".format(i, 2*j+1, i-1, 2*j+1, 2*j+1, RB))
                f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}       VSS {:s}\n".format(i, 2*j, i-1, 2*j, CBS))
                f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}       VSS {:s}\n".format(i, 2*j+1, i-1, 2*j+1, CBS))
            else:
                f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   b_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i-1, 2*j, i, 2*j, RB))
                f.write("RB_{:0d}_{:0d}     b_{:0d}_{:0d}   b_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i-1, 2*j+1, i, 2*j+1, RB))
                f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j, i-1, 2*j, CBS))
                f.write("CBS_{:0d}_{:0d}    b_{:0d}_{:0d}   VSS {:s}\n".format(i, 2*j+1, i-1, 2*j+1, CBS))
            
            if i == 0:
                f.write("RS_{:0d}_{:0d}     s_{:0d}_{:0d}   SL_B<{:0d}>   {:s}\n".format(i, j, i, j, j, RS))
                f.write("CSS_{:0d}_{:0d}    SL_B<{:0d}>   VSS         {:s}\n".format(i, j, j, CSS))
            elif i == NROW - 1:
                f.write("RS_{:0d}_{:0d}     s_{:0d}_{:0d}   SL_T<{:0d}>   {:s}\n".format(i, j, i-1, j, j, RS))
                f.write("CSS_{:0d}_{:0d}    s_{:0d}_{:0d}       VSS         {:s}\n".format(i, j, i-1, j, CSS))
            else:
                f.write("RS_{:0d}_{:0d}     s_{:0d}_{:0d}   s_{:0d}_{:0d}   {:s}\n".format(i, j, i-1, j, i, j, RS))
                f.write("CSS_{:0d}_{:0d}    s_{:0d}_{:0d}   VSS {:s}\n".format(i, j, i-1, j, CSS))
                
    # Create coupling capacitance
    for i in range(NROW):
        for j in range(int(NCOL/2)):
            if i == 0:
                f.write("CBSC_{:0d}_{:0d}   BL_B<{:0d}>   SL_B<{:0d}>   {:s}\n".format(i, 2*j, 2*j, j, CBSC))
                f.write("CBSC_{:0d}_{:0d}   BL_B<{:0d}>   SL_B<{:0d}>   {:s}\n".format(i, 2*j+1, 2*j+1, j, CBSC))
            else:
                f.write("CBSC_{:0d}_{:0d}   b_{:0d}_{:0d}   s_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i-1, 2*j, i-1, j, CBSC))
                f.write("CBSC_{:0d}_{:0d}   b_{:0d}_{:0d}   s_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i-1, 2*j+1, i-1, j, CBSC))
                
            if i != NROW - 1:
                f.write("CWWC_{:0d}_{:0d}   w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j, i, 2*j, i+1, 2*j, CWWC))
                f.write("CWWC_{:0d}_{:0d}   w_{:0d}_{:0d}   w_{:0d}_{:0d}   {:s}\n".format(i, 2*j+1, i, 2*j, i+1, 2*j, CWWC))
            
            if j != int(NCOL/2) - 1:
                if i == 0:
                    f.write("CBBC_{:0d}_{:0d}   BL_B<{:0d}>   BL_B<{:0d}>   {:s}\n".format(i, j, 2*j+1, 2*j+2, CBBC))
                else:
                    f.write("CBBC_{:0d}_{:0d}   b_{:0d}_{:0d}   b_{:0d}_{:0d}   {:s}\n".format(i, j, i-1, 2*j+1, i-1, 2*j+2, CBBC))

    fweight.close()

f.write(".ends\n")
f.close()
