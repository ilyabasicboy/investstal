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

    //Reinit popup
    let target = document.querySelectorAll('.ajax-update-popup');
    target.forEach(element => {
        if (element) {
            let observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    initModal();
                });
            });
            let config = { childList: true, characterData: true };
            observer.observe(element, config);
        }
    });

});