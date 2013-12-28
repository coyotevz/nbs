define([
  'jquery',
  'chaplin',
], function($, Chaplin) {
  "use strict";

  var Layout = Chaplin.Layout.extend({
    title: 'Nobix Layout Test',

    listen: {
      'dispatcher:dispatch mediator': 'navigate',
    },

    regions: {
      main: '',
    },

    initialize: function(options) {
      Layout.__super__.initialize.apply(this, options);
      console.log('Layout#initialize');
    },

    navigate: function(controller, params, route) {
      this.$('[rel="tooltip"]').tooltip();
    },

  });

  return Layout;
});
