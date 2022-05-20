import '../css/index.css';

import Alpine from 'alpinejs';
import htmx from 'htmx.org';
import Sortable from 'sortablejs';

import mtmWidget from './mtmWidget';
import stringWidget from './stringWidget';
import tagWidget from './tagWidget';

window.Alpine = Alpine;
window.htmx = htmx;
window.Sortable = Sortable;

htmx.onLoad((content) => {
  const sortables = content.querySelectorAll('.sortable');
  for (let i = 0; i < sortables.length; i++) {
    const sortable = sortables[i];
    new Sortable(sortable, {
      animation: 150,
      ghostClass: 'blue-background-class',
    });
  }
});

Alpine.data('mtmWidget', mtmWidget);
Alpine.data('stringWidget', stringWidget);
Alpine.data('tagWidget', tagWidget);

Alpine.start();
