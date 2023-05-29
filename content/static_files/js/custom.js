// Custom JS scripts to run on base.html template

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
