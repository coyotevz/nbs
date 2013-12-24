define([
  'views/base/view',
], function(View) {
  "use strict";

  var ProductEditView = View.extend({
    template: 'admin/product/edit.html',
    noWrap: true,

    initialize: function(params) {
      ProductEditView.__super__.initialize.apply(this, arguments);
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
