## Кроссплатформенная графика на языке C

### Работа с графикой на SDL3 в ОС Windows

SDL3 (Simple DirectMedia Layer) @sdl3 -- кроссплатформенная библиотека на языке C для разработки переносимых игр и других мультимедийных приложений.

В SDL3 поддерживаются следующие периферийные устройства: звуковая карта; клавиатура; мышь; джойстик; видеокарта с OpenGL и Direct3D.

Поддерживаемые библиотекой SDL3 платформы включают: Windows, macOS, Linux, iOS, Android.

Рассмотрим реализацию кроссплатформенного приложения с поддержкой вывода графики на SDL3. Изобразим с помощью программы на SDL3 картину «Чёрный квадрат» с белыми полями.

В этом разделе предполагается, что отладка и тестирование программы на языке C осуществляется на устройстве с архитектурой x86-64 под управлением ОС Windows. Для использования библиотеки SDL3 в ОС Windows x86-64 с компилятором `gcc`, включённым в набор инструментов для разработки MinGW @mingw, необходимо сохранить архив `SDL3-devel-3.2.24-mingw.zip` @sdl3 на устройство пользователя и распаковать его, например, в корень диска C. После распаковки архива будет создана папка `SDL3-devel-3.2.24-mingw`.

Создадим файл `program.c` со следующим содержимым: 

```c
#define SDL_MAIN_USE_CALLBACKS 1
#include <stdio.h>
#include "SDL3/SDL.h"
#include "SDL3/SDL_main.h"

SDL_AppResult SDL_AppInit(void **appstate, int argc, char **argv) {
    SDL_Init(SDL_INIT_VIDEO);
    SDL_CreateWindow("App", 500, 500, SDL_WINDOW_OPENGL);
    return SDL_APP_CONTINUE;
}

SDL_AppResult SDL_AppEvent(void *appstate, SDL_Event *event) {
    if (event->type == SDL_EVENT_QUIT)
        return SDL_APP_SUCCESS;
    return SDL_APP_CONTINUE;
}

SDL_AppResult SDL_AppIterate(void *appstate) { return SDL_APP_CONTINUE; }

void SDL_AppQuit(void *appstate, SDL_AppResult result) {}
```

Определённая в начале файла `program.c` константа `SDL_MAIN_USE_CALLBACKS` указывает SDL3 на необходимость использования функций `SDL_AppInit`, `SDL_AppEvent`, `SDL_AppIterate` и `SDL_AppQuit`, которые являются частью нового API для упрощения создания программ на SDL3.

Этот API избавляет разработчика от необходимости вручную создавать основной цикл SDL3 и функцию `main`, причём:

- `SDL_AppInit` вызывается однократно при запуске приложения.
- `SDL_AppEvent` вызывается каждый раз при возникновении нового события.
- `SDL_AppIterate` используется для обновления графики.
- `SDL_AppQuit` вызывается однократно перед завершением работы SDL3.

Воспользуемся следующими командами в терминале PowerShell для копирования dll-файла библиотеки SDL3 в текущую директорию, сборки файла `program.c` с библиотекой SDL3, запуска скомпилированной программы:

```powershell
PS C:\> cp C:\SDL3-3.2.22\x86_64-w64-mingw32\bin\SDL3.dll .
PS C:\> gcc -std=c99 program.c -o program.exe -IC:\SDL3-3.2.22\x86_64-w64-mingw32\include -LC:\SDL3-3.2.22\x86_64-w64-mingw32\lib -lmingw32 -lSDL3
PS C:\> .\program.exe
```

Опция `-I` позволяет указать путь к заголовочным файлам SDL3, `-L` позволяет указать путь к библиотечным файлам SDL3 с расширением `.a`, опции `-lmingw32` и `-lSDL3` связывают компилируемую программу с MinGW @mingw и с библиотекой SDL3 @sdl3.

После запуска скомпилированной программы `program.exe` откроется пустое окно с чёрным фоном (см. @fig:emptywindow), созданное функцией `SDL_CreateWindow`, вызванной из `SDL_AppInit`.

![Пустое окно, созданное библиотекой SDL3](./empty-window.png){#fig:emptywindow width=40%}

Поскольку в функции `SDL_AppEvent` обработано событие `SDL_EVENT_QUIT`, при этом в обработчике события `SDL_EVENT_QUIT` из функции возвращается код успешного завершения работы программы `SDL_APP_SUCCESS`, открывшееся окно удастся закрыть нажатием на соответствующую кнопку.

Для вывода на экран чёрного квадрата с белыми полями требуется создать отрисовщик `SDL_Renderer`. В SDL3 реализована система двойной буферизации: все графические операции выполняются со скрытым буфером, а на экран выводятся только полностью готовые кадры при вызове функции `SDL_RenderPresent`. Этот подход устраняет мерцание, так как во время подготовки нового кадра пользователь продолжает видеть предыдущий кадр.

Обновим реализацию функции `SDL_AppInit` -- при помощи вызова функции `SDL_CreateRenderer` создадим новый отрисовщик для окна при запуске программы, сохраним отрисовщик в глобальную переменную `renderer` в файле `program.c`:

```c
SDL_Renderer* renderer;

SDL_AppResult SDL_AppInit(void **appstate, int argc, char **argv) {
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window* window = SDL_CreateWindow("SDL", 500, 500, SDL_WINDOW_OPENGL);
    renderer = SDL_CreateRenderer(window, NULL);
    return SDL_APP_CONTINUE;
}
```

Для визуализации чёрного квадрата с белыми полями нарисуем белый прямоугольник, ширина и высота которого совпадают с шириной и высотой окна, после чего нарисуем квадрат в середине окна. Точка с координатами (0, 0) расположена в левом верхнем углу окна, поэтому для отрисовки чёрного квадрата со стороной 200 точек внутри квадратного окна со стороной 500 точек установим значения координат левого верхнего угла чёрного квадрата `x` и `y` равными 150.

В функции `SDL_AppIterate` в файле `program.c` зададим цвет отрисовки фона при помощи вызова функции `SDL_SetRenderDrawColor`, передав в `SDL_SetRenderDrawColor` 4 компоненты белого цвета в формате RGBA (Red, Green, Blue, Alpha). Затем инициализируем структуру `SDL_FRect` с описанием прямоугольника размером во всё окно и выполним его заливку посредством вызова функции `SDL_RenderFillRect`, для заливки прямоугольника будет использован белый цвет, заданный ранее при помощи функции `SDL_SetRenderDrawColor`.

Аналогичным образом выполним отрисовку чёрного квадрата в середине окна. По завершении выполнения графических операций вызовем функцию `SDL_RenderPresent`, которая выполнит переключение буферов -- подготовленный кадр станет виден на экране:

```c
SDL_AppResult SDL_AppIterate(void *appstate) {
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_FRect back = {.x = 0, .y = 0, .w = 500, .h = 500};
    SDL_RenderFillRect(renderer, &back);
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
    SDL_FRect rect = {.x = 150, .y = 150, .w = 200, .h = 200};
    SDL_RenderFillRect(renderer, &rect);
    SDL_RenderPresent(renderer);
    return SDL_APP_CONTINUE;
}
```

Скомпилируем и запустим обновлённую программу на SDL3:

```powershell
PS C:\> gcc -std=c99 program.c -o program.exe -IC:\SDL3-3.2.22\x86_64-w64-mingw32\include -LC:\SDL3-3.2.22\x86_64-w64-mingw32\lib -lmingw32 -lSDL3
PS C:\> .\program.exe
```

В результате выполнения указанных команд откроется окно, в середине которого изображён чёрный квадрат с белыми полями, показанное на @fig:square.

![Чёрный квадрат на SDL3 в ОС Windows](./square.png){#fig:square width=40%}

### Адаптация SDL3-графики для веб-браузера

Кроссплатформенное графическое приложение, написанное на языке C с использованием библиотеки SDL3 @sdl3, несложно портировать и в веб-браузер. Для этого воспользуемся компилятором Emscripten @emcc.

Первая версия компилятора Emscripten поддерживала трансляцию промежуточного представления LLVM (Low Level Virtual Machine) в код на языке JavaScript для веб-браузеров @emccjs. Промежуточное представление LLVM может быть получено в результате компиляции программы на языке C с использованием, например, компилятора `clang`. Однако, в дальнем компилятор Emscripten был доработан для поддержки трансляции кода на языке C в WebAssembly (Wasm) @emcc. Известные применения Emscripten включают, например, использование `emcc` для запуска многопользовательских SDL-игр в веб-браузерах.

Для портирования программы на SDL3 в веб-браузер установим Emscripten версии 4.0.8:

```powershell
PS C:\> git clone https://github.com/emscripten-core/emsdk.git
PS C:\> cd emsdk
PS C:\emsdk> git checkout 419021fa040428bc69ef1559b325addb8e10211f
HEAD is now at 419021f Release 4.0.8 (#1556)
PS C:\emsdk> .\emsdk.ps1 install latest
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

После установки соберём при помощи компилятора `emcc` реализованное ранее графическое приложение на SDL3. В результате сборки в рабочей директории будет создан файл `index.html` и ряд вспомогательных файлов:

```powershell
PS C:\> emcc gui.c -o index.html -s USE_SDL=3
ports:INFO: retrieving port: sdl3 from https://github.com/libsdl-org/SDL/archive/release-3.2.4.zip
ports:INFO: unpacking port: sdl3
cache:INFO: generating port: sysroot\lib\wasm32-emscripten\libSDL3.a...
emcc: warning: sdl3 port is still experimental [-Wexperimental]
system_libs:INFO: compiled 174 inputs in 31.26s
cache:INFO: - ok
```

Опция `-o` компилятора `emcc` позволяет задать имя HTML-файла с результатом сборки, а значение `USE_SDL=3` опции `-s` указывает Emscripten на необходимость подключения к компилируемому приложению библиотеки SDL3 @sdl3.

Для корректного функционирования веб-приложения в браузере необходимо обеспечить раздачу файлов веб-приложения через HTTP-сервер, поскольку корректно открыть полученный на предыдущем шаге HTML-файл по протоколу `file://` не удастся из-за ограничений безопасности браузеров. В этой связи запустим стандартный веб-сервер на языке Python, используя порт 8000:

```powershell
PS C:\> python -m http.server 8000
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

Открыв в веб-браузере страницу по адресу `http://127.0.0.1:8000` увидим чёрный квадрат и логотип проекта Emscripten (см. @fig:web).

![Чёрный квадрат на SDL3 в веб-браузере](./web.png){#fig:web width=40%}
