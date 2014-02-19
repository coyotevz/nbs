define([
  'underscore',
  'chaplin',
  'views/base/view',
  'views/toolbar',
  'views/sidebar',
], function(_, Chaplin, View, Toolbar, Sidebar) {
  "use strict";

  var DetailSidebar = Sidebar.extend({
    template: 'admin/product/detail_sidebar.html',

    events: {
      'click .new-product': 'newProduct',
    },

    newProduct: function() {
      _dialog.show();
      //Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

  var DetailToolbar = Toolbar.extend({
    template: 'admin/product/detail_toolbar.html',

    events: {
      'click [name=go-back]': 'goBack',
      'click [name=edit]': 'edit',
      'click [name=delete]': 'delete',
    },

    goBack: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      Chaplin.utils.redirectTo({name: 'product_list'});
    },

    edit: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      Chaplin.utils.redirectTo({
        name: 'product_edit',
        params: { id: this.view.model.id }
      });
    },

    delete: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      console.log('delete');
    },
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
      toolbar = new DetailToolbar({region: 'toolbar', view: this});
      this.subview('toolbar', toolbar);
      sidebar = new DetailSidebar({region: 'sidebar', view: this});
      this.subview('sidebar', sidebar);
    },
  });

  return ProductDetailView;
});
