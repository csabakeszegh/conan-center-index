#include <SDL3/SDL.h>
#include <SDL3_mixer/SDL_mixer.h>

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    SDL_AudioSpec spec = { MIX_DEFAULT_CHANNELS, MIX_DEFAULT_FORMAT, MIX_DEFAULT_FREQUENCY };

    const int version = Mix_Version();
    printf("SDL3_mixer version: %d.%d.%d\n",
        SDL_VERSIONNUM_MAJOR(version),
        SDL_VERSIONNUM_MINOR(version),
        SDL_VERSIONNUM_MICRO(version));

    if (SDL_Init(SDL_INIT_AUDIO) == 0) {
        int initted = Mix_Init(MIX_INIT_FLAC | MIX_INIT_MOD | MIX_INIT_MP3 | MIX_INIT_OGG | MIX_INIT_MID | MIX_INIT_OPUS);
        printf("%s %s\n", "Supported MIX_INIT_MOD: " , (initted & MIX_INIT_MOD  ? "Yes" : "No"));
        printf("%s %s\n", "Supported MIX_INIT_MP3: " , (initted & MIX_INIT_MP3  ? "Yes" : "No"));
        printf("%s %s\n", "Supported MIX_INIT_OGG: " , (initted & MIX_INIT_OGG  ? "Yes" : "No"));
        printf("%s %s\n", "Supported MIX_INIT_FLAC: ", (initted & MIX_INIT_FLAC ? "Yes" : "No"));
        printf("%s %s\n", "Supported MIX_INIT_MID: " , (initted & MIX_INIT_MID  ? "Yes" : "No"));
        printf("%s %s\n", "Supported MIX_INIT_OPUS: ", (initted & MIX_INIT_OPUS ? "Yes" : "No"));

        if (Mix_OpenAudio(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &spec) == 0) {
            int num_chunk_decoders = Mix_GetNumChunkDecoders();
            int num_music_decoders = Mix_GetNumMusicDecoders();
            int i = 0;
            printf("%s\n", "chunk decoders:");
            for (i = 0; i < num_chunk_decoders; ++i)
                printf("\t%s\n", Mix_GetChunkDecoder(i));
            printf("%s\n", "music decoders:");
            for (i = 0; i < num_music_decoders; ++i)
                printf("\t%s\n", Mix_GetMusicDecoder(i));
            Mix_CloseAudio();
            Mix_Quit();
        }
    }

    return 0;
}
