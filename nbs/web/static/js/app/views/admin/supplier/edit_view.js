define([
  'views/base/view',
], function(View) {
  "use strict";

  var SupplierEditView = View.extend({
    template: 'admin/supplier/edit.html',
    noWrap: true,

    initialize: function(params) {
      SupplierEditView.__super__.initialize.apply(this, arguments);
      console.log('SuppierEditView %s', JSON.stringify(params));
    },

    getTemplateData: function() {
      return _.extend(
        SupplierEditView.__super__.getTemplateData.apply(this, arguments),
        {cid: this.cid}
      );
    },
  });

  return SupplierEditView;
});
