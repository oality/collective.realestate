FacetedEdit.IntRangeWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.min = jQuery('input[name=min]', this.widget);
  this.max = jQuery('input[name=max]', this.widget);

  var js_widget = this;
  this.min.change(function(){
    js_widget.set_default(this);
  });

  this.max.change(function(){
    js_widget.set_default(this);
  });
};

FacetedEdit.IntRangeWidget.prototype = {
  set_default: function(element){
    var min = this.min.val();
    var max = this.max.val();
    if((!min && max) || (min && !max)){
      return;
    }

    var value = '';
    if(min && max){
      if(max<min){
        var msg = 'max should be greater than min';
        jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: msg});
        return;
      }
      value = min + '=>' + max;
    }
    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query['faceted.' + this.wid + '.default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeIntRangeWidget = function(){
  jQuery('div.faceted-range-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.IntRangeWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeIntRangeWidget);
});
