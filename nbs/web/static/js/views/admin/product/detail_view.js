define([
  'underscore',
  'chaplin',
  'views/base/view',
], function(_, Chaplin, View) {
  "use strict";

  var DetailToolbar = View.extend({
    template: 'admin/product/detail_toolbar.html',
  });

  var ProductDetailView = View.extend({
    template: 'admin/product/detail.html',
    noWrap: true,

    render: function() {
      ProductDetailView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    initSubviews: function() {
      var toolbar, sidebar;
      toolbar = new DetailToolbar({region: 'toolbar'});
      this.subview('toolbar', toolbar);
      toolbar.delegate('click', '.btn[name="go-back"]', _.bind(this.goBack, this));
    },

    // Toolbar callbacks
    goBack: function() {
      Chaplin.utils.redirectTo({name: 'product_list'});
    },
  });

  return ProductDetailView;
});
