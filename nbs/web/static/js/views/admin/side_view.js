define([
  'chaplin',
  'views/base/view',
], function(Chaplin, View) {
  "use strict";

  var SideView = View.extend({
    template: 'admin/side.html',

    getTemplateData: function() {
      return _.extend(
        View.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },
  });

  return SideView;
});
