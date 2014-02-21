define([
  'views/pos/base_row_view',
  'models/search',
], function(BaseRowView, Search) {
  "use strict";

  var AppenderView = BaseRowView.extend({
    id: 'appender',
    autoRender: true,

    listen: {
      'row-done': 'onRowDone',
    },

    onRowDone: function($target) {
      this.trigger('append', this.model.clone());
      this.model.clear();
      this.$('.composed-field input').focus().val("");
    },

  });

  return AppenderView;
});
