define([
  'chaplin',
  'views/standard_view',
  'views/dialog',
  'views/admin/header_view',
  'views/admin/body_view',
  'views/admin/sidebar_view',
], function(Chaplin,
            StandardView,
            DialogView,
            HeaderView,
            BodyView,
            SidebarView) {
  "use strict";

  var AdminController = Chaplin.Controller.extend({
    title: 'Admin',

    beforeAction: function(params, route) {
      this.reuse('main', StandardView, {region: 'main'});
      this.reuse('dialog', DialogView, {region: 'main'});
      this.reuse('header', HeaderView, {region: 'header'});
      this.reuse('body', BodyView, {region: 'body'});
      this.reuse('sidebar', SidebarView, {region: 'sidebar'});
    },

    index: function(params) {
      console.log('reach admin page...');
    }
  });

  return AdminController;
});
