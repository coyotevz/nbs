// Pos application
require([
  'pace',
  'chaplin',
  'views/layout',
  'routes/pos',
  'bootstrap.tooltip',
  'bootstrap.modal',

  'jquery.number',
  'nbs.keycode',
  'nbs.fixedheader',
], function(Pace, Chaplin, PosLayout, routes) {
  "use strict";

  Pace.start();
  Pace.on("hide", function() {
    $('body').removeClass('pace-init').addClass('pace-async');
    Chaplin.mediator.publish('pace:hide');
  });
  Pace.on("done", function() {
    Chaplin.mediator.publish('pace:done');
  });

  var Application = Chaplin.Application.extend({
    title: 'Nobix POS',

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
