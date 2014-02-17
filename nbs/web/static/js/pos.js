// Admin application
require([
  'chaplin',
  'views/layout',
  'routes/pos',
  'bootstrap',

  'nbs.keycode',
  'nbs.number',
], function(Chaplin, PosLayout, routes) {
  "use strict";

  var Application = Chaplin.Application.extend({
    title: 'Nobix',

    initLayout: function(options) {
      options = options || {};
      options.title = options.title || this.title;
      this.layout = new PosLayout(options);
    },
  });

  var app = new Application({
    routes: routes,
    pushState: false,
  });
});
