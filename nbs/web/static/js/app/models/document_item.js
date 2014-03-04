define([
  'backbone',
  'models/base/model',
  'models/product',
], function(Backbone, Model, Product) {
  "use strict";

  var DocumentItem = Model.extend({
    /* Posible fields
     * ~~~~~~~~~~~~~~
     *
     * product_id (reference to Product)
     * sku
     * description
     * quantity
     * price
     * total
     * line_order
     */

    relations: [{
      type: Backbone.One,
      key: 'product',
      relatedModel: Product,
    }],

    defaults: {
      quantity: 1,
      total: 0,
    },

    validation: {
      quantity: {
        required: true,
        pattern: 'number',
      },
    },

    initialize: function(attributes, options) {
      Model.prototype.initialize.apply(this, arguments);
      this.on('change:quantity change:price', this.updateTotal);
      this.on('change:product', this.updateProduct);
      if (this.has('product')) {
        this.updateProduct();
      }
    },

    updateTotal: function() {
      if (this.has('price') && this.has('quantity')) {
        this.set('total', this.get('price') * this.get('quantity'));
      }
    },

    updateProduct: function() {
      if (this.has('product')) {
        this.set(this.get('product').pick(['price', 'sku', 'description']));
      }
    },

  });

  return DocumentItem;
});
