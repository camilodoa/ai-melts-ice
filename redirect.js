// Single Page Apps for GitHub Pages
// https://github.com/rafrex/spa-github-pages
// Copyright (c) 2016 Rafael Pedicini, licensed under the MIT License
// ----------------------------------------------------------------------
(function(l) {
  const nonHomeUrls = ['/about', '/county', '/donate', '/home', '/safety'];
  for (let i = 0; i < nonHomeUrls.length; i++) {
    const urlRegex = new RegExp(nonHomeUrls[i], 'i');
    const verifyUrl = urlRegex.test(l.pathname);
    if (verifyUrl) {
      return;
    }
  }

  if (l.search) {
    var q = {};
    l.search.slice(1).split('&').forEach(function(v) {
      var a = v.split('=');
      q[a[0]] = a.slice(1).join('=').replace(/~and~/g, '&');
    });
    if (q.p !== undefined) {
      window.history.replaceState(null, null,
        l.pathname.slice(0, -1) + (q.p || '') +
        (q.q ? ('?' + q.q) : '') +
        l.hash
      );
    }
  }
  }(window.location))
