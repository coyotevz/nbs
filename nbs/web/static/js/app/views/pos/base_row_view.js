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

    listen: {
      'show': function() {
        this.$('[name=term]').focus().val(this.firstChar || '');
      },
      'hide': function() {
        var cf = this.currentFocus,
            selector = 'input:first';
        if (this.selected) selector = 'input.quantity';
        // _.defer here is necessary for Firefox to work properly
        _.defer(function() {
          cf.find(selector).focus();
        });
      },
      'beforeReposition': function() {
        this.resize();
      },
      'visibilityChange': 'updateTerms',
    },

    render: function() {
      this.collection.reset();
      SearchDialogView.__super__.render.apply(this, arguments);
      this.delegate('keydown', '[name=term]', this.onTermKeydown);
      this.delegate('keyup', '[name=term]', this.onTermKeyup);
      this.$term = this.$('[name=term]');
      this.dialog.$d.addClass('search-dialog');
      this.$('table').fixHeader();
      // Only for debug, remove this
      this.search(this.$term.val().trim());
    },

    resize: function() {
      var availableHeight = this.$el.height() - this.$('.modal-header').outerHeight(true) - this.$('.modal-footer').outerHeight(true);
      this.$('.search-container').height(availableHeight);
    },

    onTermKeydown: function(evt) {
      var k = $.keycode(evt);

      switch(k) {
        case 'esc':
          this.dialog.close();
          return false;
        case 'down':
          console.log('down pressed!');
          return false;
        case 'up':
          console.log('up pressed!');
          return false;
        case 'return':
          console.log('return pressed!');
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
      terms = terms.split(' ');
      this.collection.many({description: {contains: terms}});
    },

    // debounce to avoid multiple calls
    updateTerms: _.debounce(function(items) {
      if (this.term && this.term !== '' && items) {
        var re = RegExp(this.term.split(' ').join("|"), 'ig');
        _.each(items, function(item, index, list) {
          var view = this.subview('itemView:'+item.cid),
              $e = view.$('.cell-description');
          $e.html($e.text().replace(re, '<span class="matched">$&</span>'));
        }, this);
      }
    }, 50),

  });

  var BaseRowView = View.extend({
    template: 'pos/document_item_row.html',
    container: 'tbody',
    tagName: 'tr',

    bindings: {
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
        observe: 'product',
        onGet: function(product, options) {
          if (product) {
            if (product.has('stock')) {
              return 'Stock: ' + $.number(product.get('stock.local'), 0);
            }
            return 'Sin control de stock';
          }
        },
      }
    },

    initialize: function() {
      BaseRowView.__super__.initialize.apply(this, arguments);
      this.initUiEvents();
      // For stylize only
      var $e = this.$el;
      _.defer(function() {
        _dialog.run({
          view: SearchDialogView,
          template: 'pos/search_product.html',
          firstChar: "codo",
          currentFocus: $e,
          collection: Product.search,
          delay: 50,
        });
      });
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
      if (/^\d/.test(val)) {
        product = Product.search.one(
          {sku: val.toUpperCase()},
          {data: { fields: ['sku', 'description', 'stock', 'price'] }}
        );
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
          currentFocus: this.$el,
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
