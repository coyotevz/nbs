define([
  'chaplin',
], function(Chaplin) {
  "use strict";

  var AdminController = Chaplin.Controller.extend({
    title: 'Admin',

    beforeAction: function(params, route) {
      // params is the parsed query string
      //
      // route attributes: {
      //    'action': <controller_method_name>,
      //    'controller': <controller_name>,
      //    'name': <name setted in routes.js for this action>,
      //    'path': <matched path>,
      //    'previous': <previous route?>,
      //    'query': <raw_query_string>,
      // }
      // sample: { 'action': "index", 'controller': "admin",
      //           'name': "admin_index", 'path': "admin" }

      console.log('admin#beforeAction');
      console.log('params:', params);
      console.log('route:', route);

      // Call here composite based on route info
    },

    index: function(params) {
      console.log('reach admin page...');
    }
  });

  return AdminController;
});
