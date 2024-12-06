Tkinter Application

Приложение предназначено для обработки рабочей информации, хранящейся в БД приложенияб и вывода в графики(matplotlib, pandas) по выбранным параметрам. Использует MySQL в качестве базы данных.

Перед тем как начать, убедитесь, что у вас установлены следующие компоненты:

    Python (версия 3.11+)
    MySQL (версия 14+)
    pip
    virtualenv (опционально)

Установка

python -m venv venv source venv/bin/activate # Для macOS/Linux venv\Scripts\activate # Для Windows
Установите зависимости:

pip install -r requirements.txt

Настройте базу данных: Создайте базу данных в MySQL и обновите настройки в .env вашего проекта:

host = "host"
port = 'port'
user = "admin"
password = "password"
database = "database"

##Запуск приложения
Чтобы запустить приложение, выполните следующую команду: python3 main.py