CC = gcc

compile:
	$(CC) main.c \
	helpers/helperString.c \
	helpers/helperInput.c \
	-o init

test:
	$(CC) main.c \
	helpers/helperGUI.c \
	-o init

gui:
	$(CC) main.c helpers/helperGUI.c helpers/helperLayout.c helpers/helperWidgets.c -o guiApp `sdl2-config --cflags --libs` -lSDL2_ttf