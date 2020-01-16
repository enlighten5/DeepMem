use_module(library(clpfd)).



possible_task_struct(Pid_offset, MM_offset, MM_offset2, Comm_offset) :- 	
    isint(Pid_offset),
    isint(Tgid_offset),
	Tgid_offset is Pid_offset + 4.
    /* for struct mm_struct mm */
	/*possible_mm_struct(mm_offset, base_addr),*/


possible_pid(Pid_offset, MM_offset, MM_offset2, Comm_offset, Real_parent_offset) :- 
    isint(Pid_offset),
    isint(Tgid_offset),
	Tgid_offset is Pid_offset + 4,	
    Tgid_offset > 400,

    /* for struct mm_struct mm */
	/*possible_mm_struct(mm_offset, base_addr),*/

    ispointer(MM_offset),
    MM_offset < Tgid_offset,
    MM_offset > 400,
    /*possible_mm_struct(mm_offset2, base_addr),*/

    ispointer(MM_offset2),
    MM_offset2 is MM_offset + 8,

    /* comm */
	iscomm(Comm_offset),  
	Comm_offset > Pid_offset,
    Comm_offset < 1000,

    /* struct real_parent  */
	ispointer(Real_parent_offset), 
	Real_parent_offset < Comm_offset,
    Real_parent_offset > Pid_offset.