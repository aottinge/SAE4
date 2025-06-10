#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['GET', 'POST'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''
        SELECT c.*, u.login, SUM(lc.quantite) AS quantite, (SELECT SUM(lc.quantite * lc.prix) FROM ligne_commande lc WHERE lc.commande_id = c.id_commande) AS prix_total, e.libelle
        FROM commande c
        JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
        JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        JOIN etat e ON c.etat_id = e.id_etat
        GROUP BY c.id_commande,c.date_achat,c.utilisateur_id,c.etat_id,u.login,e.libelle
    '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande is not None:
        # Sélection du détail d'une commande avec le nom du jean
        sql = '''
            SELECT lc.*, v.nom_velo AS nom , (lc.quantite * lc.prix) AS prix_ligne
            FROM ligne_commande lc
            JOIN velo v ON lc.article_id = v.id_velo
            WHERE lc.commande_id = %s
        '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()


    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           articles_commande=articles_commande,
                           commande_adresses=commande_adresses)


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
