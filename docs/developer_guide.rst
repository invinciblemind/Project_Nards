Руководство разработчика
========================

Подготовка окружения
--------------------

1. Установите Python 3.12.
2. Создайте виртуальное окружение.
3. Установите проект в editable-режиме с dev-зависимостями.

.. code-block:: bash

   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   python -m pip install -e .[dev]

Основные команды
----------------

.. code-block:: bash

   python -m doit lint
   python -m doit test
   python -m doit coverage
   python -m doit docs
   python -m doit build
   python -m doit check

Соглашения по коду
------------------

* Публичные классы и функции должны иметь типы и docstring.
* Доменный слой должен оставаться изолированным от tkinter и socket API.
* Новая функциональность добавляется небольшими PR с тестами и документацией.
