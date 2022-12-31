let connSdSelect = null;
let currDeck = null;
let currDeckId = null;
let config = null;
let currButton = null;
let actionFieldsArea = null;
let buttonTextField = null;
let buttonImageField = null;
let buttonBackgroundColorField = null;
let buttonTextColorField = null;
let buttonFontSizeField = null;
let textActionValueElem = null;
let multiKeyActionValueElem = null;
let multiKeySelect = null;
let selectedKeysElem = null;
let applicationActionValueElem = null;
let multiKeySelectedKeys = [];
let delayActionValueElem = null;
let currActionType = null;
let emulatorMode = false;

$(document).ready(function () {
    setup();
});

function setup() {
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
}

function rescan() {
    $.ajax({
        url: '/rescan',
        type: 'PUT',
        success: function(result) {
            document.querySelector('html').innerHTML = result;
            setup();
        }
    });
}

function updateConfigFields(data) {
    config.html(data);
    buttonTextField = $("#buttonText");
    buttonBackgroundColorField = $("#buttonBackgroundColor");
    buttonTextColorField = $("#buttonTextColor");
    buttonFontSizeField = $("#buttonFontSize");
    buttonImageField = $("#buttonImage");

    buttonImageField.change(function() {
        // Check if image already displayed
        if ($("#displayButtonImage").length > 0) {
            $("#displayButtonImage").remove();
        }

        if (!$('#buttonImageUpload').hasClass('image-upload')) {
            $('#buttonImageUpload').addClass('image-upload')
        }

        let imageUploadDiv = $('#buttonImageUpload');
        let imgFile = buttonImageField.prop('files')[0];

        let previewImageDiv = $('<label for="buttonImage" style="cursor:pointer;"></label>')
        let previewImage = $("<img alt='Button Image' height='72' width='72''>").attr('id', 'displayButtonImage');
        previewImageDiv.append(previewImage);
        imageUploadDiv.append(previewImageDiv);

        let reader = new FileReader();
        reader.readAsDataURL(imgFile);
        reader.onload = function () {
            previewImage.attr('src', reader.result);
        };

    })
}

function openConfig(position) {
    if (emulatorMode) {
        $.post('/testButton', {'deckId': currDeckId, 'button': position})
    } else {

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
            case 'application':
                showApplicationActionFields();
                break;
            case 'delay':
                showDelayActionFields();
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
            action_text = multiKeySelectedKeys.join(';');
        } else if (currActionType === 'APPLICATION') {
            action_text = applicationActionValueElem.val();
        } else if (currActionType === 'DELAY') {
            action_text = delayActionValueElem.val().toString();
        }

        // Submit creation of action
        $.post('/setButtonAction', {
            'deckId': currDeckId,
            'button': currButton,
            'action_text': action_text,
            'type': currActionType
        }, 'json').done(
            function (data) {
                // Close Modal
                closeActionModalButton.click()

                // Reset MultiKeySelectedKeys
                multiKeySelectedKeys = []

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
    let newMultiKey = $("<span style='padding:5px;'></span>").text(keyName).attr("id", "multikey-" + keyName);
    let newKeyRemoveX = $("<span style='padding-left:10px; padding-right: 5px; cursor: pointer;'></span>").attr("id", "delete-" + keyName).attr("onclick", "removeMultiKey('" + keyName + "')").html("&times;");

    newMultiKey.append(newKeyRemoveX);
    newMultiKey.addClass("multi-key");
    selectedKeysElem.append(newMultiKey);
}

function removeMultiKey(keyName) {
    let keyToRemoveId = 'multikey-' + keyName;
    $('#' + keyToRemoveId).remove();
    let removalIndex = multiKeySelectedKeys.indexOf(keyName);

    if (removalIndex > -1) {
        multiKeySelectedKeys.splice(removalIndex, 1);
    }

    // Re-add removed key to the MultiKeySelect
    updateMultiKeySelect();
}

async function updateMultiKeySelect() {
    // Get Supported Keys
    let response = await fetch('/api/v1/keys');
    let data = await response.json();

    let selectHtml = `<option value="">Select...</option>`;
    for (let i = 0; i < data.groups.length; i++) {
        selectHtml += `<optgroup label="` + data.groups[i].name + `">`;

        for (let j = 0; j < data.groups[i].keys.length; j++) {
            let key = data.groups[i].keys[j].value;

            if (!multiKeySelectedKeys.includes(key)) {
                selectHtml += `<option value="` + key + `">` + key + `</option>`;
            }
        }

        selectHtml += `</optgroup>`;
    }

    multiKeySelect = $("#multiKeySelect");
    multiKeySelect.html(selectHtml);
}

async function showMultiKeyActionFields() {
    // Reset MultiKeySelectedKeys
    multiKeySelectedKeys = []

    actionFieldsArea.html(`
        <label for="multiKeyValue">Keys: </label>
        <span id="selectedKeys"></span>
        <select id="multiKeySelect"></select>
    `);

    await updateMultiKeySelect();

    selectedKeysElem = $("#selectedKeys");

    multiKeySelect.on('change', function () {
        let selectedVal = multiKeySelect.val();
        if (selectedVal !== 'Select...') {
            addMultiKeyToDisplay(selectedVal);
            multiKeySelectedKeys.push(selectedVal);
            multiKeySelect.val("");
        }

        updateMultiKeySelect();
    });

    multiKeyActionValueElem = $("#multiKeyValue");
    currActionType = 'MULTIKEY'

}

function showApplicationActionFields() {
    actionFieldsArea.html(`
        <label for="applicationPathValue">Application Path: </label>
        <input type="text" id="applicationPathValue" style="margin-top: 5px;"/>
    `);

    applicationActionValueElem = $("#applicationPathValue");
    currActionType = 'APPLICATION';
}

function showDelayActionFields() {
    actionFieldsArea.html(`
        <label for="delayValue">Delay (in seconds): </label>
        <input type="number" id="delayValue" style="margin-top: 5px;"/>
    `);

    delayActionValueElem = $("#delayValue");
    currActionType = 'DELAY';
}

function showDefaultActionFields() {
    actionFieldsArea.html(`
        <p>Unknown action type!</p>
    `);

    currActionType = null;
}

function test_action() {
    let xhr = new XMLHttpRequest();
    $.post('/testButton', {
        'deckId': currDeckId,
        'button': currButton
    }, 'json').done(
        function (data) {
            console.log("Testing button action!")
        }
    );
}

function emulatorToggle() {
    emulatorMode = !emulatorMode;

    if (emulatorMode) {
        // Set button to Emulator Mode
        $("#emulatorToggle").text('Emulator Mode')

        // Clear off any configs/clicked buttons
        $("#config").html('');

        // Remove from all other elements
        $('.clicked').each(function (i, elem) {
            $(elem).removeClass('clicked');
        });

    } else {
        // Set button to Edit Mode
        $("#emulatorToggle").text('Edit Mode')
    }
}

function createVirtualSD() {
    $.get('/newVirtualSDForm', function(data) {
        $("#config").html(data)
    })
}

function addVirtualStreamDeck() {
    $.post('/api/v1/newVirtualStreamDeck', {
        'name': $("#virtualName").val(),
        'cols': $("#cols").val(),
        'rows': $("#rows").val()
    })
}

function submit() {
    let buttonText = buttonTextField.val()
    let backgroundColor = buttonBackgroundColorField.val();
    let textColor = buttonTextColorField.val();
    let fontSize = buttonFontSizeField.val();
    let backgroundImg = buttonImageField.prop('files')[0];

    let fd = new FormData();
    fd.append('deckId', currDeckId);
    fd.append('button', currButton);
    fd.append('buttonText', buttonText);
    fd.append('backgroundColor', backgroundColor);
    fd.append('textColor', textColor);
    fd.append('fontSize', fontSize);
    fd.append('backgroundImage', backgroundImg);

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/setButtonConfig");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            $('#' + currButton + '-img').attr('src', 'data:image/PNG;base64, ' + xhr.responseText);
        }
    }
    xhr.send(fd);
}