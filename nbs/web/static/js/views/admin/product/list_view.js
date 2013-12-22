define([
  'views/base/collection_view',
  'views/admin/product/item_view',
], function(CollectionView, ProductItemView) {
  "use strict";

  var ProductListView = CollectionView.extend({
    template: 'admin/product/list.html',
    noWrap: true,
    listSelector: 'tbody',
    fallbackSelector: '.fallback',
    loadingSelector: '.loading',
    itemView: ProductItemView,
    animationDuration: 0,

    initialize: function(params) {
      ProductListView.__super__.initialize.apply(this, arguments);
      console.log('ProductListView(%s)', JSON.stringify(params));
    },
  });

  return ProductListView;
});
