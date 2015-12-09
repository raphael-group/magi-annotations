d3.xhr('/annotations/metadata/genes/all') // todo: use urlparams?
    .header('content-type', 'application/json')
    .get(function(err,res) {
        var data = JSON.parse(res.responseText);
        initQueryWidget(data);
    });

function initQueryWidget(data) {
  // first add recent queries to the menu bar if they exist

  // TODO in the future if more complex querying is needed, magiQueryHrefFN
  //    should be promoted to its own global module so that adding query
  //    parameters can be done in a systematic, complete fashion
  function magiQueryHrefFn() {
    var datasets = 'datasets=' + addedList.join('%2C'),
        genes = 'genes=' + loadedGenes.join('%2C'),
        search = [genes, datasets];

    return window.location.origin + '/view?'+search.join('&');
  }

    var geneList = data.genes,
        geneListLowerCase = geneList.map(function(d) { return d.toLowerCase(); });

    // Gene input entry autocomplete
    var substringMatcher = function(strs) {
      return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp('^' + q, 'gi');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
          if (substrRegex.test(str)) {
            matches.push({ gene: str});
          }
        });

        // Sort ascending by length so exact matches are first
        matches.sort(function(x, y){
          var m = x.gene.length,
              n = y.gene.length;
            return m === n ? d3.ascending(x.gene, y.gene) : d3.ascending(m, n);
        });

        cb(matches);
      };
    };

    $('input.gene-typeahead').typeahead({
      hint: false,
      highlight: false,
      minLength: 1
    },
    {
      name: 'genes',
      display: 'gene',
      limit: 20,
	source: substringMatcher(geneList),
       templates: {
         empty: [
           '<div class="empty-message">',
             'Unable to find any genes that match the current query.',
           '</div>'
         ].join('\n'),
        suggestion: Handlebars.compile('<div class="requery-geneSuggestion">{{gene}}</div>')
      }
    });

    d3.select('input.gene-typeahead').on('keypress', function() {
      if(d3.event.keyCode === 13) {
        d3.event.preventDefault();
      }
    });
}
