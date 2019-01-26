
// For responsive footer
function checkWidth(init)
{
    /*If browser resized, check width again */
    if ($(window).width() < 800) {
    $('#footer_col_01').addClass('col-10');
            $('#footer_col_02').addClass('col-10');  
            $('#footer_col_01').removeClass('col-4');
            $('#footer_col_02').removeClass('col-4');
            $('#footer_container').addClass('center');
            
    }
    else {
    $('#footer_col_01').addClass('col-4');
            $('#footer_col_02').addClass('col-4');  
            $('#footer_col_01').removeClass('col-10');
            $('#footer_col_02').removeClass('col-10');
            $('#footer_container').removeClass('center');
    }
}

$(document).ready(function() {
    checkWidth();
    $(window).resize(function() {
        checkWidth();
    });
});