import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Union

load_dotenv()


class SupabaseManager():
    def __init__(self) -> None:
        self.supabase: Client = self._init_supabase()

    def _init_supabase(self) -> Client:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        return create_client(url, key)

    def add_qa(self, question: str, answer: str) -> int:
        """Add a question and answer to the database.

        Args:
            question: The question that was asked.
            answer: The answer that was selected.

        Returns:
            The id of the new entry.
        """
        data = self.supabase.table("qa").insert(
            {"question": question, "answer": answer}).execute()
        return data.data[0]["id"]

    def add_rating(self, id: int, rating: int) -> None:
        """Add a rating to a question and answer.

        Args:
            id: The id of the question and answer.
            rating: The rating (0 or 1).
        """
        self.supabase.table("qa").update(
            {"rating": rating}).eq("id", id).execute()

    def get_qa(self) -> List[Dict[str, Union[int, str]]]:
        """Get all QA.

        Returns:
            A list of all QA.
        """
        data = self.supabase.table("qa").select("*").execute()
        return data.data
