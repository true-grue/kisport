### Кроссплатформенный сценарий сборки для Doom с TUI

Полученная в предыдущем разделе реализация ASCII-графики Doom для платформ с терминалом `doomgeneric_tty.c` отличается кроссплатформенностью -- рассмотренные реализации платформозависимых функций (см. @tbl:funcs) в файле `doomgeneric_tty.c` позволяют обеспечить корректную работу игры Doom как в терминалах на ОС Linux, так и в терминалах на ОС Windows.

Кроссплатформенность `doomgeneric_tty.c` достигается за счёт использования директивы компилятора `#ifdef` для включения специфичного для Windows кода только на ОС Windows, а также за счёт ускоренного построчного вывода на экран изображения, состоящего из символов, функцией `puts` вместо посимвольного вывода изображения функцией `printf`, медленного на ОС Windows.

Однако, сборка проекта Doom для платформ с терминалом из файлов с исходным кодом выполнялась зависящим от целевой ОС способом -- так, на ОС Linux использовалась система сборки GNU Make и адаптированный для ОС Linux файл `Makefile.tty`, созданный при помощи команд в терминале с языком оболочки Bash, а на ОС Windows использовался сценарий сборки `build.ps1`, созданный при помощи команд PowerShell @holmes2012windows.

Для реализации сценария сборки, совместимого и с ОС Windows, и с ОС Linux, воспользуемся кроссплатформенной системой сборки GNU Make @kisscm. В папке с исходным кодом `doomgeneric` и с файлом `doomgeneric_tty.c` создадим файл `Makefile.tty` со следующим содержимым:

```makefile
CC = gcc -std=gnu99
OBJS = dummy.o am_map.o doomdef.o doomstat.o dstrings.o d_event.o d_items.o d_iwad.o d_loop.o d_main.o d_mode.o d_net.o f_finale.o f_wipe.o g_game.o hu_lib.o hu_stuff.o info.o i_cdmus.o i_endoom.o i_joystick.o i_scale.o i_sound.o i_system.o i_timer.o memio.o m_argv.o m_bbox.o m_cheat.o m_config.o m_controls.o m_fixed.o m_menu.o m_misc.o m_random.o p_ceilng.o p_doors.o p_enemy.o p_floor.o p_inter.o p_lights.o p_map.o p_maputl.o p_mobj.o p_plats.o p_pspr.o p_saveg.o p_setup.o p_sight.o p_spec.o p_switch.o p_telept.o p_tick.o p_user.o r_bsp.o r_data.o r_draw.o r_main.o r_plane.o r_segs.o r_sky.o r_things.o sha1.o sounds.o statdump.o st_lib.o st_stuff.o s_sound.o tables.o v_video.o wi_stuff.o w_checksum.o w_file.o w_main.o w_wad.o z_zone.o w_file_stdc.o i_input.o i_video.o doomgeneric.o doomgeneric_tty.o

%.o: %.c
	$(CC) -c $< -o $@

doom.exe: $(OBJS)
	$(CC) $(OBJS) -o doom.exe

clean:
ifeq ($(OS), Windows_NT)
    if exist *.o del /q *.o
else
    rm -f *.o
endif
```

В переменную `CC` поместим имя компилятора `gcc` с опцией `-std=gnu99`, указывающей на необходимость использования стандарта C99 и нестандартных GNU-расширений при компиляции Doom. В переменную `OBJS` поместим перечень файлов с расширением `.o`, полученный из файла с именем `Makefile`, уже присутствовавшего в репозитории `doomgeneric`.

За переменными в `Makefile.tty` следуют 2 цели сборки.

Первая цель сборки `%.o: %.c` описывает правило преобразования файлов с кодом на языке C в объектные файлы с расширением `.o`. При этом для сборки любого `.o`-файла требуется наличие на диске `.c`-файла с тем же именем. Например, для успешного выполнения цели `doomgeneric_tty.o`, которая может быть запущена командой `make -f Makefile.tty doomgeneric_tty.o`, требуется наличие на диске файла `doomgeneric_tty.c`.

Выражение `$(CC)` позволяет подставить в сборочную команду значение переменной `CC`, а выражение `$<` позволяет получить имя первой зависимости `%.c` цели `%.o` -- то есть, имя конкретного файла с расширением `.c`. Выражение `$@`, в свою очередь, позволяет получить имя цели `%.o` -- то есть, имя конкретного файла с расширением `.o`.

Таким образом, в результате выполнения команды `make -f Makefile.tty doomgeneric_tty.o` выражение `$(CC) -c $< -o $@` преобразуется в команду `gcc -std=gnu99 -c doomgeneric_tty.c -o doomgeneric_tty.o`, после чего команда выполнится.

Вторая цель сборки `doom.exe: $(OBJS)` зависит от всех файлов с расширением `.o`, перечисленных в переменной `OBJS`. Перед выполнением цели `doom.exe` GNU Make выполнит цель `%.o: %.c` для каждого файла из `OBJS`, и в результате на диске будут созданы все объектные файлы, перечисленные в `OBJS`, из соответствующих им файлов с кодом на языке C. В результате выполнения цели `doom.exe` на диске будет создан исполняемый файл с именем `doom.exe` путём компоновки всех объектных файлов из `OBJS`.

Для удаления с диска артефактов сборки с расширениями `.o` в конец файла с именем `Makefile.tty` добавлена цель `clean`. На ОС Linux для удаления объектных файлов используется команда `rm`, а на ОС Windows -- команда `del`:

Проверим работу `Makefile.tty` на ОС Windows x86-64:

```powershell
PS C:\doomgeneric\doomgeneric> make -f Makefile.tty
gcc -std=gnu99 -c dummy.c -o dummy.o
gcc -std=gnu99 -c am_map.c -o am_map.o
gcc -std=gnu99 -c doomdef.c -o doomdef.o
...
PS C:\doomgeneric\doomgeneric> .\doom.exe doom1.wad
```

Проверим работу `Makefile.tty` на ОС Ubuntu Linux x86-64:

```bash
~/doomgeneric/doomgeneric$ make -f Makefile.tty
gcc -std=gnu99 -c dummy.c -o dummy.o
gcc -std=gnu99 -c am_map.c -o am_map.o
gcc -std=gnu99 -c doomdef.c -o doomdef.o
...
~/doomgeneric/doomgeneric$ ./doom.exe doom1.wad
```

При помощи кроссплатформенной реализации ASCII-графики для Doom `doomgeneric_tty.c` и кроссплатформенного сценария сборки `Makefile.tty` становится возможным собрать и запустить игру в рамках одной SSH-сессии, как показано на @fig:ssh.

![Кадр из приветственной анимации игры Doom в SSH-сессии](./ssh.png){#fig:ssh width=65%}

Для лучшего визуального эффекта необходимо уменьшить размер выводимых в терминал символов до минимально возможного при помощи сочетания клавиш `Ctrl` и `-` после запуска программы в SSH-сессии, открытой в терминале на ОС Windows.
