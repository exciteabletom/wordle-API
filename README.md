# Wordle API
Public JSON API for Wordle with an example Vue.js [frontend](https://word.digitalnook.net).

This repo is a great base for making your own [variations](https://github.com/momonala/nerdle) of Wordle.
Or you can use the API to quickly integrate Wordle logic into your own apps.


## Architecture
What's notable about this rendition of Wordle is that the guessing logic is completely server-side. As opposed to the original, which stores all the answers in the browser.

This means that it is impossible to know the answer without playing through the game.

Even looking at the backend source code will not reveal the answer, as the wordlist is shuffled before it is inserted into the database.

## API Documentation
If you need any help with using this API, please open an issue!

### POST `/api/v1/start_game/`
### Request body (optional)
```
{
  "wordID": int
}
```
If you don't include `wordID`, a random word is chosen.

### Response body
```
{
  "id": int,
  "key": string,
  "wordID": int
}
```
`id` is a unique ID for this game.

`key` is a random string used to validate future actions for this game.

`wordID` is a unique ID identifying this word. You can use this ID to play the same game again, without leaking the answer.

### POST `/api/v1/guess/`
### Request body
```
{
  "id": int,
  "key": string,
  "guess": string
}
```

### Response body
```
[
  {
    "letter": char,
    "status": int
  },
  cont...
]
```
`status` is an int of value `0`, `1`, or `2`. `0` means the letter is not present in the word. `1` means the letter is present in the word. `2` means the letter is present in the word **and** is in the correct position.

For example: ⬛🟨🟨🟩⬛ is represented as `0 1 1 2 0`

### Errors
- `400 Bad Request` if the word is the wrong length, contains non-letters, or is not in the dictionary
- `403 Forbidden` if the game has been finished, or already has 6 guesses


### POST `/api/v1/finish_game`
### Request body
```
{
  "id": int,
  "key": string
}
```

### Response body
```
{
   "answer": string
}
```
After calling this, you will be unable to make more guesses as the answer has been revealed.

## Dev environment quick start
`python3 -m venv .venv`

`. .venv/bin/activate`

`python3 -m pip install --upgrade wheel pip`

`python3 -m pip install -r requirements.txt -r requirements-dev.txt`

`pre-commit install`

`python3 init.py`

`FLASK_DEBUG=1 flask run --cert=adhoc --host=0.0.0.0`

The dev server is accessible on https://localhost:5000 and on your local IP address from another device.

https is necessary for the async clipboard API to work on IOS.
You may have to click through a warning about an invalid certificate.
