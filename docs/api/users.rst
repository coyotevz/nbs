.. _api/users:

Usuarios
========

.. http:get:: /users

    Solicita una lista de usuarios.

    **Respuesta:**

    .. sourcecode:: http

        HTTP/1.1 200 OK

        {"objects": 
          [{
            "id": 1,
            "username": "augusto",
            "email": "augusto@rocctech.com.ar",
            "name": "Augusto Roccasalva",
            "state": "active",
            "created_at": "2012-05-23T08:00:58Z",
            "bio": null
          },
          {
            "id": 2,
            "username": "german",
            "email": "german@rioplomo.com.ar",
            "name": "Germán Roccasalva",
            "state": "active",
            "created_at": "2012-05-24T12:42:02Z",
            "bio": null
          }]
        }


.. http:get:: /users/<id>

    Solicita un determinado usuario identificado con ``id``.

    :param id: identificación de usuario.
    :type id: int

    **Respuesta:**

    .. sourcecode:: http
    
       HTTP/1.1 200 OK
    
       {
         "id": 1,
         "username": "augusto",
         "email": "augusto@rocctech.com.ar",
         "name": "Augusto Roccasalva",
         "state": "active",
         "created_at": "2012-05-23T08:00:58Z",
         "bio": null
       }


.. http:post:: /users

    Crea un nuevo usuario. Solo los administradores puede crear nuevos
    usuarios.

    :param email: El email del usuario.
    :type email: requerido
    :param password: La contraseña de usuario.
    :type password: requerido
    :param username: Nombre de usuario.
    :type username: requerido
    :param name: Nombre completo del usuario.


.. http:put:: /users/<id>

    Modifica un usuario existente. Solo los administradores pueden cambiar los
    atributos de un usuario.

    :param id: identificación de usuario.
    :type id: requerido


.. http:delete:: /users/<id>

    Elimina un usuario. Disponible solo para los administradores. Esta es una
    función idenpotente, llamar esta función para un usuario no existente
    devuelve :http:statuscode:`200`. La única diferencia si el usuario fue
    realmente eliminado es que devuelve los datos en formato JSON.

    :param id: identificación de usuario.
    :type id: requerido
