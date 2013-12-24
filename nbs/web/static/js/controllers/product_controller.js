define([
  'controllers/admin_controller',
  'models/product_collection',
  'views/admin/product/list_view',
  'views/admin/product/sidebar_view',
], function(AdminController,
            ProductsCollection,
            ProductListView,
            ProductSidebarView) {
  "use strict";

  var ProductController = AdminController.extend({
    title: 'Products',

    beforeAction: function() {
      ProductController.__super__.beforeAction.apply(this, arguments);
      this.publishEvent('menu:setCurrent', 'product');
      this.compose('sidebar', ProductSidebarView, {region: 'sidebar'});
    },

    index: function(params) {
      console.log('Product#index(%s)', JSON.stringify(params));
      this.productList = new ProductsCollection();
      this.view = new ProductListView({
        collection: this.productList,
        region: 'content',
      });
    },

  });

  return ProductController;
});
