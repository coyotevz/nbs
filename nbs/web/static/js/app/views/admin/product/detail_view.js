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

  // TODO: Remove this toolbar
  var DetailToolbar = Toolbar.extend({
    template: 'admin/product/detail_toolbar.html',

    events: {
      'click [name=edit]': 'edit',
      'click [name=delete]': 'delete',
    },

    edit: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      Chaplin.utils.redirectTo({
        name: 'product_edit',
        params: { id: this.view.model.id }
      });
    },

    delete: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      console.log('delete');
    },
  });

  var EditBasicInfoDialog = EditDialogContent.extend({
    content_form: 'admin/product/basic_info_edit.html',

    listen: {
      'change model': 'onModelChange',
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

    save: function() {
      console.log('this.model:', this.model);
      console.log('save on basic info');
      this.model.save(this.model.getPatch(), {patch: true, validate: false});
    },

    cancel: function() {
      this.dialog.close();
    },

    onModelChange: function(model, options) {
      if (options.stickitChange) {
        var isValid = model.isValid(options.stickitChange.observe),
            enabled = isValid && model.hasStoredChange() && _.isEmpty(model.validationError || {});
        this.$('[name=save]').attr('disabled', !enabled);
      }
    },
  });

  var BasicInfoView = View.extend({
    template: 'admin/product/basic_info.html',

    events: {
      'click [name=edit]': 'edit',
    },

    edit: function() {
      //Chaplin.utils.redirectTo({
      //  name: 'product_edit',
      //  params: { id: this.model.id }
      //});
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
