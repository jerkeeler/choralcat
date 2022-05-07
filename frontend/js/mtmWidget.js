export default (options, selected) => ({
  options,
  filtered: options,
  selected,
  idx: -1,
  maxIdx: options.length - 1,
  itemVal: '',
  showDropdown: false,
  filterOptions() {
    this.filtered = this.options.filter((val) => val[1].toLowerCase().includes(this.itemVal.toLowerCase()));
    this.maxIdx = this.filtered.length;
    this.showDropdown = this.filtered.length !== 0;
  },
  addValue() {
    const alreadyAdded = this.selected.find(val => val[0] === this.filtered[this.idx][0]);
    if (this.idx !== -1 && !alreadyAdded) this.selected.push(this.filtered[this.idx]);
    this.idx = -1;
    this.itemVal = '';
    this.filterOptions();
  },
  removeValue(opt) {
    this.selected = this.selected.filter(val => val[0] !== opt[0]);
  }
});
