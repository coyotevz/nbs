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

    validation: {
      quantity: {
        required: true,
        pattern: 'number',
      },
    },

    relations: [{
      type: Backbone.HasOne,
      key: 'product',
      relatedModel: Product,
      keyDestination: 'product_id',
      includeInJSON: 'id',
    }],

    initialize: function(attributes, options) {
      DocumentItem.__super__.initialize.apply(this, arguments);
      this.on('change:quantity change:price', this.recalcTotal);
      this.recalcTotal();
    },

    recalcTotal: function() {
      this.set('total', this.get('price') * this.get('quantity'));
    },

  });

  return DocumentItem;
});
