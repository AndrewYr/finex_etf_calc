

# finex_etf_calc

## Инфо по проекту

<details>
  <summary>Показать</summary>

| Наименование        | Значение                                                                                           |
|---------------------|----------------------------------------------------------------------------------------------------|
| Разработчик         | AndrewYr                                                                                           |
| Цель                | Сервис предназначенный для хранения информации о сделках (покупка/продажа) finex с предоставлением информации актуального количества и цены, основан на https://finex-etf.ru/calc/nav |
| Язык реализации     | Python 3.11                                                                                        |

</details>


## OpenAPI, Swagger UI

<details>
  <summary>Показать</summary>

* Спецификация OpenAPI v3.0.2 находится по относительному адресу `/spec/`
* Swagger UI v3 находится по относительному адресу `/docs/`

</details>


## Взаимодействие со сторонними сервисами
<details>
  <summary>Показать</summary>

* https://finex-etf.ru/
* https://www.cbr.ru

</details>
* --------------------


# Разработка

## Установка зависимостей

<details>
  <summary>Показать</summary>

Создать виртуальное окружение через pyenv:

    $ cd finex_etf_calc
    $ pyenv virtualenv 3.11.4 finex_etf_calc // создание виртуального окружения для проекта
    $ pyenv local finex_etf_calc // активация виртуального окружения для текущей папки

Установить необходимые пакеты:

    (finex_etf_calc)$ pip install -U setuptools pip pipenv // установка утилиты для работы с зависимостями
    (finex_etf_calc)$ pipenv install  // установка основных зависимостей проекта
    (finex_etf_calc)$ pipenv install --dev // установка dev-зависимостей проекта

Важно: 
перед запуском внутри Docker, нужно обязательно выполнить команду `pipenv install`, 
чтобы сформировался Pipfile.lock, именно из этого файла должна браться информация о зависимостях при сборке докер образа.

</details>

## Запуск внутри Docker
    
<details>
  <summary>Показать</summary>

    $ cp docker-compose.yml.sample docker-compose.yml // не добавлять docker-compose.yml под систему контроля версий, там хранятся только локальные настройки проекта
    $ docker-compose up

</details>

## Запуск тестов

<details>
  <summary>Показать</summary>

    $ python -m pytest -vvs

Оценка покрытия тестами 

    $ pytest --cov=finex_etf_calc tests/

Детальный отчет покрытия

    $ python -m pytest -vvs --cov=finex_etf_calc --cov-branch --cov-report=html:tests/coverage.html

</details>

## Запуск анализатора кода Flake

<details>
  <summary>Показать</summary>

    $ flake8

или

    $ python -m flake8 -v

</details>

## Установка pre-commit hook

<details>
  <summary>Показать</summary>

    $ pre-commit install

* Git должен быть установлен

</details>
