define([
  'views/base/view',
], function(View) {
  "use strict";

  var HeaderView = View.extend({
    template: 'admin/header.html',

    regions: {
      ribbon: '',
      banner: '',
    },

    initialize: function() {
      HeaderView.__super__.initialize.apply(this, arguments);
      console.log('HeaderView#initialize(%s)', this.cid);
    },
  });

  return HeaderView;
});
