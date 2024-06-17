# Periodic table

Periodic table with responsive layout.

## Demo

[netbek.github.io/periodic-table](https://netbek.github.io/periodic-table)

## Integration

Install the package:

```shell
npm install @netbek/periodic-table
```

Create a Sass file:

```scss
@import 'node_modules/@netbek/periodic-table/src/css/mixins';

// Define vars that should override defaults
$nb-periodic-table-cell-bg:                       #eee;
$nb-periodic-table-cell-border:                   #ccc;

// Load default vars
@import 'node_modules/@netbek/periodic-table/src/css/variables';

// Mobile-first layout
@include nb-periodic-table-base;
@include nb-periodic-table-color;
@include nb-periodic-table-size;

// Wide breakpoint layout
@media (min-width: 82em) {
  @include nb-periodic-table-color('category');
  @include nb-periodic-table-size('wide');
}
```

Create a Nunjucks template:

```html
{%- from "path/to/node_modules/@netbek/periodic-table/nunjucks/macros/nb_pt_legend.njk" import nb_pt_legend %}
{%- from "path/to/node_modules/@netbek/periodic-table/nunjucks/macros/nb_pt_table_18.njk" import nb_pt_table_18 %}
<html>
  <body>
    {% set element_columns = {
        atomic_number: 'Atomic number',
        symbol: 'Symbol',
        name: 'Name',
        atomic_mass: 'Atomic mass',
        electronegativity: 'Electronegativity'
    } %}
    {{ nb_pt_legend(elements, categories, element_columns) }}
    {{ nb_pt_table_18(elements, groups) }}
  </body>
</html>
```

Render the Nunjucks template:

```js
import nunjucks from 'nunjucks';
import periodicTable from '@netbek/periodic-table';

async function render() {
  const categories = await periodicTable.loadCategories();
  const elements = await periodicTable.loadElements();
  const groups = await periodicTable.loadGroups();

  const data = {
    categories,
    elements,
    groups
  };

  return nunjucks.render('path/to/template.njk', data);
}

render();
```

## Development

Install Node and Python dependencies:

```shell
cd /path/to/periodic-table
./scripts/install.sh
```

Automatically build and refresh browser during development:

```shell
gulp livereload
```

Build the Python distribution package:

```shell
npm run build-dist
```

Publish the Node and Python distribution packages:

```shell
npm run publish-dist
```

## Feature ideas

* Group and period axes
* Color by group or block; different palettes ([mendeleevapp](https://github.com/lmmentel/mendeleevapp))

## Credit

* Wikipedia contributors, "List of chemical elements," Wikipedia, The Free Encyclopedia, [https://en.wikipedia.org/w/index.php?title=List_of_chemical_elements&oldid=755677624](https://en.wikipedia.org/w/index.php?title=List_of_chemical_elements&oldid=755677624) (accessed December 19, 2016). (CC BY-SA 3.0)
* Doug Hogan, "Periodic Table Data" [http://php.scripts.psu.edu/djh300/cmpsc221/p3s11-pt-data.htm](http://php.scripts.psu.edu/djh300/cmpsc221/p3s11-pt-data.htm) (?)
* [mendeleev](https://mendeleev.readthedocs.io/en/stable/bibliography.html) (MIT License)

## License

Copyright (c) 2016 Hein Bekker. Licensed under the GNU Affero General Public License, version 3.
