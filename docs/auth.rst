.. _auth:

Autenticación
=============

Aquí se describe el proceso de autenticación y su utilización en el sistema
Nobix.

La authenticación se utiliza de varios modos en el sistema, las más comúnes son
en la API REST y en la interfaz de administración.

Obtención del ``Private Token``
-------------------------------

Para obtener el ``Private Token`` se debe realizar una petición contra la url
``/auth/login`` especificando el usuario y la contraseña como parámetros
``username`` y ``password``, ejemplo::

    http --json :5000/auth/login username=admin password=admin

esto nos devuelve un  mensaje de estado y el ``private_token`` que utilizaremos
de aquí en adelante.

.. sourcecode:: javascript

    {
      "login": "OK",
      "private_token": "WZGicHpiU7gpDJi750ib"
    }

Uso de la autenticación
-----------------------

Todos las peticiones a la API requieren autenticación por parte del usuario.  Es
necesario el parámetro ``private_token`` en la url o en la cabecera de la
petición.  Si se pasa en la cabecera, el nombre debe ser ``PRIVATE-TOKEN`` (en
mayusculas y con el guión medio en lugar del guión bajo).  Ud. puede encontrar
y reestablecer su ``private_token`` en su perfil de usuario.

Si no se especifica o si el ``private_token`` es inválido se devolverá un
mensaje de error con el código ``401``:

.. sourcecode:: javascript

    {
      "message": "401 Unauthorized"
    }

Ejemplo de una petición correcta:

.. sourcecode:: http

    GET http://example.com/api/documents?private_token=QVy1PB7sTxfy4pqfZM1U

Ejemplo de una petición correcta usando curl y autenticación por cabecera::

    curl --header "PRIVATE-TOKEN: QVy1PB7sTxfy4pqfZM1U" "http://example.com/api/documents"

Ejemplo de petición utilizando httpie::

    http :5000/api/suppliers/1 private_token=QVy1PB7sTxfy4pqfZM1U

o::

    http :5000/api/suppliers/1 PRIVATE-TOKEN:QVy1PB7sTxfy4pqfZM1U
