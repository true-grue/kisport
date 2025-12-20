### Адаптация Doom для ОС Windows с TUI

В этом разделе предполагается, что отладка и тестирование кода ведётся на устройстве под управлением ОС Windows x86-64.

Попробуем запустить реализованную в предыдущем разделе версию игры Doom с поддержкой вывода графики в терминал в виде ASCII-символов на ОС Windows.

Для этого в терминале PowerShell @holmes2012windows переместимся в загруженный ранее репозиторий с кодом переносимой версии игры Doom `doomgeneric` @doomgeneric, в папку `doomgeneric`. После этого создадим новый файл `doomgeneric_tty.c` и на основе созданного ранее сценария сборки Doom с GUI для ОС Windows `build.ps1` создадим новый сценарий `build-term.ps1` для сборки Doom с TUI для ОС Windows:

```powershell
PS C:\doomgeneric\doomgeneric> New-Item doomgeneric_tty.c
PS C:\doomgeneric\doomgeneric> Get-Content build.ps1 | ForEach-Object { $_ -replace 'doomgeneric_win.c', 'doomgeneric_tty.c' } | Out-File -FilePath build-term.ps1
```

Содержимое файла `build-term.ps1` отличается от содержимого файла `build.ps1` тем, что подстрока с именем файла платформы с GUI `doomgeneric_win.c` в нём заменена подстрокой с именем файла платформы с TUI `doomgeneric_tty.c`.

Поместим в созданный файл `doomgeneric_tty.c` функции, перечисленные в @tbl:funcs и реализованные в предыдущем разделе для ОС Ubuntu Linux x86-64:

```c
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include "doomgeneric.h"

void DG_Init() { printf("Doom launched!\n"); }
void DG_SleepMs(uint32_t ms) {}
void DG_SetWindowTitle(const char *title) {}
 int DG_GetKey(int *pressed, unsigned char *key) { return 0; }

void DG_DrawFrame() {
    printf("\033[1;1H");
    for (int y = 0; y < DOOMGENERIC_RESY; y += 5) {
        for (int x = 0; x < DOOMGENERIC_RESX; x += 3) {
            int i = y * DOOMGENERIC_RESX + x;
            uint32_t pixel = DG_ScreenBuffer[i];
            unsigned char r = (pixel >> 16) & 255;
            unsigned char g = (pixel >>  8) & 255;
            unsigned char b = (pixel >>  0) & 255;
            float lum = (0.2126f * r + 0.7152f * g + 0.0722f * b) / 255;
            char *chars = " .:-+=*0#";
            int index = (int) (lum * sizeof(chars));
            printf("%c", chars[index]);
        }
        printf("\n");
    }
}

uint32_t DG_GetTicksMs() {
    static uint32_t counter = 0;
    usleep(1000);
    return counter++;
}

int main(int argc, char **argv) {
    doomgeneric_Create(argc, argv);
    while (1) doomgeneric_Tick();
    return 0;
}
```

Выполним сборку проекта и запустим Doom в PowerShell-терминале:

```powershell
PS C:\doomgeneric\doomgeneric> .\build-term.ps1
PS C:\doomgeneric\doomgeneric> .\doomgeneric.exe doom1.wad
```

После запуска программы в терминал будут выведены кадры, сформированные функцией `DG_DrawFrame`, показанные на @fig:doomslideshow.

![ASCII-графика экрана заставки игры Doom в терминале ОС Windows без поддержки управляющих последовательностей ANSI](./doom-slideshow.png){#fig:doomslideshow width=50%}

По умолчанию в некоторых версиях Windows отключены управляющие последовательности ANSI, из-за чего выполнение инструкции `printf("\033[1;1H")`, перемещающей курсор в левый верхний угол экрана, не приведёт к ожидаемому результату. Вместо перемещения курсора управляющая последовательность будет выведена на экран как обычный текст. В результате в терминал кадры будут выводиться последовательно, как показано на @fig:doomslideshow.

Для включения поддержки управляющих последовательностей ANSI на ОС Windows воспользуемся Windows-специфичными функциями `GetStdHandle`, `GetConsoleMode` и `SetConsoleMode`.

В функции инициализации `DG_Init` (см. @tbl:funcs) в файле `doomgeneric_tty.c` получим дескриптор `HANDLE` для стандартного вывода при помощи функции `GetStdHandle`, после чего получим текущие настройки консоли -- для этого применим функцию `GetConsoleMode`. Добавим к настройкам консоли `dwMode` флаг `ENABLE_VIRTUAL_TERMINAL_PROCESSING` и сохраним настройки функцией `SetConsoleMode`:

```c
#ifdef _WIN32
#include <windows.h>
#endif

void DG_Init() {
#ifdef _WIN32
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwMode;
    GetConsoleMode(handle, &dwMode);
    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
    SetConsoleMode(handle, dwMode);
#endif
}
```

Для использования функций `GetStdHandle`, `GetConsoleMode`, `SetConsoleMode` необходимо подключить заголовочный файл `windows.h`. Этот заголовочный файл доступен только на ОС Windows и содержит специфичные для ОС Windows сигнатуры функций и типы данных.

В связи с этим для обеспечения переносимости реализации ASCII-графики Doom в файле `doomgeneric_tty.c` воспользуемся директивой компилятора `#ifdef` для проверки, компилируется ли программа для ОС Windows -- в случае, если константа `_WIN32` не определена, компилятор удалит добавленный нами Windows-специфичный код внутри директив `#ifdef`, и код в файле `doomgeneric_tty.c` продолжит работать на ОС Linux без изменений.

Скомпилируем и запустим обновлённую версию Doom:

```powershell
PS C:\doomgeneric\doomgeneric> .\build-term.ps1
PS C:\doomgeneric\doomgeneric> .\doomgeneric.exe doom1.wad
```

После включения управляющих последовательностей ANSI поведение программы на ОС Windows (см. @fig:doomwindowsascii) совпадает с поведением на ОС Linux (см. @fig:doomascii) в части формата вывода графики.

![ASCII-графика экрана заставки игры Doom в терминале ОС Windows](./doom-windows-ascii.png){#fig:doomwindowsascii width=65%}

Однако, частота смены кадров терминальной версии Doom на ОС Windows существенно ниже частоты смены кадров на ОС Linux -- из-за различий в деталях реализации консольного вывода посимвольный вывод, интенсивно используемый для отрисовки графики в виде ASCII-символов в терминале, работает намного медленнее на ОС Windows по сравнению с ОС Linux.

Для устранения этого различия исправим функцию `DG_DrawFrame` -- вместо вызова функции `printf` для каждого выводимого символа в обновлённой функции `DG_DrawFrame` будем сохранять в массив `line` все символы очередной строки, которую необходимо вывести на экран, после чего выведем сформированную строку `line` при помощи вызова стандартной функции `puts`. Кроме того, переместим задержку из функции `DG_GetTicksMs` в функцию `DG_DrawFrame`:

```c
void DG_DrawFrame() {
    char line[DOOMGENERIC_RESX];
    printf("\033[1;1H");
    for (int y = 0; y < DOOMGENERIC_RESY; y += 5) {
        int pos = 0;
        for (int x = 0; x < DOOMGENERIC_RESX; x += 3) {
            int i = y * DOOMGENERIC_RESX + x;
            uint32_t pixel = DG_ScreenBuffer[i];
            unsigned char r = (pixel >> 16) & 255;
            unsigned char g = (pixel >>  8) & 255;
            unsigned char b = (pixel >>  0) & 255;
            float lum = (0.2126f * r + 0.7152f * g + 0.0722f * b) / 255;
            char *chars = " .:-+=*0#";
            int index = (int) (lum * sizeof(chars));
            line[pos++] = chars[index];
        }
        line[pos] = 0;
        puts(line);
    }
    usleep(1000);
}

uint32_t DG_GetTicksMs() {
    static uint32_t counter = 0;
    return counter++;
}
```

Скомпилируем и запустим Doom с исправленными функциями:

```powershell
PS C:\doomgeneric\doomgeneric> .\build-term.ps1
PS C:\doomgeneric\doomgeneric> .\doomgeneric.exe doom1.wad
```

Обновлённая версия Doom теперь характеризуется приемлемой частотой смены кадров -- приветственная анимация игрового процесса, один из кадров которой показан на @fig:doomanimate, теперь выводится на экран плавно.

![Кадр из приветственной анимации игры Doom на ОС Windows с TUI](./doom-animate.png){#fig:doomanimate width=65%}
