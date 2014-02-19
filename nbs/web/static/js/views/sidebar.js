define([
  'views/base/view',
], function(View) {
  "use strict";

  /* Base class for sidebar implementations */
  var Sidebar = View.extend({
    optionNames: View.prototype.optionNames.concat(['view']),

    initialize: function() {
      Sidebar.__super__.initialize.apply(this, arguments);
    },
  });

  return Sidebar;
});
