define([
  'controllers/admin_controller',
  'views/admin/supplier/test_body_view',
], function(AdminController, TestBodyView) {
  "use strict";

  var SupplierController = AdminController.extend({
    title: 'Suppliers',

    beforeAction: function(params, route) {
      SupplierController.__super__.beforeAction.apply(this, arguments);
      this.compose('body', TestBodyView, {'region': 'body'})
    },

    index: function(params) {
      console.log('Supplier#index(%s)', JSON.stringify(params));
    },

    'new': function(params) {
      console.log('Supplier#new(%s)', JSON.stringify(params));
    },

    show: function(params) {
      console.log('Supplier#show(%s)', JSON.stringify(params));
    },

    edit: function(params) {
      console.log('Supplier#edit(%s)', JSON.stringify(params));
    },

  });

  return SupplierController;
});
