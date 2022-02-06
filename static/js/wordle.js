"use strict";

class API {
    constructor(base_url = "/api") {
        this.base_url = base_url;
    }

    async return_or_error (resp) {
        if (resp.ok) {
            return await resp.json()
        } else {
            alert("HTTP ERROR: " + error)
        }
    }

    async start_game() {
        let resp = await fetch(`${this.base_url}/start_game/`, {method: "POST"});
        await this.return_or_error(resp)
    }

    async guess(id, word) {
        let resp = await fetch(`${this.base_url}/guess/`, {
            method: "POST",
            body: {
                id: id,
                guess: word,
            }.toJSON()
        })
        return await this.return_or_error(resp);
    }


}

class Letter {
    constructor(letter = "", state = 0) {
        this.letter = letter;
        this.state = state;
    }
}

function init_word_grid() {
    let grid = [];
    for (let i = 0; i < 6; i++) {
        let row = [];
        for (let j = 0; j < 5; j++) {
            row.push(new Letter)
        }
        grid.push(row);
    }
    return grid
}

window.app = new Vue({
    el: "#vue-root",
    data: {
        grid: init_word_grid(),
        currentRow: 0,
        api: new API,
        gameID: null,
        wordLength: 5,
        finished: false,
    },
    delimiters: ['[[', ']]'],
    methods: {
        letterShading: function(letterObj) {
            return  {
                "cell-empty": letterObj.state === 0 && !letterObj.letter,
                "cell-absent": letterObj.state === 0 && letterObj.letter,
                "cell-present": letterObj.state === 1,
                "cell-correct": letterObj.state === 2,
            }
        },
        getRow: function() {
            return this.grid[this.currentRow];
        },
        backspace: function() {
            let row = this.getRow();

            // If array is full
            if (row[row.length - 1].letter !== "") {
                row[row.length - 1].letter = "";
                return;
            }

            for (let i = 0; i < row.length; i++) {
                if (row[i].letter === "") {
                    try {
                        row[i-1].letter = "";
                    } catch {} // in case index isn't valid
                    return;
                }
            }
        },
        addLetter: function(letter) {
            let row = this.getRow();
            for (let i = 0; i < row.length; i++) {
                if (row[i].letter === "") {
                    row[i].letter = letter;
                    break;
                }
            }
        },
        guessWord: function() {
            const word = this.grid[this.currentRow].toString();
            this.api.guess(word)
        },
        reset: async function () {
            this.gameID = (await this.api.start_game())["id"];
        }

    },
    mounted() {
        this.reset();
    }
})
