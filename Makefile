## make

all:sched_test.c
	gcc sched_test.c -lpthread -o sched_test 

clean: 
	rm -f sched_test
