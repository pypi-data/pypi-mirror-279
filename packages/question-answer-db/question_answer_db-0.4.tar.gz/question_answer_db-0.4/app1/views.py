from .models import User, ChatSession, SimilarQuestion

from django.db import transaction

def save_to_database(**kwargs):
    user_name = kwargs.get('user_name', 'DefaultUser')
    session_id = kwargs.get('session_id', 'DefaultSessionID')
    question = kwargs.get('question', 'DefaultQuestion')
    answer = kwargs.get('answer', 'DefaultAnswer')

    try:
        with transaction.atomic():
            # Assuming 'ChatSession' is the model and has been imported correctly.
            chat_session = ChatSession(
                user_name=user_name,
                session_id=session_id,
                question=question,
                answer=answer
            )
            chat_session.save()
            print(f"Data saved for user {user_name}")
            return True
    except Exception as e:
        print(f"Failed to save data: {str(e)}")
        return False

