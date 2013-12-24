define([
  'chaplin',
  'views/base/view',
], function(Chaplin, View) {
  "use strict";

  var ProductSidebarView = View.extend({
    template: 'admin/product/sidebar.html',

    initialize: function() {
      ProductSidebarView.__super__.initialize.apply(this, arguments);
      this.delegate('click', '.new-product', this.newProduct);
    },

    newProduct: function() {
      Chaplin.utils.redirectTo({url: 'products/new'});
    },
  });

  return ProductSidebarView;
});
