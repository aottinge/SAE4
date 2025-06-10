#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session, jsonify

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()
    
    # Récupérer toutes les catégories de vélos avec le nombre d'articles dans les wishlists
    # On utilise LEFT JOIN pour inclure toutes les catégories, même celles sans articles
    # COALESCE permet de remplacer NULL par 0 quand il n'y a pas d'articles
    sql = '''SELECT tv.id_type_velo, tv.libelle_type_velo as libelle, 
             COALESCE(COUNT(le.id_article), 0) as nb_articles
             FROM type_velo tv
             LEFT JOIN velo v ON v.type_velo_id = tv.id_type_velo
             LEFT JOIN liste_envie le ON le.id_article = v.id_velo
             GROUP BY tv.id_type_velo, tv.libelle_type_velo
             ORDER BY tv.libelle_type_velo'''
    mycursor.execute(sql)
    wishlist_par_categorie = mycursor.fetchall()
    
    # Préparer les données pour le graphique des wishlists
    # On extrait les libellés et les valeurs dans des listes séparées
    labels = [item['libelle'] for item in wishlist_par_categorie]
    values = [item['nb_articles'] for item in wishlist_par_categorie]
    
    # Récupérer toutes les catégories avec le nombre d'articles consultés dans le dernier mois
    # Même principe que pour les wishlists, mais avec la table historique
    sql = '''SELECT tv.id_type_velo, tv.libelle_type_velo as libelle, 
             COALESCE(COUNT(h.id_article), 0) as nb_articles
             FROM type_velo tv
             LEFT JOIN velo v ON v.type_velo_id = tv.id_type_velo
             LEFT JOIN historique h ON h.id_article = v.id_velo
             WHERE h.date_consultation >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
             GROUP BY tv.id_type_velo, tv.libelle_type_velo
             ORDER BY tv.libelle_type_velo'''
    mycursor.execute(sql)
    historique_par_categorie = mycursor.fetchall()
    
    # Préparer les données pour le graphique d'historique
    labels_historique = [item['libelle'] for item in historique_par_categorie]
    values_historique = [item['nb_articles'] for item in historique_par_categorie]

    # Vérifier si une catégorie est sélectionnée dans l'URL
    id_categorie = request.args.get('categorie')
    categorie = None
    articles_wishlist = []
    articles_historique = []
    labels_articles = []
    values_wishlist = []
    values_historique_detail = []

    # Si une catégorie est sélectionnée, récupérer les détails
    if id_categorie:
        # Récupérer le nom de la catégorie sélectionnée
        sql = '''SELECT libelle_type_velo FROM type_velo WHERE id_type_velo = %s'''
        mycursor.execute(sql, (id_categorie,))
        categorie = mycursor.fetchone()
        
        # Récupérer tous les articles de cette catégorie avec leur nombre d'apparitions dans les wishlists
        sql = '''SELECT v.id_velo, v.nom_velo, COUNT(le.id_article) as nb_wishlist
                 FROM velo v
                 LEFT JOIN liste_envie le ON v.id_velo = le.id_article
                 WHERE v.type_velo_id = %s
                 GROUP BY v.id_velo, v.nom_velo
                 ORDER BY nb_wishlist DESC'''
        mycursor.execute(sql, (id_categorie,))
        articles_wishlist = mycursor.fetchall()
        
        # Récupérer tous les articles de cette catégorie avec leur nombre de consultations
        sql = '''SELECT v.id_velo, v.nom_velo, COUNT(h.id_article) as nb_consultations
                 FROM velo v
                 LEFT JOIN historique h ON v.id_velo = h.id_article
                 WHERE v.type_velo_id = %s
                 AND h.date_consultation >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                 GROUP BY v.id_velo, v.nom_velo
                 ORDER BY nb_consultations DESC'''
        mycursor.execute(sql, (id_categorie,))
        articles_historique = mycursor.fetchall()
        
        # Préparer les données pour les graphiques détaillés
        labels_articles = [item['nom_velo'] for item in articles_wishlist]
        values_wishlist = [item['nb_wishlist'] for item in articles_wishlist]
        values_historique_detail = [item['nb_consultations'] for item in articles_historique]

    # Rendre le template avec toutes les données nécessaires
    return render_template('admin/dataviz/dataviz_etat_1.html',
                         wishlist_par_categorie=wishlist_par_categorie,
                         historique_par_categorie=historique_par_categorie,
                         labels=labels,
                         values=values,
                         labels_historique=labels_historique,
                         values_historique=values_historique,
                         id_categorie=id_categorie,
                         categorie=categorie,
                         articles_wishlist=articles_wishlist,
                         articles_historique=articles_historique,
                         labels_articles=labels_articles,
                         values_wishlist=values_wishlist,
                         values_historique_detail=values_historique_detail)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )

@admin_dataviz.route('/admin/dataviz/wishlist')
def admin_dataviz_wishlist():
    mycursor = get_db().cursor()
    
    # Récupérer toutes les catégories
    sql = '''SELECT id_type_velo, libelle_type_velo FROM type_velo ORDER BY libelle_type_velo'''
    mycursor.execute(sql)
    categories = mycursor.fetchall()
    
    # Récupérer le nombre d'articles dans les wishlists par catégorie
    sql = '''SELECT tv.libelle_type_velo as libelle, COUNT(*) as nb_articles
             FROM liste_envie le
             JOIN velo v ON le.velo_id = v.id_velo
             JOIN type_velo tv ON v.type_velo_id = tv.id_type_velo
             GROUP BY tv.libelle_type_velo
             ORDER BY nb_articles DESC'''
    mycursor.execute(sql)
    wishlist_par_categorie = mycursor.fetchall()
    
    # Préparer les données pour le graphique
    labels = [item['libelle'] for item in wishlist_par_categorie]
    values = [item['nb_articles'] for item in wishlist_par_categorie]
    
    # Récupérer le nombre d'articles dans l'historique par catégorie sur le dernier mois
    sql = '''SELECT tv.libelle_type_velo as libelle, COUNT(*) as nb_articles
             FROM historique h
             JOIN velo v ON h.velo_id = v.id_velo
             JOIN type_velo tv ON v.type_velo_id = tv.id_type_velo
             WHERE h.date_consultation >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
             GROUP BY tv.libelle_type_velo
             ORDER BY nb_articles DESC'''
    mycursor.execute(sql)
    historique_par_categorie = mycursor.fetchall()
    
    # Préparer les données pour le graphique d'historique
    labels_historique = [item['libelle'] for item in historique_par_categorie]
    values_historique = [item['nb_articles'] for item in historique_par_categorie]
    
    return render_template('admin/dataviz/dataviz_etat_1.html',
                         categories=categories,
                         wishlist_par_categorie=wishlist_par_categorie,
                         historique_par_categorie=historique_par_categorie,
                         labels=labels,
                         values=values,
                         labels_historique=labels_historique,
                         values_historique=values_historique)

@admin_dataviz.route('/admin/dataviz/wishlist/categorie/<int:id_categorie>')
def admin_dataviz_wishlist_categorie(id_categorie):
    mycursor = get_db().cursor()
    
    # Récupérer les informations de la catégorie
    sql = '''SELECT libelle_type_velo FROM type_velo WHERE id_type_velo = %s'''
    mycursor.execute(sql, (id_categorie,))
    categorie = mycursor.fetchone()
    
    # Récupérer les articles dans les wishlists pour cette catégorie
    sql = '''SELECT v.id_velo, v.nom_velo, COUNT(le.id_liste_envie) as nb_wishlist
             FROM velo v
             LEFT JOIN liste_envie le ON v.id_velo = le.velo_id
             WHERE v.type_velo_id = %s
             GROUP BY v.id_velo, v.nom_velo
             ORDER BY nb_wishlist DESC'''
    mycursor.execute(sql, (id_categorie,))
    articles_wishlist = mycursor.fetchall()
    
    # Récupérer l'historique des consultations pour cette catégorie
    sql = '''SELECT v.id_velo, v.nom_velo, COUNT(h.id_historique) as nb_consultations
             FROM velo v
             LEFT JOIN historique h ON v.id_velo = h.velo_id
             WHERE v.type_velo_id = %s
             AND h.date_consultation >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
             GROUP BY v.id_velo, v.nom_velo
             ORDER BY nb_consultations DESC'''
    mycursor.execute(sql, (id_categorie,))
    articles_historique = mycursor.fetchall()
    
    # Préparer les données pour les graphiques
    labels_articles = [item['nom_velo'] for item in articles_wishlist]
    values_wishlist = [item['nb_wishlist'] for item in articles_wishlist]
    values_historique = [item['nb_consultations'] for item in articles_historique]
    
    return render_template('admin/dataviz/dataviz_etat_1.html',
                         categorie=categorie,
                         articles_wishlist=articles_wishlist,
                         articles_historique=articles_historique,
                         labels_articles=labels_articles,
                         values_wishlist=values_wishlist,
                         values_historique=values_historique,
                         id_categorie=id_categorie)


