.. _api/suppliers:

Proveedores
===========

.. http:get:: /supplier

    Devuelve una lista de proveedores, acepta parametros de búsqueda.

    **Respuesta**

    .. sourcecode:: http

        HTTP/1.1 200 OK

        {
          "page": 1,
          "num_results": 82,
          "num_pages": 4,
          "objects": [{"id": 1, "fancy_name": "IPS", ...}, ...]
        }

.. http:get:: /supplier/<id>

    Devuelve la información de un proveedor identificado con ``id``.

    .. sourcecode:: http

        HTTP/1.1 200 OK

        {
          "id": 1,
          "fancy_name": "IPS",
          "name": "IPS S.A.C.I.yF.",
          "pament_term": 30,
          "contacts": [{"display_name": "Kamel Mirchak", "id": 1, ...}, ...],
          ...
        }

.. http:get:: /supplier/<id>/contacts

    Devuelve los contactos relacionados con el proveedor identificado con
    ``id``.

    .. sourcecode:: http

        HTTP/1.1 200 OK

        {
          "page": 1,
          "num_pages": 1,
          "num_result": 2,
          "objects": [{"display_name": "Kamel Mirchak", "id": 1, ...}, ...],
        }
