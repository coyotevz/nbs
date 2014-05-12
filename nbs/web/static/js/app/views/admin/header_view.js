define([
  'views/base/view',
  'views/admin/search_view',
], function(View, SearchView) {
  "use strict";

  var HeaderView = View.extend({
    template: 'admin/header.html',
    noWrap: true,

    render: function() {
      HeaderView.__super__.render.apply(this, arguments);

      var search = new SearchView({
        container: this.$('.search-box'),
      });
      this.subview('searchbox', search);
    },
  });

  return HeaderView;
});
