define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/base/collection_view',
  'views/admin/product/item_view',
], function(_, Chaplin, View, CollectionView, ProductItemView) {
  "use strict";

  var Pager = View.extend({

    setCollection: function(collection) {
      this.collection = collection
    },

    setField: function(field) {
      this.field = field;
    },

    prevPage: function() {
      console.log('Pager.prevPage');
      this.$('[rel=tooltip]').tooltip('hide');
      this.collection.fetch({ data: $.param({
        page: this.collection.page - 1
      })});
    },

    nextPage: function() {
      console.log('Pager.nextPage');
      this.$('[rel=tooltip]').tooltip('hide');
      this.collection.fetch({ data: $.param({
        page: this.collection.page + 1
      })});
    },
  });

  var ListSidebar = View.extend({
    template: 'admin/product/list_sidebar.html',
  });

  var ListToolbar = View.extend({
    template: 'admin/product/list_toolbar.html',

    initialize: function() {
      var pager = this.pager = new Pager({collection: this.collection});
      this.delegate('click', '[name=prev-page]', _.bind(pager.prevPage, pager));
      this.delegate('click', '[name=next-page]', _.bind(pager.nextPage, pager));
    },
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

      toolbar.pager.setCollection(this.collection);
      toolbar.pager.setField('name');

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

    // Sidebar callbacks

    newProduct: function() {
      Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

  return ProductListView;
});
