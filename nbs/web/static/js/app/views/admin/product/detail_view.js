define([
  'jquery',
  'underscore',
  'chaplin',
  'views/base/view',
  'views/base/collection_view',
  'views/base/tab_collection_view',
  'views/toolbar',
  'views/sidebar',
  'views/admin/edit_dialog',
], function($, _, Chaplin, View, CollectionView, TabCollectionView, Toolbar,
            Sidebar, EditDialogContent) {
  "use strict";

  var DetailSidebar = Sidebar.extend({
    template: 'admin/product/detail_sidebar.html',

    events: {
      'click .new-product': 'newProduct',
    },

    t1: function(dialog) {
      console.log('dialog callback t1:', dialog);
    },

    t2: function(dialog) {
      console.log('dialog callback t2:', dialog);
      dialog.close();
    },

    newProduct: function() {
      _dialog.run({
        title: 'Some title',
        text: 'Hello, we are in dialog paragraph.',
        buttons: {
          'success': {
            'label': 'OK',
            'style': 'primary',
            'action': this.t1,
          },
          'cancel': {
            'label': 'Cancel',
            'action': this.t2,
          }
        },
      });
      //Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

  var EditBasicInfoDialog = EditDialogContent.extend({
    content_form: 'admin/product/basic_info_edit.html',
    _changedKeys: [],

    listen: {
      'change model': 'onModelChange',
      'show': 'onShow',
      'hide': 'onHide',
    },

    bindings: {
      '[name=sku]': 'sku',
      '[name=description]': 'description',
      '[name=price]': {
        observe: 'price',
        onGet: $.numeric,
        onSet: function(val) {
          return val.replace('.', '').replace(',', '.');
        }
      },
    },

    onShow: function() {
      this.model.startTracking();
    },

    onHide: function() {
      this.model.stopTracking();
      _.each(this._changedKeys, function(element, index, list) {
        this.model.trigger('change:' + element, this.model, this.model.get(element));
      }, this);
      this._changedKeys = [];
    },

    save: function() {
      var changedAttrs = this.model.unsavedAttributes();
      this._changedKeys = _.keys(changedAttrs);
      this.model.save(changedAttrs, {patch: true, validate: false});
      this.dialog.close();
    },

    cancel: function() {
      this.model.resetAttributes();
      this.dialog.close();
    },

    onModelChange: function(model, options) {
      if (options.stickitChange) {
        var isValid = model.isValid(options.stickitChange.observe),
            enabled = isValid && model.isChanged() && _.isEmpty(model.validationError || {});
        this.$('[name=save]').attr('disabled', !enabled);
      }
    },
  });

  var BasicInfoView = View.extend({
    template: 'admin/product/basic_info.html',

    events: {
      'click [name=edit]': 'edit',
    },

    bindings: {
      '[name=sku]': {
        observe: 'sku',
        updateView: 'mustUpdate',
      },
      '[name=description]': {
        observe: 'description',
        updateView: 'mustUpdate',
      },
      '[name=price]': {
        observe: 'price',
        onGet: function(val) {
          return '$ ' + $.number(val, 2, ',', '.');
        },
        updateView: 'mustUpdate',
      },
    },

    mustUpdate: function(val, options) {
      return !this.model.isTracked();
    },

    edit: function() {
      _dialog.run({
        title: 'Editar información basica',
        view: EditBasicInfoDialog,
        model: this.model,
      });
    },
  });

  var StockView = View.extend({
    template: 'admin/product/stocks.html',

    events: {
      'click [name=detail]': 'detail',
    },

    detail: function() {
      console.log('TODO: This must show stock details & statistics');
    }
  });

  var SupplierInfoItemView = View.extend({
    template: 'admin/product/supplier_info_item.html',
    noWrap: true,

    activate: function() {
      this.$el.addClass("active").addClass("in");
    }
  });

  var SupplierInfoHeaderView = View.extend({
    template: 'admin/product/supplier_info_header.html',
    noWrap: true,

    activate: function() {
      this.$el.addClass("active");
    },
  });

  var SupplierInfoView = TabCollectionView.extend({
    template: 'admin/product/supplier_info.html',
    noWrap: true,
    listSelector: 'div.tab-content',
    headerSelector: 'ul.nav',
    itemView: SupplierInfoItemView,
    headerView: SupplierInfoHeaderView,
    animationDuration: 0,

    events: {
      'click [name=add-supplier]': 'add',
    },

    add: function() {
      console.log('TODO: This must show new supplier info form');
    },
  });

  var ProductDetailView = View.extend({
    template: 'admin/product/detail.html',

    render: function() {
      ProductDetailView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    initSubviews: function() {
      var toolbar, sidebar, basicinfo, stock, spi;
      //toolbar = new DetailToolbar({region: 'toolbar', view: this});
      //this.subview('toolbar', toolbar);
      sidebar = new DetailSidebar({region: 'sidebar', view: this});
      this.subview('sidebar', sidebar);

      basicinfo = new BasicInfoView({
        container: this.$('.basicinfo-container'),
        model: this.model,
      });
      this.subview('basicinfo', basicinfo);
      window.basicinfo = basicinfo;

      stock = new StockView({
        container: this.$('.stock-container'),
        model: this.model,
      });
      this.subview('stock', stock);

      spi = new SupplierInfoView({
        container: this.$('.spi-container'),
        collection: this.model.getSuppliersInfo(),
      });
      this.subview('spi', spi);
      spi.collection.fetch();
    },

    edit: function(evt) {
      evt.preventDefault();
      Chaplin.utils.redirectTo({
        name: 'product_edit',
        params: { id: this.model.id }
      });
    },
  });

  return ProductDetailView;
});
