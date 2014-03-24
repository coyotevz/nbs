define([
  'chaplin',
  'views/admin/dashboard/dashboard_view',
], function(Chaplin, DashboardView) {
  "use strict";

  var DashboardController = Chaplin.Controller.extend({
    title: 'Dashboard',

    index: function(params) {
      this.view = new DashboardView();
      console.log('DashboardController#index');
    },
  });

  return DashboardController;
});
