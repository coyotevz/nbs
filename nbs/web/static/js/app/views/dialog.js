define([
  'views/base/view',
], function(View) {
  "use strict";

  // NOTE: We are wrapping Bootstrap modal dialog.

  var DialogContentView = View.extend({
    optionNames: View.prototype.optionNames.concat(['template']),
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

    regions: {
      'dialog-content': '.modal-body',
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
    },

    run: function(options) {
      options || (options = {});
    },

    /*
    run: function(contentTemplate) {
      this.subview('dialog-content', new DialogContentView({
        template: contentTemplate,
        region: 'dialog-content',
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
  });

  return DialogView;
});
