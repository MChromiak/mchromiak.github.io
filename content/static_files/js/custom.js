// Custom JS scripts to run on base.html template

(function () {
    function updateCopyrightYear() {
        var year = String(new Date().getFullYear());
        document.querySelectorAll('[data-current-year]').forEach(function (element) {
            element.textContent = year;
        });
    }

    updateCopyrightYear();
    window.addEventListener('pageshow', updateCopyrightYear);
    document.addEventListener('visibilitychange', updateCopyrightYear);
    // Refresh a page left open across New Year without requiring a rebuild.
    window.setInterval(updateCopyrightYear, 60000);
})();

//<script src="https://hypothes.is/embed.js" async></script>
(function() {
    var hostname = window.location.hostname;
    var new_tab = true;
    var set_icon = true;
    for (var links = document.links, i = 0, a; a = links[i]; i++) {
        if (a.hostname !== hostname) {
            if (new_tab)
                a.target = '_blank';
            if (set_icon)
                a.innerHTML +=
                    '&nbsp;<i class="fa fa-external-link fa-1 external-link-margin" />';
        }
    }
})();
