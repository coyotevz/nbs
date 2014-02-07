define([
  'models/base/model'
], function(Model) {
  "use strict";

  var Product = Model.extend({

    urlRoot: '/api/products',

    defaults: {
    },

    validation: {
      'sku': {
        required: true,
      },
      'description': {
        required: true,
      },
      'price': {
        required: true,
      },
    },

  });

  return Product;
});
