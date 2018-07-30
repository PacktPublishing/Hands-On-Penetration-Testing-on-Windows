#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char **argv) {
 printf("\nBuffer Copier v1.0\n");
 char buff[1024];
 if(argc != 2) {
 printf("\nUsage: %s <data to be stored in buffer>\n", argv[0]);
 system("echo Exiting");
 exit(0);
 }
 else {
 strcpy(buff, argv[1]);
 printf("Buffer: %s\n", buff);
 system("echo Data received.");
 return 0;
 }
}
