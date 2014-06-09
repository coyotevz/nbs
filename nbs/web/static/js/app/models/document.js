define([
  'models/base/model',
  'models/base/collection',
  'models/document_item',
], function(Model, Collection, DocumentItem) {
  "use strict";

  var DocumentItemsCollection = Collection.extend({
    model: DocumentItem,
    url: function() {
      return this.document.url() + '/items';
    },

    initialize: function(document) {
      DocumentItemsCollection.__super__.initialize.apply(this, arguments);
      this.document = document;
    },

    parse: function(data) {
      var objects = data.document_items || data;

      this.document_id = data.document_id || null;
      return objects;
    },
  });

  var Document = Model.extend({
    urlRoot: '/api/documents',

    defaults: {
      type: 'FAC',
      total: 0,
      customer: null,
      //items: [],
    },

    //relations: [
    //  {
    //    type: Backbone.Many,
    //    key: 'items',
    //    collectionType: DocumentItems,
    //  },
    //  // TODO: Add relations to: customer, salesman
    //],

    initialize: function() {
      Model.prototype.initialize.apply(this, arguments);
      //this.on('add:items remove:items', this.updateTotal);
      //this.on('change:items[*].total', this.updateTotal);
      //if (this.has('items')) {
      this.updateTotal();
    },

    getItems: function() {
      if (!this._items) {
        var items = new DocumentItemsCollection(this);
        // bind some events
        items.on('add remove', this.updateTotal, this);
        items.on('change:total', this.updateTotal, this); // FIXME:?? test if work
        this._items = items;
      }
      return this._items;
    },

    updateTotal: function() {
      //var total = this.get('items').reduce(function(tot, item) {
      var total = this.getItems().reduce(function(tot, item) {
        return tot + item.get('total');
      }, 0);
      this.set('total', total);
    },
  });

  /*
  var Document = Model.extend({

    urlRoot: '/api/documents',

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
  */

  return Document;
});
