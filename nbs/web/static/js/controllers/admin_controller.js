define([
  'controllers/base_admin_controller',
], function(BaseAdminController) {
  "use strict";

  var AdminController = BaseAdminController.extend({
    title: 'Admin',

    index: function(params) {
      console.log('reach admin page...');
    }
  });

  return AdminController;
});
