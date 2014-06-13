define([
  'models/base/paginated_collection',
  'models/product',
], function(PaginatedCollection, Product) {
  "use strict";

  var ProductsCollection = PaginatedCollection.extend({

    model: Product,
    urlRoot: '/products',

    initialize: function() {
      PaginatedCollection.prototype.initialize.apply(this, arguments);
      this.fetch();
    },

  });

  return ProductsCollection;
});
