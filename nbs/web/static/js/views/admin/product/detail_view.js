define([
  'underscore',
  'chaplin',
  'views/base/view',
], function(_, Chaplin, View) {
  "use strict";

  var DetailSidebar = View.extend({
    template: 'admin/product/detail_sidebar.html',
    optionNames: View.prototype.optionNames.concat(['detailv']),

    events: {
      'click .new-product': 'newProduct',
    },

    newProduct: function() {
      Chaplin.utils.redirectTo({name: 'product_new'});
    },
  });

  var DetailToolbar = View.extend({
    template: 'admin/product/detail_toolbar.html',
    optionNames: View.prototype.optionNames.concat(['detailv']),

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
        params: { id: this.detailv.model.id }
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
      toolbar = new DetailToolbar({region: 'toolbar', detailv: this});
      this.subview('toolbar', toolbar);
      sidebar = new DetailSidebar({region: 'sidebar', detailv: this});
      this.subview('sidebar', sidebar);
    },
  });

  return ProductDetailView;
});
