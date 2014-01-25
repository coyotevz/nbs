define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/base/collection_view',
  'views/admin/product/item_view',
], function(_, Chaplin, View, CollectionView, ProductItemView) {
  "use strict";

  var Pager = View.extend({
    template: 'admin/product/list_pager.html',
    noWrap: true,
    optionNames: View.prototype.optionNames.concat(['collection', 'field']),
    events: {
      'click [name=prev-page]': 'prevPage',
      'click [name=next-page]': 'nextPage',
    },

    prevPage: function(evt) {
      this._changePage(-1);
    },

    nextPage: function(evt) {
      this._changePage(+1);
    },

    _changePage: function(n) {
      this.$('[rel=tooltip]').tooltip('hide');
      this.collection.fetch({
        data: $.param({
          page: this.collection.page + n
        })
      });
    }
  });

  var ListSidebar = View.extend({
    template: 'admin/product/list_sidebar.html',
    optionNames: View.prototype.optionNames.concat(['listv']),

    events: {
      'click .new-product': 'newProduct',
    },

    newProduct: function() {
      Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

  var ListToolbar = View.extend({
    template: 'admin/product/list_toolbar.html',
    optionNames: View.prototype.optionNames.concat(['listv']),

    events: {
      'click [name=select-all]': 'selectAll',
      'click .btn[name=reload]': 'reload',
    },

    regions: {
      'pager': '.pager-container',
    },

    render: function() {
      var pager;
      ListToolbar.__super__.render.apply(this, arguments);
      pager = new Pager({region: 'pager', collection: this.listv.collection});
      this.subview('pager', pager);
    },

    reload: function() {
      this.listv.collection.fetch();
    },

    selectAll: function(evt) {
      console.log('select-all', evt.currentTarget.value, evt);
      return false;
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
      toolbar = new ListToolbar({region: 'toolbar', listv: this});
      this.subview('toolbar', toolbar);
      sidebar = new ListSidebar({region: 'sidebar', listv: this});
      this.subview('sidebar', sidebar);
    },
  });

  return ProductListView;
});
