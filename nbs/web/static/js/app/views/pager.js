define([
  'views/base/view',
], function(View) {
  "use strict";

  var Pager = View.extend({
    template: 'admin/pager.html',
    noWrap: true,
    optionNames: View.prototype.optionNames.concat(['collection', 'field']),
    events: {
      'click [name=prev-page]': 'prevPage',
      'click [name=next-page]': 'nextPage',
    },

    initialize: function() {
      Pager.__super__.initialize.apply(this, arguments);
      this.listenTo(this.collection, 'sync', this._update);
    },

    render: function() {
      Pager.__super__.render.apply(this, arguments);
      this._update();
    },

    prevPage: function(evt) {
      this._changePage(-1);
    },

    nextPage: function(evt) {
      this._changePage(+1);
    },

    _update: function() {
      if (this.collection.length > 0) {
        var coll = this.collection;
        this.$('.first').text(coll.first().get(this.field).split(' ')[0]);
        this.$('.last').text(coll.last().get(this.field).split(' ')[0]);
        this.$('[name=prev-page]').prop('disabled', coll.page <= 1);
        this.$('[name=next-page]').prop('disabled', coll.page >= coll.num_pages);
      }
    },

    _changePage: function(n) {
      this.$('[rel=tooltip]').tooltip('hide');
      this.collection.fetch({
        data: {
          page: this.collection.page + n
        }
      });
    }
  });

  return Pager;
});
