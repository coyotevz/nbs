define([
  'views/base/view',
], function(View) {
  "use strict";

  var StandardView = View.extend({
    id: 'wrapper',
    template: 'standard_page.html',
    regions: {
      'header': 'header',
      'body': '#body',
      'footer': 'footer',
    },

    initialize: function() {
      StandardView.__super__.initialize.apply(this, arguments);
      console.log('StandardView#initialize(%s)', this.cid);
    },
  });

  return StandardView;
});
