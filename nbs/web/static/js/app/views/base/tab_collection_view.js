define([
  'views/base/collection_view',
], function(CollectionView) {
  "use strict";

  /* Borrowed from chaplinjs code */
  var insertView = function(list, viewEl, position, length, itemSelector) {
    var children, childrenLength, insertInMiddle, isEnd, method;
    insertInMiddle = (0 < position && position < length);
    isEnd = function(length) {
      return length === 0 || position == length;
    };
    if (insertInMiddle || itemSelector) {
      children = list.children(itemSelector);
      childrenLength = children.length;
      if (children[position] !== viewEl) {
        if (isEnd(childrenLength)) {
          return list.append(viewEl);
        } else {
          if (position === 0) {
            return children.eq(position).before(viewEl);
          } else {
            return children.eq(position - 1).after(viewEl);
          }
        }
      }
    } else {
      method = isEnd(length) ? 'append' : 'prepend';
      return list[method](viewEl);
    }
  };

  /* Override default collection view for render Tab/Pill view
   */

  var TabCollectionView = CollectionView.extend({
    headerView: null,
    headerSelector: null,
    $header: null,
    optionNames: CollectionView.prototype.optionNames.concat(['headerView']),

    render: function() {
      /* Create $header element and delegates to super */
      var headerSelector, _orig_renderItems;
      _orig_renderItems = this.renderItems;
      this.renderItems = false;

      CollectionView.__super__.render.apply(this, arguments);
      headerSelector = _.result(this, 'headerSelector');
      this.$header = headerSelector ? this.$(headerSelector) : void 0;

      this.renderItems = _orig_renderItems;
      if (this.renderItems) {
        return this.renderAllItems();
      }
    },

    renderHeader: function(item) {
      var view;
      view = this.subview("headerView:" + item.cid);
      if (!view) {
        view = this.initHeaderView(item);
        this.subview("headerView:" + item.cid, view);
      }
      view.render();
      return view;
    },

    initHeaderView: function(model) {
      if (this.headerView) {
        return new this.headerView({
          autoRender: false,
          model: model,
        });
      } else {
        throw new Error('The TabCollectionView#haderView property must be ' +
                        'defined or the initHeaderView() must be overriden.');
      }
    },



    insertView: function(item, view, position, enableAnimation) {
      var elem, included, length, header, hview;
      hview = this.subview("headerView:" + item.cid);
      if (!hview) {
        hview = this.renderHeader(item);
      }
      if (typeof position !== 'number') {
        position = this.collection.indexOf(item);
      }
      included = typeof this.filterer === 'function' ? this.filterer(item, position) : true;
      elem = hview.$el;
      if (this.filterer) {
        this.filterCallback(hview, included);
      }
      length = this.collection.length;
      header = this.$header;
      insertView(header, elem, position, length, this.headerSelector);
      return CollectionView.__super__.insertView.apply(this, arguments);
    },

    removeViewForItem: function(item) {
      TabCollectionView.__super__.removeViewForItem.apply(this, arguments);
      this.removeSubview('headerView:' + item.cid);
    },
  });

  return TabCollectionView;
});
