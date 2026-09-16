//Import variable
import {
	breakpointXSMax
} from './match-media';

$(function () {

	//Menu more
	$('.menu-more').each(function () {
		let $nav = $(this);
		let $container = $nav.find('.menu-wrapper');
		let $menu = $container.find('.header__menu');
		let $leftMenu = $menu.find('.header__menu-left');
		let $rightMenu = $menu.find('.header__menu-right');
		let $overflow = $menu.find('.menu-hidden');
		let $moreCta = $menu.find('.menu-hidden-btn');
		let $search = $rightMenu.children('.header__search');
		let $rightItems = $rightMenu.children('.header__menu-item');
		let $lastItem = $rightItems.last();

		let leftItems = [];
		let rightItems = [];

		$leftMenu.children('.header__menu-item').each(function () {
			leftItems.push({
				$el: $(this)
			});
		});

		$rightItems.not($lastItem).each(function () {
			rightItems.push({
				$el: $(this)
			});
		});

		let allItems = leftItems.concat(rightItems);

		let getWidth = function ($items) {
			let width = 0;

			$items.each(function () {
				width += Math.ceil($(this).outerWidth(true));
			});

			return width;
		};

		let restoreItems = function () {
			leftItems.forEach(function (item) {
				item.$el.appendTo($leftMenu);
			});

			rightItems.forEach(function (item) {
				item.$el.appendTo($rightMenu);
			});

			if ($lastItem.length) {
				$lastItem.appendTo($rightMenu);
				$moreCta.insertBefore($lastItem);
			} else {
				$moreCta.appendTo($rightMenu);
			}

			if ($search.length) {
				$search.appendTo($rightMenu);
			}

			$overflow.empty();
		};

		let isOverflowing = function (withMore) {
			let leftWidth = getWidth($leftMenu.children('.header__menu-item'));
			let rightWidth = getWidth($rightMenu.children('.header__menu-item'));

			if ($search.length) {
				rightWidth += Math.ceil($search.outerWidth(true));
			}

			if (withMore) {
				rightWidth += Math.ceil($moreCta.outerWidth(true));
			}

			return leftWidth > Math.floor($leftMenu.width()) || rightWidth > Math.floor($rightMenu.width());
		};

		let moveItemsToOverflow = function (items) {
			items
				.sort(function (a, b) {
					return allItems.indexOf(a) - allItems.indexOf(b);
				})
				.forEach(function (item) {
					item.$el.appendTo($overflow);
				});
		};

		let reposition = function () {
			if (!$leftMenu.length || !$rightMenu.length || !$moreCta.length || !$overflow.length) {
				return;
			}

			restoreItems();
			$moreCta.addClass('hidden');

			if (!isOverflowing(false)) {
				return;
			}

			$moreCta.removeClass('hidden');

			let movedItems = [];
			let leftQueue = leftItems.slice().reverse();
			let rightQueue = rightItems.slice().reverse();
			let nextSide = 'right';

			while (isOverflowing(true) && (leftQueue.length || rightQueue.length)) {
				let item = null;

				if (nextSide === 'right' && rightQueue.length) {
					item = rightQueue.shift();
					nextSide = 'left';
				} else if (nextSide === 'left' && leftQueue.length) {
					item = leftQueue.shift();
					nextSide = 'right';
				} else if (rightQueue.length) {
					item = rightQueue.shift();
					nextSide = 'left';
				} else if (leftQueue.length) {
					item = leftQueue.shift();
					nextSide = 'right';
				}

				if (item) {
					item.$el.detach();
					movedItems.push(item);
				}
			}

			moveItemsToOverflow(movedItems);

			if (!$overflow.children().length) {
				$moreCta.addClass('hidden');
			}
		};

		if ($(window).outerWidth() > 767) {
			reposition();
		}

		$(window).on('load', function() {
			if ($(window).outerWidth() > 767) {
				reposition();
			}
		});

		$(window).on('resize', function() {
			if ($(window).outerWidth() > 767) {
				reposition();
			} else {
				restoreItems();
				$moreCta.addClass('hidden');
			}
		});

	});

});
