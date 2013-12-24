define([
  'controllers/admin_controller',
  'models/product_collection',
  'views/admin/product/list_view',
  'views/admin/product/sidebar_view',
  'views/admin/product/edit_view',
], function(AdminController,
            ProductsCollection,
            ProductListView,
            ProductSidebarView,
            ProductEditView) {
  "use strict";

  var ProductController = AdminController.extend({
    title: 'Products',

    beforeAction: function() {
      ProductController.__super__.beforeAction.apply(this, arguments);
      this.publishEvent('menu:setCurrent', 'product');
      this.compose('sidebar', ProductSidebarView, {region: 'sidebar'});
    },

    index: function(params) {
      this.productList = new ProductsCollection();
      this.view = new ProductListView({
        collection: this.productList,
        region: 'content',
      });
    },

    'new': function(params) {
      this.view = new ProductEditView({region: 'content'});
    },

    edit: function(params) {
      console.log('Product#edit(%s)', JSON.stringify(params));
    },

  });

  return ProductController;
});
