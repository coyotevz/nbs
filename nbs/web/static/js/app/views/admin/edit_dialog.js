define([
  'views/dialog',
], function(DialogView) {
  "use strict";

  var EditDialogContent = DialogView.DialogContentView.extend({
    template: 'admin/edit_dialog.html',
    closeButton: false,
    optionNames: DialogView.DialogContentView.prototype.optionNames.concat([
      'content_form',
    ]),

    events: {
      'click [name=cancel]': 'cancel',
      'click [name=save]': 'save',
    },

    cancel: function() {},
    save: function() {},
  });

  return EditDialogContent;
});
