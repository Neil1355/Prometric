"""Produce a plain-text SQL UPDATE statement to populate
`security_question` and `security_answer` for existing users.

Usage (PowerShell):
    python migrations\set_security_answer_plain.py --user_type student --user_id 123 --question "What is your first pet?" --answer "fluffy"

This prints a SQL UPDATE statement and can optionally execute it against
localhost when run with --execute.
"""
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--user_type', choices=['student','employee','manager'], required=True)
    p.add_argument('--user_id', required=True)
    p.add_argument('--question', required=True)
    p.add_argument('--answer', required=True)
    p.add_argument('--execute', action='store_true', help='(optional) execute against local DB using mysql-connector; not recommended from remote environments')
    args = p.parse_args()

    table_map = {
        'student': ('student', 'student_id'),
        'employee': ('employee_personal', 'employee_id'),
        'manager': ('managers', 'id')
    }
    table, id_col = table_map[args.user_type]
    # escape single quotes in question and answer
    q_esc = args.question.replace("'","\\'")
    a_esc = args.answer.replace("'","\\'")

    print('-- SQL to run (copy+paste into MySQL):')
    print("UPDATE {table} SET security_question = '{q}', security_answer = '{h}' WHERE {id_col} = {uid};".format(
        table=table, q=q_esc, h=a_esc, id_col=id_col, uid=args.user_id
    ))

    if args.execute:
        try:
            import mysql.connector
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='prometricdb')
            cur = conn.cursor()
            cur.execute("UPDATE {table} SET security_question=%s, security_answer=%s WHERE {id_col}=%s".format(table=table, id_col=id_col), (args.question, args.answer, args.user_id))
            conn.commit()
            print('-- Executed against localhost: prometricdb')
        except Exception as e:
            print('-- Execution failed:', e)


if __name__ == '__main__':
    main()
