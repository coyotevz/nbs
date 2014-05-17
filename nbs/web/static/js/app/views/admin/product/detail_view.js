define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/toolbar',
  'views/sidebar',
], function(_, Chaplin, View, Toolbar, Sidebar) {
  "use strict";

  var DetailSidebar = Sidebar.extend({
    template: 'admin/product/detail_sidebar.html',

    events: {
      'click .new-product': 'newProduct',
    },

    newProduct: function() {
      _dialog.show();
      //Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

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

  var BasicInfoView = View.extend({
    template: 'admin/product/basic_info.html',

    events: {
      'click [name=edit]': 'edit',
    },

    edit: function() {
      console.log('TODO: This must show basic info editor');
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

  var ProductDetailView = View.extend({
    template: 'admin/product/detail.html',

    render: function() {
      ProductDetailView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    initSubviews: function() {
      var toolbar, sidebar, basicinfo, stock;
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
