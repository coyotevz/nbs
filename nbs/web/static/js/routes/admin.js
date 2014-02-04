define(function() {
  "use strict";

  // The routes for the application. This module returns a function.
  // `match` is a match method of the Router
  var routes = function(match) {

    /* dashboard controller */
    //match('', 'dashboard#index', {name: 'index'});
    //match('dashboard', 'dashboard#index', {name: 'index'});
    //match('pos', 'pos#index', {name: 'pos_index'});
    match('', 'admin#index', {name: 'admin_index'});

    match('products', 'product#list', {name: 'product_list'});
    match('products/new', 'product#new', {name: 'product_new'});
    match('products/:id', 'product#show', {name: 'product_show'});
    match('products/:id/edit', 'product#edit', {name: 'product_edit'});

    match('suppliers', 'supplier#list', {name: 'supplier_list'});
    match('suppliers/new', 'supplier#new', {name: 'supplier_new'});
    match('suppliers/:id', 'supplier#show', {name: 'supplier_show'});
    match('suppliers/:id/edit', 'supplier#edit', {name: 'supplier_edit'});
  };

  return routes;
});
