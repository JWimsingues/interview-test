# Test technique Nalia

## Consignes
L'objectif de ce test est de récupérer par API des données sur Intercom et de les stocker dans une base de donnée sur AWS.
Pour ce faire vous devez : 
* Ecrire la fonction python `import_intercom()` dans le fichier `app.py` du dossier `fargate1` pour extraite toutes les données des contacts et des conversations.
* Stocker ces données dans un bucket S3
* Ecrire la fonction python `etl_datalake_to_datawarehouse` dans le fichier `app.py` du dossier `fargate2` pour transférer les données de la S3 sur la database
* Déployer les images docker sur AWS
* Run les tasks ECS manuellement (sans orchestrateur)

## Info d'environnement

* api intercom : token = `dG9rOjI2N2JmN2VlX2E0MmNfNGFlYl9hZmI4XzRjOGZlYWU0NjMxOToxOjA=`
    * contacts à lire : `tous (9)`
    * conversations à lire : `toutes`
* datalake (bucket S3) : ``nalia-technical-test``
* chemin du fichier à écrire : ``s3://data/users.json`` et ``s3://data/conversations.json``
* datawarehouse (aurora) :
	* `mdp : Pb81F7RFQaPHKWGnLk5q`
	* `user : admin`
	* `port : 3306`
	* `host : database-2.cgvivklne8l4.eu-west-3.rds.amazonaws.com`
	* `db : naliatest`
	* Tables :
		* `conversation`
		* `users`
* endpoint de ECR pour déployer les images : 
	* Scrapping image : `974801592436.dkr.ecr.eu-west-3.amazonaws.com/scrapping`
	* Push db image : `974801592436.dkr.ecr.eu-west-3.amazonaws.com/database`

    
## Optionnels

* écrire un script de CD dans github action qui publie les containers docker à chaque commit
* remonter les erreurs de vos scripts fargate dans un compte sentry
* brancher datadog (ou un autre) sur le compte AWS que l'on vous a donné
    
## Hypothèses simplificatrices pour le test

* utiliser des variables en dur dans le code
* lire seulement l'utilisateur qui est donnée
* vider la table de aurora à chaque exécution du fargate pour etre rempli de nouveau
* ré-écrire le fichier dans le datalake à chaque appel sur intercom


## Support

* https://developers.intercom.com/intercom-api-reference/v2.0/reference -> API de référence Intercom
* Pour toute question, contacter alexis@nalia.io
