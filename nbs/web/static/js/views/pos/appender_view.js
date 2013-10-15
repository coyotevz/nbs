define([
  'views/pos/base_row_view',
  'models/search',
], function(BaseRowView, Search) {
  "use strict";

  var AppenderView = BaseRowView.extend({
    id: 'appender',
    autoRender: true,

    onQuantityKeydown: function(evt) {
      if ($.keycode_is(evt, 'return tab') && this.model.isValid('quantity')) {
        this.trigger('append', this.model.clone());
        this.model.clear();
        this.$('.composed-field input').focus().val("");
        return false;
      }
    },
  });

  return AppenderView;
});
