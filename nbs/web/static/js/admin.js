// Admin application
require([
  'chaplin',
  'views/layout',
  'routes/admin',
  'bootstrap',

  // jQuery plugins
  'jquery.keycode',
  'jquery.number',
  'jquery.autogrow',
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
