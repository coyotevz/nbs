define([
  'underscore',
  'views/base/view',
], function(_, View) {
  "use strict";

  // NOTE: We are wrapping Bootstrap modal dialog.

  var DialogContentView = View.extend({
    template: 'dialog_content.html',
    optionNames: View.prototype.optionNames.concat([
      'dialog', 'title', 'text', 'buttons', 'template'
    ]),

    initialize: function() {
      DialogContentView.__super__.initialize.apply(this, arguments);
      for (var key in this.buttons) {
        this.delegate('click', '[name='+key+']',
          _.wrap(this.buttons[key].action, this.wrapper)
        );
      }
    },

    wrapper: function(action, evt) {
      return action(this.dialog, evt);
    },

    getTemplateData: function() {
      return this;
    },
  });

  var DialogView = View.extend({
    autoRender: false,
    template: 'dialog.html',
    noWrap: true,

    events: {
      'click .modal-close': 'close',
    },

    render: function() {
      DialogView.__super__.render.apply(this, arguments);
      this.delegate('shown.bs.modal', function() {
        this.subview('modal-content').trigger('show');
      });
      this.delegate('shown.bs.modal', this.reposition);

      this.delegate('hidden.bs.modal', function() {
        this.subview('modal-content').trigger('hide');
      });

      this.$el.modal({
        show: false,
      });

      this.$d = this.$('.modal-dialog');
      $(window).resize(_.debounce(_.bind(this.reposition, this), 200));

      // Grab global copy of this instance
      window._dialog = this;
    },

    reposition: function() {
      this.subview('modal-content').trigger('beforeReposition');
      this.$d.css({
        'left': ($(window).width() - this.$d.width()) / 2,
        'top': ($(window).height() - this.$d.height()) / 2,
      });
      this.subview('modal-content').trigger('afterReposition');
    },

    show: function() {
      this.$el.modal('show');
    },

    hide: function() {
      this.$el.modal('hide');
    },

    close: function() {
      this.$el.modal('hide');
      this.removeSubview('modal-content');
    },

    toggle: function() {
      this.$el.modal('toggle');
    },

   /* API Details:
    * dialog.run({
    *   title: 'Some title',
    *   text: 'Hello, we are in dialog paragraph.',
    *   view: CustomContentView, // inherited from DialogContentView
    *   template: 'templates/body.html', // extend from dialog_content.html
    *   buttons: {
    *     'success': {
    *       'label': 'OK',
    *       'style': 'primary',
    *       'action': <some callback>(dialog,),
    *     },
    *     'cancel': {
    *       'label': 'Cancel',
    *       <style=default> as default,
    *       'action': <some callback>(dialog,),
    *     }
    *   }
    * });
    */
   run: function(options) {
     var defaults = {
       className: 'modal-content',
       container: this.$d,
       dialog: this,

       title: null,
       text: null,
       buttons: {},
     };
     var ContentView = options.view || DialogContentView;
     delete options.view;
     options = _.extend(defaults, options);
     
     this.subview('modal-content', new ContentView(options));
     this.show();
   },
  });

  DialogView.DialogContentView = DialogContentView;

  return DialogView;
});
