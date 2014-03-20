define([
  'underscore',
  'views/base/view',
  'views/base/collection_view',
  'models/product',
  'models/document_item',
], function(_, View, CollectionView, Product, DocumentItem) {
  "use strict";

  var letter = /^[a-z]$/,
      number = /^\d$/;

  var SearchDialogRowView = View.extend({
    template: 'pos/search_item_row.html',
    tagName: 'tr',
    className: 'search-result-row',
  });

  var SearchDialogView = CollectionView.extend({
    optionNames: CollectionView.prototype.optionNames.concat([
      'dialog', 'template', 'firstChar', 'currentFocus', 'delay',
    ]),
    term: null,
    timer: null,
    delay: 300,
    listSelector: 'tbody',
    itemView: SearchDialogRowView,
    animationDuration: 0,

    // Internal properties
    _selected_idx: null,

    listen: {
      'show': function() {
        this.$('[name=term]').focus().val(this.firstChar || '');
      },
      'hide': function() {
        var cf = this.currentFocus;
        if (this.selected) {
          this.selected.fetch({ async: false, });
          cf._setProduct(this.selected);
        } else {
          _.defer(function() {
            // _.defer here is necessary for Firefox to work properly
            cf.$('input:first').focus();
          });
        }
      },
      'beforeReposition': function() {
        this.resize();
      },
      'fetched': function(collection) {
        this.updateTerms(collection.models);
        this.select(0);
      },
    },

    render: function() {
      this.collection.reset();
      SearchDialogView.__super__.render.apply(this, arguments);
      this.delegate('keydown', '[name=term]', this.onTermKeydown);
      this.delegate('keyup', '[name=term]', this.onTermKeyup);
      this.$term = this.$('[name=term]');
      this.dialog.$d.addClass('search-dialog');
      this.$('table').fixHeader();
    },

    resize: function() {
      var availableHeight = this.$el.height() - this.$('.modal-header').outerHeight(true) - this.$('.modal-footer').outerHeight(true);
      this.$('.search-container').height(availableHeight);
    },

    onTermKeydown: function(evt) {
      var idx,
          k = $.keycode(evt);

      switch(k) {
        case 'esc':
          this.selected = null;
          this.dialog.close();
          return false;
        case 'down':
          this.moveSelect(+1);
          return false;
        case 'up':
          this.moveSelect(-1);
          return false;
        case 'return':
          if (this.selected) this.dialog.close();
          return false;
      }
    },

    onTermKeyup: function(evt) {
      var terms = this.$term.val().trim();
      if (this.term !== terms) {
        this.term = terms;
        this.collection.cancel();
        if (this.timer) clearTimeout(this.timer);
        if (terms !== '') {
          var search = _.bind(this.search, this, terms);
          this.timer = _.delay(search, this.delay);
        } else {
          this.collection.reset();
        }
      }
    },

    search: function(terms) {
      var view = this;
      terms = terms.split(' ');
      this.collection.many({description: {contains: terms}}, {
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

    moveSelect: function(m) {
      var idx = (this._selected_idx || 0) + m;
      if (idx >= 0 && idx < this.collection.length) {
        this.select(idx);
      }
    },

    select: function(idx) {
      var itemView, selected;
      if (this._selected_idx !== null && this.selected) {
        itemView = this.subview('itemView:'+this.selected.cid);
        if (itemView) itemView.$el.removeClass('selected');
      }
      selected = this.collection.at(idx);
      if (selected) {
        itemView = this.subview('itemView:'+selected.cid);
        if (itemView) {
          itemView.$el.addClass('selected');
          this.checkScrollFor(itemView.$el);
        }
        this._selected_idx = idx;
      } else {
        this._selected_idx = null;
      }
      this.selected = selected;
    },

    checkScrollFor: function(el) {
      var container = this.$('.search-container'),
          gap = this.$('.search-results thead').height(),
          cellTop = el.offset().top - gap,
          cellBottom = cellTop + el.outerHeight() + gap,
          containerTop = container.offset().top,
          containerBottom = containerTop + container.outerHeight(),
          scrollTop = container.scrollTop();

      if (cellTop < containerTop) {
        container.scrollTop(scrollTop - (containerTop - cellTop));
      } else if (cellBottom > containerBottom) {
        container.scrollTop(scrollTop + (cellBottom - containerBottom));
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
        // FIXME: This not always work
        observe: ['product', 'product.stock'],
        onGet: function(values, options) {
          var product = values[0],
              stock = values[1],
              qty;
          if (product && product.has('stock')) {
            qty = product.get('stock.quantity');
          } else if (stock) {
            qty = stock.get('quantity');
          }

          if (qty !== undefined) {
            return 'Stock: ' + $.number(qty, 0);
          }
          return 'Sin control de stock';
        },
        /*
        onGet: function(product, options) {
          console.log('product:', product);
          if (product) console.log('product.stock:', product.get('stock'));
          if (product && product.has('stock')) {
            return 'Disponible: ' + $.number(product.get('stock.quantity'), 0);
          }
          return 'Sin control de stock';
        },*/
      },

      /*
      '.stock-info': {
        observe: 'product.stock',
        onGet: function(stock, options) {
          if (stock) return 'Stock: ' + $.number(stock.get('quantity'), 0);
          else return 'Sin control de stock';
        }
      },*/
    },

    initialize: function() {
      BaseRowView.__super__.initialize.apply(this, arguments);
      this.initUiEvents();
      // For stylize only
      /*
      var $this = this;
      _.defer(function() {
        _dialog.run({
          view: SearchDialogView,
          template: 'pos/search_product.html',
          firstChar: "codo",
          currentFocus: $this,
          collection: Product.search,
          delay: 50,
        });
      });*/
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

      // FIXME: Special events for debug only
      this.model.on('change', function() { console.log('change', arguments); });
      this.model.on('change:product', function() { console.log('change:product', arguments); });
      this.model.on('change:product.stock', function() { console.log('change:product.stock', arguments); });
      this.model.on('change:product.stock.quantity', function() { console.log('change:product.stock.quantity', arguments); });
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
      if (/^\d/.test(val)) {
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
      //console.log('set product:', product);
      //if (this.model.has('product')) console.log('model:', this.model.toJSON());
      this.model.set('product', product);
      //console.log('stock:', this.model.get('product.stock'));
      //console.log('final product.cid:', this.model.get('product').cid);
      var q = this.$('.quantity'),
          val = q.val() || 1;
      q.val(val).focus().select();
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
          view: SearchDialogView,
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
