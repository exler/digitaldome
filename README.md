<p align="center">
    <img src="digitaldome/static/img/logo.svg" width="180">
    <h3 align="center">Digital Dome</h3>
    <p align="center">⏺️ Comprehensive media tracker</p>
</p>

Digital Dome is a comprehensive media tracking service designed to handle a diverse range of entities.

## Install

You can set up Digital Dome using Docker or run it locally.

### Docker

To set up Digital Dome using Docker, follow these steps:

* Clone the repository and navigate to the project directory.
* Run `docker compose up` to start all containers

### Local

You can also choose to run the webapp locally:

* Clone the repository and navigate to the project directory.
* Run `uv sync` to install dependencies using [uv](https://docs.astral.sh/uv/)

### Environment

In both cases, you should use the `.env.example` file as a template for your environment variables. 
Copy it to `.env` and fill in the required values.

## Usage

See [entrypoint.sh](entrypoint.sh) for usage options.

To create an admin user, run `docker compose exec web python manage.py createsuperuser` and follow the prompts.

## Development

In order to change the page's styles, you need to have [Bun](https://bun.sh/) installed. Run `bun run watch` or `bun run compile` to compile TailwindCSS styles.
