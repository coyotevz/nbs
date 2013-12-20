define([
  'views/base/view',
], function(View) {
  "use strict";

  var SideHeaderView = View.extend({
    template: 'admin/side_header.html',
    noWrap: true,

    items: [
      {
        title: 'Productos',
        url: 'products',
      },
      {
        title: 'Proveedores',
        url: 'suppliers',
      }
    ],

    initialize: function() {
      this.subscribeEvent('router:match', this._update);
      return SideHeaderView.__super__.initialize.apply(this, arguments);
    },

    _update: function(route, params, options) {
      console.info('match:', route, params, options);
    },

    getTemplateData: function() {
      return {items: this.items};
    },

  });

  return SideHeaderView;
});
