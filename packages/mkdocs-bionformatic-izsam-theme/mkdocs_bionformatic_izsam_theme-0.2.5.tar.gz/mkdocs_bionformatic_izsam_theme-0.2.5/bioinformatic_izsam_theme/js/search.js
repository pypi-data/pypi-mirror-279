/* Get indexed configurations parameters */
// s_config is declared in search_docs.js built with mkdocs-izsam-search
let config = s_config[0];
/* Get indexed docs */
// s_index is declared in search_docs.js built with mkdocs-izsam-search
let documents = s_index;
let idx;

let separator = config.separator;
let min_search_length = config.min_search_length;

function getSearchTermFromLocation() {
  let sPageURL = window.location.search.substring(1);
  let sParameterName = sPageURL.split('=');
  if (sParameterName[0] == 'q') {
    return decodeURIComponent(sParameterName[1].replace(/\+/g, '%20'));
  }
}

function joinUrl (base, path) {
  if (path.substring(0, 1) === "/") {
    // path starts with `/`. Thus it is absolute.
    return path;
  }
  if (base.substring(base.length-1) === "/") {
    // base ends with `/`
    return base + path;
  }
  return base + "/" + path;
}

function formatResult (location, title, summary) {
  return '<article><h3><a href="' + joinUrl(base_url, location) + '">'+ title + '</a></h3><p class="location">' + location + '</p><p>' + summary +'</p></article>';
}

function displayResults (results) {
  let search_results = document.getElementById("mkdocs-search-results");
  while (search_results.firstChild) {
    search_results.removeChild(search_results.firstChild);
  }
  if (results.length > 0){
    // compare object and return an object of matched elements
    let filtered_results = documents.filter(function (o1) {
      return results.some(function (o2) {
        return o1.location === o2.ref; // return the ones with equal location and ref
      });
    });
    // now we need to reorder the keys with the scores given in results object
    // first I will make the same order of the two matching objects
    let ordered_results = results.sort(function(a, b) {
       return a.ref.toLowerCase().localeCompare(b.ref);
    });
    let ordered_filtered_results = filtered_results.sort(function(a, b) {
       return a.location.toLowerCase().localeCompare(b.location);
    });
    // now I will assign the score to the filtered results
    function isEqual(object1, object2) {
      return object1.location === object2.ref;
    }
    ordered_filtered_results.forEach((result, index) => {
      if (isEqual( ordered_filtered_results, ordered_results)) {
        result.score = ordered_results[index].score;
      }
    });
    let sorted_results = ordered_filtered_results.sort(function(a, b) {
      return b.score - a.score;
    });
    sorted_results.forEach(result => {
      let summary = (result.text.substring(0, 200) + " [...]");
      let html = formatResult(result.location, result.title, summary);
      search_results.insertAdjacentHTML('beforeend', html);
    });
  } else {
    let noResultsText = search_results.getAttribute('data-no-results-text');
    if (!noResultsText) {
      //loc_obj is in theme-loc-**.js
      noResultsText = loc_obj.search_page_no_results;
    }
    search_results.insertAdjacentHTML('beforeend', '<p>' + noResultsText + '</p>');
  }
}

function doSearch () {
  let query = document.getElementById('mkdocs-search-query').value;
  if (query.length > min_search_length) {
    displayResults(idx.search(query));
  } else {
    // Clear results for short queries
    displayResults([]);
  }
}

function initSearch () {
  let search_input = document.getElementById('mkdocs-search-query');
  if (search_input) {
    search_input.addEventListener("keyup", doSearch);
  }
  let term = getSearchTermFromLocation();
  if (term) {
    search_input.value = term;
    doSearch();
  }
}

/* Start the magic */
if (documents) {
  let lang = document.documentElement.lang;
  idx = lunr(function () {
    if (lang != 'en') {
      this.use(lunr.multiLanguage('en', lang))
    }
    this.ref('location')
    this.field('text')
    this.field('title')
    // we need to add to what lunr considers a token separator
    // this.tokenizer.separator = /[\s\-\_]+/
    this.tokenizer.separator = separator
    // if using the lunr.Index#search method to query then the
    // term separator also needs to be updated
    lunr.QueryLexer.termSeparator = lunr.tokenizer.separator
    documents.forEach(function (doc) {
      this.add(doc)
    }, this)
  });
  allow_search = true;
  initSearch(allow_search);
} else {
  initSearch(allow_search);
}
