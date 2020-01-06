possible_pid(pid_offset, base_addr) :- 
/* the next one is pid_t tgid */
	isint(tgid_offset, base_addr),
	tgid_offset is pid_offset + 4,	

    /* for void* stack
    ispointer(stack_offset, base_addr), 
	stack_offset < pid_offset,*/

    /* for struct mm_struct mm */
	/*possible_mm_struct(mm_offset, base_addr),*/
    ispointer(mm_offset, base_addr)
    mm_offset < tgid_offset,
    /*possible_mm_struct(mm_offset2, base_addr),*/
    ispointer(mm_offset2, base_addr)
    mm_offset2 is mm_offset + 8,

    /* comm */
	isstring(comm_offset, base_addr),  
	comm_offset > pid_offset,

	/* struct real_parent 
	possible_ts_struct(real_parent_offset, base_addr), 
	real_parent_offset < comm_offset, */

	/* struct group_leader 
	possible_ts_struct(group_leader_offset, base_addr), 
	group_leader_offset > real_parent_offset,*/

    /* for struct list_head task 
	possible_list_head(task_offset, base_addr), 
	task_offset < mm_offset,*/

    /* for thread_group
	possible_list_head(thread_group_offset, base_addr), 
	thread_group_offset > group_leader_offset,
	thread_group_offset < comm_offset. */
	

possible_mm_struct(mm_offset, base_addr) :- 
	ispointer(mmap_offset, base_addr),
	mmap_offset < size_of_mm.

