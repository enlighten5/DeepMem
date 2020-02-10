from program import *
from pyswip.core import *
from pyswip import *

def main():
    image_path = sys.argv[1]
    image_name = os.path.basename(image_path)
    log(image_name)

    log('get available_pages')
    dict_paddr_to_size, set_vaddr_page = read_available_pages(image_name)

    log('find pointer-dest map')
    #dict_vaddr_to_dest = get_pointer_to_dest(image_path, dict_paddr_to_size, set_vaddr_page)
    #addr = dict_vaddr_to_dest.keys()
    #addr.sort()


    paddr = vaddr_to_paddr(0xffff88001c278080) # apache task struct address
    #paddr = 0x160d3b8
    #paddr = 0x1605000
    #paddr = 0
    #while paddr < 4096 * 1024 * 512:
    
    construct_kb(image_path, paddr, 1024, set_vaddr_page)
    
    #extract_info(image_path, paddr, 2048, set_vaddr_page, "test")


    p = Prolog()
    p.consult("./knowledge/kb_all.pl")
#    possible_task_struct = Functor("possible_task_struct", 4)
    count = 0
    query_cmd = "possible_task_struct(Base_addr)"
    for s in p.query(query_cmd, catcherrors=False):
        count += 1
        #print(s["Base_addr"], s["Pid_offset"], s["MM_offset"], s["MM_offset2"], s["MM_pointer"])
    #    pass
    print "count result:", count
log('finish')
    


def construct_kb(image_path, paddr, size, set_vaddr_page):
    with open("./knowledge/kb_all.pl", 'w') as kb:
        kb.write("use_module(library(clpfd))." + "\n")
        kb.write(":- discontiguous(ispointer/3)." + "\n")
        kb.write(":- discontiguous(isint/3)." + "\n")
        kb.write(":- discontiguous(isstring/3)." + "\n" + "\n")
        kb.write(":- discontiguous(islong/3)." + "\n" + "\n")


    valid_pointers = extract_info_r(image_path, paddr, size, set_vaddr_page, './knowledge/kb_all.pl')
    #keys = valid_pointers.keys()
    #for key in keys:
    #    extract_info_r(image_path, valid_pointers[key], size, set_vaddr_page)

    with open("./knowledge/kb_all.pl", 'a') as outfile:
        with open("./knowledge/init_query.pl", 'r') as inputfile:
            outfile.write(inputfile.read())
    
if __name__ == "__main__":
    main()