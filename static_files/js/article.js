// Scripts automatically included by the article template.
(function () {
    'use strict';

    function languageFromClass(element) {
        var classes = element.className ? String(element.className).split(/\s+/) : [];
        for (var i = 0; i < classes.length; i += 1) {
            if (classes[i].indexOf('language-') === 0) {
                return classes[i].slice('language-'.length);
            }
        }
        return '';
    }

    function detectLanguage(block, code) {
        var explicit = languageFromClass(code) ||
            languageFromClass(code.parentElement) ||
            languageFromClass(block);

        if (explicit) {
            return explicit;
        }

        var source = code.textContent.trim();
        if (/^(from|import)\s+[A-Za-z_]|^def\s+[A-Za-z_]|^class\s+[A-Za-z_]|\bwith\s+[A-Za-z_].*:\s*$/m.test(source)) {
            return 'python';
        }
        if (/^(const|let|var)\s+|\bfunction\s+[A-Za-z_$]|=>/m.test(source)) {
            return 'javascript';
        }
        if (/^#!.*\b(bash|sh)\b|^(curl|npm|pnpm|yarn|git|docker)\s+/m.test(source)) {
            return 'shell';
        }
        if (/^(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+/im.test(source)) {
            return 'sql';
        }
        if (/^\s*</.test(source)) {
            return 'html';
        }
        return 'text';
    }

    function displayLanguage(language) {
        var labels = {
            bash: 'Shell',
            html: 'HTML',
            javascript: 'JavaScript',
            js: 'JavaScript',
            json: 'JSON',
            python: 'Python',
            py: 'Python',
            shell: 'Shell',
            sql: 'SQL',
            text: 'Text'
        };
        return labels[language.toLowerCase()] || language;
    }

    function fallbackCopy(text) {
        var textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        var copied = document.execCommand('copy');
        document.body.removeChild(textarea);
        return copied ? Promise.resolve() : Promise.reject(new Error('Copy failed'));
    }

    function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text);
        }
        return fallbackCopy(text);
    }

    function enhanceCodeBlock(block) {
        if (block.classList.contains('code-window')) {
            return;
        }

        var pre = block.querySelector('pre');
        var code = pre && pre.querySelector('code');
        if (!pre || !code) {
            return;
        }

        var language = displayLanguage(detectLanguage(block, code));
        var toolbar = document.createElement('div');
        var controls = document.createElement('span');
        var label = document.createElement('span');
        var copyButton = document.createElement('button');
        var copyIcon = document.createElement('i');
        var copyLabel = document.createElement('span');

        block.classList.add('code-window');
        toolbar.className = 'code-window__toolbar';
        controls.className = 'code-window__controls';
        controls.setAttribute('aria-hidden', 'true');
        label.className = 'code-window__language';
        label.textContent = language;

        copyButton.className = 'code-window__copy';
        copyButton.type = 'button';
        copyButton.setAttribute('aria-label', 'Copy ' + language + ' code');
        copyIcon.className = 'fa fa-copy';
        copyIcon.setAttribute('aria-hidden', 'true');
        copyLabel.textContent = 'Copy';
        copyButton.appendChild(copyIcon);
        copyButton.appendChild(copyLabel);

        pre.tabIndex = 0;
        toolbar.appendChild(controls);
        toolbar.appendChild(label);
        toolbar.appendChild(copyButton);
        block.insertBefore(toolbar, pre);

        copyButton.addEventListener('click', function () {
            copyText(code.textContent).then(function () {
                copyIcon.className = 'fa fa-check';
                copyLabel.textContent = 'Copied';
                copyButton.classList.add('is-copied');
                window.setTimeout(function () {
                    copyIcon.className = 'fa fa-copy';
                    copyLabel.textContent = 'Copy';
                    copyButton.classList.remove('is-copied');
                }, 1800);
            }).catch(function () {
                copyIcon.className = 'fa fa-exclamation-circle';
                copyLabel.textContent = 'Select code';
                pre.focus();
            });
        });
    }

    document.querySelectorAll('.entry-content .highlight').forEach(enhanceCodeBlock);
})();
