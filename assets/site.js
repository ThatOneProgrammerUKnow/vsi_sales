import htmx from 'htmx.org';

function copyLinkToClipboard(text) {
    navigator.clipboard.writeText(text);
    toastMessage("Link copied!");
}

window.copyLinkToClipboard = copyLinkToClipboard;