define([
  'views/base/view',
], function(View) {
  "use strict";

  var EditToolbarView = View.extend({
    template: 'admin/product/edit_toolbar.html',

    initialize: function() {
      EditToolbarView.__super__.initialize.apply(this, arguments);
      this.delegate('click', '.btn[name="back"]', this.goBack);
    },

    goBack: function() {
      window.history.back();
    },
  });

  var ProductEditView = View.extend({
    template: 'admin/product/edit.html',
    noWrap: true,

    initialize: function(params) {
      ProductEditView.__super__.initialize.apply(this, arguments);
      this.view = new EditToolbarView();
      console.log('ProductEditView');
    },

    getTemplateData: function() {
      return _.extend(
        ProductEditView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },

  });

  return ProductEditView;
});
