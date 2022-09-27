"use strict";
function init_keyboard() {
    Array.from(document.getElementsByClassName("simple-keyboard")).forEach(el => {
            while (el.firstChild) {
                el.removeChild(el.lastChild)
            }
        }
    )
    window.Keyboard = new SimpleKeyboard.default({
        onKeyPress: key => onKeyPress(key),
        theme: "keyboard-theme hg-theme-default",
        layout: {
            default: [
                "0 1 2 3 4",
                "5 6 7 6 9",
                "{enter} + - * / {bksp}",
            ]
        },
        display: {
            "{enter}": "=",
            "{bksp}": "⌫",
        },
    });

}

function onKeyPress(key) {
    switch (key) {
        case "{enter}":
            app.guessWord();
            break;
        case "{bksp}":
            app.backspace();
            break;
        default:
            app.addLetter(key);
            break;
    }
}

// Make physical keyboard also work
document.addEventListener("keydown", ev => {
    switch (ev.key) {
        case "Enter":
            onKeyPress("{enter}");
            break;
        case "Backspace":
            onKeyPress("{bksp}");
            break;
        default:
            if ("0123456789+-*/".includes(ev.key)) {
               onKeyPress(ev.key);
            }
            break;
    }
});

function styleKeys(row) {
    row.forEach(letterObj => {
        const letter = letterObj.letter;
        const state = letterObj.state;

        let className;
        switch (state) {
            case 0:
                className = "absent";
                break;
            case 1:
                className = "present";
                break;
            case 2:
                className = "correct"
                break;
        }

        let button = Keyboard.getButtonElement(letter)
        if (!button.classList.contains("correct")) {
            button.classList.add(className)
        }
    })
}
