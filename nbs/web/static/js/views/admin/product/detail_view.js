define([
  'underscore',
  'chaplin',
  'views/base/view',
], function(_, Chaplin, View) {
  "use strict";

  var DetailToolbar = View.extend({
    template: 'admin/product/detail_toolbar.html',
  });

  var DetailSidebar = View.extend({
    template: 'admin/product/detail_sidebar.html',
  });

  var ProductDetailView = View.extend({
    template: 'admin/product/detail.html',
    noWrap: true,

    render: function() {
      ProductDetailView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    initSubviews: function() {
      var toolbar, sidebar;
      toolbar = new DetailToolbar({region: 'toolbar'});
      this.subview('toolbar', toolbar);
      toolbar.delegate('click', '.btn[name="go-back"]', _.bind(this.goBack, this));

      sidebar = new DetailSidebar({region: 'sidebar'});
      this.subview('sidebar', sidebar);
      sidebar.delegate('click', '.new-product', _.bind(this.newProduct, this));
    },

    // Toolbar callbacks
    goBack: function() {
      Chaplin.utils.redirectTo({name: 'product_list'});
    },

    // Sidebar callbacks
    newProduct: function() {
      Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

  return ProductDetailView;
});
