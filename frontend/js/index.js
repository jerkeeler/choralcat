import '../css/index.css';
import Alpine from 'alpinejs';
import htmx from 'htmx.org';
import Sortable from 'sortablejs';

window.Alpine = Alpine;
window.htmx = htmx;
window.Sortable = Sortable;

Alpine.start();

htmx.onLoad(function (content) {
  const sortables = content.querySelectorAll('.sortable');
  for (let i = 0; i < sortables.length; i++) {
    const sortable = sortables[i];
    new Sortable(sortable, {
      animation: 150,
      ghostClass: 'blue-background-class',
    });
  }
});
