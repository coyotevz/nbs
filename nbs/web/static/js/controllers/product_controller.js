define([
  'controllers/admin_controller',
  'models/product',
  'models/product_collection',
  'views/admin/product/list_view',
  'views/admin/product/detail_view',
  'views/admin/product/edit_view',
  'views/admin/product/sidebar_view',
  'views/admin/product/toolbar_view',
], function(AdminController,
            Product,
            ProductsCollection,
            ProductListView,
            ProductDetailView,
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

    list: function(params) {
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
      console.log('Product#show', params);
      var model;
      model = Product.findOrCreate({id: params.id});
      model.fetch();
      this.view = new ProductDetailView({
        region: 'content',
        model: model,
      });
    },

    edit: function(params) {
      console.log('Product#edit(%s)', JSON.stringify(params));
    },

  });

  return ProductController;
});
