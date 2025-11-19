##Tkinter Application

Приложение предназначено для обработки рабочей информации, хранящейся в БД приложения, и вывода в графику(matplotlib, pandas) по выбранным параметрам. Использует MySQL в качестве базы данных.

Перед тем как начать, убедитесь, что у вас установлены следующие компоненты:

    Python (версия 3.11+)
    MySQL (версия 14+)
    pip
    virtualenv (опционально)

Установка

python -m venv venv source .venv/bin/activate 

# Для macOS/Linux .venv\Scripts\activate

pip install -r requirements.txt

Настройте базу данных: Создайте базу данных в MySQL (database_example.txt) и обновите настройки в .env вашего проекта:

DB_HOST="host"
DB_PORT=port
DB_USER="user"
DB_PASSWORD="password"
DB_NAME="database_name"

##Запуск
Чтобы запустить приложение, выполните следующую команду: python3 main.py