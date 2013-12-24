define([
  'views/base/view',
], function(View) {
  "use strict";

  var ProductSidebarView = View.extend({
    template: 'admin/product/sidebar.html',
  });

  return ProductSidebarView;
});
