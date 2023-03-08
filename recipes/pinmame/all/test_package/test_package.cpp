#include <libpinmame.h>
#include <stdio.h>

void CALLBACK Game(PinmameGame *game) {
  printf("Game(): name=%s, description=%s, manufacturer=%s, year=%s, "
         "flags=%lu, found=%d\n",
         game->name, game->description, game->manufacturer, game->year,
         (unsigned long)game->flags, game->found);
}

int main(int argc, char *argv[]) {
  PinmameConfig config = {AUDIO_FORMAT_FLOAT,
                          44100,
                          "",
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0,
                          0};
  PinmameSetConfig(&config);

  PinmameSetHandleKeyboard(0);
  PinmameSetHandleMechanics(0);

  PinmameGetGames(&Game);
  return 0;
}
