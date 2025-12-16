### Сборка Doom для ОС Windows с GUI

В этом разделе предполагается, что сборка проекта `doomgeneric` выполняется на устройстве с архитектурой x86-64 под управлением ОС Windows.

Для сборки переносимой версии игры Doom `doomgeneric` с GUI на ОС Windows воспользуемся компилятором gcc, включённым в набор инструментов для разработки MinGW @mingw. Перед началом работы необходимо установить MinGW и добавить путь к папке с компилятором gcc в переменную окружения `PATH`, а также установить СКВ git.

В терминале PowerShell @holmes2012windows при помощи СКВ git сохраним репозиторий с кодом проекта `doomgeneric` на устройство под управлением ОС Windows x86-64:

```powershell
PS C:\> git clone https://github.com/ozkl/doomgeneric.git
PS C:\> cd doomgeneric\doomgeneric
PS C:\doomgeneric\doomgeneric> ls
Length Name
------ ----
 27807 am_map.c
  1243 am_map.h
  2801 config.h
       ...
```

Сценарии сборки в файлах, имена которых начинаются с подстроки `Makefile`, адаптированы для ОС Linux. В связи с этим сборку Doom на ОС Windows выполним при помощи команды компилятора gcc, сформированной вручную на основе содержимого `Makefile`.

Перечень файлов с кодом на языке C для компиляции кроссплатформенного ядра Doom получим из `Makefile`. Дополнительно подключим файл `doomgeneric_win.c`, содержащий реализации платформозависимых функций для ОС Windows -- сборку проекта с `doomgeneric_win.c` необходимо осуществлять с опцией `-lgdi32`, которая указывает компоновщику на необходимость подключения библиотеки GDI32 (Graphics Device Interface).

Сформируем сценарий сборки `build.ps1`, содержащий команду для компиляции переносимой версии Doom, на основе содержимого `Makefile` при помощи набора PowerShell-команд, объединённых оператором конвейера:

```powershell
PS C:\doomgeneric\doomgeneric> Get-Content Makefile | Where-Object { $_ -match 'SRC_DOOM = *' } | ForEach-Object { $_ -replace 'SRC_DOOM = ', '' -replace '\.o', '.c' -replace 'doomgeneric_xlib.c', 'doomgeneric_win.c' } | ForEach-Object { "gcc -o doomgeneric.exe $_ -lgdi32" } | Out-File -FilePath build.ps1
```

PowerShell-команда `Get-Content` построчно читает содержимое файла с именем `Makefile` и передаёт прочитанные строки как объекты платформы .NET на вход команде `Where-Object`, для этого используется оператор конвейера `|`. В отличие от конвейера на Unix-подобных ОС @kisscm, PowerShell-конвейер на ОС Windows передаёт между командами объекты платформы .NET со свойствами и методами вместо обычного текста @holmes2012windows. 

Команда `Where-Object` оставляет в коллекции .NET-объектов на выходе только те строки, которые соответствуют выражению `SRC_DOOM = *`, где символ * соответствует произвольной последовательности символов. Выражение `$_` позволяет получать доступ к очередному объекту на каждой итерации цикла.

После этого команда `ForEach-Object` заменяет в полученной строке `$_` префикс `SRC_DOOM =` на пустую строку, заменяет расширения файлов `.o` на `.c`, заменяет имя файла с платформозависимыми функциями `doomgeneric_xlib.c` на `doomgeneric_win.c`. Сформированная в результате замен строка, содержащая перечень файлов для компиляции на ОС Windows, подставляется в строку с вызовом компилятора gcc с опцией `-lgdi32`, результат подстановки сохраняется в файл `build.ps1` при помощи команды `Out-File` @holmes2012windows. В последней команде `ForEach-Object` используются двойные кавычки для раскрытия значения переменной `$_`.

Выведем содержимое файла `build.ps1` на экран:

```powershell
PS C:\doomgeneric\doomgeneric> Get-Content build.ps1
gcc -o doomgeneric.exe dummy.c am_map.c doomdef.c doomstat.c dstrings.c d_event.c d_items.c d_iwad.c d_loop.c d_main.c d_mode.c d_net.c f_finale.c f_wipe.c g_game.c hu_lib.c hu_stuff.c info.c i_cdmus.c i_endoom.c i_joystick.c i_scale.c i_sound.c i_system.c i_timer.c memio.c m_argv.c m_bbox.c m_cheat.c m_config.c m_controls.c m_fixed.c m_menu.c m_misc.c m_random.c p_ceilng.c p_doors.c p_enemy.c p_floor.c p_inter.c p_lights.c p_map.c p_maputl.c p_mobj.c p_plats.c p_pspr.c p_saveg.c p_setup.c p_sight.c p_spec.c p_switch.c p_telept.c p_tick.c p_user.c r_bsp.c r_data.c r_draw.c r_main.c r_plane.c r_segs.c r_sky.c r_things.c sha1.c sounds.c statdump.c st_lib.c st_stuff.c s_sound.c tables.c v_video.c wi_stuff.c w_checksum.c w_file.c w_main.c w_wad.c z_zone.c w_file_stdc.c i_input.c i_video.c doomgeneric.c doomgeneric_win.c -lgdi32
```

Скомпилируем и запустим Doom на ОС Windows, а для проверки работы Doom воспользуемся файлом с игровыми данными `doom1.wad` @doom1wad:

```powershell
PS C:\doomgeneric\doomgeneric> .\build.ps1
PS C:\doomgeneric\doomgeneric> .\doomgeneric.exe doom1.wad
```

После выполнения команд на ОС Windows откроется окно с GUI игры Doom, показанное на @fig:doomwindows.

![Экран заставки игры Doom на ОС Windows с GUI](./doom-windows.png){#fig:doomwindows width=65%}
