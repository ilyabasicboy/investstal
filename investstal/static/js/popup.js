//Import function
import ajaxReset from './feedback';

$(function () {

    //Form Modal
    function initModal() {
        $('.modal-open').each(function() {
            $(this).magnificPopup({
                type: 'inline',
                items: {
                    src: $(this).data('href')
                },
                removalDelay: 500,
                mainClass: 'mfp-move',
                autoFocusLast: false,
                callbacks: {
                    open: function () {
                        $('body').addClass("noscroll");
                    },
                    close: function () {
                        $('body').removeClass("noscroll");

                        //Reload Form
                        ajaxReset(this.content.find('[data-reset]'));
                    },
                },
            });
        });
    };
    initModal();

    //Gallery Modal
    function initGallery() {
        $('.mfp-gallery').each(function() {
            $(this).magnificPopup({
                type: 'image',
                removalDelay: 500,
                mainClass: 'mfp-fade',
                autoFocusLast: false,
                image: {
                    cursor: null,
                    tClose: 'Закрыть',
                    titleSrc: function(item) {
                        return item.img.attr('alt');
                    }
                },
                gallery: {
                    enabled: true,
                    preload: [0, 2],
                    navigateByImgClick: true,
                    tPrev: 'Предыдущее фото',
                    tNext: 'Следующее фото'
                },
                delegate: 'a[href$=".png"][target!="_blank"], \
                               a[href$=".PNG"][target!="_blank"], \
                               a[href$=".jpeg"][target!="_blank"], \
                               a[href$=".JPEG"][target!="_blank"], \
                               a[href$=".jpg"][target!="_blank"], \
                               a[href$=".JPG"][target!="_blank"]',
                callbacks: {
                    buildControls: function() {
                        if (this.items.length > 1) {
                            this.contentContainer.append(this.arrowLeft.add(this.arrowRight));
                        }
                    },
                    open: function() {
                        $('body').addClass('noscroll');
                    },
                    close: function() {
                        $('body').removeClass('noscroll');
                    }
                },
                closeMarkup: '<button title="Закрыть" type="button" class="mfp-close"></button>',
            });
        });
    };
    initGallery();

    //Reinit popup
    let target = document.querySelectorAll('.ajax-update-popup');
    target.forEach(element => {
        if (element) {
            let observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    initModal();
                    initGallery();
                });
            });
            let config = { childList: true, characterData: true };
            observer.observe(element, config);
        }
    });

});