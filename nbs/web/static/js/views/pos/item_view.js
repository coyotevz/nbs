define([
  'views/pos/base_row_view',
], function(BaseRowView) {
  "use strict";

  var ItemView = BaseRowView.extend({
    className: 'item-row',

    onQuantityKeydown: function(evt) {
      if ($.keycode_is(evt, 'return tab') && this.model.isValid('quantity')) {
        this.$el.next().find('input:first').focus();
        return false;
      }
    },
  });

  return ItemView;
});
