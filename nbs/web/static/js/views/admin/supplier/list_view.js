define([
  'views/base/view',
], function(View) {
  "use strict";

  var SupplierListView = View.extend({
    template: 'admin/supplier/list.html',
    noWrap: true,

    initialize: function(params) {
      SupplierListView.__super__.initialize.apply(this, arguments);
      console.log('SupplierListView %s', JSON.stringify(params));
    },

    getTemplateData: function() {
      return _.extend(
        SupplierListView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },
  });

  return SupplierListView;
});
