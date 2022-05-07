export default (name, currentValue, options) => ({
  options,
  filtered: options,
  idx: -1,
  maxIdx: options.length - 1,
  currentValue,
  showDropdown: false,
  filterOptions() {
    this.filtered = this.options.filter((val) => val.toLowerCase().includes(this.currentValue.toLowerCase()));
    this.maxIdx = this.filtered.length;
    this.showDropdown = this.filtered.length !== 0;
  },
  setValue() {
    if (this.idx !== -1) this.currentValue = this.filtered[this.idx];
    this.idx = -1;
    this.filterOptions();
  }
});
