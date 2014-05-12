define([
  'views/base/view',
], function(View) {
  "use strict";

  var SearchView = View.extend({
    template: 'admin/searchbar.html',
    noWrap: true,

    events: {
      'change [name=term]': 'onSearch',
      'click [name=search]': 'onSearch',
    },

    render: function() {
      SearchView.__super__.render.apply(this, arguments);
      this.$termInput = this.$('[name=term]');
    },

    onSearch: function(evt) {
      var term = this.$termInput.val();
      if (term === "") {
        console.log('no search term for', this.$termInput);
      } else {
        console.log('search activated! term:', term);
      }
    },
  });

  return SearchView;
});
