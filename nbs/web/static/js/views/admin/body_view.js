define([
  'views/base/view',
], function(View) {
  "use strict";

  var BodyView = View.extend({
    template: 'admin/body.html',

    initialize: function() {
      BodyView.__super__.initialize.apply(this, arguments);
      console.log('BodyView#initialize(%s)', this.cid);
    },
  });

  return BodyView;
});
