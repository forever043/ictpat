delete from patmgr_patentstate;
insert into patmgr_patentstate (name, sort, disabled) values ('审核中', 1, 0);
insert into patmgr_patentstate (name, sort, disabled) values ('授权', 2, 0);
insert into patmgr_patentstate (name, sort, disabled) values ('撤回', 3, 0);
