define([
  'controllers/admin_controller',
  'models/product',
  'models/product_collection',
  'views/admin/product/list_view',
  'views/admin/product/detail_view',
  'views/admin/product/edit_view',
], function(AdminController,
            Product,
            ProductsCollection,
            ProductListView,
            ProductDetailView,
            ProductEditView) {
  "use strict";

  var ProductController = AdminController.extend({
    title: 'Products',

    beforeAction: function() {
      ProductController.__super__.beforeAction.apply(this, arguments);
      this.publishEvent('menu:setCurrent', 'product');
    },

    list: function(params) {
      this.productList = new ProductsCollection();
      this.view = new ProductListView({
        collection: this.productList,
        region: 'content',
      });
      // FIXME: For debug only
      window.view = this.view;
    },

    'new': function(params) {
      this.view = new ProductEditView({
        region: 'content',
      });
    },

    show: function(params) {
      console.log('Product#show', params);
      var model = Product.findOrFetch({id: params.id});
      this.view = new ProductDetailView({
        region: 'content',
        model: model,
      });
    },

    edit: function(params) {
      var model = Product.findOrFetch({id: params.id});
      this.view = new ProductEditView({
        region: 'content',
        model: model,
      });
    },

  });

  return ProductController;
});
