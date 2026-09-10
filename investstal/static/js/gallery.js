import jQueryBridget from 'jquery-bridget';
import Masonry from 'masonry-layout';
import imagesLoaded from 'imagesloaded';
import { Fancybox } from '@fancyapps/ui';

import getScrollbarWidth from './getscrollbarwidth';

Fancybox.bind("[data-fancybox]", {
    on: {
        init: () => {
            $('.header').css('padding-right', `${getScrollbarWidth()}px`);
        },
        destroy: () => {
            $('.header').css('padding-right', '0px');
        }
    }
});

imagesLoaded.makeJQueryPlugin($);
jQueryBridget('masonry', Masonry, $);

$(document).ready(function() {
    $('.gallery__column').each(function() {
        const $grid = $(this);

        if ($grid.length !== 0) {
            $grid.imagesLoaded(function() {
                $grid.masonry({
                    itemSelector: '.gallery__column-item',
                    columnWidth: '.gallery__column-sizer',
                    percentPosition: true,
                    gutter: 20
                });

                $grid.removeClass('gallery__column--hidden');
            });
        }
    });
});

function ajaxSend($form, pagination = false, page = '') {
    const formURL = $form.attr('action') + page;
    const formArray = $form.serializeArray();
    const data = {};

    for (let i = 0; i < formArray.length; i++) {
        data[formArray[i].name] = formArray[i].value;
    }

    const $container = $form.closest('.section-default');
    const $grid = $container.find('.gallery__column');

    if (!pagination) {
        $grid.addClass('gallery__column--hidden');
    }

    $.get(formURL, data, function(data) {
        if (pagination) {
            const $newItems = $(data.html).filter('.gallery__column-item');

            $newItems.addClass('gallery__column--hidden');
            $container.find('.images-list').append($newItems);
            $newItems.imagesLoaded().done(function() {
                $grid.masonry('appended', $newItems);
                $newItems.removeClass('gallery__column--hidden');
            });

            $container.find('.images-list .show-more').replaceWith($(data.html).filter('.show-more'));
            $container.find('.loader-js').removeClass('active');
        } else {
            setTimeout(function() {
                const $sizer = $container.find('.gallery__column-sizer').detach();

                $container.find('.images-list').html(data.html);
                $grid.prepend($sizer);

                $grid.imagesLoaded().done(function() {
                    if ($grid.data('masonry')) {
                        $grid.masonry('destroy');
                        $grid.removeData('masonry');
                    }

                    $grid.masonry({
                        itemSelector: '.gallery__column-item',
                        columnWidth: '.gallery__column-sizer',
                        percentPosition: true,
                        gutter: 20
                    });
                    $grid.masonry('layout');
                    $grid.removeClass('gallery__column--hidden');
                });
            }, 200);
        }
    });
}

$(document).on('change', '.gallery-form', function() {
    ajaxSend($(this));
});

$(document).on('click', '.images-list .show-more a', function(e) {
    e.preventDefault();

    const $container = $(this).closest('.section-default');
    let $form = $container.find('.gallery-form');

    if ($form.length === 0) {
        $form = $(this).closest('.update-gallery-object');
    }

    $container.find('.loader-js').addClass('active');
    ajaxSend($form, true, $(this).attr('href'));
});
