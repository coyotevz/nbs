define([
  'jquery',
], function($) {
  "use strict";

  // RADIO CLASS DEFINITION
  // ======================

  var Radio = function(input, group) {
    this.group = group;
    this.input = $(input);
    this.radio = this.input.parents('.radio, .radio-inline').first();
    this.init();
  };

  Radio.prototype.init = function() {
    var label = this.radio.is('label') ? this.radio : this.radio.find('label');
    var mark = $('<div class="control-radio-checkmark">');
    this.control = $('<div class="control-radio">');

    this.input.toggleClass('radio-element', true);
    this.control.append(mark);
    this.input.after(this.control);
    this.input.on('change', $.proxy(this, 'onChange'));
    this.input.on('focusin focusout', $.proxy(this, 'onFocusChange'));

    if (label) {
      label.on('mouseenter mouseleave', $.proxy(this, 'onHover'));
    }

    this.control.on('mouseenter mouseleave', $.proxy(this, 'onHover'));
    this.onChange(); // Check initial state

    this.radio.data('nbs.radio', this); // Attach object to radio element
  };

  Radio.prototype.clear = function() {
    this.control.removeClass('checked');
  };

  Radio.prototype.onChange = function() {
    if (this.input.prop('checked')) {
      this.group.clearChecked();
      this.control.addClass('checked');
      this.group.checked = this;
    }
  };

  Radio.prototype.onFocusChange = function(evt) {
    this.control.toggleClass('focus', evt.type == "focusin");
  };

  Radio.prototype.onHover = function(evt) {
    this.control.toggleClass('hover', evt.type == "mouseenter");
  };

  // RADIO GROUP CLASS DEFINITION
  // ============================

  var RadioGroup = function(element) {
    var form, name, inputs, _this;
    this.checked = null;

    form = $(element).parents('form');
    name = $(element).find('input[type=radio]').prop('name');
    inputs = form.find('input[type=radio][name=' + name + ']');
    _this = this;
    inputs.each(function(idx, input) {
      var i = new Radio(input, _this);
    });
  };

  RadioGroup.prototype.clearChecked = function() {
    if (this.checked) this.checked.clear();
  };

  // PLUGIN DECLARATION
  // ==================

  $.fn.nbsRadio = function(options) {
    return this.each(function() {
      var $this = $(this);
      var data = $this.data('nbs.radio');

      if (!data) new RadioGroup(this);
    });
  };

  // Activate plugin on default elements
  $(document).find('.radio, .radio-inline').nbsRadio();

});
