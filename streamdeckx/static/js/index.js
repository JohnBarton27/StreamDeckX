let connSdSelect = null;
let currDeck = null;

$(document).ready(function() {
    connSdSelect = $("#conn-sd-select");
    currDeck = $("#curr-deck");

    // Set listener on dropdown
    connSdSelect.on('change', function () {
        $.get('/deckHtml', {'deckId': connSdSelect.val()}, function(data) {
            currDeck.html(data);
        });
    });
});