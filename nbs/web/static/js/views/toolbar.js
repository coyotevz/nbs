define([
  'views/base/view',
], function(View) {
  "use strict";

  /* Base class for toolbar implementations */
  var Toolbar = View.extend({
    optionNames: View.prototype.optionNames.concat(['view']),

    initialize: function() {
      Toolbar.__super__.initialize.apply(this, arguments);
      this.delegate('click', '[name=go-back]', this.goBack);
    },

    goBack: function() {
      this.hideTooltips();
      window.history.back();
    },

    hideTooltips: function() {
      this.$('[rel=tooltip]').tooltip('hide');
    }

  });

  return Toolbar;
});
