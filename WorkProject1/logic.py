import sqlite3

DB_PATH = 'schedule.db'
TIMEZONE = 'по МСК'

def get_schedule_for_day(day: str) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, time, subject FROM schedule WHERE day = ? ORDER BY time", (day,))
        lessons = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"⚠️ Ошибка при получении расписания: {e}"

    if not lessons:
        return f"❌ Нет расписания на {day}."

    result = f"📅 *Расписание на {day} ({TIMEZONE}):*\n\n"
    for lesson_id, time, subject in lessons:
        result += f"#{lesson_id} ⏰ {time} — {subject}\n"
    return result

def get_week_schedule() -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT day, time, subject FROM schedule ORDER BY day, time")
        lessons = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"⚠️ Ошибка при получении расписания: {e}"

    if not lessons:
        return "❌ Расписание пустое."

    result = f"📚 *Расписание на всю неделю ({TIMEZONE}):*\n\n"
    days = {}
    for day, time, subject in lessons:
        days.setdefault(day, []).append(f"⏰ {time} — {subject}")

    for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
        if day in days:
            result += f"*{day}:*\n" + "\n".join(days[day]) + "\n\n"
    return result

def add_lesson(day: str, time: str, subject: str) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO schedule (day, time, subject) VALUES (?, ?, ?)", (day, time, subject))
        conn.commit()
        conn.close()
        return f"✅ Добавлено: {day}, {time}, {subject}"
    except Exception as e:
        return f"❌ Ошибка добавления: {e}"

def delete_lesson_by_id(lesson_id: int) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule WHERE id = ?", (lesson_id,))
        if cursor.rowcount == 0:
            return "⚠️ Урок с таким ID не найден."
        conn.commit()
        conn.close()
        return f"✅ Урок #{lesson_id} удалён."
    except Exception as e:
        return f"❌ Ошибка удаления: {e}"
