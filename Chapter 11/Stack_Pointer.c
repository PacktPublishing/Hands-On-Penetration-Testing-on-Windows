#include <stdio.h>
void main() {
   register int esp asm("esp");
   printf("ESP is %#010x\n", esp);
}
