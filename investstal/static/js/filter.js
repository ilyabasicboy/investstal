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

//Catalog filter
function catalog_filter_ajax_send($form, pagination=false, page='') {
    let formURL = $form.attr('action') + page;
    let form_array = $form.serializeArray();
    let data = {};
    for (let i = 0; i < form_array.length; i++)
        data[form_array[i].name] = form_array[i].value;

    $.get(formURL, data, function(data) {
        if (pagination) {
            $('.show-more-filter').replaceWith(data['html']);
            $('.loader-js').removeClass('active');
        } else {
            $('.product-list-js').html(data['html']);
            $('.products_count').html(data['count']);
            scroll_to_catalog();
        }
    });
}

function scroll_to_catalog() {
    let $catalogPanel = $('.catalog__panel');
    if (!$catalogPanel.length) {
        return;
    }

    let headerHeight = $('.header__bottom').outerHeight() || $('.header').outerHeight() || 0;
    let destination = $catalogPanel.offset().top - headerHeight - 40;
    $('html, body').animate({ scrollTop: destination }, 500, 'swing');
}

$(document).on('change', '.filter-form select', function(e) {
    e.preventDefault();
    catalog_filter_ajax_send($(this).closest('.filter-form'));
});

$(document).on('change', '.filter-form .filter__price-input', function(e) {
    e.preventDefault();
    catalog_filter_ajax_send($(this).closest('.filter-form'));
});

$(document).on('keypress', '.filter-form .filter__price-input', function(e) {
    if (e.which === 13) {
        e.preventDefault();
        catalog_filter_ajax_send($(this).closest('.filter-form'));
    }
});

$(document).on('click', '.show-more-filter a', function(e) {
    e.preventDefault();
    $('.loader-js').addClass('active');
    catalog_filter_ajax_send($('.filter-form'), true, $(this).attr('href'));
});

$(document).on('click', '.filter-reset-js', function(e) {
    e.preventDefault();

    let $form = $('.filter-form');
    $form.find('select[name="dir"]').val('new');
    $form.find('select[name="category"]').val('');
    $form.find('.filter__price-input--min').val('');
    $form.find('.filter__price-input--max').val('');

    catalog_filter_ajax_send($form);
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
