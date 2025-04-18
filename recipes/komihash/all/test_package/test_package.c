#include <stdio.h>
#include <komihash.h>

int main(void)
{
    const char s1[] = "This is a test of komihash.";
    const char s2[] = "7 chars";

    printf( "%016llx\n", komihash( s1, strlen( s1 ), 0 )); // 5b13177fc68b4f96
    printf( "%016llx\n", komihash( s2, strlen( s2 ), 0 )); // 2c514f6e5dcb11cb

    return 0;
}