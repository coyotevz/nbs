define([
  'views/base/view',
], function(View) {
  "use strict";

  var ThreePaneView = View.extend({
    id: 'wrapper',
    template: 'three_pane.html',
    region: 'main',
    regions: {
      'header': 'header',
      'body': '#body',
      'footer': 'footer',
    },
  });

  return ThreePaneView;
});
