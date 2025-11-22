from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.components.database import get_session
from app.dto import LLMMessageInput, Message, MessageUserInput
from app.services import create_assistant_message, create_user_message, list_messages

router = APIRouter(prefix="/api/messages", tags=["Messages"])


@router.get("", response_model=list[Message])
def get_messages(session: Session = Depends(get_session)) -> list[Message]:
    return list_messages(session)


@router.post("", response_model=Message, status_code=status.HTTP_201_CREATED)
def post_message(payload: MessageUserInput, session: Session = Depends(get_session)) -> Message:
    try:
        return create_user_message(session, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/llm", response_model=Message, status_code=status.HTTP_201_CREATED)
def post_llm_message(payload: LLMMessageInput, session: Session = Depends(get_session)) -> Message:
    try:
        return create_assistant_message(session, payload)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
