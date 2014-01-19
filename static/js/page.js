$(document).ready(function () {
    // Highlight current link
    $('nav.header li').removeClass('active');
    $('nav.header li:has(a[href="' + document.location.pathname + '"])').addClass('active');

    // Open up old modal if the form wasn't filled out correctly
    $('div.openmodal').each(function () {
        var element = $('#' + this.id);
        if (element.hasClass('modal')) {
            element.modal({show: true});
        }
    });

    // Add in a success message
    $('div.successmsg').each(function () {
        var form = $($('#' + $(this).attr('for'))[0]);
        insertAfterLastInput('<p class="text-success">' + $(this).text() + '</p>', form);
    })


    // get the id of the container of the form
    var outerlayer = $($("body")[0]);
    if (!($('div.openmodal')[0] === undefined)) {
        var outerlayer = $('#' + $('div.openmodal')[0].id);
    }

    // Fill in the old values in the form
    $('dl.origvals div').each(function () {
        var name = $('dt', this).text();
        var on = $('input[name=' + name + ']', outerlayer);
        var msg = $('dd', this).text();
        on.attr('value', msg);
    });

    // Fill in the error messages telling them what they did wrong
    $('dl.errlist div').each(function () {
        var name = $('dt', this).text();
        var msg = $('dd', this).text();
        if (name == '') {
            insertAfterLastInput('<span class="text-danger">' +
                msg + '</span>', outerlayer);
        } else {
            var on = $('input[name=' + name + ']', outerlayer).parent();
            on.parent().addClass('has-error');
            on.append('<p class="help-block">' + msg + '</p>');
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
