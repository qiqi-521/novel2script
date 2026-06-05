"""HTTP routes for the backend bootstrap phase."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import yaml

from backend.app.schemas import (
    ExtractStoryStructureRequest,
    ExtractStoryStructureResponse,
    GenerateScriptRequest,
    HealthResponse,
    ParseNovelRequest,
    ParseNovelResponse,
    ScriptDocument,
)
from backend.app.services.chapter_parser import parse_novel_content
from backend.app.services.mock_generator import build_mock_script
from backend.app.services.story_extractor import extract_story_structure

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health_check() -> HealthResponse:
    """Basic health endpoint used for local verification."""

    return HealthResponse()


@router.post("/scripts/generate", response_model=ScriptDocument, tags=["scripts"])
def generate_script(payload: GenerateScriptRequest) -> ScriptDocument:
    """Return a schema-valid mock script document."""

    return build_mock_script(payload)


@router.post("/novels/parse", response_model=ParseNovelResponse, tags=["novels"])
def parse_novel(payload: ParseNovelRequest) -> ParseNovelResponse:
    """Validate novel input and return structured chapter segments."""

    return parse_novel_content(payload.content)


@router.post(
    "/novels/extract-structure",
    response_model=ExtractStoryStructureResponse,
    tags=["novels"],
)
def extract_novel_structure(
    payload: ExtractStoryStructureRequest,
) -> ExtractStoryStructureResponse:
    """Extract character candidates, chapter events, and scene drafts."""

    return extract_story_structure(payload.content)


@router.post("/scripts/generate/yaml", response_class=PlainTextResponse, tags=["scripts"])
def generate_script_yaml(payload: GenerateScriptRequest) -> PlainTextResponse:
    """Return the mock script serialized to YAML for quick inspection."""

    document = build_mock_script(payload)
    rendered = yaml.safe_dump(
        document.model_dump(mode="json"),
        allow_unicode=True,
        sort_keys=False,
    )
    return PlainTextResponse(rendered, media_type="application/yaml")
