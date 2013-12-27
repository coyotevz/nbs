define([
  'chaplin',
  'views/base/view',
], function(Chaplin, View) {
  "use strict";

  var EditToolbar = View.extend({
    template: 'admin/product/edit_toolbar.html',
  });

  var ProductEditView = View.extend({
    template: 'admin/product/edit.html',
    noWrap: true,

    render: function(params) {
      ProductEditView.__super__.render.apply(this, arguments);
      this.initSubviews();
    },

    initSubviews: function() {
      var toolbar, sidebar;
      toolbar = new EditToolbar({region: 'toolbar'});
      this.subview('toolbar', toolbar);
      toolbar.delegate('click', '.btn[name="go-back"]', _.bind(this.goBack, this));
      toolbar.delegate('click', '.btn[name="save"]', _.bind(this.saveChanges, this));
    },

    // toolbar callbacks
    goBack: function() {
      Chaplin.utils.redirectTo({name: 'product_list'});
    },

    saveChanges: function() {
      console.log('saveChanges called!');
    },
  });

  return ProductEditView;
});
