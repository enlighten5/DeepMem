use_module(library(clpfd)).

iscomm(920).
iscomm(1002).
iscomm(2483).
iscomm(2712).
iscomm(2811).
isint(0).
isint(22).
isint(48).
isint(52).
isint(56).
isint(72).
isint(82).
isint(87).
isint(140).
isint(147).
isint(155).
isint(163).
isint(224).
isint(228).
isint(337).
isint(346).
isint(356).
isint(447).
isint(463).
isint(484).
isint(488).
isint(499).
isint(703).
isint(711).
isint(719).
isint(727).
isint(761).
isint(767).
isint(775).
isint(787).
isint(791).
isint(803).
isint(808).
isint(815).
isint(926).
isint(939).
isint(1021).
isint(1201).
isint(1291).
isint(1295).
isint(1302).
isint(1315).
isint(1409).
isint(1416).
isint(1424).
isint(1431).
isint(1440).
isint(1449).
isint(1466).
isint(1474).
isint(1479).
isint(1487).
isint(1591).
isint(1691).
isint(1697).
isint(1705).
isint(1767).
isint(1792).
isint(1814).
isint(1840).
isint(1844).
isint(1848).
isint(1864).
isint(1874).
isint(1879).
isint(1932).
isint(1937).
isint(1947).
isint(1953).
isint(2016).
isint(2020).
isint(2047).
isint(2127).
isint(2137).
isint(2148).
isint(2169).
isint(2176).
isint(2247).
isint(2255).
isint(2276).
isint(2280).
isint(2290).
isint(2393).
isint(2399).
isint(2417).
isint(2423).
isint(2441).
isint(2447).
isint(2465).
isint(2471).
isint(2485).
isint(2551).
isint(2569).
isint(2578).
isint(2585).
isint(2594).
isint(2600).
isint(2716).
isint(2813).
isint(2993).
isint(3083).
isint(3087).
isint(3093).
isint(3105).
isint(3200).
isint(3215).
isint(3279).
isint(3383).
isint(3483).
isint(3489).
isint(3497).
ispointer(8).
ispointer(64).
ispointer(112).
ispointer(120).
ispointer(184).
ispointer(200).
ispointer(208).
ispointer(240).
ispointer(368).
ispointer(376).
ispointer(392).
ispointer(400).
ispointer(408).
ispointer(416).
ispointer(424).
ispointer(432).
ispointer(504).
ispointer(512).
ispointer(520).
ispointer(528).
ispointer(536).
ispointer(544).
ispointer(552).
ispointer(560).
ispointer(568).
ispointer(576).
ispointer(584).
ispointer(600).
ispointer(608).
ispointer(624).
ispointer(632).
ispointer(648).
ispointer(656).
ispointer(664).
ispointer(672).
ispointer(848).
ispointer(856).
ispointer(864).
ispointer(872).
ispointer(880).
ispointer(888).
ispointer(896).
ispointer(904).
ispointer(984).
ispointer(992).
ispointer(1112).
ispointer(1144).
ispointer(1152).
ispointer(1160).
ispointer(1168).
ispointer(1176).
ispointer(1208).
ispointer(1216).
ispointer(1320).
ispointer(1328).
ispointer(1384).
ispointer(1512).
ispointer(1520).
ispointer(1528).
ispointer(1552).
ispointer(1560).
ispointer(1600).
ispointer(1608).
ispointer(1624).
ispointer(1632).
ispointer(1680).
ispointer(1800).
ispointer(1856).
ispointer(1904).
ispointer(1912).
ispointer(1976).
ispointer(1992).
ispointer(2000).
ispointer(2032).
ispointer(2160).
ispointer(2184).
ispointer(2192).
ispointer(2200).
ispointer(2208).
ispointer(2296).
ispointer(2304).
ispointer(2312).
ispointer(2320).
ispointer(2328).
ispointer(2336).
ispointer(2344).
ispointer(2352).
ispointer(2360).
ispointer(2368).
ispointer(2376).
ispointer(2408).
ispointer(2432).
ispointer(2456).
ispointer(2640).
ispointer(2648).
ispointer(2656).
ispointer(2664).
ispointer(2672).
ispointer(2680).
ispointer(2776).
ispointer(2784).
ispointer(2960).
ispointer(3000).
ispointer(3008).
ispointer(3112).
ispointer(3120).
ispointer(3304).
ispointer(3312).
ispointer(3320).
ispointer(3344).
ispointer(3352).
ispointer(3392).
ispointer(3400).
ispointer(3416).
ispointer(3424).
ispointer(3448).
ispointer(3456).

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