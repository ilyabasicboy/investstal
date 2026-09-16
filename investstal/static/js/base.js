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

	//Check Anchor Margin
	let headerFixedHeight = 0;
	headerFixedHeight = $('.header').height();

	//Anchor Link
	$('.anchor-link').on('click', function(e) {
		e.preventDefault();
		let elementClick = $(this).attr('href');
		let destination = $(elementClick).offset().top - headerFixedHeight - 40;

		$('html, body').animate( { scrollTop: destination }, 1500, 'swing');
	});

	//Create modal product page
	function productModal(modalId, triggerClass) {
		$(document).on('click', triggerClass, function() {
			const product = $(this).parents('.product');
			let title = $(document).find('.title').text().trim();

			//Get selected options
			const selectedOptions = [];
			$('.option-card__input:checked').each(function() {
				const optionCard = $(this).closest('.option-card');
				const optionText = optionCard.find('.option-card__text').text().trim();
				selectedOptions.push(`${optionText}`);
			});

			//Update form info with options
			let fullInfo = `${title}`;
			if (selectedOptions.length > 0) {
				fullInfo += `, дополнительно: ${selectedOptions.join(', ')}`;
			}

			//Update modal content
			const modal = $(`#${modalId}`);
			modal.find('.modal__subtitle').text(fullInfo);

			modal.find('#id_rackman-info').val(fullInfo);
			modal.find('#id_order-info').val(fullInfo);
		});
	};
	productModal('rackman-modal', '.product__rackman');
	productModal('order-modal', '.product__order');

	//Create modal product card
	$(document).on('click', '.product-card__btn', function() {
		const product = $(this).parents('.product-card');
		const modal = $('#order-modal');

		//Update title
		const title = product.find('.product-card__title').text().trim();
		const article = product.find('.product-card__article').text().trim();
		const link = product.attr('href');

		//Update price
		const priceDefault = product.find('.product-card__price-default').text().trim();

		//Update form info
		const fullInfo = `${title}, ${article}, ${priceDefault}`;
		modal.find('.modal__subtitle').text(fullInfo);
		modal.find('#id_order-link').val(link);
		modal.find('#id_order-info').val(fullInfo);
	});

    //Toggle Text
    $.fn.extend({
        toggleText: function (a, b) {
            if (this.text() == a) {
                this.text(b);
            }
            else {
                this.text(a)
            }
        }
    });

    //Sidebar Menu Load Items
    let sidebarMore = $('.sidebar__more');
    sidebarMore.each(function(index, item) {
        let sidebarMoreBtn = $(item).find('.sidebar__more-btn');
        sidebarMoreBtn.on('click', function() {
            sidebarMoreBtn.prev().toggleClass('sidebar__submenu-load');
            sidebarMoreBtn.toggleText('Скрыть', 'Смотреть еще');
        });
    });

	//Filter Open/Close
	$('.filter-open').on('click', function(event) {
		event.preventDefault();
		$('.filter__price-content').addClass('active');
	});
	$(document).click(function(e) {
		let div = $('.filter-open');
		let div2 = $('.filter__price-content');
		if (!div.is(e.target) && div.has(e.target).length === 0 && !div2.is(e.target) && div2.has(e.target).length === 0) {
			$('.filter__price-content').removeClass('active');
		}
	});

});
