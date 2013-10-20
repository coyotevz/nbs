define([
  'views/pos/base_row_view',
], function(BaseRowView) {
  "use strict";

  var ItemView = BaseRowView.extend({
    className: 'item-row',

    listen: {
      'row-done': 'onRowDone',
    },

    onRowDone: function($target) {
      this.$el.next().find('input:first').focus();
    },
  });

  return ItemView;
});
