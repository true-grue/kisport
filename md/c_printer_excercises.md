### Упражнения

**Задача 1.** Реализуйте функцию `is_little_endian` для определения порядка байт в системе.

**Задача 2.** Следующая программа ведёт себя по-разному в Linux и Windows:

```c
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

```bash
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

```bash
0000000a
00000001
00000002
00000003
00000004
00000005
00000006
00000007
```

Найдите и исправьте ошибку. Перепишите функции `load_from_file` и `save_to_file` таким образом, чтобы файлом с данными можно было пользоваться на платформах с разным порядком байт.

**Задача 3.** Напишите программу, которая выведет на экран для конкретной структуры последовательность смещений ее полей. Анализируемая структура является частью программы, но способ вывода смещений полей должен легко адаптироваться для других структур. Например, для следующей структуры:

```c
struct data {
    char c;
    short s;
    double d;
};
```

На экран должны быть выведены следующие значения смещений полей:

```c
c: 0
s: 2
d: 8
```

Получите без изменения исходного текста программы другие значения смещений полей при выводе.

**Задача 4.** Реализуйте простейший аналог команды `ls` с использованием POSIX-функций @posix. Добавьте к реализации `ls` обработку ключа `-l`. Используйте POSIX-функцию `getopt`.
