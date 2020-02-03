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
    
    ispointer(Base_addr, MM_offset2, MM_pointer2),
    MM_offset2 is MM_offset + 8,
    possible_mm_struct(MM_pointer2),

    /* a bunch of list_head */

    /* comm */
    isstring(Base_addr, Comm_offset, Comm_value),
    Comm_offset > MM_offset2,

    /* fs_struct */
    ispointer(Base_addr, FS_offset, FS_value),
    FS_offset > Comm_offset,
    possible_fs_struct(FS_value),

    /* files_struct */
    /* tlbflush_unmap_batch */
    ispointer(Base_addr, TLB_offset, TLB_value),
    TLB_offset > FS_offset,
    TLB_offset < 2000,
    possible_tlbflush_unmap_batch(TLB_value).


    

possible_mm_struct(Base_addr) :- 
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

    islong(Base_addr, Offset6, Value6),
    islong(Base_addr, Offset7, Value7),
    Offset7 is Offset6 + 8,
    islong(Base_addr, Offset8, Value8),
    Offset8 is Offset7 + 8,
    islong(Base_addr, Offset9, Value9),
    Offset9 is Offset8 + 8,
    islong(Base_addr, Offset10, Value10),
    Offset10 is Offset9 + 8.

possible_sched_info(Base_addr) :- 
    islong(Base_addr, Offset1, Value1),
    Offset1 < 10.


possible_list_head(Base_addr) :- 
    ispointer(Base_addr, Offset1, Value1),
    Offset1 is 0,
    ispointer(Base_addr, Offset2, Value2),
    Offset2 is Offset1 + 8.

possible_fs_struct(Base_addr) :- 
    /* 3 integers */
    isint(Base_addr, Offset1, Value1),
    isint(Base_addr, Offset2, Value2),
    Offset2 > Offset1,
    isint(Base_addr, Offset3, Value3),
    Offset3 > Offset2.

possible_tlbflush_unmap_batch(Base_addr):- 
    ispointer(Base_addr, Offset, Value).
