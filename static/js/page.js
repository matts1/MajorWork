$(document).ready(function () {
    // Highlight current link
    $('nav.header li').removeClass('active');
    $('nav.header li:has(a[href="' + document.location.pathname + '"])').addClass('active');

    // Open up old modal if the form wasn't filled out correctly
    //noinspection JSJQueryEfficiency
    $('div.openmodal').each(function () {
        var element = $('#' + this.id);
        if (element.hasClass('modal')) {
            element.modal({show: true});
        }
    });

    // Add in a success message
    $('div.successmsg').each(function () {
        var form = $($('#' + $(this).attr('data-formid'))[0]);
        insertAfterLastInput('<div class="alert alert-success">' + $(this).text() + '</div>', form);
    });


    // get the id of the container of the form
    var outerlayer = $($("body")[0]);
    //noinspection JSJQueryEfficiency
    if (!($('div.openmodal')[0] === undefined)) {
        outerlayer = $('#' + $('div.openmodal')[0].id);
    }

    // Fill in the old values in the form
    $('div.origvals div').each(function () {
        var name = $('p', this).text();
        var on = $('input[name=' + name + ']', outerlayer);
        var msg = $('span', this).text();
        on.attr('value', msg);
    });

    // Fill in the error messages telling them what they did wrong
    $('div.errlist div').each(function () {
        var name = $('p', this).text();
        var msg = $('span', this).text();
        if (msg != '') {
            if (name == '') {
                insertAfterLastInput('<div class="alert alert-danger">' +
                    msg + '</div>', outerlayer);
            } else {
                var on = $('input[name=' + name + ']', outerlayer).parent();
                on.parent().addClass('has-error');
                on.append('<div class="alert alert-danger">' + msg + '</div>');
            }
        }
    });
});

function insertAfterLastInput(data, container) {
    // all inputs other than submit
    var on = $('input:not([type=submit])', container);
    // get the last input, then go up 2 levels to get the div input is in
    on = $(on[on.length - 1]).parent().parent();
    on.after('<div class="text-center help-block">' + data + '</div>');
}
