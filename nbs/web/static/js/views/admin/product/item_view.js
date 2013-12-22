define([
  'views/base/view',
], function(View) {
  "use strict";

  var ProductItemView = View.extend({
    template: 'admin/product/item.html',
    tagName: 'tr', // we can't insert <tr> element inside <div> with native code
  });

  window.ProductItemView = ProductItemView;

  return ProductItemView;
});
