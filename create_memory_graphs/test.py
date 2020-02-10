from pyswip.core import *
from pyswip import *
from time import gmtime, strftime
import random
global image_path
def main():
    p = Prolog()
    p.consult("./pages/test_py.pl")
    idx = [0, 8, 16, 24, 32, 72, 112, 120, 128, 136]
    idx2 = [0, 4, 8]

    assertz = Functor("assertz")
    ispointer = Functor("ispointer", 1)
    isint = Functor("isint", 1)

    possible_task_struct = Functor("possible_task_struct", 4)
    possible_mm_struct = Functor("possible_mm_struct", 1)

    for s in p.query("possible_task_struct(Base_addr, Pid_offset, MM_offset, MM_offset2)", catcherrors=False):
        print(s["Base_addr"], s["Pid_offset"], s["MM_offset"], s["MM_offset2"])

    kb = newModule("test")
    for key in idx:
        call(assertz(ispointer(str(key))), module=kb)
    #print str(isint.name)
    #kb = construct_kb(assertz, ispointer, idx, "test")
    #kb = construct_kb(assertz, ispointer, idx, "test")
    #kb = construct_kb(assertz, isint, idx2, "test")
    X = Variable()
    q = Query(possible_mm_struct(X), module = kb)
    while q.nextSolution():
        #print(X.value)
        pass
    q.closeQuery()

    q = Query(ispointer(X), module = kb)
    while q.nextSolution():
        #print(X.value)
        pass
    q.closeQuery()

    #extract_info(image_path, 0x1C278080, 1024, "test")

    

'''

    Y = Variable()
    print ("")
    registerForeign(atom_checksum, arity=2)
    q = Query(ispointer(Y), module = kb2)
    while q.nextSolution():
        #print(Y.value)
        pass
    q.closeQuery()
    p = Prolog()
    listing = Functor("listing", 1)
    p.consult("./pages/kb_file.pl", kb2)
    p.consult("./pages/rules.pl", kb2)
    Pid_offset = Variable()
    Comm_offset = Variable()
    possible_task_struct = Functor("possible_task_struct", 5)
    for s in p.query("possible_task_struct(Pid_offset, Comm_offset, MM_offset, MM_offset2)", catcherrors=False):
        print(s["Pid_offset"])
'''
    #call(listing(ispointer))



def atom_checksum(*a):
    v = str(a[0])
    print "test", v
    return True

def construct_kb(assertz, func, dicts, kb_name, paddr=0):
    kb = newModule(str(kb_name))
    for key in dicts:
        call(assertz(func(str(key))), module=kb)
    return kb

def extract_info_r(image_path, paddr, size, set_vaddr_page, name, file_h=None):
    valid_pointer = {}
    valid_comm = {}
    valid_int = {}

    image = open(image_path, 'r')
    image.seek(paddr)
    content = image.read(size)
    # find pointers
    i = 0
    while i < len(content):
        tmp = content[i:i+8]
        if(tmp.endswith("\xff\xff")):
            if not len(tmp)==8:
                break
            dest = is_valid_pointer_64(tmp, 0, set_vaddr_page)
            if dest: 
                valid_pointer[i] = hex(dest)[:-1]
                i += 7
                
        i += 1
    # find strings
    idx = 0
    while idx < len(content):
        tmp = content[idx:idx+8]
        if tmp.startswith('\x00'):
            idx += 1
            continue
        find_comm = tmp.replace('\x00', '').replace('\xff', '')
        tmp_len = 0
        for item in find_comm:
            if ord(item) >= 0x30 and ord(item) <= 0x7f:
                tmp_len += 1
        if tmp_len == len(find_comm) and len(find_comm) > 2:
            valid_comm[idx] = find_comm
            #print("found string at", idx, tmp)
            idx = idx + 7
        idx += 1
    # find unsigned long 
    i = 0
    while i < len(content):
    #for i in range(len(content)):
        tmp = content[i:i+4]
        if not tmp.endswith("\x00\x00"):
            i += 1
            continue
        # not entirely true    
        if len(tmp.replace('\xff', '')) < 4:
            i += 4
            continue
        tmp_len = 0
        summ = 0
        for idx in reversed(range(len(tmp))):
            summ += ord(tmp[idx]) << 8*idx
            if ord(tmp[idx]) < 0xff and ord(tmp[idx]) > 0x00:
                tmp_len += 1
        if summ < 9000 and tmp_len > 0:
            valid_int[i] = summ
            i += 3
            #print("found pid", i, tmp, summ)
        i += 1
    image.close()


    if not file_h:
        file_h = open("./pages/kb_all.pl", 'w')
        kb_all = file_h
        keys = valid_pointer.keys()
        keys.sort()
        for key in keys:
            fact = "ispointer(" + str(paddr) + "," + str(key) + "," + str(valid_pointer[key]) + ")." + "\n"
            kb_all.write(fact)
            
        keys = valid_int.keys()
        keys.sort()
        for key in keys:
            fact = "isint(" + str(paddr) + "," + str(key) + "," + str(valid_int[key]) + ")." + "\n"
            kb_all.write(fact)

        keys = valid_comm.keys()
        keys.sort()
        for key in keys:
            fact = "isstring(" + str(paddr) + "," + str(key) + "," + str(valid_comm[key]) + ")." + "\n"
            kb_all.write(fact)

        kb_all.write("\n")
    
    if len(valid_pointer) > 0:
        keys = valid_pointer.keys()
        keys.sort()
        for key in keys:
            extract_info_r(image_path, valid_pointer[key], 1024, set_vaddr_page, "ts_struct", file_h)


if __name__ == "__main__":
    main()

   