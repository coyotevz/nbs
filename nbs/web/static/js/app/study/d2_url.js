// document sample test
// jshint -W097

"use strict";

var require = require;
var console = console;

var Backbone = require('backbone-associations');
var lodash = require('lodash');

Backbone.AssociatedModel.prototype.url = lodash.wrap(
  Backbone.AssociatedModel.prototype.url,
  function(originalUrl) {
    var base, p;
    base = originalUrl.call(this);
    p = this.collection && this.collection.parents;
    if (p && p.length === 1) {
      base = lodash.result(p[0], 'url') + base;
    }
    return base;
  }
);

var Location = Backbone.AssociatedModel.extend({
  defaults: {
    id: -1,
    zip: "",
  },
});

var Locations = Backbone.Collection.extend({
  model: Location,
  url: '/locations',
});

var Department = Backbone.AssociatedModel.extend({
  relations: [
    {
      type: Backbone.Many,
      key: 'locations',
      collectionType: Locations,
    }
  ],
  defaults: {
    name: '',
    number: -1,
  },
});

var Departments = Backbone.Collection.extend({
  model: Department,
  url: '/departments',
});

var departments = new Departments();

departments.add({
  name: 'dep1',
  id: 1,
  locations: [
    {
      id: 'loc1-1',
      zip: '91001',
    },
    {
      id: 'loc1-2',
      zip: '91002',
    },
  ]
});

departments.add({
  name: 'dep2',
  id: 2,
  locations: [
    {
      id: 'loc2-1',
      zip: '91004',
    },
    {
      id: 'loc2-2',
      zip: '91005',
    },
    {
      id: 'loc2-3',
      zip: '91006',
    },
  ],
});
