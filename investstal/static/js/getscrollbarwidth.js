//Check Scroll Width
const getScrollbarWidth = () => {
	const item = document.createElement('div');

	item.style.position = 'absolute';
	item.style.top = '-9999px';
	item.style.width = '50px';
	item.style.height = '50px';
	item.style.overflow = 'scroll';
	item.style.visibility = 'hidden';

	document.body.appendChild(item);
	const scrollbarWidth = item.offsetWidth - item.clientWidth;
	document.body.removeChild(item);

	return scrollbarWidth;
};

//Export Function
export default getScrollbarWidth;
