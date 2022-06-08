from ast import Not
import sys
import os
import io

from flask import Flask, flash, redirect, request, render_template
from numpy import not_equal
import pymysql
# import mysql.connector
# from mysql.connector.constants import ClientFlag
# import pandas as pd

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

config = {
    'user': 'kanaka',
    'password': '11225',
    'database': 'work_shop_db',
    'host': '35.226.133.70',
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}


app = Flask(__name__, template_folder='template')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Data Received")
    return render_template('index.html')


@app.route('/single-row-insert', methods=['GET', 'POST'])
def singleRowInsert():

    connection = pymysql.connect(**config)
    cur = connection.cursor()

    if request.method == 'GET':
        with connection:
            with cur as cursor:

                cursor.execute("select * from test_country_table")
                result = cursor.fetchall()

            cur.close()

        return render_template('single-row-insert.html', result=result)

    if request.method == 'POST':

        with connection:

            sqlStatement = ("CREATE DATABASE IF NOT EXISTS work_shop_db")
            cur.execute(sqlStatement)

            createTable = ("CREATE TABLE IF NOT EXISTS test_country_table ("
                           "id INT NOT NULL AUTO_INCREMENT,"
                           "countryName VARCHAR(100),"
                           "currency  VARCHAR(50),"
                           "population VARCHAR(200),"
                           "gdp VARCHAR(50),"
                           "flagURI VARCHAR(500),"
                           "PRIMARY KEY (id))")

            cur.execute(createTable)

            sqlData = ("INSERT INTO test_country_table (id, countryName, currency, population, gdp, flagURI) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")

            cur.execute(sqlData, (0, "sample name", "sample currency",
                                  "sample population", "sample gdp", "sample flagURI"))
            connection.commit()

            with cur as cursor:

                cursor.execute("select * from test_country_table")
                result = cursor.fetchall()

            cur.close()

        return render_template('single-row-insert.html', result=result)


@app.route('/country-table', methods=['GET', 'POST', 'PUT'])
def countryTable():

    connection = pymysql.connect(**config)
    cur = connection.cursor()

    if request.method == 'GET':

        with connection:
            with cur as cursor:

                cursor.execute("select * from country_table")
                result = cursor.fetchall()

            cur.close()

        return render_template('country-table.html', result=result)

    if request.method == 'POST':

        country_name = request.form['country_name']
        currency = request.form['currency']
        population = request.form['population']
        gdp = request.form['gdp']
        flag_url = request.form['flag_url']

        with connection:

            sqlStatement = ("CREATE DATABASE IF NOT EXISTS work_shop_db")
            cur.execute(sqlStatement)

            createTable = ("CREATE TABLE IF NOT EXISTS country_table ("
                           "id INT NOT NULL AUTO_INCREMENT,"
                           "countryName VARCHAR(100),"
                           "currency  VARCHAR(50),"
                           "population VARCHAR(200),"
                           "gdp VARCHAR(50),"
                           "flagURI VARCHAR(500),"
                           "PRIMARY KEY (id))")

            cur.execute(createTable)

            sqlData = ("INSERT INTO country_table (id, countryName, currency, population, gdp, flagURI) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")

            cur.execute(sqlData, (0, country_name, currency,
                                  population, gdp, flag_url))
            connection.commit()

            with cur as cursor:

                cursor.execute("select * from country_table")
                result = cursor.fetchall()

            cur.close()

        return render_template('country-table.html', result=result)


@app.route('/country-table-update', methods=['GET', 'POST'])
def updateTable():

    connection = pymysql.connect(**config)
    cur = connection.cursor()

    if request.method == 'POST':

        id = request.form['id']
        country_name = request.form['country_name']
        currency = request.form['currency']
        population = request.form['population']
        gdp = request.form['gdp']
        flag_url = request.form['flag_url']

        sqlUpdate = "UPDATE `country_table` SET `countryName` = %s, `currency` = %s, `population` = %s, `gdp` = %s, `flagURI` = %s   WHERE `id` = %s"

        cur.execute(sqlUpdate, (country_name, currency,
                                population, gdp, flag_url, id))
        connection.commit()

        with cur as cursor:

            cursor.execute("select * from country_table")
            result = cursor.fetchall()

        cur.close()

        return render_template('country-table.html', result=result)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
