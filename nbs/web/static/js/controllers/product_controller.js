define([
  'controllers/base_admin_controller',
], function(BaseAdminController) {
  "use strict";

  var ProductController = BaseAdminController.extend({
    title: 'Products',

    index: function(params) {
      console.log('Product#index(%s)', params);
    },

  });

  return ProductController;
});
