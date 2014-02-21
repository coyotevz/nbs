define([
  'views/base/collection_view',
  'views/pos/item_view',
], function(CollectionView, ItemView) {
  "use strict";

  var ItemsView = CollectionView.extend({
    el: 'table.item-list',
    listSelector: 'tbody',
    itemView: ItemView,
    animationDuration: 0,
  });

  return ItemsView;
});
