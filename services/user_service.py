
from db_instance import get_db


db = get_db()

def get_all_users_count():
    users = db.collection('users').get()
    count = 0
    for user in users:
        if user.get('role') == 'author':
            count += 1
        elif user.get('role') == 'editor':
            count += 1
        elif user.get('role') == 'reviewer':
            count += 0
        elif user.get('role') == 'admin':
            count += 0
    return count
