function get_vehicle_color(){
    new Ajax.Request('/auto/ajax_purpose_staff/', {
    method: 'post',
    parameters: $H({'type':$('id_type').getValue()}),
    onSuccess: function(transport) {
        var e = $('id_color')
        if(transport.responseText)
            e.update(transport.responseText)
    }
    }); // end new Ajax.Request
}