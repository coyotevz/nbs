define([
  'views/base/view',
], function(View) {
  "use strict";

  var SidebarView = View.extend({
    template: 'admin/sidebar.html',
    noWrap: true,

    menuItems: [
      {
        name: 'dashboard',
        title: 'Tablero principal',
        url: 'dashboard',
        icon: 'dashboard',
    }, {
        name: 'product',
        title: 'Productos',
        url: 'products',
      }, {
        name: 'supplier',
        title: 'Proveedores',
        url: 'suppliers',
      },
    ],

    initialize: function() {
      this._current = null;
      this.subscribeEvent('menu:setCurrent', this.setCurrentMenu);
      return SidebarView.__super__.initialize.apply(this, arguments);
    },

    getTemplateData: function() {
      return {items: this.menuItems};
    },

    setCurrentMenu: function(menu) {
      if (this._current == menu) return;
      var item = this._getMenuItem(menu);
      console.log('setCurrentMenu', item, menu);
      if (item !== null) {
        this._current = menu;
        this.$('li.active').removeClass('active');
        this.$('li#menu-item-'+menu).addClass('active');
      }
    },

    _getMenuItem: function(name) {
      for (var i in this.menuItems) {
        if (this.menuItems[i].name == name) return this.menuItems[i];
      }
      return null;
    },
  });

  return SidebarView;
});
