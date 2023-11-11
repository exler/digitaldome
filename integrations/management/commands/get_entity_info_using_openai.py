import json
from argparse import ArgumentParser
from typing import Any, Self

from django.core.management.base import BaseCommand

from integrations.openai.client import get_openai_json_response
from integrations.openai.prompts import GET_ENTITY_PROMPT


class Command(BaseCommand):
    help = "Get entity information using OpenAI API"

    def add_arguments(self: Self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "prompt",
            type=str,
            help="The user prompt to send to the OpenAI API",
        )

    def handle(self: Self, *args: Any, **options: Any) -> None:
        prompt = options["prompt"]
        response = get_openai_json_response(system_prompt=GET_ENTITY_PROMPT, user_prompt=prompt)
        self.stdout.write(json.dumps(response, indent=4))
