# Wordle API
A public JSON API for Wordle. This repo also includes a frontend made with Vue.js.

See it in action [here](https://word.digitalnook.net).

## Why?
The original Wordle game only allows you to play 1 game per day. It is also extremely easy to cheat as the answer to the puzzle is sent to the client before it has been solved.

I wanted to create my own version that solves these issues.

## Architecture
What's notable about this rendition of Wordle is that all of the guessing happens through a public server-side JSON api.

This means that it is **impossible to cheat**, the answer is never stored in the browser before the puzzle has been finished.

Even looking at the backend source code will not reveal the answer, as the wordlist is shuffled before it is inserted into the database.

## Public API
You can use the public API to make your own Wordle game! Also feel free to copy the backend code and self-host it.

## API Documentation
If you need any help with using this API, please feel free to open an issue!

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
  ...
]
```
`status` is an int of value `0`, `1`, or `2`. `0` means the letter is not present in the word. `1` means the letter is present in the word. `2` means the letter is present in the word **and** is in the correct position. For example: ⬛🟨🟨🟩⬛ is represented as `0 1 1 2 0`

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

## Developing
Install all the requirements with `python3 -m pip install -r requirements.txt -r requirements-dev.txt`

To download the libraries and setup an empty db, run `python3 init.py`

Run the dev server with `FLASK_DEBUG=1 flask run`
