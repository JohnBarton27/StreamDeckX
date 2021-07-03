let connSdSelect = null;
let currDeck = null;
let config = null;

$(document).ready(function() {
    connSdSelect = $("#conn-sd-select");
    currDeck = $("#curr-deck");
    config = $("#config");

    // Set listener on dropdown
    connSdSelect.on('change', function () {
        $.get('/deckHtml', {'deckId': connSdSelect.val()}, function(data) {
            currDeck.html(data);
        });
    });
});

function openConfig(position) {
    let buttonElem = $("#" + position);

    if (buttonElem.hasClass('clicked')) {
        // If we are un-clicking
        buttonElem.removeClass('clicked');
        config.html('');
        return;
    }

    buttonElem.addClass('clicked');

    $.get('/configHtml', {'deckId': connSdSelect.val(), 'button': position}, function(data) {
        config.html(data);
    });
}