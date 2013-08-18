define([
  'chaplin',
], function(Chaplin) {
  "use strict";

  var DashboardController = Chaplin.Controller.extend({

    index: function(params) {
      console.log("dashboard#index", params);
    }

  });

  return DashboardController;
});
