define([
  'views/base/view',
], function(View) {
  "use strict";

  var ProductToolbarView = View.extend({
    template: 'admin/product/toolbar.html',

    initialize: function() {
      ProductToolbarView.__super__.initialize.apply(this, arguments);
      this.delegate('click', '.btn[name="back"]', this.goBack);
    },

    getTemplateData: function() {
      return _.extend(
        ProductToolbarView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },

    goBack: function() {
      window.history.back();
    }
  });

  return ProductToolbarView;
});
