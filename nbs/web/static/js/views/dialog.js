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
      // Grab global copy of this instance
      window._dialog = this;
    },

    show: function() {
      this.$el.modal('show');
    },

    hide: function() {
      this.$el.modal('hide');
    },

    toggle: function() {
      this.$el.modal('toggle');
    },
  });

  return DialogView;
});
