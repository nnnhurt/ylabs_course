#HW1

Домашняя работа для YLABS

## Инструкция по запуску

1. Следует зарегистрироваться в postgres
   (```su - postgres ```)
2. Выполнить команды
   ```createdb <имя базы>```
   ```createuser -- interactive```
### Запуск
1. Для запуска сервепа воспользуйтесь командой:
   ```su - postgres -c "sudo pg_ctlcluster 14 main start"
2. Для установки зависимостей:
   ```python -m venv venv```
   ```source venv/bin/activate```
   ```pip install -r requirements.txt```

3. Важные данные(DN_NAME, DB_USER, DB_PASSWORD, DB_HOST) следует разместить в файле .env
4. Запуск api-сервера:
   ```unicorn sql_app.main:app --reload```

##Результаты тестов находятся в файле menu app.postman_test_run.json
