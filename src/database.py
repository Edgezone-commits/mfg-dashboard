import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('data/operations.db')

def get_all_jobs():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM job_orders", conn)
    conn.close()
    return df

def get_completed_today():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM job_orders 
        WHERE status = 'Complete'
        ORDER BY completion_date DESC
    """, conn)
    conn.close()
    return df

def get_rush_orders():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT job_id, customer_name, product, due_date, status, department
        FROM job_orders 
        WHERE rush_order = 1
        ORDER BY due_date ASC
    """, conn)
    conn.close()
    return df

def get_overdue_jobs():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT job_id, customer_name, product, due_date, status
        FROM job_orders
        WHERE due_date < date('now')
        AND status != 'Complete'
        ORDER BY due_date ASC
    """, conn)
    conn.close()
    return df

def get_department_summary():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            department,
            COUNT(job_id) as total_jobs,
            SUM(CASE WHEN status = 'Complete' THEN 1 ELSE 0 END) as completed,
            ROUND(AVG(actual_build_hours), 2) as avg_hours
        FROM job_orders
        GROUP BY department
        ORDER BY total_jobs DESC
    """, conn)
    conn.close()
    return df