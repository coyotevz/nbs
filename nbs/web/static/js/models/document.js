define([
  'models/base/model',
  'models/document_items',
  'models/document_item',
], function(Model, DocumentItems, DocumentItem) {
  "use strict";

  var Document = Model.extend({

    urlRoot: '/api/document',

    defaults: {
      type: 'FAC',
      customer: null,
      total: 0,
    },

    initialize: function(attributes, options) {
      Model.prototype.initialize.apply(this, arguments);

      var items = new DocumentItems();
      var appender = new DocumentItem();
      // bind to events of items collection
      this.listenTo(items, 'add remove', this._onItemsAddRemove);
      this.listenTo(items, 'reset', this._onItemsReset);
      this.listenTo(items, 'change', this._onModelChange);
      this.listenTo(items, 'change:total', this._onModelTotalChange);
      this.listenTo(appender, 'change:total', this._onModelTotalChange);

      this.items = items;
      this.appender = appender;
    },

    updateTotal: function() {
      // Recalc total of document
      var total = this.items.reduce(function(memo, model) {
        return memo + model.get('total');
      }, this.appender.get('total') || 0);
      this.set('total', total);
    },

    _onItemsAddRemove: function(model, collection, options) {
      // Check options.add (true || false) to see which event has occurred
      this.updateTotal();
    },

    _onItemsReset: function(collection, options) {
      this.updateTotal();
    },

    _onModelChange: function(model, options) {
    },

    _onModelTotalChange: function(model, value, options) {
      this.updateTotal();
    },
  });

  return Document;
});
