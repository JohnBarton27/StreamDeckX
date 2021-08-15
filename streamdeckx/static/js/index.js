let connSdSelect = null;
let currDeck = null;
let config = null;
let currButton = null;
let actionFieldsArea = null;

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

    // Remove from all other elements
    $('.clicked').each(function(i, elem) {
        $(elem).removeClass('clicked');
    });

    currButton = position;
    buttonElem.addClass('clicked');

    $.get('/configHtml', {'deckId': connSdSelect.val(), 'button': position}, function(data) {
        config.html(data);
    });
}

function openAddActionModal() {
    actionFieldsArea = $("#actionFields");
    actionFieldsArea.html('');

    let addActionModal = $("#addActionModal");
    addActionModal.css("display", "block");

    // Add listeners
    let actionTypeSelect = $("#actionTypeSelect");
    actionTypeSelect.change(function() {
        let selectedActionType = actionTypeSelect.val();
        switch (selectedActionType) {
            case "text":
                showTextActionFields();
                break;
            default:
                showDefaultActionFields();
        }
    });

    let closeActionModalButton = $("#closeActionModal");
    closeActionModalButton.click(function() {
        addActionModal.css("display", "none");
    });

    let addActionButton = $("#addActionButton");
    addActionButton.click(function() {
        // Submit creation of action
    });
}

function showTextActionFields() {
    actionFieldsArea.html(`
        <label for="textValue">Text: </label>
        <input type="text" id="textValue" style="margin-top: 5px;"/>
    `);
}

function showDefaultActionFields() {
    actionFieldsArea.html(`
        <p>Unknown action type!</p>
    `);
}