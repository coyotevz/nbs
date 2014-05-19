// Admin application
require([
  'pace',
  'jquery',
  'chaplin',
  'views/layout',
  'routes/admin',
  'bootstrap.dropdown',
  'bootstrap.modal',
  'bootstrap.tab',
  'bootstrap.tooltip',
  'bootstrap.transition',

  'jquery.number',
  'nbs.keycode',
  'nbs.autogrow',
  'nbs.fixedheader',
], function(Pace, $, Chaplin, AdminLayout, routes) {
  "use strict";

  Pace.start();
  Pace.once("hide", function() {
    $('body').removeClass('pace-init').addClass('pace-async');
  });


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
