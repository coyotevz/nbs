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

    goBack: function() {
      window.history.back();
    },
  });

  return ProductToolbarView;
});
