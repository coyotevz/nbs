.. _api:

Nobix Application Server API
============================

Esta parte de la documentación se encarga de describir el funcionamiento de la
interfaz de aplicación.


API
---

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

Las peticiones a la API deben ser solicitadas con el prefijo ``api`` en la URL.

Ejemplo de una petición correcta:

.. sourcecode:: http

    GET http://example.com/api/documents?private_token=QVy1PB7sTxfy4pqfZM1U

Ejemplo de una petición correcta usando curl y autenticación por cabecera::

    curl --header "PRIVATE-TOKEN: QVy1PB7sTxfy4pqfZM1U" "http://example.com/api/documents"

La API utiliza JSON para serializar los datos de respuesta, por lo tanto no se
debe especificar el formato esperado al final de la URL.


Código de Estado
~~~~~~~~~~~~~~~~

La API ha sido diseñada para devolver distintos códigos de estado de acuerdo al
contexto y la acción solicitada.  De esta forma si una petición es erronea el
que realizó la petición tiene la posibilidad de investigar que el lo que estubo
mal, por ejemplo el código de estado ``400 Bad Request`` es devuelto si un
atributo requerido está ausente en la petición. La siguiente lista enumera como
se comportan generalmente las funciones de la API.

Tipos de petición (HTTP Verb):

* ``GET`` solicita acceso a uno o más recursos y devuelve el resultado en
  formato JSON.

* ``POST`` esta solicitud devuelve ``201 Created`` si el recurso fue creado
  eixtosamente y devuelve el recurso creato en formato JSON.

* ``GET``, ``PUT`` y ``DELETE`` devuelven ``200 Ok`` si el recurso es
  accedido, modificado o borrado exitosamente, el resultado (modificado) es
  devulelto en formato JSON.

* ``DELETE`` solicitud diseñada para ser idempotente, esto significa que una
  solicitud a recurso con este verbo siempre devolverá ``200 Ok`` incluso si
  ha sido borrado anteriormente o nunca existió.  El razonamiento destras de
  esto es que al usuario no le interesa si este recurso existía antes o no.

La siguiente lista muestra los posibles códigos de estado que son devueltos por
la API:

* ``200 Ok`` - Las solicitudes ``GET``, ``PUT`` y ``DELETE`` han sido exitosas,
  el/los recursos/s son devueltos en formato JSON.

* ``201 Created`` - La solicitud ``POST`` fue exitosa y el recurso es devuelto
  en formato JSON.

* ``400 Bad Request`` - Falta un atributo requerido por la solicitud a la API.

* ``401 Unauthorized`` - El usuario no ha sido autenticado, se requiere un
  *token* válido de usuario.

* ``403 Forbidden`` - La solicitud no esta permitida.

* ``404 Not Found`` - El recurso no puede ser accedido.

* ``405 Method Not Allowed`` - La solicitud no es soportada para el método
  dado.

* ``409 Conflict`` - Existe un recurso que genera conflicto, por ejemplo crear
  un artículo con un código que ya existe.

* ``500 Server Error`` - Mientras se procesaba la solicitud algo andubo mal en
  el servidor.


Paginación
~~~~~~~~~~

Cuando se solicita una lista de recursos se pueden utilizar los siguentes
parametros.

* ``page`` (default: **1**) - número de página.

* ``per_page`` (default: **25**, max: **100**) - cantidad de items por página.


Elementos disponibles en la API
-------------------------------

.. toctree::
   :maxdepth: 1

   api/users
   api/suppliers
