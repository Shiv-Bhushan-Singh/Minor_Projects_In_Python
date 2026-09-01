import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from utils.config import DATABASE_PATH


def get_connection():

    Path(DATABASE_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,

            FOREIGN KEY (
                conversation_id
            )
            REFERENCES conversations(id)
            ON DELETE CASCADE
        )
        """
    )


    connection.commit()

    connection.close()


def create_conversation(
    title: str
) -> int:

    now = datetime.now().isoformat()

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO conversations (
            title,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            now,
            now
        )
    )


    conversation_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return conversation_id


def add_message(
    conversation_id: int,
    role: str,
    content: str
):

    now = datetime.now().isoformat()

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO messages (
            conversation_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content,
            now
        )
    )


    cursor.execute(
        """
        UPDATE conversations
        SET updated_at = ?
        WHERE id = ?
        """,
        (
            now,
            conversation_id
        )
    )


    connection.commit()

    connection.close()


def get_conversations():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM conversations
        ORDER BY updated_at DESC
        """
    )


    conversations = cursor.fetchall()

    connection.close()

    return conversations


def get_messages(
    conversation_id: int
) -> List[Tuple]:

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (
            conversation_id,
        )
    )


    messages = cursor.fetchall()

    connection.close()

    return messages


def delete_conversation(
    conversation_id: int
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM messages
        WHERE conversation_id = ?
        """,
        (
            conversation_id,
        )
    )


    cursor.execute(
        """
        DELETE FROM conversations
        WHERE id = ?
        """,
        (
            conversation_id,
        )
    )


    connection.commit()

    connection.close()