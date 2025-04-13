#define SDL_MAIN_HANDLED
#include "SDL_image.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int version = IMG_Version();
    printf("SDL3_image compile version: %d.%d.%d\n",
        SDL_IMAGE_MAJOR_VERSION, SDL_IMAGE_MINOR_VERSION, SDL_IMAGE_MICRO_VERSION);
    printf("SDL3_image link version: %d.%d.%d\n",
        SDL_VERSIONNUM_MAJOR(version), SDL_VERSIONNUM_MINOR(version), SDL_VERSIONNUM_MICRO(version));
    return EXIT_SUCCESS;
}
