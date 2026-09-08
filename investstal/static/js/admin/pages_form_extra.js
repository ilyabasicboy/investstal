/* Initialization of the change_form page - this script is run once everything is ready. */

/* Автозаполнение слага только при первом заполнении title */
$(document).ready(function() {
    if ($('#id_title').val()) {
        $('#id_title').unbind('keyup');
    }
});