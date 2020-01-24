% use_module(library(clpfd)).


possible_task_struct(Base_addr, Pid_offset, MM_offset, MM_offset2) :- 	
    isint(Base_addr, Pid_offset, Value),
    isint(Base_addr, Tgid_offset, Value2),
	Tgid_offset is Pid_offset + 4,
    /* for struct mm_struct mm */
	/*possible_mm_struct(mm_offset, base_addr),*/

    ispointer(Base_addr, MM_offset, MM_pointer),
    MM_offset < Tgid_offset,
    MM_offset > 400,
    
    ispointer(Base_addr, MM_offset2, MM_pointer),
    MM_offset2 is MM_offset + 8,
    possible_mm_struct(MM_pointer).
    

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