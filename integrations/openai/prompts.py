GET_ENTITY_PROMPT = """
Your task is to provide information about different media in JSON format.
Given an entity type (for example: "movie", "show", "book", "game") and it's name, return the following:
- description: maximum of 500 characters
- tags: array of strings, mostly genres or the relevant topics (first letter capitalized: "Action", "Science Fiction")
- wikipedia_url: URL for the wikipedia article (if doesn't exist, return null)

Also, depending on the entity, return those additional fields:
Movie:
- release_date: date of first release (format: YYYY-MM-DD)
- imdb_url: URL to IMDB page of this movie (if doesn't exist, return null)
- director: array of names of each director
- cast: array of names of the movie stars
- length: integer, represents minutes of movie

Show:
- release_date: date of first release (format: YYYY-MM-DD)
- imdb_url: URL to IMDB page of this movie (if doesn't exist, return null)
- creator: array of names of each creator
- stars: array of names of the show stars

Game:
- release_date: date of first release (format: YYYY-MM-DD)
- steam_url: URL to the Steam store page of this game (if not on Steam, return null)
- platforms: array of names of each platform that the game came out on
- developer: array of names of the game developers
- published: array of names of the game publishers

Book:
- publish_date: date of the first publication (format: YYYY-MM-DD)
- goodreads_url: URL to the Goodreads page of this book 
(if not on Goodreads, return null; if multiple found, return most popular match)
- author: array of names of the book authors
"""
