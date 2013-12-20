define([
  'models/base/collection',
  'models/menu_item',
], function(Collection, MenuItem) {
  "use strict";

  var MenuItems = Collection.extend({
    model: MenuItem,
  });

  return MenuItems;
});
