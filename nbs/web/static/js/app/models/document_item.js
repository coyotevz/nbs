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
      this.on('change:quantity change:price', this.recalcTotal);
      this.recalcTotal();
    },

    recalcTotal: function() {
      this.set('total', this.get('price') * this.get('quantity'));
    },

  });

  return DocumentItem;
});
