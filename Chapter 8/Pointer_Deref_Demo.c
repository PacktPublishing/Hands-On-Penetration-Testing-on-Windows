#include <stdio.h>
int main(int argc, char **argv)
{
    int x = 10;
    int *point = &x;
    int deref = *point;
    printf("\nVariable x is currently %d. *point is %d.\n\n", x, deref);
    *point = 20;
    int dereftwo = *point;
    printf("After assigning 20 to the address referenced by point, *point is now %d.\n\n", dereftwo);
    printf("x is now %d.\n\n", x);
}
