# Практическое занятие №4

П.Н. Советов, РТУ МИРЭА

В следующих задачах используется материал главы 6 учебника [The AWK Programming Language](https://cdn.hackaday.io/files/255831094543072/The_AWK_Programming_Language.pdf).

Необходимо реализовать ассемблер и интерпретатор кода для одноадресной виртуальной машины из раздела 6.1 An Assembler and Interpreter.

## Задача 1

Реализуйте первый проход ассемблера с получением промежуточного представления в символической форме.

Пример исходного текста (подсчет суммы вводимых чисел):

```python
# print sum of input numbers (terminated by zero)
    ld zero # initialize sum to zero
    st sum
loop get    # read a number
    jz done # no more input if number is zero
    add sum # add in accumulated sum
    st sum  # store new value back in sum
    j loop  # go back and read another number
done ld sum # print sum
    put
    halt
zero const 0
sum const
```

Таблица символов:

```python
{'loop': 2, 'done': 7, 'zero': 10, 'sum': 11}
```

Промежуточный код:

```python
('ld', 'zero')
('st', 'sum')
('get', 0)
('jz', 'done')
('add', 'sum')
('st', 'sum')
('j', 'loop')
('ld', 'sum')
('put', 0)
('halt', 0)
('const', 0)
('const', 0)
```

## Задача 2

Реализуйте второй проход ассемблера с заменой меток их значениями из таблицы символов.

```python
0: ('ld', 10)
1: ('st', 11)
2: ('get', 0)
3: ('jz', 7)
4: ('add', 11)
5: ('st', 11)
6: ('j', 2)
7: ('ld', 11)
8: ('put', 0)
9: ('halt', 0)
10: ('const', 0)
11: ('const', 0)
```

## Задача 3

Закодируйте промежуточное представление в виде списка чисел в формате: первые 2 десятичные цифры задают код операции, а остальные 3 цифры – поле аргумента.

Коды операций:

```python
{'const': 0, 'get': 1, 'put': 2, 'ld': 3, 'st': 4, 'add': 5, 'sub': 6, 'jpos': 7, 'jz': 8, 'j': 9, 'halt': 10}
```

Результат кодирования:

```python
[3010, 4011, 1000, 8007, 5011, 4011, 9002, 3011, 2000, 10000, 0, 0]
```

## Задача 4

Реализуйте интерпретацию кода, полученного в предыдущей задаче.

Пример сеанса работы с интерпретатором:

```
<- 1
<- 2
<- 3
<- 4
<- 5
<- 6
<- 7
<- 8
<- 9
<- 0
-> 45
```

