"use strict";
const Keyboard = new window.SimpleKeyboard.default({
    onKeyPress: button => onKeyPress(button),
    theme: "hg-theme-default hg-layout-default",

    layout: {
        default: [
            "q w e r t y u i o p {bksp}",
            "a s d f g h j k l {enter}",
            "z x c v b n m"

        ]

    }
});

function onKeyPress(button) {
    console.log(button)
}
