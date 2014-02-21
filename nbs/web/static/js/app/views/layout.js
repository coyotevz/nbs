define([
  'jquery',
  'chaplin',
], function($, Chaplin) {
  "use strict";

  var Layout = Chaplin.Layout.extend({
    title: 'Nobix',

    listen: {
      'dispatcher:dispatch mediator': 'navigate',
    },

    regions: {
      main: '',
    },

    navigate: function(controller, params, route) {
      this.$('[rel="tooltip"]').tooltip({
        container: 'body',
        delay: { show: 500, hide: 0},
      });
    },

  });

  return Layout;
});
