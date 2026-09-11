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
$('.filter-form-short input, .filter-form-short select').on('change', function(e) {
    e.preventDefault();
    ajax_send($(this).closest('.filter-form-short'));
});
