import sys
from program import *
from pyswip.core import *
from pyswip import *
import os
def main():
    base_addr = sys.argv[1]
    query_rule = sys.argv[2]
    construct(base_addr)
    p = Prolog()
    p.consult("./pages/test_py.pl")
    #os.system("rm ./pages/temp_kb.pl")
    # 0 is false, 1 is true
    print 1


def construct(paddr):
    size = 1024
    image_path = "/home/zhenxiao/DeepMem/memory_dumps/linux-sample-1.bin"
    print image_path
    dict_paddr_to_size, set_vaddr_page = read_available_pages("linux-sample-1.bin")
    with open("./pages/temp_kb.pl", 'w') as kb:
            kb.write("use_module(library(clpfd))." + "\n")
            kb.write(":- discontiguous(ispointer/3)." + "\n")
            kb.write(":- discontiguous(isint/3)." + "\n")
            kb.write(":- discontiguous(isstring/3)." + "\n" + "\n")
            kb.write(":- discontiguous(islong/3)." + "\n" + "\n")
    
    valid_pointers = extract_info_r(image_path, paddr, size, set_vaddr_page)

    with open("./pages/temp_kb.pl", 'a') as outfile:
        with open("./pages/ts_rules.pl", 'r') as inputfile:
            outfile.write(inputfile.read())

if __name__ == "__main__":
    main()