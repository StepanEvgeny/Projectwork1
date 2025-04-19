import sqlite3

# Подключаемся к базе (создаст файл, если его нет)
conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

# Создаём таблицу расписания
cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    subject TEXT NOT NULL
)
''')

# Пример данных
sample_data = [
    ('Понедельник', '10:00', 'Математика'),
    ('Понедельник', '12:00', 'Английский'),
    ('Вторник', '09:00', 'Физика'),
    ('Среда', '11:00', 'История'),
    ('Четверг', '13:00', 'Химия'),
    ('Пятница', '14:00', 'Биология'),
    ('Суббота', '15:00', 'Информатика'),
]

# Вставляем данные
cursor.executemany('INSERT INTO schedule (day, time, subject) VALUES (?, ?, ?)', sample_data)

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных создана и заполнена!")
