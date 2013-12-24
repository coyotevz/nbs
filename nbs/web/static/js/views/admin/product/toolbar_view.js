define([
  'views/base/view',
], function(View) {
  "use strict";

  var ProductToolbarView = View.extend({
    template: 'admin/product/toolbar.html',

    getTemplateData: function() {
      return _.extend(
        ProductToolbarView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },
  });

  return ProductToolbarView;
});
