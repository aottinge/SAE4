#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

from flask import session, g
import pymysql.cursors

import os                                 # à ajouter
from dotenv import load_dotenv            # à ajouter
load_dotenv()                             # à ajouter

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",                # à modifier
            user="root",               # à modifier
            password="0tt1ngeR",        # à modifier
            database="SAE4",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

'''
def activate_db_options(db):
    cursor = db.cursor()
    # Vérifier et activer l'option ONLY_FULL_GROUP_BY si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            print('MYSQL : il manque le mode ONLY_FULL_GROUP_BY')   # mettre en commentaire
            cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
            db.commit()
        else:
            print('MYSQL : mode ONLY_FULL_GROUP_BY  ok')   # mettre en commentaire
    # Vérifier et activer l'option lower_case_table_names si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result:
        if result['Value'] != '0':
            print('MYSQL : valeur de la variable globale lower_case_table_names differente de 0')   # mettre en commentaire
            cursor.execute("SET GLOBAL lower_case_table_names = 0")
            db.commit()
        else :
            print('MYSQL : variable globale lower_case_table_names=0  ok')    # mettre en commentaire
    cursor.close()
'''