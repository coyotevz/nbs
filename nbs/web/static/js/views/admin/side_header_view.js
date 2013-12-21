define([
  'views/base/view',
], function(View) {
  "use strict";

  var SideHeaderView = View.extend({
    template: 'admin/side_header.html',
    noWrap: true,

    menuItems: [
      {
        name: 'product',
        title: 'Productos',
        url: 'products',
      },
      {
        name: 'supplier',
        title: 'Proveedores',
        url: 'suppliers',
      },/*
      { name: '-divider-' },
      {
        name: 'invoice',
        title: 'Facturas',
        url: null,
        disabled: true,
      },
      {
        name: 'contacts',
        title: 'Contactos',
        url: null,
        disabled: true,
      },*/
    ],

    initialize: function() {
      this._current = null;
      this.subscribeEvent('menu:setCurrent', this.setCurrentMenu);
      return SideHeaderView.__super__.initialize.apply(this, arguments);
    },

    getTemplateData: function() {
      return {items: this.menuItems};
    },

    setCurrentMenu: function(menu) {
      if (this._current == menu) return;
      var item = this._getMenuItem(menu);
      if (item != null) {
        this._current = menu;
        this.$('.dropdown-toggle span').text(item.title);
        this.$('.dropdown-menu li.current').removeClass('current');
        this.$('.dropdown-menu li.'+menu).addClass('current');
      }
    },

    _getMenuItem: function(name) {
      for (var i in this.menuItems) {
        if (this.menuItems[i].name == name) return this.menuItems[i];
      }
      return null;
    },

  });

  return SideHeaderView;
});
