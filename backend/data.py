import os
from dotenv import load_dotenv
from supabase import create_client
from typing import List, Dict, Union

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def add_question_answer(question: str, answer: str) -> int:
    """Add a question and answer to the database.

    Args:
        question: The question that was asked.
        answer: The answer that was selected.

    Returns:
        The id of the new entry.
    """
    data = (
        supabase.table("qa").insert({"question": question, "answer": answer}).execute()
    )
    return data.data[0]["id"]


def add_chat_message(
    user_id: int, message_type: str, content: str, application: str = ""
) -> int:
    """Add a chat message to the database.

    Args:
        user_id: The user id associated with the message.
        message_type: The type of the message (e.g. 'human', 'jelly' or 'tool').
        content: The content of the message.

    Returns:
        The id of the new entry.
    """
    data = (
        supabase.table("chat_messages")
        .insert(
            {
                "user_id": user_id,
                "message_type": message_type,
                "content": content,
                "application": application,
            }
        )
        .execute()
    )
    return data.data[0]["id"]


def get_question_answers() -> List[Dict[str, Union[int, str]]]:
    """Get all QA.

    Returns:
        A list of all QA.
    """
    data = supabase.table("qa").select("*").execute()
    return data.data


def check_user_exists(user_token: str) -> Union[int, None]:
    """Check if a user exists based on the user_token.

    Args:
        user_token: The user_token to search.

    Returns:
        The user_id if the user exists, otherwise None.
    """
    data = (
        supabase.table("users").select("user_id").eq("user_token", user_token).execute()
    )
    if data.data and len(data.data) > 0:
        return data.data[0]["user_id"]
    else:
        return None


def create_user(user_token: str) -> int:
    """Create a new user.

    Args:
        user_token: The user_token for the new user.

    Returns:
        The user_id of the new user.
    """
    data = supabase.table("users").insert({"user_token": user_token}).execute()
    return data.data[0]["user_id"]


def get_chat_history(user_id: int) -> List[Dict[str, Union[int, str, str]]]:
    """Get all chat messages of a certain user based on their user_id.

    Args:
        user_id: The user_id of the user.

    Returns:
        A list of all chat messages of the specified user.
    """
    data = (
        supabase.table("chat_messages")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp")
        .execute()
    )
    return data.data


def get_chat_memory(user_id: int) -> List[Dict[str, Union[int, str, str]]]:
    """Get all human and Jelly chat messages of a certain user based on their user_id. This leaves out all other chat messages, because they are not relevant for the memory.

    Args:
        user_id: The user_id of the user.

    Returns:
        A list of all human and Jelly chat messages of the specified user.
    """
    data = (
        supabase.table("chat_messages")
        .select("*")
        .eq("user_id", user_id)
        .in_("message_type", ["human", "jelly"])  # Filter for human and Jelly messages
        .order("timestamp", desc=True)
        .limit(10)
        .execute()
    )
    reversed_data = list(reversed(data.data))
    return reversed_data


def get_total_human_messages() -> int:
    """Get the total number of human messages.

    Returns:
        The total number of human messages.
    """
    data = (
        supabase.table("chat_messages")
        .select("id")
        .eq("message_type", "human")
        .execute()
    )
    return len(data.data)
