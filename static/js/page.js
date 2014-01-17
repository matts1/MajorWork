$(document).ready(function () {
    // Highlight current link
    $('nav.header li').removeClass('active');
    $('nav.header li:has(a[href="' + document.location.pathname + '"])').addClass('active');

    // Open up old modal if the form wasn't filled out correctly
    $('div.openmodal').each(function () {
        $('#' + this.id).modal({show: true});
    });

    // Fill in the old values in the form
    var outerlayer = $('#' + $('div.openmodal')[0].id);
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
            var on = $('.modal-body', outerlayer);
            on.append('<div class="text-center"><span class="help block has-error">' +
                msg + '</span></div>');
        } else {
            var on = $('input[name=' + name + ']', outerlayer).parent();
            on.parent().addClass('has-error');
            on.append('<span class="help block">' + msg + '</span>');
            console.log(on);
        }
    });
});
