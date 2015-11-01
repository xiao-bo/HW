#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<string.h>
#include<unistd.h>
pthread_t tid[2];

void *tid1_fun(){
	//unsigned long i =0;
	int i=0;
	pthread_t id = pthread_self();
	for(i=0;i<3;i++){
		if(pthread_equal(id,tid[0])){
			printf("thread 1 say : running\n");
		}else{

			printf("thread 2 say : running\n");
		}
	}

}
void *tid2_fun(){
	//unsigned long i =0;
	//pthread_t id = pthread_self();
	int i=0;
	for(i=0;i<3;i++){
		printf("thread 2 say : running\n");
	}
}

int main(int argc, char *argv[]){
	//printf("test %s\n",argv[1]);
	
	int i=0;
	int err;
	
	//while (i<2){
		err=pthread_create(&(tid[0]),NULL,&tid1_fun,NULL);
		if(err!=0){
			printf("\n can not create thread :[%s]",strerror(err));
		}else{
			printf("\n successfully create thread 1\n");
		}
		
		err=pthread_create(&(tid[1]),NULL,&tid2_fun,NULL);
		if(err!=0){
			printf("\n can not create thread :[%s]",strerror(err));
		}else{
			printf("\n successfully create thread 2\n");
		}
	//	i++;
	//sleep(1);
	
	sleep(1);
	return 0;

}
