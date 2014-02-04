define([
  'jquery',
  'chaplin',
], function($, Chaplin) {
  "use strict";

  var Layout = Chaplin.Layout.extend({
    title: 'Point of Sale',

    listen: {
      'dispatcher:dispatch mediator': 'navigate',
    },

    regions: {
      main: '',
    },

    initialize: function(options) {
      Layout.__super__.initialize.apply(this, options);
      console.log('PosLayout#initialize');
    },

    navigate: function(controller, params, route) {
      console.log('pos navigate');
    },

  });

  return Layout;
});
