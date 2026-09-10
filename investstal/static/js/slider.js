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

});