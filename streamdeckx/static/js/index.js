let connSdSelect = null;
let currDeck = null;
let currDeckId = null;
let config = null;
let currButton = null;
let actionFieldsArea = null;
let buttonTextField = null;
let buttonBackgroundColorField = null;
let buttonTextColorField = null;
let buttonFontSizeField = null;
let textActionValueElem = null;
let multiKeyActionValueElem = null;
let multiKeySelect = null;
let selectedKeysElem = null;
let currActionType = null;

$(document).ready(function () {
    connSdSelect = $("#conn-sd-select");
    currDeck = $("#curr-deck");
    config = $("#config");
    currDeckId = connSdSelect.val();

    // Set listener on dropdown
    connSdSelect.on('change', function () {
        currDeckId = connSdSelect.val();
        $.get('/deckHtml', {'deckId': currDeckId}, function (data) {
            currDeck.html(data);
        });
    });
});

function updateConfigFields(data) {
    config.html(data);
    buttonTextField = $("#buttonText");
    buttonBackgroundColorField = $("#buttonBackgroundColor");
    buttonTextColorField = $("#buttonTextColor");
    buttonFontSizeField = $("#buttonFontSize");
}

function openConfig(position) {
    let buttonElem = $("#" + position);

    if (buttonElem.hasClass('clicked')) {
        // If we are un-clicking
        buttonElem.removeClass('clicked');
        config.html('');
        return;
    }

    // Remove from all other elements
    $('.clicked').each(function (i, elem) {
        $(elem).removeClass('clicked');
    });

    currButton = position;
    buttonElem.addClass('clicked');

    $.get('/configHtml', {'deckId': currDeckId, 'button': position}, function (data) {
        updateConfigFields(data);
    });
}

function openAddActionModal(position) {
    actionFieldsArea = $("#actionFields");
    actionFieldsArea.html('');

    let addActionModal = $("#addActionModal");
    addActionModal.css("display", "block");

    // Add listeners
    let actionTypeSelect = $("#actionTypeSelect");
    actionTypeSelect.change(function () {
        let selectedActionType = actionTypeSelect.val();
        switch (selectedActionType) {
            case "text":
                showTextActionFields();
                break;
            case "multikey":
                showMultiKeyActionFields();
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
        let action_text = null;

        if (currActionType === 'TEXT') {
            action_text = textActionValueElem.val();
        } else if (currActionType === 'MULTIKEY') {
            action_text = multiKeyActionValueElem.val();
        }

        // Submit creation of action
        $.post('/setButtonAction', {
            'deckId': currDeckId,
            'button': currButton,
            'action_text': action_text,
            'type': currActionType
        }, 'json').done(
            function (data) {
                console.log(data);

                // Close Modal
                closeActionModalButton.click()

                // Refresh Config HTML
                $.get('/configHtml', {'deckId': currDeckId, 'button': position}, function (data) {
                    updateConfigFields(data)
                    currActionType = null;
                });
            }
        );
    });
}

function deleteAction(button_id, action_id) {
    $.ajax('/setButtonAction',
        {
            type: 'DELETE',
            data: {
                'deckId': currDeckId,
                'button': button_id,
                'action': action_id
            },
            success: function (data) {
                updateConfigFields(data);
            }
        });
}

function showTextActionFields() {
    actionFieldsArea.html(`
        <label for="textValue">Text: </label>
        <input type="text" id="textValue" style="margin-top: 5px;"/>
    `);

    textActionValueElem = $("#textValue");
    currActionType = 'TEXT';
}

function addMultiKeyToDisplay(keyName) {
    let newMultiKey = $("<span></span>").text(keyName);
    let newKeyRemoveX = $("<span></span>").attr("id", "delete-" + keyName).attr("onclick", "removeMultiKey(" + keyName + "_)").html("&times;");

    newMultiKey.append(newKeyRemoveX);
    newMultiKey.addClass("multi-key");
    selectedKeysElem.append(newMultiKey);
}

async function showMultiKeyActionFields() {
    // Get Supported Keys
    let response = await fetch('/api/v1/keys');
    let data = await response.json();

    let selectHtml = ``;
    for (let i = 0; i < data.groups.length; i++) {
        selectHtml += `<optgroup label="` + data.groups[i].name + `">`;

        for (let j = 0; j < data.groups[i].keys.length; j++) {
            let key = data.groups[i].keys[j].value;
            selectHtml += `<option value="` + key + `">` + key + `</option>`;
        }

        selectHtml += `</optgroup>`;
    }

    actionFieldsArea.html(`
        <label for="multiKeyValue">Keys: </label>
        <span id="selectedKeys"></span>
        <select id="multiKeySelect">` + selectHtml + `</select>
    `);

    multiKeySelect = $("#multiKeySelect");
    selectedKeysElem = $("#selectedKeys");

    multiKeySelect.on('change', function () {
        addMultiKeyToDisplay(multiKeySelect.val());
    });

    multiKeyActionValueElem = $("#multiKeyValue");
    currActionType = 'MULTIKEY'

    // Listeners
    let pressedKeys = []
    let allPressedKeys = []

    // Listen for key presses
    $(document).on("keydown", function (e) {
        // If this is our first pressed key, clear out allPressedKeys
        if (pressedKeys.length === 0) {
            allPressedKeys = []
        }

        pressedKeys.push(e.key);
        allPressedKeys.push(e.key);

        multiKeyActionValueElem.val(allPressedKeys.join(';'));
    });

    // Listen for key releases
    $(document).on("keyup", function (e) {
        const keyIndex = pressedKeys.indexOf(e.key);
        if (keyIndex > -1) {
            pressedKeys.splice(keyIndex, 1);
        }
    });

}

function showDefaultActionFields() {
    actionFieldsArea.html(`
        <p>Unknown action type!</p>
    `);

    currActionType = null;
}

function submit() {
    let buttonText = buttonTextField.val()
    let backgroundColor = buttonBackgroundColorField.val();
    let textColor = buttonTextColorField.val();
    let fontSize = buttonFontSizeField.val();

    $.post('/setButtonConfig', {'deckId': currDeckId, 'button': currButton, 'buttonText': buttonText, 'backgroundColor': backgroundColor, 'textColor': textColor, 'fontSize': fontSize}, 'json').done(
        function(data) {
            $('#' + currButton + '-img').attr('src', 'data:image/PNG;base64, ' + data);
        }
    );
}