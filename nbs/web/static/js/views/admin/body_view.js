define([
  'jquery',
  'views/base/view',
], function($, View) {
  "use strict";

  var BodyView = View.extend({
    template: 'admin/body.html',

    regions: {
      sidebar_header: '#sidebar_header',
      sidebar: '#sidebar',
      sidebar_footer: '#sidebar_footer',
      toolbar: '#toolbar',
      content_header: '#content_header',
      content: '#content',
      content_footer: '#content_footer',
    },

    initialize: function() {
      BodyView.__super__.initialize.apply(this, arguments);
      console.log('BodyView#initialize(%s)', this.cid);
      console.log(this.$('#content_wrapper'));
    },

    render: function() {
      BodyView.__super__.render.apply(this, arguments);
      $(window).resize(this.resize);
      $(window).focus(this.resize);
      this.resize();
    },

    resize: function() {
      var contentWrapper = this.$('#content_wrapper'),
          scrollWrapper = this.$('#scroll_wrapper'),
          contentAvlWidth = $(window).width() - $('aside').width(),
          contentAvlHeight = $(window).height() - contentWrapper.position().top;

      console.log('window.width:', $(window).width(), 'aside.width:', $('aside').width());

      contentWrapper.width(contentAvlWidth);
      contentWrapper.height(contentAvlHeight);
      scrollWrapper.height(contentAvlHeight);
    },
  });

  return BodyView;
});
