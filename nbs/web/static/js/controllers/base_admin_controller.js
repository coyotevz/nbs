define([
  'chaplin',
], function(Chaplin) {
  "use strict";

  var BaseAdminController = Chaplin.Controller.extend({
    beforeAction: function(params, route) {
      console.log('base_admin#beforeAction');
      console.log('params:', params);
      console.log('route:', route);

      // Call here composite
    },
  });

  return BaseAdminController;
});
