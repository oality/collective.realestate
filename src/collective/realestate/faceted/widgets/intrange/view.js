/* Range Widget
*/

Faceted.IntRangeWidget = function(wid){
  var js_widget = this;
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();

  this.min = jQuery('input[name=min]', this.widget);
  this.max = jQuery('input[name=max]', this.widget);
  this.selected = [];

  var min = this.min.val();
  var max = this.max.val();
  if(min && max){
    this.selected = [this.min, this.max];
    Faceted.Query[this.wid] = [min, max];
  }

  // Handle clicks
  jQuery('form', this.widget).submit(function(){
    return false;
  });
  var handle = function(evt){js_widget.select_change(this, evt);};
  this.min.change(handle);
  this.max.change(handle);

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
};

Faceted.IntRangeWidget.prototype = {
  select_change: function(element){
    this.do_query(element);
  },

  do_query: function(element){
    var min = Number(this.min.val());
    if (isNaN(min) || min == 0) {
      min = '';
    }
    var max = Number(this.max.val());
    if (isNaN(max) || max == 0) {
      max = '';
    }
    if(!min && !max){
      this.selected = [];
      return false;
    }

    var value = [min, max];
    if(max!="" && max<min){
      var msg = max+"<"+min;
      Faceted.Form.raise_error(msg, this.wid + '_errors', []);
    }else{
      this.selected = [this.min, this.max];
      Faceted.Form.clear_errors(this.wid + '_errors', []);
      Faceted.Form.do_query(this.wid, value);
    }
  },

  reset: function(){
    this.selected = [];
    this.min.val('');
    this.max.val('');
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
      return false;
    }
    if(!value.length){
      this.reset();
      return false;
    }
    if(value.length<2){
      this.reset();
      return false;
    }

    var min = value[0];
    var max = value[1];

    // Set min, max inputs
    this.min.val(min);
    this.max.val(max);
    this.selected = [this.min, this.max];
  },

  criteria: function(){
    var html = [];
    var title = this.criteria_title();
    var body = this.criteria_body();
    if(title){
      html.push(title);
    }
    if(body){
      html.push(body);
    }
    return html;
  },

  criteria_title: function(){
    if(!this.selected.length){
      return '';
    }

    var link = jQuery('<a href="#">[X]</a>');
    link.attr('id', 'criteria_' + this.wid);
    link.attr('title', 'Remove ' + this.title + ' filters');
    var widget = this;
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });

    var html = jQuery('<dt>');
    html.append(link);
    html.append('<span>' + this.title + '</span>');
    return html;
  },

  criteria_body: function(){
    if(!this.selected.length){
      return '';
    }

    var widget = this;
    var html = jQuery('<dd>');
    var span = jQuery('<span class="faceted-range-criterion">');
    var min = this.min.val();
    var max = this.max.val();

    var label = min + ' - ' + max;
    var link = jQuery('<a href="#">[X]</a>');

    link.attr('id', 'criteria_' + this.wid + '_');
    link.attr('title', 'Remove ' + label + ' filter');
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });
    span.append(link);
    jQuery('<span>').text(label).appendTo(span);
    html.append(span);
    return html;
  },

  criteria_remove: function(){
    this.reset();
    return Faceted.Form.do_query(this.wid, []);
  }
};

Faceted.initializeIntRangeWidget = function(evt){
  jQuery('div.faceted-intrange-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.IntRangeWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeIntRangeWidget);
});
