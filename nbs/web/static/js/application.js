define([
  'chaplin',
  'views/layout',
  'bootstrap',

  // jQuery plugins
  'jquery.keycode',
  'jquery.number',
], function(Chaplin, Layout) {
  'use strict';

  // The application object
  // Choose a maingful name for your application
  var Application = Chaplin.Application.extend({
    // Set your application name here so the document title is set to
    // "Controller title - Site title" (see Layout#adjustTitle)
    title: 'Nobix',

    initLayout: function(options) {
      if (options == null) {
        options = {};
      }
      if (options.title == null) {
        options.title = this.title;
      }
      this.layout = new Layout(options);
    },

  });

  return Application;
});
