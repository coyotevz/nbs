define([
  'controllers/admin_controller',
], function(AdminController) {
  "use strict";

  var ProductController = AdminController.extend({
    title: 'Products',

    index: function(params) {
      console.log('Product#index(%s)', params);
    },

  });

  return ProductController;
});
