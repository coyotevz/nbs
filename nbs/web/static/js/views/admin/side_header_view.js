define([
  'views/base/view',
], function(View) {
  "use strict";

  var SideHeaderView = View.extend({
    template: 'admin/side_header.html',
    noWrap: true,

    render: function() {
      console.log('rendering SideHeaderView');
      return SideHeaderView.__super__.render.apply(this, arguments);
    },

    attach: function() {
      console.log('attaching SideHeaderView');
      return SideHeaderView.__super__.attach.apply(this, arguments);
    },
  });

  return SideHeaderView;
});
