### Адаптация Doom для ОС Linux с TUI

В этом разделе предполагается, что отладка и тестирование кода ведётся на устройстве под управлением ОС Ubuntu Linux x86-64.

Написанную в переносимом стиле программу с GUI несложно адаптировать для вывода графики в консоль. Приложение командной строки, или CLI-приложение (Command Line Interface, CLI), использующее терминал для вывода графики, позволяет обеспечить поддержку не только распространённых ОС, таких как Windows, Linux или MacOS, но и серверных ОС без поддержки GUI, а также устройств, обладающих ограниченными вычислительными ресурсами, сессий протокола SSH (Secure Shell Protocol).

Более того, передача GUI с использованием протокола удаленного доступа к рабочему столу (Remote Desktop Protocol, RDP), например, протокола RBF (Remote FrameBuffer), требует высокой пропускной способности канала связи, в то время как передача простого текста по протоколу SSH таких ограничений на канал связи не накладывает.

Рассмотрим процесс портирования программы с GUI на новую платформу с TUI (Text-based User Interface) на примере версии игры Doom `doomgeneric` @doomgeneric с улучшенной переносимостью.

Для добавления поддержки новой платформы для `doomgeneric` необходимо реализовать всего 6 платформозависимых функций, названия которых приведены в файле с документацией по проекту `README.md` и в @tbl:funcs. 

```{=html}
<table id="Функции, которые следует реализовать для портирования doomgeneric {#tbl:funcs}">
<tr>
<th align="left">Функция</th>
<th align="left">Описание</th>
</tr>
<tr>
<td align="left">DG_Init</td>
<td align="left">Инициализация платформозависимых функций.</td>
</tr>
<tr>
<td>DG_DrawFrame</td>
<td>Вывод кадрового буфера `DG_ScreenBuffer` на экран.</td>
</tr>
<tr>
<td>DG_SleepMs</td>
<td>Задержка в миллисекундах.</td>
</tr>
<tr>
<td>DG_GetTicksMs</td>
<td>Время в миллисекундах.</td>
</tr>
<tr>
<td>DG_GetKey</td>
<td>Обработка нажатий клавиатуры.</td>
</tr>
<tr>
<td>DG_SetWindowTitle</td>
<td>Обновление заголовка окна.</td>
</tr>
</table>
```

Адаптируем игру для поддержки вывода ASCII-графики в терминал, реализовав TUI для Doom вместо GUI.

Для портирования Doom с GUI на новую платформу -- терминал с выводом графики в виде ASCII-символов -- переместимся на ОС Ubuntu Linux в загруженный ранее репозиторий с кодом переносимой версии игры Doom `doomgeneric` @doomgeneric, в папку `doomgeneric`.

Создадим новый файл `doomgeneric_tty.c` при помощи команды `touch`. Также создадим новый сценарий сборки на основе напечатанного командой `cat` в стандартный вывод содержимого файла `Makefile`. Заменим в стандартном выводе `cat` при помощи утилиты `sed` подстроку с именем объектного файла `doomgeneric_xlib.o` на подстроку с именем нового объектного файла `doomgeneric_tty.o`, этот файл будет создан в процессе компиляции файла с исходным кодом `doomgeneric_tty.c`. Для перенаправления стандартного вывода утилиты `cat` в стандартный ввод утилиты `sed` воспользуемся оператором конвейера Unix `|` @kisscm, а для перенаправления вывода утилиты `sed` в файл с именем `Makefile.tty` воспользуемся оператором `>`:

```bash
~/doomgeneric/doomgeneric$ touch doomgeneric_tty.c
~/doomgeneric/doomgeneric$ cat Makefile | sed s/doomgeneric_xlib.o/doomgeneric_tty.o/ | sed s/-lX11// > Makefile.tty
```

Запустим сборку проекта, используя созданный сценарий `Makefile.tty`:

```bash
~/doomgeneric/doomgeneric$ make -f Makefile.tty
mkdir -p build
[Compiling dummy.c]
[Compiling am_map.c]
[Compiling doomdef.c]
...
(.text+0x24): undefined reference to `main'
collect2: error: ld returned 1 exit status
```

Сборка проекта завершилась неудачей, поскольку созданный файл `doomgeneric_tty.c` пока не содержит функции `main` и платформозависимых функций.

При реализации указанных в @tbl:funcs функций сначала необходимо для каждой функции определить её сигнатуру -- тип возвращаемого значения, количество и типы принимаемых на вход аргументов.

Для поиска сигнатур функций в заголовочных файлах с расширением `.h` воспользуемся утилитой `grep`:

```c
~/doomgeneric/doomgeneric$ grep DG_Init *.h
doomgeneric.h:void DG_Init();
~/doomgeneric/doomgeneric$ grep DG_DrawFrame *.h
doomgeneric.h:void DG_DrawFrame();
~/doomgeneric/doomgeneric$ grep DG_SleepMs *.h
doomgeneric.h:void DG_SleepMs(uint32_t ms);
~/doomgeneric/doomgeneric$ grep DG_GetTicksMs *.h
doomgeneric.h:uint32_t DG_GetTicksMs();
~/doomgeneric/doomgeneric$ grep DG_GetKey *.h
doomgeneric.h:int DG_GetKey(int* pressed, unsigned char* key);
~/doomgeneric/doomgeneric$ grep DG_SetWindowTitle *.h
doomgeneric.h:void DG_SetWindowTitle(const char * title);
```

Поместим найденные сигнатуры и тривиальные реализации всех функций из @tbl:funcs в файл `doomgeneric_tty.c`. Добавим, как указано в `README.md`, главный цикл программы в функцию с именем `main` в том же файле, подключим заголовочный файл с сигнатурами функций `doomgeneric.h` в `doomgeneric_tty.c`:

```c
#include <stdio.h>
#include <stdint.h>
#include "doomgeneric.h"

void DG_Init() { printf("Doom launched!\n"); }
void DG_SleepMs(uint32_t ms) {}
void DG_SetWindowTitle(const char *title) {}
void DG_DrawFrame() {}

uint32_t DG_GetTicksMs() { return 0; }
int DG_GetKey(int *pressed, unsigned char *key) { return 0; }

int main(int argc, char **argv) {
    doomgeneric_Create(argc, argv);
    while (1) doomgeneric_Tick();
    return 0;
}
```

Вновь запустим сборку проекта:

```bash
~/doomgeneric/doomgeneric$ make -f Makefile.tty
[Compiling doomgeneric_tty.c]
[Linking doomgeneric]
[Size]
size doomgeneric
  text  data    bss    dec   hex filename
322570 82200 271240 676010 a50aa doomgeneric
```

Сборка проекта с платформозависимыми функциями-заглушками была выполнена успешно, в результате компилятором был создан новый исполняемый файл с именем `doomgeneric`. 

Проверим работу скомпилированной программы:

```bash
~/doomgeneric/doomgeneric$ ./doomgeneric doom1.wad
Doom launched!
Doom Generic 0.1
Z_Init: Init zone memory allocation daemon.
zone memory: 0x7f2fba975010, 600000 allocated for zone
Using . for configuration and saves
...
player 1 of 1 (1 nodes)
Emulating the behavior of the 'Doom 1.9' executable.
HU_Init: Setting up heads up display.
ST_Init: Init status bar.
```

Версия Doom с функциями-заглушками, размещёнными в файле `doomgeneric_tty.c` вместо платформозависимых реализаций функций, перечисленных в @tbl:funcs, запустилась -- на экран было выведено приветственное сообщение `Doom launched`, размещённое в функции-заглушке `DG_Init`, а также отладочные сообщения. Однако, затем выполнение программы остановилось. Это ожидаемое проведение программы, поскольку не все из платформозависимых функций (см. @tbl:funcs) в файле `doomgeneric_tty.c` реализованы корректно.

Исправим реализацию функции `DS_GetTicksMs` -- как указано в @tbl:funcs, эта функция должна возвращать время, прошедшее с начала игры, в миллисекундах. 

Для реализации этой функции создадим глобальную переменную `counter`, значение которой будет увеличиваться и возвращаться при каждом вызове функции `DG_GetTicksMs`. При помощи стандартной функции `usleep`, для использования которой необходимо подключить стандартный заголовочный файл `unistd.h`, добавим задержку, снижающую частоту смены кадров для упрощения отладки:

```c
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include "doomgeneric.h"

void DG_Init() { printf("Doom launched!\n"); }
void DG_SleepMs(uint32_t ms) {} 
void DG_SetWindowTitle(const char *title) {}
void DG_DrawFrame() {}
 
uint32_t DG_GetTicksMs() {
    static uint32_t counter = 0;
    usleep(1000);
    printf("Tick: %d\n", counter);
    return counter++;
}

int DG_GetKey(int *pressed, unsigned char *key) { return 0; } 

int main(int argc, char **argv) { 
    doomgeneric_Create(argc, argv); 
    while (1) doomgeneric_Tick();
    return 0; 
}
```

Выполним сборку и проверим работу программы:

```bash
~/doomgeneric/doomgeneric$ make -f Makefile.tty
~/doomgeneric/doomgeneric$ ./doomgeneric doom1.wad
Doom launched!
Doom Generic 0.1
Z_Init: Init zone memory allocation daemon.
zone memory: 0x7fd914c28010, 600000 allocated for zone
Using . for configuration and saves
...
player 1 of 1 (1 nodes)
Emulating the behavior of the 'Doom 1.9' executable.
HU_Init: Setting up heads up display.
ST_Init: Init status bar.
Tick: 0
Tick: 1
Tick: 2
Tick: 3
Tick: 4
Tick: 5
...
```

Теперь после инициализации Doom не прекращает работу, а продолжает выводить в терминал отладочные сообщения с текущим значением переменной `counter`.

Для реализации функции `DS_DrawFrame`, задача которой -- вывести кадровый буфер `DG_ScreenBuffer` на экран (см. @tbl:funcs), необходимо определить тип глобальной переменной `DG_ScreenBuffer`:

```bash
~/doomgeneric/doomgeneric$ grep DG_ScreenBuffer *.h
doomgeneric.h:extern pixel_t* DG_ScreenBuffer;
~/doomgeneric/doomgeneric$ grep pixel_t *.h
doomgeneric.h:typedef uint32_t pixel_t;
doomgeneric.h:extern pixel_t* DG_ScreenBuffer;
~/doomgeneric/doomgeneric$ grep RES doomgeneric.h
#define DOOMGENERIC_RESX 640
#define DOOMGENERIC_RESY 400
```

Из вывода утилиты `grep` можно сделать вывод о том, что глобальная переменная `DG_ScreenBuffer` -- это массив чисел типа `uint32_t`, поскольку `pixel_t` -- это псевдоним типа `uint32_t`. Число пикселей в массиве пикселей оценивается как произведение ширины экрана `DOOMGENERIC_RESX` на его высоту `DOOMGENERIC_RESY`. Таким образом, для размера экрана 640 на 400 точек число пикселей в массиве `DG_ScreenBuffer` равно 256 000, пиксели в массиве сохраняются ядром Doom (см. @fig:doomarch) построчно.

Каждое число в массиве `DG_ScreenBuffer` кодирует цвет пикселя и занимает 4 байта, причём 3 младших байта содержат цвет в формате RGB (Red, Green, Blue). Обновим реализацию функции `DG_DrawFrame`, при помощи побитовых операций в цикле извлечём компоненты цвета каждого 2-го пикселя по горизонтали и каждого 4-го пикселя по вертикали и выведем их на экран:

```c
void DG_DrawFrame() {
    for (int y = 0; y < DOOMGENERIC_RESY; y += 5) {
        for (int x = 0; x < DOOMGENERIC_RESX; x += 3) {
            int i = y * DOOMGENERIC_RESX + x;
            uint32_t pixel = DG_ScreenBuffer[i];
            unsigned char r = (pixel >> 16) & 255;
            unsigned char g = (pixel >>  8) & 255;
            unsigned char b = (pixel >>  0) & 255;
            printf("%d %d %d; ", r, g, b);
        }
        printf("\n");
    }
}
```

Номер пикселя `i` в массиве `DG_ScreenBuffer` вычисляется как номер строки `y` умноженный на ширину экрана `DOOMGENERIC_RESX`, к которому прибавляется номер пикселя в строке `x`. Для извлечения байта красной компоненты цвета `r`, зелёной компоненты цвета `g` и синей компоненты цвета `b` используется побитовый сдвиг вправо `>>` и побитовое «и» `&`. Для извлечения красной компоненты значение `pixel` сдвигается вправо на 16 бит (на 2 байта), для извлечения зелёной компоненты -- на 8 бит (на 1 байт). Побитовое «и» используется для наложение маски из восьми единиц для исключения из числа-результата старших разрядов.

Удалим инструкцию, выводящую отладочные сообщения, из функции `DG_GetTicksMs`. Скорость вывода цветов пикселей в консоль можно регулировать, меняя число миллисекунд, подаваемое на вход функции `usleep`, вызываемой из функции `DG_GetTicksMs`. Проверим работу обновлённой версии программы:

```
~/doomgeneric/doomgeneric$ make -f Makefile.tty
~/doomgeneric/doomgeneric$ ./doomgeneric doom1.wad
...
0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0; ...
...
128 1 1; 116 1 1; 116 1 1; 104 1 1; 128 1 1; 155 1 1; 155 1 1; 167 1 1; 255 255 72; 155 92 20; ...
...
```

Через некоторое время после вывода чёрных пикселей на экран начинают выводиться и другие цвета, например, `255 255 72` (ярко-жёлтый цвет).

Для поддержки вывода графики Doom в виде ASCII-символов в терминале на следующем шаге необходимо преобразовать цвет каждого пикселя в формате RGB в ASCII-символ. Выбор ASCII-символа, соответствующего пикселю, может осуществляться, например, на основе относительной яркости (relative luminance) цвета пикселя, определённой в @caldwell2008web.

Воспользуемся следующей упрощённой формулой на основе @caldwell2008web для вычисления относительной яркости цвета:

$$
l(r, g, b) = 255^{-1} (0.2126r + 0.7152g + 0.0722b)
$$ {#eq:luminance}

где *r*, *g* и *b* -- численные значения красной, зелёной и синей компонент цвета в формате RGB, значения функции *l* принадлежат вещественному промежутку от 0 до 1 включительно.

Реализуем формулу @eq:luminance на языке C и используем вычисленное по ней округлённое вниз вещественное значение в функции `DG_DrawFrame` для выбора ASCII-символа пикселя из строковой глобальной переменной `chars`. Номер символа в строке `chars` соответствует его яркости -- пробел будем считать самым тусклым, а `#` -- самым ярким символом. Округление вниз для вещественных значений произведём при помощи оператора приведения типа данных `(int)`.

Перед отрисовкой каждого кадра в терминале воспользуемся управляющей последовательностью ANSI (ANSI escape code) `\033[1;1H` -- эта последовательность позволяет переместить курсор на позицию 1;1, в левый верхний угол терминала, и продолжить консольный вывод с этой позиции:

```c
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
```

При помощи команды `make -f Makefile.tty` выполним сборку новой версии программы и проверим её работу, запустив программу при помощи команды `./doomgeneric doom1.wad`. Экран заставки игры Doom, выведенный в терминал ОС Linux в виде ASCII-символов, показан на @fig:doomascii.

![ASCII-графика экрана заставки игры Doom в терминале ОС Linux](./doom-ascii.png){#fig:doomascii width=65%}
