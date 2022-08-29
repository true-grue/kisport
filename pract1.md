# Практическое занятие №1

П.Н. Советов, РТУ МИРЭА

## Задача 1

Реализуйте функцию `print_data`, которая выведет на экран значения в том порядке байт, который принят в вашей системе.

Пример работы `print_data`.

```
short s = 127;
int i = 0xaabbccdd;
long long ll = 42;
double f = 0.5;
```

```
s: 0x7f 0x00 
i: 0xdd 0xcc 0xbb 0xaa 
ll: 0x2a 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
f: 0x00 0x00 0x00 0x00 0x00 0x00 0xe0 0x3f 
```

## Задача 2

Следующая программа ведет себя по-разному в Linux и Windows.

```C
#include <stdio.h>

int arr[] = { 0xa, 1, 2, 3, 4, 5, 6, 7 };

#define ARR_SIZE (sizeof(arr) / sizeof(int))

void save_to_file(char *filename, int *arr, int size) {
  FILE *fp = fopen(filename, "w");
  fwrite(arr, sizeof(int), size, fp);
  fclose(fp);
}

void load_from_file(char *filename, int *arr, int size) {
  FILE *fp = fopen(filename, "rb");
  fread(arr, sizeof(int), size, fp);
  fclose(fp);
}

void print_array(int *arr, int size) {
  for (int i = 0; i < size; i += 1) {
      printf("%08x\n", arr[i]);
  }
}

int main(int argc, char** argv) {
  int new_arr[ARR_SIZE];
  save_to_file("data.bin", arr, ARR_SIZE);
  load_from_file("data.bin", new_arr, ARR_SIZE);
  print_array(new_arr, ARR_SIZE);
  return 0;
}
```

Вывод в Windows:

```
00000a0d
00000100
00000200
00000300
00000400
00000500
00000600
00000700
```

Вывод в Linux:

```
0000000a
00000001
00000002
00000003
00000004
00000005
00000006
00000007
```

Найдите и исправьте ошибку. Перепишите `load_from_file` и `save_to_file` таким образом, чтобы файлом с данными можно было пользоваться на платформах с разным порядком байт.

## Задача 3

Напишите программу, которая выведет для конкретной структуры последовательность смещений ее полей.

Пример работы программы:

```C
struct data {
    char c;
    short s;
    double d;
};
```

```
c: 0
s: 2
d: 8
```

Получите без изменения исходного текста программы другие значения смещений полей при выводе.

## Задача 4

Реализуйте простейший аналог команды `ls` с использованием POSIX-функций.

## Задача 5

Добавьте к реализации `ls` обработку ключа `-l`. Используйте POSIX-функцию `getopt`.

## Задача 6

Изобразите с помощью программы на SDL2 картину «Черный квадрат» (с белыми полями). Проверьте работу в Windows и Linux.

## Задача 7

Реализуйте средствами SDL2 клеточный автомат, имитирующий снег, как показано в видео ниже.

![](images/snow.gif).

## Задача 8

Реализуйте элементы графического интерфейса с помощью SDL2. Это может быть, например, меню игры. Какие элементы реализуются в SDL2 легко? Какие элементы требуют возможностей полноценной библиотеки для графического интерфейса?