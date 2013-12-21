define([
  'controllers/admin_controller',
], function(AdminController) {
  "use strict";

  var ProductController = AdminController.extend({
    title: 'Products',

    beforeAction: function() {
      ProductController.__super__.beforeAction.apply(this, arguments);
      this.publishEvent('menu:setCurrent', 'product');
    },

    index: function(params) {
      console.log('Product#index(%s)', params);
    },

  });

  return ProductController;
});
