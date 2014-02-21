define([
  'models/base/collection',
  'models/document_item',
], function(Collection, DocumentItem) {
  "use strict";

  var DocumentItems = Collection.extend({
    model: DocumentItem,
  });

  return DocumentItems;
});
