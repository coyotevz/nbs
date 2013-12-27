define([
  'controllers/admin_controller',
  'models/product_collection',
  'views/admin/product/list_view',
  'views/admin/product/edit_view',
  'views/admin/product/sidebar_view',
  'views/admin/product/toolbar_view',
], function(AdminController,
            ProductsCollection,
            ProductListView,
            ProductEditView,
            ProductSidebarView,
            ProductToolbarView) {
  "use strict";

  var ProductController = AdminController.extend({
    title: 'Products',

    beforeAction: function() {
      ProductController.__super__.beforeAction.apply(this, arguments);
      this.publishEvent('menu:setCurrent', 'product');
      //this.compose('sidebar', ProductSidebarView, {region: 'sidebar'});
      //this.compose('toolbar', ProductToolbarView, {region: 'toolbar'});
    },

    index: function(params) {
      this.productList = new ProductsCollection();
      this.view = new ProductListView({
        collection: this.productList,
        region: 'content',
      });
    },

    'new': function(params) {
      this.view = new ProductEditView({
        region: 'content',
      });
    },

    show: function(params) {
      console.log('Product#show(%s)', JSON.stringify(params));
    },

    edit: function(params) {
      console.log('Product#edit(%s)', JSON.stringify(params));
    },

  });

  return ProductController;
});
