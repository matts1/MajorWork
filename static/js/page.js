$(document).ready(function () {
    /* Highlight current link */
    $('nav.header li').removeClass('active');
    $('nav.header li:has(a[href="' + document.location.pathname + '"])').addClass('active');
});
