//Import swiper
import Swiper, {
    Navigation,
    Pagination,
    EffectFade,
    Autoplay,
    Thumbs,
} from 'swiper';

Swiper.use([
    Navigation,
    Pagination,
    EffectFade,
    Autoplay,
    Thumbs,
]);

$(function () {

	//Init Intro Slider
	function swiperIntroInit() {
		const swiperIntroSliderBlock = document.querySelector('.intro--slider');
		if ($(swiperIntroSliderBlock).length > 0) {
			const swiperIntroSliderCount = $(swiperIntroSliderBlock).find('.swiper-slide').length;

			let swiperIntro = new Swiper('.intro--slider', {
				slidesPerView: 'auto',
				speed: 600,
				loop: (swiperIntroSliderCount > 1) ? true : false,
				autoplay: {
					delay: 2500,
					disableOnInteraction: false,
					pauseOnMouseEnter: true,
				},
				effect: 'fade',
				fadeEffect: {
					crossFade: true
				},
				pagination: {
					el: swiperIntroSliderBlock.querySelector('.swiper-pagination'),
					type: 'bullets',
					clickable: true,
				},
                navigation: {
                    nextEl: swiperIntroSliderBlock.parentElement.querySelector('.slider__nav-next'),
                    prevEl: swiperIntroSliderBlock.parentElement.querySelector('.slider__nav-prev')
                },
			});
		}
	};
	swiperIntroInit();

	//Init Advantages Slider
	function swiperAdvantagesInit() {
		const swiperAdvantagesBlock = document.querySelectorAll('.advantages--slider');
		swiperAdvantagesBlock.forEach((el) => {
			const swiperAdvantagesCount = $(el).find('.swiper-slide').length;

			let swiperAdvantages = new Swiper(el, {
				slidesPerView: 'auto',
				speed: 800,
				loop: (swiperAdvantagesCount > 3) ? true : false,
			});
		});
	};
	swiperAdvantagesInit();

	//Init Goods Slider
	function swiperGoodsInit() {
		const swiperGoodsBlock = document.querySelectorAll('.goods--slider');
		swiperGoodsBlock.forEach((el) => {
			if (el.swiper && !el.swiper.destroyed) {
				el.swiper.destroy(true, true);
			}

			const swiperGoodsCount = $(el).find('.swiper-slide').length;
			let swiperGoods = new Swiper(el, {
				slidesPerView: 'auto',
				speed: 800,
				loop: (swiperGoodsCount > 4) ? true : false,
				observer: true,
				observeSlideChildren: true,
				pagination: {
					el: '.swiper-pagination',
					type: 'bullets',
					clickable: true,
					dynamicBullets: true,
				}
			});

			//Update slider
			swiperGoods.on('observerUpdate', (event) => {
				swiperGoodsInit();
			});
		});
	};
	swiperGoodsInit();

	//Init Steps Slider
	function swiperStepsInit() {
		const swiperStepsBlock = document.querySelectorAll('.steps--slider');
		swiperStepsBlock.forEach((el) => {
			let swiperSteps = new Swiper(el, {
				slidesPerView: 'auto',
				speed: 800,
			});
		});
	};
	swiperStepsInit();

	//Init Product Gallery Slider
	function swiperProductGalleryInit() {
		const swiperProductGallery = document.querySelectorAll('.product__gallery');
		swiperProductGallery.forEach((el) => {
			let swiperProductGalleryThumbs = new Swiper(el.querySelector('.product--thumb'), {
				slidesPerView: 'auto',
				speed: 800,
				freeMode: true,
				direction: 'vertical',
			});
			let swiperProductGalleryParent = new Swiper(el.querySelector('.product--slider'), {
				modules: [Thumbs],
				slidesPerView: 'auto',
				speed: 800,
				thumbs: {
					swiper: swiperProductGalleryThumbs,
					autoScrollOffset: 3
				}
			});
		});
	};
	swiperProductGalleryInit();

    //Init Option Slider
    function swiperOptionInit() {
        const swiperOptionBlock = document.querySelectorAll('.option__slider');
        swiperOptionBlock.forEach((el) => {
            let swiperOption = new Swiper(el.querySelector('.option--slider'), {
                slidesPerView: 'auto',
                observer: true,
                observeParents: true,
                speed: 800,
            });
        });
    };
    swiperOptionInit();

    //Update Option Slider
	function swiperOptionUpdate(sliderElement) {
		let domElement = sliderElement[0] || sliderElement;
		let swiper = domElement.swiper;
		if (swiper) {
			swiper.update();
			swiper.slideTo(0);
		}
	};

	//Filter Option Slider
	$('.option__list-item').on('click', function() {
		let target = $(this).data('link');

		$('.option__list-item').removeClass('active');
		$(this).addClass('active');

		if (target === 'option_all') {
			$('.option__slide').fadeIn(300).promise().done(function() {
				$('.option--slider').each(function() {
					swiperOptionUpdate(this);
				});
			});
		} else {
			$('.option__slide').hide();
			$('.option__slide[data-target="' + target + '"]').fadeIn(300).promise().done(function() {
				$('.option--slider').each(function() {
					swiperOptionUpdate(this);
				});
			});
		}
	});

});