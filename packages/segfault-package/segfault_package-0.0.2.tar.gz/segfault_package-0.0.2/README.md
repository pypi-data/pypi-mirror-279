# Segfault Package / Пакет Segfault
---
## English

### Description

`Segfault` is a package I created as a joke, containing exactly one method that triggers a C exception: `raise(SIGSEGV)`

Why was this package created? I was bored.

### Installation

To install, run the following command:

```python
import segfault

segfault.cause_segfault()
```

### Usage

Import and call the function cause_segfault:

```python
import segfault

segfault.cause_segfault()
```

This will cause the program to terminate with a segmentation fault.

### License

This package is provided "as is" without any warranties. Use at your own risk.

---

## Русский

### Описание

`Segfault` — пакет который я создал ради шутки и содержит ровно 1 метод, вызывающий исключение C : `raise(SIGSEGV)`

С какой целю был создан пакет? Мне было скучно.


### Установка

Для установки пропишите команду:

```sh
pip install segfault_package
```

### Использование

Импортируйте и вызовите функцию cause_segfault:

```python
import segfault

segfault.cause_segfault()
```

Это приведет к аварийному завершению программы с сегментационным нарушением.

### Лицензия

Этот пакет предоставляется "как есть" без каких-либо гарантий. Используйте на свой страх и риск.
