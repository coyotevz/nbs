define([
  'underscore',
  'views/base/view',
  'models/product',
  'models/search',
  'models/document_item',
], function(m, View, Product, Search, DocumentItem) {
  "use strict";

  var BaseRowView = View.extend({
    template: 'pos/document_item_row.html',
    container: 'tbody',
    tagName: 'tr',
    fallbackSelector: '.fallback',
    loadingSelector: '.loading',

    bindings: {
      '.total-price': { observe: 'total', onGet: $.numeric },
      '.unit-price': { observe: 'price', onGet: $.numeric },
      '.description': 'description',
      '.quantity': 'quantity',
    },

    listen: {
      'change:product model': 'onProductChange',
    },

    model: DocumentItem,

    initialize: function() {
      BaseRowView.__super__.initialize.apply(this, arguments);
      this.initUiEvents();
      Backbone.Validation.bind(this);
      this.search = new Search(Product);
    },

    onProductChange: function(model, product, options) {
      var q = this.$('.unit-price, .total-price');
      if (product !== null) {
        this.model.set(product.pick("sku", "description", "price"));
        q.css('visibility', 'visible');
      } else {
        q.css('visibility', 'hidden');
      }
    },

    initUiEvents: function() {
      this.delegate('click', '.composed-field', this.onComposedClick);
      this.delegate('focusin focusout', 'input', this.onInputFocusChange);
      this.delegate('keydown', 'input.code', this.onCodeKeydown);
      this.delegate('keydown', 'input.quantity', this.onQuantityKeydown);
    },

    onComposedClick: function(evt) {
      this.$('.composed-field input').focus();
    },

    onInputFocusChange: function(evt) {
      var $target = $(evt.target);
      if (evt.type == "focusin") $target.select();
      $target.parent().toggleClass("focused", evt.type == "focusin");
    },

    onCodeKeydown: function(evt) {

      if ($.keycode_is(evt, 'return tab')) {
        // search and get one article based on user provided sku
        var val = $(evt.target).val().toUpperCase(),
            product = this.search.one({sku: val});

        if (product !== undefined) {
          this.model.set('product', product);
          var q = this.$('.quantity');
          var val = q.val() || 1;
          q.val(val).focus().select();
        }

        return false;
      } else if ($.keycode_is(evt, 'up')) {
        this.$el.prev().find('input:first').focus();
        return false;
      } else if ($.keycode_is(evt, 'down')) {
        this.$el.next().find('input:first').focus();
        return false;
      }
    },

    onQuantityKeydown: function(evt) {
      throw new Error("BaseRowView#onQuantityKeydown must be overrided!");
    },

  });

  return BaseRowView;
});
