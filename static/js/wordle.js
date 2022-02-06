"use strict";

function init_word_grid() {
    let grid = [];
    for (let i = 0; i < 6; i++) {
        let row = [];
        for (let j = 0; j < 5; j++) {
            row.push({letter: "", state: 0});
        }
        grid.push(row);
    }
    return grid
}

let vm = new Vue({
    el: "#vue-root",
    data: {
        grid: init_word_grid(),
    },
    delimiters: ['[[', ']]'],
    methods: {
        letterShading: function (letterObj) {
            return  {
                "cell-empty": letterObj.state === 0 && !letterObj.letter,
                "cell-absent": letterObj.state === 0 && letterObj.letter,
                "cell-present": letterObj.state === 1,
                "cell-correct": letterObj.state === 2,
            }
        }
    }
})
