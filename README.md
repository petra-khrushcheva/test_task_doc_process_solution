# Скрипт для обработки документов
## 🌐 Обзор
Этот скрипт обрабатывает документы из таблицы documents в базе данных, выполняя следующие шаги:

1. Извлекает первый необработанный документ с типом transfer_document, отсортированный по полю recieved_at в порядке возрастания.
2. Берет список объектов из поля objects документа.
3. Для каждого объекта в списке собирает полный список объектов из таблицы data, включая все дочерние объекты, связанные через поле parent.
4. Проверяет, соответствуют ли значения полей объекта в таблице data указанным условиям в operation_details (старое значение должно совпадать с текущим, новое значение будет установлено).
5. Обновляет поля объектов в таблице data, если они соответствуют указанным условиям.
6. После обработки документа обновляет поле processed_at в таблице documents, ставя отметку времени, чтобы зафиксировать завершение обработки.
7. Возвращает True, если обработка прошла успешно, и False в случае ошибки.  

Таким образом, скрипт автоматизирует процесс обновления данных в базе на основе документов с типом transfer_document

## 📋 Оглавление
- [Требования](#️-требования)
- [Установка и запуск](#️-установка-и-запуск)
- [Переменные окружения](#-переменные-окружения)
- [Примечания](#-примечания)


## 📌 Требования

Перед запуском убедитесь, что у вас установлены:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## ⚙️ Установка и запуск

1. **Клонирование репозитория**:
   ```bash
   git@github.com:petra-khrushcheva/test_task_doc_process_solution.git
   cd test_task_doc_process_solution
   ```

2. **Настройка переменных окружения: создайте файл .env на основе [.env.example](./.env.example) и заполните его  данными для подключения к базе данных.**

3. **Запуск Docker Compose:**

   ```bash
   docker compose up
   ```

   ❗️Рекомендуется не запускать контейнер в фоновом режиме с флагом -d, чтобы логи обработки документа были видны в реальном времени.

4. **Запуск скрипта: Скрипт автоматически запускается при старте Docker Compose.**

## 🔑 Переменные окружения

- `POSTGRES_HOST`: адрес сервера базы данных
- `POSTGRES_PORT`: порт сервера базы данных
- `POSTGRES_DB`: название базы данных
- `POSTGRES_USER`: пользователь базы данных
- `POSTGRES_PASSWORD`: пароль пользователя базы данных


Подробнее — в файле [`.env.example`](./.env.example).

## 🤔 Примечания

1. **Примечание первое**: Условие изменения данных в тз описано так: "подходят под условие блока operation_details, где каждый ключ это название поля, внутри блок со старым значением в ключе old, которое нужно проверить...". Я из этого описания сделала вывод, что совпасть с текущими данными должны одновременно **все** значения old из operation_details. Если на самом деле нужно изменять те поля, у которых old совпадает с текущим независимо от остальных значений, я могу исправить код.
2. **Примечание второе**: Поскольку owner дочерних обьектов (содержимого) всегда совпадает с owner родительских обьектов (упаковок), можно сравнивать operation_details.owner.old только с owner тех обьектов, которые мы получаем из document.objects. Но с полем status и потенциальными будущими полями эта логика не работает, поэтому проверка идет одинаковая по всем полям и для всех обьектов (и родительских и дочерних)
