from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import pdfplumber
import io
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Notes Agent"])

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)

NOTES_STYLE = {
    "beginner": (
        "Create simple, easy-to-read bullet-point notes. "
        "Use plain language. Define any technical terms in parentheses. "
        "Group related ideas together. Keep bullets short (1-2 sentences max). "
        "Add a 'Key Takeaways' section at the end."
    ),
    "intermediate": (
        "Create structured notes with clear headings and sub-bullets. "
        "Include examples where helpful. "
        "Highlight important concepts with *emphasis*. "
        "Add a summary paragraph and a list of key terms."
    ),
    "advanced": (
        "Create dense, technical notes suited for an expert. "
        "Use precise terminology. Include tradeoffs, nuances, and edge cases. "
        "Reference relevant concepts, patterns, or formulas inline. "
        "Add a 'Critical Analysis' section highlighting open questions or limitations."
    ),
}


def extract_pdf_text(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts)


class SummarizeRequest(BaseModel):
    text: str
    level: str = "beginner"


@router.post("/notes/from-pdf")
async def notes_from_pdf(file: UploadFile = File(...), level: str = Form("beginner")):
    file_bytes = await file.read()
    raw_text = extract_pdf_text(file_bytes)

    if not raw_text.strip():
        return {"error": "Could not extract text from PDF. It may be scanned/image-based."}

    # Truncate to avoid token limits
    raw_text = raw_text[:8000]

    style_hint = NOTES_STYLE.get(level, NOTES_STYLE["beginner"])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are an expert note-taker. {style_hint}",
        ),
        (
            "human",
            "Generate smart study notes from the following text:\n\n{text}",
        ),
    ])

    chain = prompt | llm
    result = chain.invoke({"text": raw_text})

    return {
        "level": level,
        "source": file.filename,
        "notes": result.content,
        "characters_processed": len(raw_text),
    }


@router.post("/notes/summarize")
async def summarize_text(req: SummarizeRequest):
    style_hint = NOTES_STYLE.get(req.level, NOTES_STYLE["beginner"])
    text = req.text[:8000]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are an expert note-taker and summarizer. {style_hint}",
        ),
        (
            "human",
            "Generate smart study notes from the following text:\n\n{text}",
        ),
    ])

    chain = prompt | llm
    result = chain.invoke({"text": text})

    return {
        "level": req.level,
        "notes": result.content,
        "characters_processed": len(text),
    }
