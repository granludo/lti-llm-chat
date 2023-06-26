# TFG: Chat GPT integrat a Moodle

Per poder provar el funcionament de l'aplicació s'han de seguir els passos següents:

1. Clonar el repositori al teu ordinador.
2. Crear un entorn virtual de Python i activar-lo:

    Windows:

        python -m venv venv
        Per activar-lo, anar al directori ./venv/Scripts i executar: ./activate

    Linux/macOs:

        python3 -m venv venv
        source venv/bin/activate

3. Instalar les dependències de l'aplicació:

    Al directori ./TFG-Pablo/chatgptapp executar:

        pip install -r requirements.txt

4. Iniciar l'aplicació:

    Al directori ./TFG-Pablo/chatgptapp executar:

        python manage.py migrate
        python manage.py runserver

5. Accedir a l'aplicació:

    Per accedir a l'aplicació des de Moodle s'han de seguir els passos següents:

    1. Anar a 'Site administration' - 'Plugins' - 'Manage tools' - 'configure a tool manually'
    2. Introduir un nom i una URL de llançament per a la eina que en aquest cas es http://127.0.0.1:8000/launch
    3. Introduir 'consumer key' i 'shared secret'
    4. En el camp 'Default launch container' seleccionar 'New window' i crear l'eina
    5. Finalment, després de crear l'eina cal anar a 'Home' i crear una nova activitat per a la nova 'External tool' que s'acava de crear


    Per accedir a l'aplicació sense Moodle s'han de seguir els passos següents:

    1. Al directori ./TFG-Pablo/chatgptapp executar:

        python manage.py createsuperuser

    2. Introduir username i password per crear el teu usuari.
    3. Accedir a http://127.0.0.1:8000 i iniciar sessió amb l'usuari que s'acaba de crear.
    4. Tornar a http://127.0.0.1:8000.