define([
  'views/base/view',
], function(View) {
  "use strict";

  var TestBodyView = View.extend({
    template: 'admin/supplier/test_body_page.html',
    noWrap: true,

    initialize: function() {
      TestBodyView.__super__.initialize.apply(this, arguments);
      console.log('TestBodyView#initialize(%s)', this.cid);
    },
  });

  return TestBodyView;
});
