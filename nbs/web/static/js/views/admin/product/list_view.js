define([
  'chaplin',
  'views/base/view',
  'views/base/collection_view',
  'views/admin/product/item_view',
], function(Chaplin, View, CollectionView, ProductItemView) {
  "use strict";

  var ListSidebar = View.extend({
    template: 'admin/product/list_sidebar.html',
  });

  var ListToolbar = View.extend({
    template: 'admin/product/list_toolbar.html',
  });

  var ProductListView = CollectionView.extend({
    template: 'admin/product/list.html',
    noWrap: true,
    listSelector: 'tbody',
    fallbackSelector: '.fallback',
    loadingSelector: '.loading',
    itemView: ProductItemView,
    animationDuration: 0,

    initialize: function(params) {
      var toolbar, sidebar;
      ProductListView.__super__.initialize.apply(this, arguments);
      console.log('ProductListView(%s)', JSON.stringify(params));

      toolbar = new ListToolbar({region: 'toolbar'});
      this.subview('toolbar', toolbar);
      toolbar.delegate('click', '.btn[name="reload"]', this.reload);
      toolbar.delegate('click', '.btn[name="prev-page"]', this.prevPage);
      toolbar.delegate('click', '.btn[name="next-page"]', this.nextPage);

      sidebar = new ListSidebar({region: 'sidebar'});
      this.subview('sidebar', sidebar);
      sidebar.delegate('click', '.new-product', this.newProduct);
    },

    // Toolbar callbacks

    reload: function() {
      console.log('reload');
    },

    prevPage: function() {
      console.log('prevPage');
    },

    nextPage: function() {
      console.log('nextPage');
    },

    // Sidebar callbacks

    newProduct: function() {
      Chaplin.utils.redirectTo({url: 'products/new'});
    },
  });

  return ProductListView;
});
