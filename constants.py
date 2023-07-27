
DEFAUT_RESOLUTION = "1080p"

RESOLUTIONS = {"1080p": dict(size=(1920, 1080),
                             crops=[(0, 0, 36, 36), (36, 0, 72, 36), (72, 0, 108, 36)],
                             region=(0, 58, 112, 36)),

               "1440p": dict(size=(2560, 1440),
                             crops=[(0, 0, 50, 50), (50, 0, 100, 50), (100, 0, 150, 50)],
                             region=(0, 77, 200, 50)),
              }
