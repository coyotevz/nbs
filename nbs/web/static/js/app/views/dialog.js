define([
  'underscore',
  'views/base/view',
], function(_, View) {
  "use strict";

  // NOTE: We are wrapping Bootstrap modal dialog.

  var DialogContentView = View.extend({
    template: 'dialog_content.html',

    initialize: function(attrs) {
      console.log('DialogContentView#initialize,', attrs);
      DialogContentView.__super__.initialize.apply(this, arguments);
    },
  });

  var DialogView = View.extend({
    autoRender: false,
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
      this.reposition();
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
    },

    /*
    run: function(contentTemplate) {
      this.subview('dialog-content', new DialogContentView({
        template: contentTemplate,
      }));
      this.render();
      this.show();
    },*/

   /* API Details:
    * dialog.run({
    *   contentView: CustomContentView,
    *   contentArgs: { arguments to use in contentView instantiation }
    * });
    *
    * dialog.run({
    *   title: 'Some title',
    *   displayFooter: false,
    *   bodyHtml: '<p>Hello, we are in dialog body</p>',
    *   bodyText: 'Hello, we are in dialog paragraph.',
    *   bodyTemplate: 'templates/body.html',
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
   run: function() {
     var content = new DialogContentView({
       className: 'modal-content',
       container: this.$d,
     });
     this.subview('modal-content', content);
     this.show();
   },
  });

  return DialogView;
});
