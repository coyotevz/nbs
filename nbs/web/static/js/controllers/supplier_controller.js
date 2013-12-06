define([
  'controllers/base_admin_controller',
  'views/test_body_view',
], function(BaseAdminController, TestBodyView) {
  "use strict";

  var SupplierController = BaseAdminController.extend({
    title: 'Suppliers',

    beforeAction: function(params, route) {
      SupplierController.__super__.beforeAction.apply(this, arguments);
      this.compose('body', TestBodyView, {'region': 'body'})
    },

    index: function(params) {
      console.log('Supplier#index(%s)', params);
    },

    show: function(params) {
      console.log('Supplier#show(%s)', params);
    },
  });

  return SupplierController;
});
