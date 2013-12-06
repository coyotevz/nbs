define([
  'views/base/view',
], function(View) {
  "use strict";

  var BodyView = View.extend({
    template: 'admin/body.html',

    regions: {
      sidebar_header: '',
      sidebar: '',
      sidebar_footer: '',
      toolbox: '',
      content_header: '',
      content: '',
      content_footer: '',
    },

    initialize: function() {
      BodyView.__super__.initialize.apply(this, arguments);
      console.log('BodyView#initialize(%s)', this.cid);
    },
  });

  return BodyView;
});
