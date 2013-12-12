define([
  'chaplin',
  'views/base/view',
], function(Chaplin, View) {
  "use strict";

  var SideView = View.extend({
    template: 'admin/side.html',

    getTemplateData: function() {
      return _.extend(
        SideView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },

    render: function() {
      console.log('rendering SideView');
      return SideView.__super__.render.apply(this, arguments);
    },

    attach: function() {
      console.log('attaching SideView');
      return SideView.__super__.attach.apply(this, arguments);
    },
  });

  return SideView;
});
