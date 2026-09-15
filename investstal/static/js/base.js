$(function () {

    //Fix Transition CSS
    $('body').removeClass('fix-anim');

    //Init Phone Mask
    $(document).on('focus', 'input[name*="phone"]', function() {
        $(this).mask('+7 (999) 999-99-99');
    });

    //Wrap for Table
    $('.placeholder table').wrap('<div class="table-wrap"></div>');

    //Wrap for Iframe
    let placeholderVideo = $('.placeholder iframe');
    placeholderVideo.each(function (index, item) {
        let videoMaxWidth = $(item).attr('width');
        $(item).wrap('<div class="iframe-wrap" style="max-width: ' + videoMaxWidth + 'px;"></div>');
    });

	//Header menu toggle
	$('.header__burger').on('click', function(event) {
		event.preventDefault();
		$(this).toggleClass('active');
		$('.header__bottom').toggleClass('active');
		$('.header__bottom').addClass('anim--active');
		$('body').toggleClass('noscroll');
	});

	//Header submenu toggle
	$('.header__menu-icon').on('click', function(event) {
		event.preventDefault();
		$(this).toggleClass('active');
		$(this).parent().next().slideToggle();
	});

});