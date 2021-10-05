let connSdSelect = null;
let currDeck = null;
let currDeckId = null;
let config = null;
let currButton = null;
let actionFieldsArea = null;
let buttonTextField = null;
let textActionValueElem = null;

$(document).ready(function() {
    connSdSelect = $("#conn-sd-select");
    currDeck = $("#curr-deck");
    config = $("#config");
    currDeckId = connSdSelect.val();

    // Set listener on dropdown
    connSdSelect.on('change', function () {
        currDeckId = connSdSelect.val();
        $.get('/deckHtml', {'deckId': currDeckId}, function(data) {
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

    $.get('/configHtml', {'deckId': currDeckId, 'button': position}, function(data) {
        config.html(data);
        buttonTextField = $("#buttonText")
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
        $.post('/setButtonAction', {
            'deckId': currDeckId,
            'button': currButton,
            'action_text': textActionValueElem.val()
        }, 'json').done(
            function (data) {
                console.log(data);
            }
        );
    });
}

function showTextActionFields() {
    actionFieldsArea.html(`
        <label for="textValue">Text: </label>
        <input type="text" id="textValue" style="margin-top: 5px;"/>
    `);

    textActionValueElem = $("#textValue");
}

function showDefaultActionFields() {
    actionFieldsArea.html(`
        <p>Unknown action type!</p>
    `);
}

function submit() {
    let buttonText = buttonTextField.val()

    $.post('/setButtonConfig', {'deckId': currDeckId, 'button': currButton, 'buttonText': buttonText}, 'json').done(
        function(data) {
            $('#' + currButton + '-img').attr('src', 'data:image/PNG;base64, ' + data);
        }
    );
}