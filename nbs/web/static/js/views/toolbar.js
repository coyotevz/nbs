define([
  'views/base/view',
], function(View) {
  "use strict";

  var Toolbar = View.extend({
    optionNames: View.prototype.optionNames.concat(['view']),

    initialize: function() {
      Toolbar.__super__.initialize.apply(this, arguments);
      this.delegate('click', '[name=go-back]', this.goBack);
    },

    goBack: function() {
      this.$('[rel=tooltip]').tooltip('hide');
      window.history.back();
    },

  });

  return Toolbar;
});
