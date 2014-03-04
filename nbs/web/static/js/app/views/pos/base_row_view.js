define([
  'underscore',
  'views/base/view',
  'models/product',
  'models/document_item',
], function(_, View, Product, DocumentItem) {
  "use strict";

  var letter = /^[a-z]$/,
      number = /^\d$/;

  var BaseRowView = View.extend({
    template: 'pos/document_item_row.html',
    container: 'tbody',
    tagName: 'tr',
    fallbackSelector: '.fallback',
    loadingSelector: '.loading',

    bindings: {
      '.cell-total-price span': {
        observe: 'total',
        onGet: $.numeric,
        afterUpdate: '_show',
      },
      '.cell-unit-price span': {
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

    initialize: function() {
      BaseRowView.__super__.initialize.apply(this, arguments);
      this.initUiEvents();
    },

    _show: function($el, val, options) {
      if (this.model.get('price')) {
        $el.css('visibility', 'visible');
      } else {
        $el.css('visibility', 'hidden');
      }
    },

    initUiEvents: function() {
      this.delegate('click', '.composed-field', this.onComposedClick);
      this.delegate('focusin focusout', 'input', this.onInputFocusChange);
      this.delegate('keydown', 'input.sku', this.onSkuKeydown);
      this.delegate('keydown', 'input.quantity', this.onQuantityKeydown);
    },

    onComposedClick: function(evt) {
      this.$('.composed-field input').focus();
    },

    onInputFocusChange: function(evt) {
      var $target = $(evt.target);
      if (evt.type == "focusin") {
        $target.select();
        if ($target.is("input.sku")) {
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
        content.scrollTop(cellBottom - content.height() + 3);
      }
    },


    _handle_return_tab: function(evt) {
      // search and get one article based on user provided sku
      var product, val = $(evt.target).val();
      if (/^\d/.test(val)) {
        product = Product.search.one({sku: val.toUpperCase()});
      } else {
        return false;
      }

      if (product !== undefined) {
        this.model.set('product', product);
        var q = this.$('.quantity');
        val = q.val() || 1;
        q.val(val).focus().select();
      }
      return false;
    },

    onSkuKeydown: function(evt) {

      var k = $.keycode(evt);

      switch(k) {
        case 'return':
        case 'tab':
          return this._handle_return_tab(evt);

        case 'up':
          this.$el.prev().find('input:first').focus();
          return false;

        case 'down':
          this.$el.next().find('input:first').focus();
          return false;

        case 'esc':
          // TODO: Forzar la actualización del campo código
          console.log("// TODO: actualizar a codigo anterior");
          return false;

        case 'ctrl+d':
          // TODO: Forzar la eliminación de la fila.
          console.log("// TODO: eliminar fila");
          return false;

        case '*':
        case '.':
        case '#':
        case '@':
          // TODO: Lanzar busqueda basado en los caracteres
          console.log("// TODO: lanzar busqueda");
          return false;
      }

      var ks = k.split('shift+')[0] || k;
      if (letter.test(ks) && evt.target.selectionStart === 0) {
        console.log("// TODO: lanzar busqueda que comience con", ks);
        return false;
      }

      console.log("Unhandled input:", k);

    },

    onQuantityKeydown: function(evt) {
      if ($.keycode_is(evt, 'return tab')) {
        this.model.set('quantity', $(evt.target).val());
        this.trigger('row-done', $(evt.target));
        return false;
      }
    },

  });

  return BaseRowView;
});
