define([
  'chaplin',
  'views/three_pane_view',
], function(Chaplin, ThreePaneView) {
  "use strict";

  var BaseAdminController = Chaplin.Controller.extend({
    beforeAction: function(params, route) {
      console.log('base_admin#beforeAction');
      console.log('params:', params);
      console.log('route:', route);

      this.compose('main', ThreePaneView);

      // Call here composite
    },
  });

  return BaseAdminController;
});
