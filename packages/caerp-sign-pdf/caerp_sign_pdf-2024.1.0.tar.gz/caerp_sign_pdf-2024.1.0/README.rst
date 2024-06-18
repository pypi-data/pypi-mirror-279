CAERP Sign PDF
======================================================

Cette librairie a pour objectif de fournir un ensemble cohérent pour la signature et l'horodatage électronique des fichiers PDF issus de [CAERP](https://framagit.org/caerp/caerp).



Activation du module
---------------------

L'API publique est configurable dans CAERP au travers du fichier de configuration .ini.


** Assurez-vous que la librairie `caerp_sign_pdf` est bien dans les `pyramid.includes` **

.. code-block:: console

   pyramid.includes = ...
                      ...
                      caerp_sign_pdf


** Configurez le service `caerp.interfaces.ISignPDFService` **

.. code-block:: console

   caerp.interfaces.ISignPDFService = caerp_sign_pdf.public.SignPDFService


** Configurez le chemin vers le certificat à utiliser pour signer et sa clé secrète **

.. code-block:: console

   caerp.sign_certificate_path=/path/to/certificate.pfx
   caerp.sign_certificate_passphrase=**************************


** Configurez les journaux de `caerp_sign_pdf` **

Voir la [documentation sur le module Python `logging`](https://docs.python.org/2/library/logging.html) pour le détail ainsi que les exemples dans le fichier development.ini.sample.
