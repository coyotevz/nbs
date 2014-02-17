define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/base/collection_view',
  'views/toolbar',
  'views/pager',
  'views/admin/product/item_view',
], function(_, Chaplin, View, CollectionView, Toolbar, Pager,
            ProductItemView) {
  "use strict";

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

  var ListToolbar = Toolbar.extend({
    template: 'admin/product/list_toolbar.html',

    regions: {
      'pager': '.pager-container',
    },

    initialize: function() {
      ListToolbar.__super__.initialize.apply(this, arguments);
      this.delegate('click','[name=reload]', this.reload);
    },

    render: function() {
      var pager;
      ListToolbar.__super__.render.apply(this, arguments);
      pager = new Pager({
        region: 'pager',
        collection: this.view.collection,
        field: 'sku',
      });
      this.subview('pager', pager);
    },

    reload: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      this.view.collection.fetch();
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
      this.delegate('click', 'th .control-checkbox', this.onCheckboxClick);
      this.initSubviews();
    },

    initSubviews: function() {
      var toolbar, sidebar;
      toolbar = new ListToolbar({region: 'toolbar', view: this});
      this.subview('toolbar', toolbar);
      sidebar = new ListSidebar({region: 'sidebar', listv: this});
      this.subview('sidebar', sidebar);
    },

    attach: function() {
      ProductListView.__super__.attach.apply(this, arguments);
      $(window).on('resize', _.debounce(this.resizeTableHeader, 150));
      $(window).on('focus', this.resizeTableHeader);
      this.resizeTableHeader();
    },

    resizeTableHeader: function() {
      self = this;
      /*
      this.$('col').each(function(index, element) {
        var cls = element.className.replace(/col-/, 'header-');
        self.$('th.'+cls).css('width', $(element).width());
      });*/
     this.$('tr:first td').each(function(index, element) {
       var cls = element.className.replace(/cell-/, 'heade-');
       self.$('th.'+cls).css('width', $(element).css('width'));
     });
    },

    initItemView: function(model) {
      if (this.itemView) {
        var view = new this.itemView({
          autoRender: true,
          model: model,
          parent: this,
        });
        this.listenTo(view, 'selected', this.onItemSelected);
        this.listenTo(view, 'unselected', this.onItemUnselected);
        return view;
      } else {
        throw new Error("The CollectionView#itemView property " +
                        "must be defined or initItemView() must be overridden.");
      }
    },

    onCheckboxClick: function(evt) {
      evt.preventDefault();
      console.log('onCheckboxClick');
      return false;
    },

    onItemSelected: function(item) {
    },

    onItemUnselected: function(item) {
    },

    selectAll: function() {
      _.invoke(_.values(this.getItemViews()), 'toggleSelect', true);
    },

    unselectAll: function() {
      _.invoke(_.values(this.getItemViews()), 'toggleSelect', false);
    },

    getSelected: function() {
      return _.filter(_.values(this.getItemViews()), 'selected');
    },
  });

  return ProductListView;
});
