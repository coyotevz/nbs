define([
  'chaplin',
  'views/standard_view',
], function(Chaplin, StandardView) {
  "use strict";

  var BaseAdminController = Chaplin.Controller.extend({
    beforeAction: function(params, route) {
      this.compose('main', StandardView);
    },
  });

  return BaseAdminController;
});
