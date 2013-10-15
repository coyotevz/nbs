define([
  'chaplin',
  'bootstrap',

  // jQuery plugins
  'jquery.keycode',
  'jquery.number',
], function(Chaplin) {
  'use strict';

  // The application object
  // Choose a maingful name for your application
  var Application = Chaplin.Application.extend({
    // Set your application name here so the document title is set to
    // "Controller title - Site title" (see Layout#adjustTitle)
    title: 'Nobix',

  });

  return Application;

});
