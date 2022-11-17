"use strict";

class API {
    constructor(base_url = "/api/v1") {
        this.base_url = base_url;
        this.headers = {
            "Content-Type": "application/json",
        }
    }

    async start_game(wordID = "") {
        let resp = await fetch(`${this.base_url}/start_game/`, {
            method: "POST",
            headers: this.headers,
            body: JSON.stringify({
                wordID: wordID,
            })
        });
        if (resp.ok) {
            return await resp.json();
        }
    }

    async finish_game(id, key) {
        let resp = await fetch(`${this.base_url}/finish_game/`, {
            method: "POST",
            headers: this.headers,
            body: JSON.stringify({
                id: id,
                key: key,
            })
        });
        if (resp.ok) {
            return await resp.json();
        }
    }

    async guess(id, key, word) {
        let resp = await fetch(`${this.base_url}/guess/`, {
            method: "POST",
            headers: this.headers,
            body: JSON.stringify({
                id: id,
                key: key,
                guess: word,
            })
        })
        if (resp.ok) {
            return await resp.json();
        } else if (resp.status === 400) {
            app.errorPopup("Invalid word!");
        } else if (resp.status === 404) {
            app.errorPopup("This game has already finished");
        } else if (resp.status === 500) {
            app.errorPopup("A server error occurred :(");
        }
    }
}

class Letter {
    constructor(letter = "", state = 0) {
        this.letter = letter;
        this.state = state;
        this.submitted = false;
    }
}

function init_word_grid() {
    let grid = [];
    for (let i = 0; i < 6; i++) {
        let row = [];
        for (let j = 0; j < 5; j++) {
            row.push(new Letter);
        }
        grid.push(row);
    }
    return grid;
}

window.app = new Vue({
    el: "#vue-root",
    data: {
        grid: null,
        currentIndex: null,
        api: new API,
        apiKey: null,
        gameID: null,
        wordID: null,
        wordLength: 5,
        answer: "",
        error: "",
        message: "",
    },
    delimiters: ['[[', ']]'],
    methods: {
        letterShading(letterObj) {
            return {
                "empty": !letterObj.letter,
                "not-submitted": letterObj.letter && !letterObj.submitted,
                "absent": letterObj.state === 0 && letterObj.submitted,
                "present": letterObj.state === 1 && letterObj.submitted,
                "correct": letterObj.state === 2 && letterObj.submitted,
            }
        },
        popup(message) {
            this.message = message;
            setTimeout(() => this.message = "", 1250);
        },
        errorPopup(error) {
            this.error = error;
            setTimeout(() => this.error = "", 1250);
        },
        getRow() {
            return this.grid[this.currentIndex];
        },
        backspace() {
            let row = this.getRow();

            // If array is full
            if (row[row.length - 1].letter !== "") {
                row[row.length - 1].letter = "";
                return;
            }

            for (let i = 0; i < row.length; i++) {
                if (row[i].letter === "") {
                    try {
                        row[i - 1].letter = "";
                    } catch {
                    } // in case index isn't valid
                    return;
                }
            }
        },
        addLetter(letter) {
            let row = this.getRow();
            for (let i = 0; i < row.length; i++) {
                if (row[i].letter === "") {
                    row[i].letter = letter;
                    break;
                }
            }
        },
        async guessWord() {
            // Prevent spamming guesses from running multiple guess API calls at the same time
            if (this.guessInProgress) return;
            try {
                this.guessInProgress = true;

                let row = this.getRow();
                let word = row.map(val => {
                    return val.letter
                }).join("");
                if (word.length < 5) return;

                const newRow = await this.api.guess(this.gameID, this.apiKey, word);
                if (!newRow) {
                    return;
                }

                let correct = true;
                newRow.forEach((val, idx) => {
                    row[idx].submitted = true;
                    row[idx].state = val.state;
                    if (row[idx].state !== 2) {
                        correct = false;
                    }
                })

                styleKeys(row);

                this.currentIndex += 1;
                if (this.currentIndex >= 6 || correct) await this.finishGame();
            } catch (e) {
                throw(e);
            } finally {
                this.guessInProgress = false;
            }
        },
        async finishGame() {
            const json = await this.api.finish_game(this.gameID, this.apiKey);
            this.answer = json["answer"];
        },
        async reset() {
            this.grid = init_word_grid();
            this.answer = "";
            this.currentIndex = 0;

            if (!this.wordID) {
                this.wordID = new URLSearchParams(window.location.search.slice(1)).get("g");
            } else {
                this.wordID = null;
            }
            // Remove old get params from url
            history.replaceState(
                {},
                document.title,
                `${location.protocol}//${location.host}${location.pathname}`
            );

            const startJson = await this.api.start_game(this.wordID);
            this.gameID = startJson["id"];
            this.apiKey = startJson["key"];
            this.wordID = startJson["wordID"];

            init_keyboard();
        },
        share() {
            const absent_emoji = "⬛️";
            const present_emoji = "🟨";
            const correct_emoji = "🟩";

            let guessNum = this.currentIndex;

            this.grid[this.currentIndex - 1].forEach(letterObj => {
                if (letterObj.state !== 2) {
                    guessNum = "X";
                }
            })

            let game_string = `Wordle #${this.wordID}, ${guessNum}/${this.grid.length}\n`;

            this.grid.slice(0, this.currentIndex).forEach(row => {
                game_string += "\n";
                row.forEach(letterObj => {
                    switch (letterObj.state) {
                        case 0:
                            game_string += absent_emoji;
                            break;
                        case 1:
                            game_string += present_emoji;
                            break;
                        case 2:
                            game_string += correct_emoji;
                            break;
                    }
                })
            });
            game_string += `\nPlay this game: ${window.location.href}?g=${this.wordID}`;
            navigator.clipboard.writeText(game_string)
                .then(() => {
                    this.popup("Copied game to clipboard");
                }, () => { // Legacy fallback if async clipboard is not supported
                    let textArea = document.createElement("textarea");
                    textArea.textContent = game_string;
                    textArea.style.position = "fixed";
                    document.body.appendChild(textArea);
                    textArea.select();
                    try {
                        document.execCommand("copy");
                        this.popup("Copied game to clipboard");
                    } catch {
                        this.errorPopup("Error copying game to clipboard");
                    } finally {
                        document.body.removeChild(textArea);
                    }
                }
            )
        }
    },
    mounted() {
        this.reset();
    }
})
