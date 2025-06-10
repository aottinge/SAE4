#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db
from controllers.client_liste_envies import client_historique_add

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')  # remplace /client
def client_article_show():  # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT id_velo AS id_article ,nom_velo AS nom, prix_velo AS prix,
            taille_id, type_velo_id, matiere, description, fournisseur, marque, image,stock,
            CASE WHEN le.id_article IS NOT NULL THEN 1 ELSE 0 END AS liste_envie
            FROM velo
            LEFT JOIN liste_envie le ON velo.id_velo = le.id_article AND le.id_client = %s'''
    list_param = [id_client]
    condition_and = ""

    if 'filter_word' in session:
        condition_and += " AND nom_velo LIKE %s"
        list_param.append(f"%{session['filter_word']}%")

    if 'filter_prix_min' in session and session['filter_prix_min'] != "":
        condition_and += " AND prix_velo >= %s"
        list_param.append(session['filter_prix_min'])

    if 'filter_prix_max' in session and session['filter_prix_max'] != "":
        condition_and += " AND prix_velo <= %s"
        list_param.append(session['filter_prix_max'])

    if 'filter_types' in session and len(session['filter_types']) > 0:
        condition_and += " AND type_velo_id IN (" + ",".join(["%s"] * len(session['filter_types'])) + ")"
        list_param.extend(session['filter_types'])

    if condition_and != "":
        sql = sql + " WHERE 1=1 " + condition_and

    if list_param:
        mycursor.execute(sql, tuple(list_param))
    else:
        mycursor.execute(sql)
    articles = mycursor.fetchall()

    # utilisation du filtre
    sql = '''SELECT id_type_velo AS id_type_article, libelle_type_velo AS libelle FROM type_velo'''
    mycursor.execute(sql)

    # pour le filtre
    types_article = mycursor.fetchall()

    sql_articles_panier = '''
               SELECT id_velo AS id_article ,nom_velo AS nom, prix_velo AS prix,
               taille_id, type_velo_id, matiere, description, fournisseur, marque, image,stock, ligne_panier.quantite FROM velo
               JOIN ligne_panier ON velo.id_velo = ligne_panier.article_id
               WHERE ligne_panier.utilisateur_id = %s
           '''

    mycursor.execute(sql_articles_panier, (id_client,))
    articles_panier = mycursor.fetchall()

    prix_total = sum(article['prix'] * article['quantite'] for article in articles_panier) if articles_panier else 0
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )

@client_article.route('/client/article/details/<int:id>')
def client_article_details(id):
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Ajouter à l'historique
    client_historique_add(id, id_client)

    # Récupération des détails de l'article
    sql = '''SELECT id_velo AS id_article, nom_velo AS nom, prix_velo AS prix,
            taille_id, type_velo_id, matiere, description, fournisseur, marque, image, stock
            FROM velo WHERE id_velo = %s'''
    mycursor.execute(sql, (id,))
    article = mycursor.fetchone()

    if article is None:
        abort(404)

    # Récupération du nombre de commandes de cet article par le client
    sql_commandes = '''SELECT COUNT(*) as nb_commandes_article
                      FROM commande
                      JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
                      WHERE commande.utilisateur_id = %s AND ligne_commande.article_id = %s'''
    mycursor.execute(sql_commandes, (id_client, id))
    commandes_articles = mycursor.fetchone()

    # Initialisation des valeurs par défaut pour les notes
    article['moyenne_notes'] = None
    article['nb_notes'] = None
    note = None

    # Initialisation des valeurs par défaut pour les commentaires
    commentaires = []
    nb_commentaires = {
        'nb_commentaires_utilisateur': 0,
        'nb_commentaires_total': 0,
        'nb_commentaires_utilisateur_valide': 0,
        'nb_commentaires_total_valide': 0
    }

    return render_template('client/article_info/article_details.html',
                         article=article,
                         commandes_articles=commandes_articles,
                         note=note,
                         commentaires=commentaires,
                         nb_commentaires=nb_commentaires)