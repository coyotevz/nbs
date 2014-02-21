define([
  'views/base/view',
], function(View) {
  "use strict";

  var SupplierDetailView = View.extend({
    template: 'admin/supplier/detail.html',
    noWrap: true,

    initialize: function(params) {
      SupplierDetailView.__super__.initialize.apply(this, arguments);
      console.log('SuppierDetailView %s', JSON.stringify(params));
    },

    getTemplateData: function() {
      return _.extend(
        SupplierDetailView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },
  });

  return SupplierDetailView;
});
