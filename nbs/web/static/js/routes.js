define(function() {
  "use strict";

  // The routes for the application. This module returns a function.
  // `match` is a match method of the Router
  var routes = function(match) {

    /* dashboard controller */
    match('', 'dashboard#index', {name: 'index'});
    match('dashboard', 'dashboard#index', {name: 'index'});
    match('pos', 'pos#index', {name: 'pos_index'});
    match('admin', 'admin#index', {name: 'admin_index'});
    match('admin/products', 'products#index', {name: 'products_index'});
  };

  return routes;
});
