define([
  'models/base/model'
], function(Model) {
  "use strict";

  var Product = Model.extend({

    urlRoot: '/api/products',

    defaults: {
    },

    initialize: function(attributes, options) {
      Model.prototype.initialize.apply(this, arguments);
    },

  });

  return Product;
});
