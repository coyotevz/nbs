define([
  'views/base/view',
], function(View) {
  "use strict";

  var SideHeaderView = View.extend({
    template: 'admin/side_header.html',
    noWrap: true,
  });

  return SideHeaderView;
});
