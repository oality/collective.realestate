FacetedEdit.MoreOrLessWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.moreorless = jQuery('input[name=moreorless]', this.widget);

  var js_widget = this;
  this.moreorless.change(function(){
    js_widget.set_default(this);
  });
};

FacetedEdit.MoreOrLessWidget.prototype = {
  set_default: function(element){
    var moreorless = this.moreorless.val();
    if(!moreorless){
      return;
    }

    var value = '';
    if(moreorless){
      value = moreorless;
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

FacetedEdit.initializeMoreOrLessWidget = function(){
  jQuery('div.faceted-moreorless-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.MoreOrLessWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeMoreOrLessWidget);
});
