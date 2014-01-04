define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/base/collection_view',
  'views/admin/product/item_view',
], function(_, Chaplin, View, CollectionView, ProductItemView) {
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

    render: function() {
      ProductListView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    initSubviews: function() {
      var toolbar, sidebar;
      toolbar = new ListToolbar({region: 'toolbar'});
      this.subview('toolbar', toolbar);
      toolbar.delegate('click', 'input[name="select-all"]', _.bind(this.selectAll, this));
      toolbar.delegate('click', '.btn[name="reload"]', _.bind(this.reload, this));
      toolbar.delegate('click', '.btn[name="prev-page"]', _.bind(this.prevPage, this));
      toolbar.delegate('click', '.btn[name="next-page"]', _.bind(this.nextPage, this));

      sidebar = new ListSidebar({region: 'sidebar'});
      this.subview('sidebar', sidebar);
      sidebar.delegate('click', '.new-product', _.bind(this.newProduct, this));
    },

    // Toolbar callbacks

    selectAll: function(evt) {
      var input = evt.currentTarget;
      input.checked = input.checked ? false : true;
      console.log('select-all:', evt.currentTarget.value, evt);
      return false;
    },

    reload: function() {
      this.collection.fetch();
    },

    prevPage: function() {
      console.log('prevPage');
    },

    nextPage: function() {
      console.log('nextPage');
    },

    // Sidebar callbacks

    newProduct: function() {
      Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

  return ProductListView;
});
