define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/base/collection_view',
  'views/toolbar',
  'views/sidebar',
  'views/pager',
  'views/admin/product/item_view',
], function(_, Chaplin, View, CollectionView, Toolbar, Sidebar, Pager,
            ProductItemView) {
  "use strict";

  var ListSidebar = Sidebar.extend({
    template: 'admin/product/list_sidebar.html',

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
      sidebar = new ListSidebar({region: 'sidebar', view: this});
      this.subview('sidebar', sidebar);
    },

    attach: function() {
      ProductListView.__super__.attach.apply(this, arguments);
      //this.$('table').fixHeader();
      this.$selectionControl = this.$('th .control-checkbox');
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
      if (this.getSelected().length > 0) {
        this.unselectAll();
      } else {
        this.selectAll();
      }
      return false;
    },

    onItemSelected: function(item) {
      if (_.keys(this.getItemViews()).length > this.getSelected().length) {
        /* partial selection */
        this.$selectionControl.removeClass('control-checkbox-checked');
        this.$selectionControl.addClass('control-checkbox-partial');
      } else {
        /* full selection */
        this.$selectionControl.removeClass('control-checkbox-partial');
        this.$selectionControl.addClass('control-checkbox-checked');
      }
      if (item) this.setActive(item);
    },

    onItemUnselected: function(item) {
      if (this.getSelected().length > 0) {
        /* partial selection */
        this.$selectionControl.removeClass('control-checkbox-checked');
        this.$selectionControl.addClass('control-checkbox-partial');
      } else {
        /* all unselected */
        this.$selectionControl.removeClass('control-checkbox-partial');
        this.$selectionControl.removeClass('control-checkbox-checked');
      }
      if (item) this.setActive(item);
    },

    selectAll: function() {
      _.invoke(_.values(this.getItemViews()), 'toggleSelect', true, false);
      this.onItemSelected();
    },

    unselectAll: function() {
      _.invoke(_.values(this.getItemViews()), 'toggleSelect', false, false);
      this.onItemUnselected();
    },

    getSelected: function() {
      return _.filter(_.values(this.getItemViews()), 'selected');
    },

    setActive: function(item) {
      this.$('tbody tr').removeClass('active-row');
      if (item) {
        item.$el.addClass('active-row');
      }
    },
  });

  return ProductListView;
});
