define([
  'controllers/admin_controller',
  'views/admin/supplier/detail_view',
  'views/admin/supplier/list_view',
  'views/admin/supplier/edit_view',
], function(AdminController,
            SupplierDetailView,
            SupplierListView,
            SupplierEditView) {
  "use strict";

  var SupplierController = AdminController.extend({
    title: 'Suppliers',

    beforeAction: function() {
      SupplierController.__super__.beforeAction.apply(this, arguments);
      this.publishEvent('menu:setCurrent', 'supplier');
    },

    list: function(params) {
      _.extend(params, {region: 'content'});
      console.log('Supplier#index(%s)', JSON.stringify(params));
      this.view = new SupplierListView(params);
    },

    'new': function(params) {
      _.extend(params, {region: 'content'});
      console.log('Supplier#new(%s)', JSON.stringify(params));
      this.view = new SupplierEditView(params);
    },

    show: function(params) {
      _.extend(params, {region: 'content'});
      console.log('Supplier#show(%s)', JSON.stringify(params));
      this.view = new SupplierDetailView(params);
    },

    edit: function(params) {
      _.extend(params, {region: 'content'});
      console.log('Supplier#edit(%s)', JSON.stringify(params));
      this.view = new SupplierEditView(params);
    },

  });

  return SupplierController;
});
