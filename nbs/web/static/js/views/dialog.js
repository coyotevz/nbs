define([
  'views/base/view',
], function(View) {
  "use strict";

  var DialogView = View.extend({
    template: 'dialog.html',
    noWrap: true,

    events: {
      'click .modal-close': 'hide',
      'click [name=save]': 'save',
      'click [name=close]': 'hide',
    },

    render: function() {
      DialogView.__super__.render.apply(this, arguments);
      this.delegate('shown.bs.modal', this.reposition);
      this.$el.modal({
        show: false,
      });
      this.$d = this.$('.modal-dialog');

      // Grab global copy of this instance
      window._dialog = this;
    },

    reposition: function() {
      this.$d.css({
        'left': ($(window).width() - this.$d.width()) / 2,
        'top': ($(window).height() - this.$d.height()) / 2,
      });
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

    save: function() {
      console.log("action save on modal dialog");
      this.hide();
    }
  });

  return DialogView;
});
