#include <libserialport.h>
#include <stdio.h>

int main(void) {
    struct sp_port **ports;
    int result = sp_list_ports(&ports);

    if (result != SP_OK) {
        fprintf(stderr, "Error listing serial ports: %d\n", result);
        return 1;
    }

    printf("Available serial ports:\n");
    for (int i = 0; ports[i] != NULL; i++) {
        const char *name = sp_get_port_name(ports[i]);
        printf(" - %s\n", name);
    }

    sp_free_port_list(ports);
    return 0;
}