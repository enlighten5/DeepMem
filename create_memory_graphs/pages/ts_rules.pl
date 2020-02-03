% use_module(library(clpfd)).
:- style_check(-singleton).

possible_task_struct(Base_addr, Pid_offset, MM_offset, MM_offset2, MM_pointer2) :- 
    /* void *stack */
    ispointer(Base_addr, Stack_offset, Stack_value),

    /* sched_info sched_info */
    ispointer(Base_addr, Sched_info_offset, Sched_info_value),
    Sched_info_offset > Stack_offset,
    possible_sched_info(Sched_info_value),

    /* list_head tasks */
    ispointer(Base_addr, Tasks_offset, Task_value),
    Tasks_offset > Sched_info_offset,
    possible_list_head(Task_value),


    isint(Base_addr, Pid_offset, Value),
    isint(Base_addr, Tgid_offset, Value2),
	Tgid_offset is Pid_offset + 4,
    Tgid_offset > Tasks_offset,
    /* for struct mm_struct mm */
	/*possible_mm_struct(mm_offset, base_addr),*/

    ispointer(Base_addr, MM_offset, MM_pointer),
    MM_offset < Tgid_offset,
    MM_offset > 400,
    
    ispointer(Base_addr, MM_offset2, MM_pointer),
    MM_offset2 is MM_offset + 8,
    print_nl('test', MM_offset2),
    possible_mm_struct(MM_pointer),
    print_nl('success', MM_offset2).

    /* a bunch of list_head */

    /* comm */
    /*
    isstring(Base_addr, Comm_offset, Comm_value),
    Comm_offset > MM_offset2,
*/
    /* children/sibling */
    /*
    ispointer(Base_addr, Child_offset, Child_value),
    Child_offset < Comm_offset,
    Child_offset > Pid_offset,
    possible_list_head(Child_value),
    ispointer(Base_addr, Sibling_offset, Sibling_value),
    Sibling_offset is Child_offset + 8,
    possible_list_head(Sibling_value),
*/
    /* fs_struct */
    /* files_struct */
 /*   
    ispointer(Base_addr, FS_offset, FS_value),
    FS_offset > Comm_offset,
    possible_fs_struct(FS_value),
    
    ispointer(Base_addr, FS_offset2, FS_value2),
    FS_offset2 is FS_offset + 8,
    print_nl('child', Child_offset),
    print_nl('fs', FS_offset).
*/
/*
    print_nl('stack', Stack_offset),
    print_nl('task', Tasks_offset),
    print_nl('pid', Pid_offset),
    print_nl('mm_struct', MM_offset2).
*/

    

possible_mm_struct(Base_addr) :- 
    /* five pointers */
    print_nl('start query mm', ''),
    ispointer(Base_addr, Offset1, Value1),
    Offset1 = 0,
    ispointer(Base_addr, Offset2, Value2),
    Offset2 is Offset1 + 8,
    ispointer(Base_addr, Offset3, Value3),
    Offset3 is Offset2 + 8,
    ispointer(Base_addr, Offset4, Value4),
    Offset4 is Offset3 + 8,
    ispointer(Base_addr, Offset5, Value5),
    Offset5 is Offset4 + 8,
    /*
        unsigned long start_code, end_code, start_data, end_data;
	    unsigned long start_brk, brk, start_stack;
	    unsigned long arg_start, arg_end, env_start, env_end;
    
    */
    islong(Base_addr, Offset6, Value6),
    islong(Base_addr, Offset7, Value7),
    Offset7 is Offset6 + 8,
    Value7 > Value6,
    islong(Base_addr, Offset8, Value8),
    Offset8 is Offset7 + 8,
    islong(Base_addr, Offset9, Value9),
    Offset9 is Offset8 + 8,
    Value9 > Value8,

    islong(Base_addr, Offset10, Value10),
    Offset10 is Offset9 + 8,
    islong(Base_addr, Offset11, Value11),
    Offset11 is Offset10 + 8,
    islong(Base_addr, Offset12, Value12),
    Offset12 is Offset11 + 8,

    islong(Base_addr, ARG_start_offset, ARG_start_value),
    ARG_start_offset is Offset12 + 8,
    islong(Base_addr, ARG_end_offset, ARG_end_value),
    ARG_end_offset is ARG_start_offset + 8,
    ARG_end_value > ARG_start_value,
    islong(Base_addr, ENV_start_offset, ENV_start_value),
    ENV_start_offset is ARG_end_offset + 8,
    islong(Base_addr, ENV_end_offset, ENV_end_value),
    ENV_end_offset is ENV_start_offset + 8,
    ENV_end_value > ENV_start_value.

possible_sched_info(Base_addr) :- 
    islong(Base_addr, Offset1, Value1),
    Offset1 < 10.


possible_list_head(Base_addr) :- 
    ispointer(Base_addr, Offset1, Value1),
    Offset1 is 0,
    ispointer(Base_addr, Offset2, Value2),
    Offset2 is Offset1 + 8,
    print_nl('list_head', Base_addr).

possible_fs_struct(Base_addr) :- 
    /* 3 integers */
    isint(Base_addr, Offset1, Value1),
    Offset1 is 0,
    isint(Base_addr, Offset2, Value2),
    Offset2 > Offset1,
    isint(Base_addr, Offset3, Value3),
    Offset3 < Offset2 + 10.

possible_tlbflush_unmap_batch(Base_addr):- 
    ispointer(Base_addr, Offset, Value).

print_nl(Name, Content) :- 
    print(Name),
    print(':'),
    print(Content),
    nl.