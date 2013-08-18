define(function() {
  "use strict";

  // The routes for the application. This module returns a function.
  // `match` is a match method of the Router
  var routes = function(match) {

    /* dashboard controller */
    match('', 'dashboard#index', {name: 'index'});
    match('dashboard', 'dashboard#index', {name: 'index'});
  };

  return routes;
});
