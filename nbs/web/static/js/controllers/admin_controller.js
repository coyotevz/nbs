define([
  'chaplin',
], function(Chaplin) {
  "use strict";

  var AdminController = Chaplin.Controller.extend({
    title: 'Admin',

    index: function(params) {
      console.log('reach admin page...');
    }
  });

  return AdminController;
});
