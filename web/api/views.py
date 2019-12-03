import json

from django.http import HttpResponse

from scrapycw.commands.projectlist import Command
from scrapycw.scrapyhandlers.project import ProjectHandler


def list(request):
    result = ProjectHandler.list()
    return HttpResponse(json.dumps(result), content_type='application/json')
