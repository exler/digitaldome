<p align="center">
    <img src="digitaldome/static/img/logo.png" width="180">
    <h3 align="center">Digital Dome</h3>
    <p align="center">⏺️ Comprehensive media tracker</p>
</p>

Digital Dome is a comprehensive media tracking service designed to handle a diverse range of entities.

## Install

### Docker Setup

To set up Digital Dome using Docker, follow these steps:

* Clone the repository and navigate to the project directory.
* Run `docker compose up` to start all containers

### Local Setup

You can also choose to run external services in Docker and the webapp locally

* Clone the repository and navigate to the project directory.
* Run `docker compose up -d db minio` to start the database and storage containers
* Run `uv sync` to install dependencies using [uv](https://docs.astral.sh/uv/)

## Usage

See [entrypoint.sh](entrypoint.sh) for usage options.

To create an admin user, run `docker compose exec web python manage.py createsuperuser` and follow the prompts.

## Development

In order to change the page's styles, you need to have [Bun](https://bun.sh/) installed. Run `bun run watch` or `bun run compile` to compile TailwindCSS styles.
