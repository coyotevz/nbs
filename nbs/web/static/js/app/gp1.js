/*
 * Grand parent can listen into changes in a (nested) collection
 */

var Backbone = require('backbone-associations');

var Model = Backbone.AssociatedModel.extend({
});
/* Models definition */
var Item = Model.extend({
  defaults: { quantity: 0 }
});

var Cart = Model.extend({
  relations: [
    {
      type: Backbone.Many,
      key: 'items',
      relatedModel: Item,
    }
  ],

  getQuantity: function() {
    return this.get('items').reduce(function(memo, item) {
      return memo + item.get('quantity');
    }, 0);
  },

  defaults: {
    items: undefined,
  }
});

var Account = Model.extend({
  initialize: function() {
    Account.__super__.initialize.apply(this, arguments);
    this.on('change', function() { console.log('change') });
    this.on('change:cart', function() { console.log('change:cart') });
    this.on('change:cart.items', function() { console.log('change:cart.items'); });
    this.on('change:cart.items[*]', function() { console.log('change:cart.items[*]'); });
    this.on('add:cart.items', function() { console.log('add:cart.items'); });
    this.on('add:cart.items[*]', function() { console.log('add:cart.items[*]'); });
  },
  relations: [
    {
      type: Backbone.One,
      key: 'cart',
      relatedModel: Cart,
    }
  ],
  defaults: {
    cart: undefined,
  }
});

var account = new Account();
var cart = new Cart();

console.log("account.set('cart', c);");
account.set('cart', cart);

var i1 = new Item({quantity: 5});
var i2 = new Item({quantity: 7});
var i3 = new Item({quantity: 3});

console.log("cart.set('items', [i1, i2]);");
cart.set('items', [i1, i2]);
console.log("-> current quantity:", cart.getQuantity());

var items = cart.get('items');
console.log("items.add(i3);");
items.add(i3);
console.log("-> current quantity:", cart.getQuantity());

console.log("items.at(0).set('quantity', 10);");
items.at(0).set('quantity', 10);
console.log("-> current quantity:", cart.getQuantity());

/* this don't fire any events */
var a = new Account({
  cart: new Cart({
    items: [
      {quantity: 20},
      {quantity: 21},
      {quantity: 22}
    ],
  })
});

console.log("-> total qty:", a.get('cart').getQuantity());
