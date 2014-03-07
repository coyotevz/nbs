define([
  'backbone',
  'models/base/model',
  'models/search',
], function(Backbone, Model) {
  "use strict";

  var StockInfo = Model.extend({
  });

  var Product = Model.extend({

    urlRoot: '/api/products',

    relations: [{
      type: Backbone.Many,
      key: 'stock',
      relatedModel: StockInfo,
    }],

    validation: {
      'sku': 'validateSku',
      'description': {
        required: true,
      },
      'price': {
        required: true,
      },
    },

    validateSku: function(val, attr, model) {
      // validate required
      var error = Backbone.Validation.validators.required(val, attr, true, this);
      if (!error) {
        // validate max field length 14
        error = Backbone.Validation.validators.maxLength(val, attr, 14, this);
      }
      if (!error) {
        // Validate start with number
        if (Backbone.Validation.validators.pattern(val, attr, /^\d+.*$/, this)) {
          error = "El código debe comenzar con un número";
        }
      }
      if (!error) {
        // Validate sku uniqueness
        // merge = false is important in options because Backbone.Relations
        // update the current model fields and Backbone.stickit updates current
        // view with server data.
        var product = Product.search.one({sku: val.toUpperCase()}, {merge: false});
        if (product && product.id !== this.id) {
          error = "El código ya es utilizado por otro producto";
        }
      }
      if (error) {
        return error;
      }
    },
  });

  Product.search = new Search(Product);

  return Product;
});
