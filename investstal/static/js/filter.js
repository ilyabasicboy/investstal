//Import variable
import {
	breakpointMDMax
} from './match-media';

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
            scrollToCatalog();
        }
    });
};

//Scroll to catalog
function scrollToCatalog() {
    let $catalogPanel = $('.catalog__panel');
    if (!$catalogPanel.length) {
        return;
    }

    let headerHeight = $('.header').outerHeight() || 0;
    let destination = $catalogPanel.offset().top - headerHeight - 40;
    $('html, body').animate({ scrollTop: destination }, 500, 'swing');
};

//Filter form check change
function debounce(func, wait) {
	let timeout;
	return function executedFunction(...args) {
		const later = () => {
			clearTimeout(timeout);
			func(...args);
		};
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
	};
};
function triggerFilter(e) {
	e.preventDefault();
	$('.filter__price-content').removeClass('active');
	catalog_filter_ajax_send($('.filter-form'));
};
const debouncedTrigger = debounce(triggerFilter, 300);
$('.filter-form input').on('input', function(e) {
	if (!breakpointMDMax.matches) {
		debouncedTrigger(e);
	}
});
$('.filter-form select').on('change', triggerFilter);
$('.filter-form').on('submit', triggerFilter);

//Filter reset ajax
$(document).on('click', '.filter-reset-js', function(e) {
	e.preventDefault();
	$('.filter-form').each(function(index, form) {
		form.reset();
	});
	let form = $('.filter-form');
	catalog_filter_ajax_send(form);
});

//Show more
$(document).on('click', '.show-more-filter a', function(e) {
    e.preventDefault();
    $('.loader-js').addClass('active');
    catalog_filter_ajax_send($('.filter-form'), true, $(this).attr('href'));
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
