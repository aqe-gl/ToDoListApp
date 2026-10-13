import json
from datetime import datetime
from pathlib import Path
from plyer import notification

BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "tasks.json"
SENT_FILE = BASE_DIR / "sent.json"

def check_reminders():
    if not TASKS_FILE.exists():
        return

    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        tasks = json.load(file)

    if SENT_FILE.exists():
        with open(SENT_FILE, "r", encoding="utf-8") as file:
            sent = json.load(file)
    else:
        sent = []

    now = datetime.now()

    for task in tasks:
        name = task[0]
        time_text = task[2]
        date_text = task[3]

        deadline = datetime.strptime(f"{date_text} {time_text}", "%d/%m/%Y %H:%M %p")

        reminder_id = f"{name}|{deadline.isoformat()}"

        if deadline <= now and reminder_id not in sent:
            notification.notify(
                title="Task Deadline Passed",
                message=f'"{name}" was due on {date_text} at {time_text}.',
                timeout=10
            )

            sent.append(reminder_id)

    with open(SENT_FILE, "w", encoding='utf-8') as file:
        json.dump(sent, file, indent=4)


if __name__ == '__main__':
    check_reminders()