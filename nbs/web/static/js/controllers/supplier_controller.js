define([
  'controllers/admin_controller',
  'views/admin/side_view',
  'views/admin/supplier/detail_view',
  'views/admin/supplier/list_view',
  'views/admin/supplier/edit_view',
], function(AdminController,
            SideView,
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
      this.compose('sidebar', SideView, {region: 'sidebar'});
      this.view = new SupplierEditView(params);
    },

    show: function(params) {
      this.compose('sidebar', SideView, {region: 'sidebar'});
      _.extend(params, {region: 'content'});
      console.log('Supplier#show(%s)', JSON.stringify(params));
      this.view = new SupplierDetailView(params);
    },

    edit: function(params) {
      this.compose('sidebar', SideView, {region: 'sidebar'});
      _.extend(params, {region: 'content'});
      console.log('Supplier#edit(%s)', JSON.stringify(params));
      this.view = new SupplierEditView(params);
    },

  });

  return SupplierController;
});
