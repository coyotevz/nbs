define([
  'views/base/view',
], function(View) {
  "use strict";

  var EditToolbar = View.extend({
    template: 'admin/product/edit_toolbar.html',
    region: 'toolbar',
  });

  var ProductEditView = View.extend({
    template: 'admin/product/edit.html',
    noWrap: true,

    initialize: function(params) {
      var toolbar;
      ProductEditView.__super__.initialize.apply(this, arguments);
      console.log('ProductEditView(%s)', JSON.stringify(params));
      toolbar = new EditToolbar();
      this.subview('toolbar', toolbar);

      toolbar.delegate('click', '.btn[name="go-back"]', this.goBack);
      toolbar.delegate('click', '.btn[name="save"]', this.saveChanges);
    },

    getTemplateData: function() {
      return _.extend(
        ProductEditView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },

    // toolbar callbacks
    goBack: function() {
      window.history.back();
    },

    saveChanges: function() {
      console.log('saveChanges called!');
    },
  });

  return ProductEditView;
});
