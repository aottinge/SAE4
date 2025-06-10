#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db
from controllers.client_liste_envies import supprimer_article_wishlist

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
    '''
    articles_panier = []
    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Sélectionner le contenu du panier de l'utilisateur
    sql_select_panier = '''
        SELECT lp.*, v.prix_velo AS prix
        FROM ligne_panier lp
        JOIN velo v ON lp.article_id = v.id_velo
        WHERE lp.utilisateur_id = %s
    '''
    mycursor.execute(sql_select_panier, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    # Vérifier si le panier est vide
    if not items_ligne_panier:
        flash(u'Pas d\'articles dans le panier', 'alert-warning')
        return redirect('/client/article/show')

    # Créer la commande
    date_achat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_insert_commande = '''
        INSERT INTO commande (date_achat, utilisateur_id, etat_id)
        VALUES (%s, %s, %s)
    '''
    mycursor.execute(sql_insert_commande, (date_achat, id_client, 1))

    # Récupérer l'ID de la dernière commande
    mycursor.execute('SELECT LAST_INSERT_ID() AS last_insert_id')
    last_insert_id = mycursor.fetchone()['last_insert_id']

    # Insérer les articles du panier dans la ligne de commande et supprimer du panier
    for item in items_ligne_panier:
        sql_insert_ligne_commande = '''
            INSERT INTO ligne_commande (article_id, commande_id, prix, quantite)
            VALUES (%s, %s, %s, %s)
        '''
        mycursor.execute(sql_insert_ligne_commande, (item['article_id'], last_insert_id, item['prix'], item['quantite']))

        # Supprimer l'article du panier
        sql_delete_panier = '''
            DELETE FROM ligne_panier WHERE utilisateur_id = %s AND article_id = %s
        '''
        mycursor.execute(sql_delete_panier, (id_client, item['article_id']))

        # Supprimer l'article de la liste d'envies s'il y est présent
        supprimer_article_wishlist(id_client, item['article_id'])

    # Valider les modifications dans la base de données
    get_db().commit()

    flash(u'Commande ajoutée avec succès', 'alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    # Sélection des commandes du client triées par état puis par date d'achat décroissante
    sql = '''
        SELECT c.id_commande, c.date_achat, c.etat_id, e.libelle,
               SUM(lc.quantite) AS nbr_articles,
               (SELECT SUM(lc.quantite * lc.prix) FROM ligne_commande lc WHERE lc.commande_id = c.id_commande) AS prix_total
        FROM commande c
        JOIN etat e ON c.etat_id = e.id_etat
        JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        WHERE c.utilisateur_id = %s
        GROUP BY c.id_commande,c.date_achat,c.utilisateur_id,c.etat_id,e.libelle
        ORDER BY c.etat_id ASC, c.date_achat DESC
    '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)

    if id_commande:
        # Récupération des articles d'une commande spécifique
        sql = '''
            SELECT v.nom_velo AS nom, lc.quantite, lc.prix, (lc.quantite * lc.prix) AS prix_ligne
            FROM ligne_commande lc
            JOIN velo v ON lc.article_id = v.id_velo
            WHERE lc.commande_id = %s
        '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

    return render_template(
        'client/commandes/show.html',
        commandes=commandes,
        articles_commande=articles_commande,
        commande_adresses=commande_adresses
    )

