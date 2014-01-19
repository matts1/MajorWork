$(document).ready(function () {
    // Highlight current link in navbar
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

    $('form').ajaxForm({
        beforeSubmit: function (arr, form, options) {
            // delete the old error messages from the screen
            $('[data-submitted=true]', form).remove();

            // add a loading icon
            insertAfterLastInput('<img src="/images/loading.gif" alt="loading">', form);
        },
        success: function (responseText, statusText, xhr, form) {
            if (responseText.length > 9 && responseText.substring(0,9) == 'REDIRECT:') {
                window.location = window.location.origin + responseText.substring(9);
            }
            // remove the loading icon if it exists
            insertAfterLastInput('', form);

            // this line fixes a bug where you can't search for the outermost tag, so we wrap it
            responseText = '<nav>' + responseText + '</nav>';

            // Fill in the error messages with the response from the server
            $('div', $(responseText)).each(function () {
                var name = $(this).attr('data-for');
                var msg = $(this.outerHTML);
                msg.attr('data-submitted', 'true');
                if (name == '') {
                    insertAfterLastInput(msg[0].outerHTML, form);
                } else {
                    $('input[name=' + name + ']', form).parent().parent().after(msg);
                }
            });
        }
    });

});

function insertAfterLastInput(data, container) {
    // all inputs other than submit
    $('div.formresults', container).html('<div class="text-center help-block">' + data + '</div>');
}
