#include <stdio.h>
#include <string.h>

int fun(char argv[]){
	char buff[512];
	printf("Welcome\n");
	strcpy(buff, argv);
	printf("%ld\n",strlen(buff));
	puts(buff);
	return 0;
}

int main(int argc, char **argv){
	fun(argv[1]);
	return 0;
}
