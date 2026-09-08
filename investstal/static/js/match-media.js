//Media Breakpoint LG Min
const breakpointLGMin = window.matchMedia('(min-width: 1200px)');

//Media Breakpoint MD Min
const breakpointMDMin = window.matchMedia('(min-width: 1024px)');

//Media Breakpoint XS Min
const breakpointXSMin = window.matchMedia('(min-width: 768px)');

//Media Breakpoint LG Max
const breakpointLGMax = window.matchMedia('(max-width: 1199px)');

//Media Breakpoint MD Max
const breakpointMDMax = window.matchMedia('(max-width: 1023px)');

//Media Breakpoint XS Max
const breakpointXSMax = window.matchMedia('(max-width: 767px)');

//Export variable
export {
    breakpointLGMin,
    breakpointMDMin,
    breakpointXSMin,
    breakpointLGMax,
    breakpointMDMax,
    breakpointXSMax
};