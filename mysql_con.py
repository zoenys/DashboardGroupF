import mysql.connector
#pip install mysql-connector-python
import streamlit as st

conn = mysql.connector.connect(
host="localhost",
port="3306",
user="root",
passwd="",
db="pertambangan")

c = conn.cursor()


def get_data(table_name):
    c.execute(f'SELECT * FROM {table_name}')
    data = c.fetchall()
    return data


# def view_all_departments():
# 	c.execute('SELECT Department FROM customers')
# 	data = c.fetchmany
# 	return data