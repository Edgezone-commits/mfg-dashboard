import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

def create_database():
    conn = sqlite3.connect('data/operations.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_orders (
            job_id TEXT PRIMARY KEY,
            customer_name TEXT,
            product TEXT,
            category TEXT,
            quantity INTEGER,
            due_date TEXT,
            completion_date TEXT,
            actual_build_hours REAL,
            estimated_build_hours REAL,
            status TEXT,
            rush_order INTEGER,
            department TEXT
        )
    ''')

    customers = ['Acme Corp', 'BuildRight LLC', 'FastFix Inc', 'MegaBuild Co', 'QuickPipe Ltd']
    products = ['Copper Pipe 1in', 'Steel Valve 2in', 'PVC Elbow', 'Bronze Fitting', 'Check Valve']
    categories = ['Plumbing', 'Valves', 'Fittings', 'Hardware']
    departments = ['Assembly', 'Machining', 'Welding', 'Packaging']
    statuses = ['Complete', 'Complete', 'Complete', 'In Progress', 'Pending']

    random.seed(42)
    for i in range(50):
        due = datetime.now() - timedelta(days=random.randint(-10, 30))
        completion = due - timedelta(hours=random.randint(1, 48)) if random.random() > 0.3 else None
        estimated = round(random.uniform(2, 16), 1)
        actual = round(estimated * random.uniform(0.8, 1.4), 1) if completion else None

        cursor.execute('''
            INSERT OR IGNORE INTO job_orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            f'JOB-{1000+i}',
            random.choice(customers),
            random.choice(products),
            random.choice(categories),
            random.randint(10, 500),
            due.strftime('%Y-%m-%d'),
            completion.strftime('%Y-%m-%d') if completion else None,
            actual,
            estimated,
            random.choice(statuses),
            1 if random.random() > 0.8 else 0,
            random.choice(departments)
        ))

    conn.commit()
    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    create_database()