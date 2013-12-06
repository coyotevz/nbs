define([
  'chaplin',
], function(Chaplin) {
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
      this.subscribeEvent("startupController", this.removeFallback);
    },

    navigate: function(controller, params, route) {
      console.log('navigate function');
    },

    removeFallback: function(opts) {
      opts.controller.adjustTitle(opts.controller.title);
      console.log('removeFallback function');
      this.unsubsribeEvent('startupController', this.removeFallback);
    },
  });

  return Layout;
});
