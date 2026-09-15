//Filter Form
function ajax_send($form, page='', callback=null) {
    //Serialize Form
    let formURL = $form.attr('action') + page;
    let form_array = $form.serializeArray();
    let data = {};
    for (let i = 0; i < form_array.length; i++)
        data[form_array[i].name] = form_array[i].value;

    //Load Content
    $.get(formURL, data, callback || function(data) {
        $('.products_count').html(data['products_count']);
        $('.filter-update-ajax').html(data['html']);
    });
};

//Categories form
$('.filter-form-short input').on('change', function(e) {
    e.preventDefault();
    ajax_send($(this).closest('.filter-form-short'));
});

//Product finish popup
$('.facing-btn-js').on('click', function() {
    let id = $(this).data('id');
    let url = $(this).data('url');
    let popup = $('#facing-modal .modal__load');

    if (id != popup.data('id')) {
        popup.addClass('load');
        $.get(url, function(data) {
            popup.html(data['html']);
            popup.data('id', id);

            popup.removeClass('load');
        });
    }
});

//Product parameter popup
$('.parameter-btn-js').on('click', function() {
    let id = $(this).data('id');
    let url = $(this).data('url');
    let popup = $('#parameter-modal .modal__load');

    if (id != popup.data('id')) {
        popup.addClass('load');
        $.get(url, function(data) {
            popup.html(data['html']);
            popup.data('id', id);

            popup.removeClass('load');
        });
    }
});
