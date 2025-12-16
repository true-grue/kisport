### Сборка Doom для веб-браузера с GUI

В этом разделе предполагается, что сборка проекта `doomgeneric` выполняется на устройстве с архитектурой x86-64 под управлением ОС Windows. Переместимся на ОС Windows x86-64 в загруженный ранее репозиторий с кодом переносимой версии игры Doom `doomgeneric` @doomgeneric, в папку `doomgeneric`.

Репозиторий переносимой версии Doom `doomgeneric`, помимо версии Doom для ОС Linux `doomgeneric_xlib.c` и версии Doom для ОС Windows `doomgeneric_win.c`, содержит кроссплатформенную реализацию вывода графики и звука на основе библиотеки SDL2 @sdl2 -- 2-й версии библиотеки SDL. Код реализации SDL-компонентов Doom приведён в файле `doomgeneric_sdl.c`.

Кроссплатформенное приложение с GUI, написанное на SDL2, легко адаптировать для работы в веб-браузере, скомпилировав код на языке C при помощи компилятора Emscripten @emcc с рядом незначительных исправлений. Код SDL-версии Doom, адаптированной для совместимости с компилятором Emscripten, приведён в файле `doomgeneric_emscripten.c`, содержащемся в репозитории.

Сравним стандартно оформленное содержимое файлов `doomgeneric_sdl.c` и `doomgeneric_emscripten.c` при помощи утилиты diff @kisscmump, использующейся в СКВ git. Опция `--no-index` команды `git diff` позволяет найти различия между двумя указанными файлами:

```diff
PS C:\doomgeneric\doomgeneric> git diff --no-index doomgeneric_sdl.c doomgeneric_emscripten.c
diff --git a/doomgeneric_sdl.c b/doomgeneric_emscripten.c
index ee556a2..4f93459 100644
--- a/doomgeneric_sdl.c
+++ b/doomgeneric_emscripten.c
@@ -1,4 +1,4 @@
-//doomgeneric for cross-platform development library 'Simple DirectMedia Layer'
+//doomgeneric emscripten port
 
 #include "doomkeys.h"
 #include "m_argv.h"
@@ -9,6 +9,7 @@
 
 #include <stdbool.h>
 #include <SDL.h>
+#include <emscripten.h>
 
 SDL_Window* window = NULL;
 SDL_Renderer* renderer = NULL;
@@ -196,8 +197,6 @@ void DG_SetWindowTitle(const char * title)
 
 int main(int argc, char **argv) {
     doomgeneric_Create(argc, argv);
-    for (int i = 0; ; i++) {
-        doomgeneric_Tick();
-    }
+    emscripten_set_main_loop(doomgeneric_Tick, 0, 1);
     return 0;
 }
```

В выводе команды `git diff` добавленные строки обозначены символом «+», а удалённые строки обозначены символом «-».

Из вывода команды `git diff` следует, что для преобразования SDL-версии Doom `doomgeneric_sdl.c` в SDL-версию Doom для Emscripten `doomgeneric_emscripten.c` главный цикл программы в функции `main` был реализован при помощи функции `emscripten_set_main_loop` вместо обычного цикла, а для использования этой функции был подключён заголовочный файл `emscripten.h`.

Сформируем сценарий сборки `emcc-build.ps1` для PowerShell @holmes2012windows, содержащий команду для сборки SDL-версии Doom для веб-браузеров при помощи компилятора `emcc`. Перечень файлов с кодом на языке C для компиляции кроссплатформенного ядра Doom получим из `Makefile`, как в предыдущем разделе. Дополнительно подключим файл `doomgeneric_emscripten.c`, содержащий реализации платформозависимых функций для SDL и Emscripten:

```powershell
PS C:\doomgeneric\doomgeneric> Get-Content Makefile | Where-Object { $_ -match 'SRC_DOOM = *' } | ForEach-Object { $_ -replace 'SRC_DOOM = ', '' -replace '\.o', '.c' -replace 'doomgeneric_xlib.c', 'doomgeneric_emscripten.c' } | ForEach-Object { "emcc $_ -o index.html --preload-file doom1.wad -s USE_SDL=2" } | Out-File -FilePath emcc-build.ps1
```

PowerShell-команды `Get-Content`, `Where-Object`, `ForEach-Object` и `Out-File` рассматривались в разделе 1.3.2. Выведем полученное в результате выполнения PowerShell-команд содержимое сценария сборки `emcc-build.ps1` на экран при помощи команды `Get-Content`:

```powershell
PS C:\doomgeneric\doomgeneric> Get-Content emcc-build.ps1
emcc dummy.c am_map.c doomdef.c doomstat.c dstrings.c d_event.c d_items.c d_iwad.c d_loop.c d_main.c d_mode.c d_net.c f_finale.c f_wipe.c g_game.c hu_lib.c hu_stuff.c info.c i_cdmus.c i_endoom.c i_joystick.c i_scale.c i_sound.c i_system.c i_timer.c memio.c m_argv.c m_bbox.c m_cheat.c m_config.c m_controls.c m_fixed.c m_menu.c m_misc.c m_random.c p_ceilng.c p_doors.c p_enemy.c p_floor.c p_inter.c p_lights.c p_map.c p_maputl.c p_mobj.c p_plats.c p_pspr.c p_saveg.c p_setup.c p_sight.c p_spec.c p_switch.c p_telept.c p_tick.c p_user.c r_bsp.c r_data.c r_draw.c r_main.c r_plane.c r_segs.c r_sky.c r_things.c sha1.c sounds.c statdump.c st_lib.c st_stuff.c s_sound.c tables.c v_video.c wi_stuff.c w_checksum.c w_file.c w_main.c w_wad.c z_zone.c w_file_stdc.c i_input.c i_video.c doomgeneric.c doomgeneric_emscripten.c -o index.html --preload-file doom1.wad -s USE_SDL=2
```

Опция `-o` компилятора `emcc` позволяет задать имя HTML-файла с результатом сборки, опция `--preload-file` позволяет упаковать файл с заданным именем в виртуальную файловую систему для использования веб-приложением, а значение `USE_SDL=2` опции `-s` указывает Emscripten на необходимость подключения к компилируемому приложению библиотеки SDL2 @sdl2.

Переместимся в папку с установленным компилятором Emscripten @emcc версии 4.0.8, процесс установки которого из git-репозитория рассматривался в разделе 1.2.2, после чего воспользуемся PowerShell-сценарием `emsdk.ps1` для активации окружения с компилятором `emcc`:

```powershell
PS C:\doomgeneric\doomgeneric> cd ..\..\emsdk\
PS C:\emsdk> .\emsdk.ps1 activate latest
Resolving SDK alias 'latest' to '4.0.8'
Resolving SDK version '4.0.8' to 'sdk-releases-56f86607aeb458086e72f23188789be2ee0e971a-64bit'
Setting the following tools as active:
   node-20.18.0-64bit
   python-3.9.2-nuget-64bit
   releases-56f86607aeb458086e72f23188789be2ee0e971a-64bit
PS C:\emsdk> emcc --version
emcc (Emscripten gcc/clang-like replacement + linker emulating GNU ld) 4.0.8
Copyright (C) 2025 the Emscripten authors (see AUTHORS.txt)
This is free and open source software under the MIT license.
```

Вернёмся в репозиторий `doomgeneric` и выполним сборку проекта при помощи созданного ранее PowerShell-сценария сборки с именем `emcc-build.ps1`:

```powershell
PS C:\emsdk> cd ..\doomgeneric\doomgeneric\
PS C:\doomgeneric\doomgeneric> .\emcc-build.ps1
ports:INFO: retrieving port: sdl2 from https://github.com/libsdl-org/SDL/archive/release-2.32.0.zip
ports:INFO: unpacking port: sdl2
cache:INFO: generating port: sysroot\lib\wasm32-emscripten\libSDL2.a...
system_libs:INFO: compiled 118 inputs in 19.77s
cache:INFO: - ok
```

В результате сборки в рабочей директории будет создан файл `index.html` и ряд вспомогательных файлов. Запустим стандартный веб-сервер на языке Python, используя порт 8000:

```powershell
PS C:\> python -m http.server 8000
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

Открыв в веб-браузере страницу по адресу `http://127.0.0.1:8000` увидим экран заставки игры Doom и логотип проекта Emscripten (см. @fig:doomweb).

![Экран заставки игры Doom в веб-браузере](./doom-web.png){#fig:doomweb width=65%}
