export default (widgetName, options) => ({
  options,
  filtered: options,
  showDropdown: false,
  idx: -1,
  selectedIdx: null,
  enterTag() {
    if (this.idx !== -1) this.newCat = this.filtered[this.idx][2];
    setTimeout(() => {
      this.$dispatch(`${widgetName}_submit`);
      setTimeout(() => {
        this.newCat = '';
        this.idx = -1;
        this.filterOptions();
      }, 0);
    }, 0);
  },
  filterOptions() {
    this.filtered = this.options.filter((val) => val[2].includes(this.newCat));
    this.maxIdx = this.filtered.length;
    this.showDropdown = this.filtered.length !== 0;
  },
  maxIdx: options.length - 1,
  newCat: '',
});
