define([
  'views/base/view',
], function(View) {
  "use strict";

  var DialogView = View.extend({
    template: 'dialog.html',
    noWrap: true,

    initialize: function() {
      DialogView.__super__.initialize.apply(this, arguments);
      console.log('DialogView#initialize');
    },

    render: function() {
      DialogView.__super__.render.apply(this, arguments);
      this.$el.modal({
        show: false,
      });
  fade     window.$el = this.$el; 
    },
  });

  return DialogView;
});
