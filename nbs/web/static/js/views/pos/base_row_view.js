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
      '.total-price span': {
        observe: 'total',
        onGet: $.numeric,
        afterUpdate: '_show',
      },
      '.unit-price span': {
        observe: 'price',
        onGet: $.numeric,
        afterUpdate: '_show',
      },
      '.description': 'description',
      '.quantity': {
        observe: 'quantity',
        updateModel: false,
      }
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

    _show: function($el, val, options) {
      if (this.model.get('price')) {
        $el.css('visibility', 'visible');
      } else {
        $el.css('visibility', 'hidden');
      }
    },

    onProductChange: function(model, product, options) {
      if (product !== null) {
        this.model.set(product.pick("sku", "description", "price"));
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
      if (evt.type == "focusin") {
        $target.select();
        if ($target.is("input.code")) {
          this.checkScrollFor($target);
        }
      }
      $target.parent().toggleClass("focused", evt.type == "focusin");
    },

    checkScrollFor: function(cell) {
      var content = cell.parents('#content'),
      table = cell.parents('table'),
      cellTop = cell.offset().top - table.offset().top,
      cellBottom = cellTop + cell.outerHeight(),
      scrollTop = content.scrollTop(),
      newScroll;

      if (cellTop < scrollTop) {
        content.scrollTop(cellTop - 3);
      } else if (cellBottom > scrollTop + content.height()) {
        content.scrollTop(cellBottom - content.height() + 3)
      }
    },

    onCodeKeydown: function(evt) {

      if ($.keycode_is(evt, 'return tab')) {
        // search and get one article based on user provided sku
        var product, val = $(evt.target).val();

        if (/^\d/.test(val)) {
          product = this.search.one({sku: val.toUpperCase()});
        } else {
          return false;
        }

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
      if ($.keycode_is(evt, 'return tab')) {
        this.model.set('quantity', $(evt.target).val());
        this.trigger('row-done', $(evt.target));
        return false;
      };
    },

  });

  return BaseRowView;
});
