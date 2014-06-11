// document sample test
// jshint -W097

"use strict";

var require = require;
var console = console;

var Backbone = require('backbone-associations');

var Product = Backbone.AssociatedModel.extend({
});

var Item = Backbone.AssociatedModel.extend({
  relations: [
    {
      type: Backbone.One,
      key: 'product',
      relatedModel: Product,
    }
  ],
  defaults: {
    quantity: 1,
  },

  initialize: function () {
    Backbone.AssociatedModel.prototype.initialize.apply(this, arguments);
    this.on('change:product', this._updateProduct);
    this.on('change:price change:quantity', this._updateTotal);
    if (this.has('product')) this._updateProduct();
  },

  _updateProduct: function () {
    this.set(this.get('product').pick(['price', 'description']));
  },

  _updateTotal: function () {
    if (this.has('price') && this.has('quantity')) {
      this.set('total', this.get('price') * this.get('quantity'));
    }
  },
});

var Items = Backbone.Collection.extend({
  model: Item,
});

var Customer = Backbone.AssociatedModel.extend({
});

var Salesman = Backbone.AssociatedModel.extend({
});

var Document = Backbone.AssociatedModel.extend({
  relations: [
    {
      type: Backbone.Many,
      key: 'items',
      collectionType: Items,
    },
    {
      type: Backbone.One,
      key: 'customer',
      relatedModel: Customer,
    },
    {
      type: Backbone.One,
      key: 'salesman',
      relatedModel: Salesman,
    }
  ],

  initialize: function() {
    Document.__super__.initialize.apply(this, arguments);
    this.on('add:items remove:items', this._updateTotal);
    this.on('change:items[*].total', this._updateTotal);
    if (this.has('items')) this._updateTotal();
  },

  _updateTotal: function() {
    var total = this.get('items').reduce(function(t, i) {
      return t + i.get('total');
    }, 0);
    this.set('total', total);
  },
});

// Create some data
var p1 = new Product({id: 1, description: "Product 1", price: 1.10});
var p2 = new Product({id: 2, description: "Product 2", price: 1.20});
var p3 = new Product({id: 3, description: "Product 3", price: 1.30});

var c1 = new Customer({id: 1, name: "Customer 1"});
var c2 = new Customer({id: 2, name: "Customer 2"});

var s1 = new Salesman({id: 1, name: "Salesman 1"});
var s2 = new Salesman({id: 2, name: "Salesman 2"});

var i1 = new Item({id: 1, product: p1, quantity: 3});
var i2 = new Item({id: 2, product: p2});
