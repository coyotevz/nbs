define([
  'underscore',
  'views/base/view',
  'models/product',
  'views/search',
], function(_, View, Product, SearchDialogView) {
  "use strict";

  var letter = /^[a-z]$/,
      number = /^\d$/;

  var ProductSearchDialog = SearchDialogView.extend({

    listen: {
      'hide': function() {
        var cf = this.currentFocus;
        if (this.selected) {
          this.selected.fetch({ async: false });
          cf._setProduct(this.selected);
        } else {
          _.defer(function() {
            // _.defer here is necessary for Firefox to work properly
            cf.$('input:first').focus();
          });
        }
      }
    },

    search: function(terms) {
      var view = this;
      terms = terms.split(' ');
      this.collection.many({description: { contains: terms }}, {
        success: function(collection, resp, options) {
          view.trigger('fetched', collection);
        }
      });
    },

    updateTerms: function(items) {
      if (this.term && this.term !== '' && items) {
        var re = new RegExp(this.term.split(' ').join("|"), 'ig');
        _.each(items, function(item, index, list) {
          var view = this.subview('itemView:'+item.cid),
              $e = view.$('.cell-description');
          $e.html($e.text().replace(re, '<span class="matched">$&</span>'));
        }, this);
      }
    },

  });

  var BaseRowView = View.extend({
    template: 'pos/document_item_row.html',
    container: 'tbody',
    tagName: 'tr',

    bindings: {
      '.sku': {
        observe: 'sku',
        updateModel: false,
      },
      '.cell-total-price span': {
        observe: 'total',
        onGet: $.numeric,
        afterUpdate: '_showPrice',
      },
      '.cell-unit-price span': {
        observe: 'price',
        onGet: $.numeric,
        afterUpdate: '_showPrice',
      },
      '.description': {
        observe: 'description',
        afterUpdate: '_showDescription',
      },
      '.quantity': {
        observe: 'quantity',
        updateModel: false,
      },
      '.stock-info': {
        observe: ['product', 'product.stock'],
        onGet: function(values, options) {
          var qty, product = this.model.get("product");
          if (product && product.has('stock')) {
            qty = product.get('stock.quantity');
          }

          if (qty !== undefined) { return 'Stock: ' + $.number(qty, 0); }
          return 'Sin control de stock';
        },
      },
    },

    initialize: function() {
      BaseRowView.__super__.initialize.apply(this, arguments);
      this.initUiEvents();
    },

    _showPrice: function($el, val, options) {
      if (this.model.get('price')) {
        $el.css('visibility', 'visible');
      } else {
        $el.css('visibility', 'hidden');
      }
    },

    _showDescription: function($el, val, options) {
      if (this.model.get('description')) {
        this.$('.container-description').css('visibility', 'visible');
      } else {
        this.$('.container-description').css('visibility', 'hidden');
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
      $target.parents('.border').toggleClass("focused", evt.type == "focusin");
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
      var product,
          val = $(evt.target).val();
      if (this.model.has('product') && this.model.get('product.sku') == val) {
        product = this.model.get('product');
        product.fetch();
      } else if (/^\d/.test(val)) {
        product = Product.search.one(
          {sku: val.toUpperCase()},
          {data: { fields: ['sku', 'description', 'stock', 'price'] }}
        );
      } else {
        return false;
      }

      if (product !== undefined) {
        this._setProduct(product);
      }
      return false;
    },

    _setProduct: function(product) {
      this.model.set('product', product);
      var q = this.$('.quantity'),
          val = q.val() || 1;
      q.val(val).css({'visibility': 'visible'}).focus().select();
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
          this.trigger('remove', this);
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
        _dialog.run({
          view: ProductSearchDialog,
          template: 'pos/search_product.html',
          firstChar: ks,
          currentFocus: this,
          collection: Product.search,
          delay: 50,
        });
        return false;
      }
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
