import pandas as pd

def get_kpis(df):
    total = len(df)
    completed = len(df[df['status'] == 'Complete'])
    rush = len(df[df['rush_order'] == 1])
    overdue = len(df[
        (df['due_date'] < pd.Timestamp.now().strftime('%Y-%m-%d')) &
        (df['status'] != 'Complete')
    ])
    avg_hours = round(df['actual_build_hours'].mean(), 1)

    return {
        'total': total,
        'completed': completed,
        'rush': rush,
        'overdue': overdue,
        'avg_hours': avg_hours
    }