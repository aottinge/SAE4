DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS velo;
DROP TABLE IF EXISTS type_velo;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS liste_envie;
DROP TABLE IF EXISTS historique;

    CREATE TABLE taille (
        id_taille INT PRIMARY KEY AUTO_INCREMENT,
        libelle_taille VARCHAR(10) NOT NULL
    );

    CREATE TABLE type_velo (
        id_type_velo INT PRIMARY KEY AUTO_INCREMENT,
        libelle_type_velo VARCHAR(50) NOT NULL
    );

    CREATE TABLE velo (
        id_velo INT PRIMARY KEY AUTO_INCREMENT,
        nom_velo VARCHAR(100) NOT NULL,
        prix_velo DECIMAL(10,2) NOT NULL,
        taille_id INT NOT NULL,
        type_velo_id INT NOT NULL,
        matiere VARCHAR(50),
        description TEXT,
        fournisseur VARCHAR(100),
        marque VARCHAR(50),
        image VARCHAR(255),
        stock INT,
        FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
        FOREIGN KEY (type_velo_id) REFERENCES type_velo(id_type_velo)
    );

    CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(255),
   password VARCHAR(255),
   email VARCHAR(255),
   role VARCHAR(255),
   est_actif tinyint(1),
   nom VARCHAR(255),
   PRIMARY KEY(id_utilisateur)
);

    CREATE TABLE etat (
        id_etat INT PRIMARY KEY AUTO_INCREMENT,
        libelle VARCHAR(50) NOT NULL
    );

    CREATE TABLE commande (
        id_commande INT PRIMARY KEY AUTO_INCREMENT,
        date_achat DATETIME NOT NULL,
        utilisateur_id INT NOT NULL,
        etat_id INT NOT NULL,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
    );

    CREATE TABLE ligne_commande (
        commande_id INT NOT NULL,
        article_id INT NOT NULL,
        prix DECIMAL(10,2) NOT NULL,
        quantite INT NOT NULL,
        PRIMARY KEY (commande_id, article_id),
        FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        FOREIGN KEY (article_id) REFERENCES velo(id_velo)
    );

    CREATE TABLE ligne_panier (
        utilisateur_id INT NOT NULL,
        article_id INT NOT NULL,
        quantite INT NOT NULL,
        date_ajout DATETIME NOT NULL,
        PRIMARY KEY (utilisateur_id, article_id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (article_id) REFERENCES velo(id_velo)
    );

    CREATE TABLE liste_envie (
        id_liste_envie INT PRIMARY KEY AUTO_INCREMENT,
        utilisateur_id INT NOT NULL,
        velo_id INT NOT NULL,
        date_ajout DATETIME NOT NULL,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (velo_id) REFERENCES velo(id_velo)
    );

    CREATE TABLE historique (
        id_historique INT PRIMARY KEY AUTO_INCREMENT,
        utilisateur_id INT NOT NULL,
        velo_id INT NOT NULL,
        date_consultation DATETIME NOT NULL,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (velo_id) REFERENCES velo(id_velo)
    );

    INSERT INTO taille (libelle_taille) VALUES
    ('XS'),
    ('S'),
    ('M'),
    ('L'),
    ('XL');

    INSERT INTO type_velo (libelle_type_velo) VALUES
    ('VTT'),
    ('Vélo de route'),
    ('Vélo électrique'),
    ('Vélo cargo'),
    ('VTT électrique');


INSERT INTO velo (nom_velo, prix_velo, taille_id, type_velo_id, matiere, description, fournisseur, marque, image,stock) VALUES
('VanMoof S3', 2298.00, 2, 3, 'Aluminium', 'Vélo électrique intelligent avec technologie intégrée', 'VanMoof B.V.', 'VanMoof','VanMoof-S3.png',10),
('Specialized Roubaix Pro SL8', 3999.00, 4, 2, 'Carbone', 'Vélo de route haut de gamme avec technologie d''amortissement', 'Specialized Bicycle Components', 'Specialized','Specialized Roubaix Pro SL8.png',8),
('Trek Domane SL 7', 5499.00, 2, 2, 'Carbone', 'Vélo de course performant pour compétition et endurance', 'Trek Bicycle Corporation', 'Trek','Domane-SL7.png',7),
('Canyon Endurace CF7', 3199.00, 1, 2, 'Carbone', 'Vélo polyvalent pour longues distances et performances', 'Canyon Bicycles', 'Canyon','Endurance-CF-7.png',6),
('Giant Propel Advanced 1', 4499.00, 3, 2, 'Carbone', 'Vélo de course ultra-rapide et aérodynamique', 'Giant Manufacturing', 'Giant','Propel-Advanced-1.png',9),
('Cannondale SuperSix EVO 4', 4799.00, 5, 2, 'Carbone', 'Vélo de compétition léger et réactif', 'Cannondale Bicycle Corporation', 'Cannondale','Supersix-Evo-4.png',5),
('Scott Spark RC', 5999.00, 1, 1, 'Carbone', 'VTT léger et performant pour cross-country', 'Scott Sports SA', 'Scott','Vélo-SCOTT-Spark-RC-SL.png',4),
('Orbea Orca M30', 4500.00, 5, 2, 'Carbone', 'Vélo de course polyvalent et élégant', 'Orbea', 'Orbea','ORCA-M30.png',10),
('Brompton Electric P Line Explore with Roller Frame', 2995.00, 4, 3, 'Acier et aluminium', 'Vélo pliant électrique compact pour la ville', 'Brompton Bicycle Ltd', 'Brompton','Brompton Electric P Line Explore with Roller Frame.png',10),
('BMC Roadmachine Two', 4799.00, 3, 2, 'Carbone', 'Vélo confortable pour longues distances', 'BMC Switzerland', 'BMC','BMC-Roadmachine-TWO.png',5),
('Santa Cruz Nomad', 6999.00, 2, 1, 'Carbone', 'VTT enduro polyvalent pour terrain difficile', 'Santa Cruz Bicycles', 'Santa Cruz','Santa-Cruz-Nomad.png',7),
('Endurance SL e - Sport Shimano 105 12-Speed', 3999.00, 4, 3, 'Carbone', 'Vélo de route électrique haut de gamme', 'Ribble Cycles', 'Ribble','Endurance SL e - Sport Shimano 105 12-Speed.png',8),
('Focus IZALCO MAX 9.9', 4299.00, 4, 2, 'Carbone', 'Vélo de course léger et performant', 'Derby Cycle AG', 'Focus','Focus-IZALCO-MAX-9.9.png',10),
('Lankeleisi MG800Max 2000W',2.599,1,5,'aluminium','VTT électrique avec une autonomie de 100km','Lankeleisi','Lankeleisi','Lankeleisi MG800Max 2000W.png',12),
('BMC Teammachine R 01 Two Shimano Dura Ace Di2', 13999.00, 5, 1, 'carbonne', 'VTT électrique avec une longue autonomie', 'BMC', 'BMC','BMC Teammachine R 01 Two Shimano Dura Ace Di2.png',10),
('LOADY', 3929.00, 1, 4, 'Titane', 'le vélo cargo longtail qui s adapte parfaitement à tous vos besoins.', 'velo-de-ville', 'velo-de-ville','Loady.png',4);

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');

INSERT INTO etat(libelle) VALUES
('en cours de traitement'),
('expédié'),
('validé');


SELECT v.nom_velo, v.prix_velo, t.libelle_taille, tv.libelle_type_velo
FROM velo v
JOIN taille t ON v.taille_id = t.id_taille
JOIN type_velo tv ON v.type_velo_id = tv.id_type_velo
ORDER BY v.prix_velo DESC;

SELECT tv.libelle_type_velo, COUNT(*) as nombre_velos
FROM velo v
JOIN type_velo tv ON v.type_velo_id = tv.id_type_velo
GROUP BY tv.libelle_type_velo;

SELECT nom_velo, prix_velo, matiere
FROM velo
WHERE matiere LIKE '%carbone%' AND prix_velo > 4000
ORDER BY prix_velo;

SELECT tv.libelle_type_velo, ROUND(AVG(v.prix_velo), 2) as prix_moyen
FROM velo v
JOIN type_velo tv ON v.type_velo_id = tv.id_type_velo
GROUP BY tv.libelle_type_velo;

SELECT login, email, role
FROM utilisateur
ORDER BY role;

SELECT v.nom_velo, v.prix_velo, t.libelle_taille
FROM velo v
JOIN taille t ON v.taille_id = t.id_taille
WHERE t.libelle_taille = 'XL';

SELECT DISTINCT marque
FROM velo
ORDER BY marque;


SELECT v.nom_velo, v.prix_velo, v.image, le.date_ajout
FROM liste_envie le
JOIN velo v ON le.velo_id = v.id_velo
WHERE le.utilisateur_id = :utilisateur_id
ORDER BY le.date_ajout DESC;


SELECT v.nom_velo, v.prix_velo, v.image, h.date_consultation
FROM historique h
JOIN velo v ON h.velo_id = v.id_velo
WHERE h.utilisateur_id = :utilisateur_id
ORDER BY h.date_consultation DESC;


