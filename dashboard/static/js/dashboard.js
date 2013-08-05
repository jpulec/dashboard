/*! Script for pulling dashboard data
 *
 */

var configs = [
// Directory Services
{
    'display_name' : 'UDS LDAP (Production)',
    'multiple' : false,
    'tr_id' : 'dir_replcheck_prod',
    'url' : 'https://middleware.doit.wisc.edu/dashboard/json/on-replcheck.dashboard.json'
},
{
    'display_name' : 'UDS LDAP (Test)',
    'multiple' : false,
    'tr_id' : 'dir_replcheck_test',
    'url' : 'https://middleware.doit.wisc.edu/dashboard/json/center-replcheck.dashboard.json'
},];

$(document).ready(function(e) {

    // Directory Services
    drawDashboard();
    updateDashboard();
    setInterval(function() {
        updateDashboard();
    }, 15000);

});

function getStatusTableRow(config, items) {

    var dttm = 0;
    var statuses = {
        'ok' : 0,
        'info' : 0,
        'warn' : 0,
        'error' : 0
    };
    var status_descriptions = [];

    $.each(items, function(index, item) {
        statuses[item.status]++;

        if (item.status != 'ok') {

            var status_description = '<span title="'
        + item.status_description
        + '"><img src="{{ STATIC_URL }}img/'
        + item.status
        + '.png" height="16" width="16"/> '
        + item.display_name + '</span>';

    status_descriptions.push(status_description);
        }

        if (dttm < item.dttm) {
            dttm = item.dttm;
        }

    });

    var environment_status;
    if (statuses['error'] > 0) {
        environment_status = 'error';
    } else if (statuses['warn'] > 0) {
        environment_status = 'warn';
    } else if (statuses['info'] > 0) {
        environment_status = 'info';
    } else {
        environment_status = 'ok';
    }

    var environment_status_description;
    if (status_descriptions.length > 0) {
        environment_status_description = status_descriptions.join('<br/>');
    } else {
        environment_status_description = '<img src="{{ STATIC_URL }}img/ok.png" height="16" width="16"/> No issues detected.'
    }

    var seconds_ago = parseInt(((new Date).getTime() - (dttm * 1000)) / 1000);
    var minutes_ago = parseInt(((new Date).getTime() - (dttm * 1000)) / 60000);
    var hours_ago   = parseInt(((new Date).getTime() - (dttm * 1000)) / 3600000);
    var days_ago    = parseInt(((new Date).getTime() - (dttm * 1000)) / 86400000);

    var last_updated = "";

    if(days_ago > 1) {
        last_updated = '<span class="text-error">' + days_ago + ' days ago</span>';
    }
    else if(hours_ago > 1) {
        last_updated = '<span class="text-error">' + hours_ago + ' hours ago</span>';
    }
    else if(minutes_ago > 1) {
        if(minutes_ago > 60) {
            last_updated = '<span class="text-error">' + minutes_ago + ' minutes ago</span>';
        }
        else if(minutes_ago > 30) {
            last_updated = '<span class="text-warning">' + minutes_ago + ' minutes ago</span>';
        }
        else {
            last_updated = minutes_ago + ' minutes ago';
        }
    }
    else {
        if(seconds_ago == 1) {
            last_updated = seconds_ago + ' second ago';
        }
        else {
            last_updated = seconds_ago + ' seconds ago';
        }
    }

    var row = '<td class="environment">' + config.display_name
        + '<br/><span class="visible-phone"><small>' + last_updated
        + '</small></span></td><td class="environment_status">'
        + environment_status_description
        + '</td><td class="last_updated hidden-phone"><small>' + last_updated
        + '</small></td>';

    return row;
}

function drawDashboard() {
    $.each(configs, function(index, config) {
        var row = '<td class="environment">'
        + config.display_name
        + '</td><td class="environment_status" colspan="2"><img src="{{ STATIC_URL }}img/ajax-loader.gif"  height="16" width="16"/> Loading...</td>';

    $('tr#' + config.tr_id).html(row);
    });
}

function updateDashboard() {

    // Build the table body
    $.each(configs, function(index, config) {

        $.ajax({
            url : config.url,
        async : true,
        cache : false,
        timeout : 10000,
        dataType : 'json',
        success : function(json) {

            var table;

            if (config.multiple == true) {
                row = getStatusTableRow(config, json.items);
            } else {
                row = getStatusTableRow(config, [ json ]);
            }

            $('tr#' + config.tr_id).html(row);

        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {

            var row = '<td class="environment">'
                + config.display_name
                + '</td><td class="environment_status" colspan="2"><img src="{{ STATIC_URL }}img/error.png"  height="16" width="16"/> Failed to fetch or process data: '
                + errorThrown + '</td>';

            $('tr#' + config.tr_id).html(row);
        }

        });
    });

}
// Allows Internet Explorer to make AJAX CORS calls
$.ajaxTransport("+*", function( options, originalOptions, jqXHR ) {
    if(!jQuery.support.cors && window.XDomainRequest) {
        var xdr;
        return {
            send: function( headers, completeCallback ) {
                // Use Microsoft XDR
                xdr = new XDomainRequest();
                xdr.open("get", options.url);
                xdr.onload = function() {
                    if(this.contentType.match(/\/xml/)){
                        var dom = new ActiveXObject("Microsoft.XMLDOM");
                        dom.async = false;
                        dom.loadXML(this.responseText);
                        completeCallback(200, "success", [dom]);
                    }else{
                        completeCallback(200, "success", [this.responseText]);
                    }
                };
                xdr.ontimeout = function(){
                    completeCallback(408, "error", ["The request timed out."]);
                };
                xdr.onerror = function(){
                    completeCallback(404, "error", ["The requested resource could not be found."]);
                };
                xdr.send();
            },
                abort: function() {
                    if(xdr)xdr.abort();
                }
        };
    }
});
