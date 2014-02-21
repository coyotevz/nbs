define([
  'models/base/paginated_collection',
  'models/product',
], function(PaginatedCollection, Product) {
  "use strict";

  var ProductsCollection = PaginatedCollection.extend({

    model: Product,
    url: '/api/products',

    initialize: function() {
      ProductsCollection.__super__.initialize.apply(this, arguments);
      this.fetch();
    },

  });

  return ProductsCollection;
});
