define([
  'chaplin',
  'views/standard_view',
  'views/admin/header_view',
  'views/admin/body_view',
], function(Chaplin, StandardView, HeaderView, BodyView) {
  "use strict";

  var AdminController = Chaplin.Controller.extend({
    title: 'Admin',

    beforeAction: function(params, route) {
      this.compose('main', StandardView);
      this.compose('header', HeaderView, {region: 'header'});
      this.compose('body', BodyView, {region: 'body'});
    },

    index: function(params) {
      console.log('reach admin page...');
    }
  });

  return AdminController;
});
