#Application de pr´eparation des donn´ees

En corr´elation avec la chaˆıne de pr´eparation des donn´ees de chaque outils et ayant `a
disposition une application Python nous avons alors d´ecid´es de mettre en place des
options de pr´eparation des donn´ees pour chaque outils.
Cela nous offre donc la possibilit´e de traiter rapidement un gros
volume d’informations et ainsi passer ces informations dans chaque outils cit´es pr´ec´edemment.
L’enjeu repose ainsi sur le format qu’attend chaque outils en param`etre pour produire
des donn´ees r´esultats.
Mais ´egalement de l’importance de garder une librairie structur´ee de l’ensemble des
informations.

===

##Fonctionnalit´es impl´ement´ees

L’application Python dispose d’un menu permettant de choisir chaque options sp´ecifiques `a chaque outils.

###Fusion des fichiers Json :
Compte-tenu des donn´ees brutes fournies par la maˆıtrise d’ouvrage qui contenaient
trois types de fichiers , nous avons propos´e `a la maˆıtrise d’ouvrage , une fusion de ces
fichiers pour un traitement optimal.
On obtient donc un fichier concat´enant ces trois types de fichiers.
-

###Grobid :
Informations recherch´ees : Contenu des articles d’un ou plusieurs articles format PDF
Fichiers g´en´er´es : fichiers d’informations structur´ees au format TEI.XML pour chaque
article.
###TXM :
Informations brutes : Ensemble de tous les fichiers json fusionn´e au nombre de 1330.
Informations recherch´ees : Contenu des articles au format TXT et un fichier CSV
Fichiers g´en´er´es : Corpus contenant les r´esum´es en format TXT.
###Iramuteq :
Informations brutes : Ensemble de tous les fichiers json fusionn´e au nombre de 1330.
Informations recherch´ees : L’ensemble des r´esum´es des articles.
Fichiers g´en´er´es : corpus texte au format iramuteq.
