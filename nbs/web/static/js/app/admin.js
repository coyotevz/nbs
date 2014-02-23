// Admin application
require([
  'chaplin',
  'views/layout',
  'routes/admin',
  'bootstrap',

  'jquery.number',
  'nbs.keycode',
  'nbs.autogrow',
  'nbs.fixedheader',

  /* Only for include in optimized version */
  'controllers/admin_controller',
  'controllers/dashboard_controller',
  'controllers/supplier_controller',
  'controllers/product_controller',
], function(Chaplin, AdminLayout, routes) {
  "use strict";

  var Application = Chaplin.Application.extend({
    title: 'Nobix',

    initLayout: function(options) {
      options = options || {};
      options.title = options.title || this.title;
      this.layout = new AdminLayout(options);
    },
  });

  var app = new Application({
    routes: routes,
    pushState: false,
  });
});
