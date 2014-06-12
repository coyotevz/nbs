define([
  'backbone',
  'models/base/model',
  'models/base/collection',
  'models/search',
], function(Backbone, Model, Collection, Search) {
  "use strict";

  var StockInfo = Model.extend({
  });

  var SupplierInfo = Model.extend({
    idAttribute: 'supplier_id',
  });

  var SupplierInfoCollection = Collection.extend({
    model: SupplierInfo,
    url: function() {
      return this.product.url() + '/suppliers_info';
    },

    initialize: function(product) {
      SupplierInfoCollection.__super__.initialize.apply(this, arguments);
      this.product = product;
    },

    parse: function(data) {
      var objects = data.suppliers_info || data;

      this.product_id = data.product_id || null;
      return objects;
    },
  });

  var Product = Model.extend({

    urlRoot: '/api/products',

    relations: [{
      type: Backbone.One,
      key: 'stock',
      relatedModel: StockInfo,
    },
    {
      type: Backbone.Many,
      key: 'suppliers_info',
      collectionType: SupplierInfoCollection,
      relatedModel: SupplierInfo,
    }],

    defaults: {
      suppliers_info: [],
    },

    validation: {
      'sku': 'validateSku',
      'description': {
        required: true,
      },
      'price': {
        required: true,
      },
    },

    initialize: function() {
      Product.__super__.initialize.apply(this, arguments);
      var prod = this;
      //this.get('suppliers_info').url = function() {
      //  return prod.urlRoot + '/' + prod.id + '/suppliers_info';
      //};
    },

    getSuppliersInfo: function() {
      if (!this._spi) {
        this._spi = new SupplierInfoCollection(this);
      }
      return this._spi;
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
  window.Product = Product;

  return Product;
});
