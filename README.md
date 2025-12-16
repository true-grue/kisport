# kisport

- [Слайды и материалы лекций](./slides)
- [Сборники практических задач](./pract)

## Начало работы

Для редактирования используется [Visual Studio Code](https://code.visualstudio.com/download).

### Сборка книги на ОС Windows

Для сборки проекта на ОС Windows необходимо выполнить следующие действия:

1. Установить [make для Windows](http://gnuwin32.sourceforge.net/packages/make.htm).
1. Установить [Python 3.12+](https://www.python.org/downloads/).
1. Установить модули `docx2pdf` и `iuliia`: `pip install docx2pdf iuliia`
1. Установить [pandoc](https://github.com/jgm/pandoc), поместив `pandoc.exe` в каталог `tools`.
1. Установить [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref), поместив `pandoc-crossref.exe` в каталог `tools`.
1. Установить [rsvg-convert](http://sourceforge.net/projects/tumagcc/files/rsvg-convert-2.40.20.7z/download), поместив `rsvg-convert.exe` в каталог `tools`.
1. Установить [mdbook](https://github.com/rust-lang/mdBook), поместив `mdbook.exe` в каталог `tools`.
1. Установить [graphviz](https://graphviz.org/download/).
1. Выполнить одну из команд для сборки книги в желаемый формат:

```makefile
make docx
make pdf
make web
```

### Сборка книги на ОС Linux

Для сборки проекта на ОС Ubuntu Linux необходимо выполнить следующие действия:

1. Установить [make](http://gnuwin32.sourceforge.net/packages/make.htm).
1. Установить [Python 3.12+](https://www.python.org/downloads/).
1. Установить модули `docx2pdf` и `iuliia`: `pip install docx2pdf iuliia`
1. Установить остальные зависимости: `make install`.
1. Выполнить команду для сборки книги:

```makefile
make web
```
