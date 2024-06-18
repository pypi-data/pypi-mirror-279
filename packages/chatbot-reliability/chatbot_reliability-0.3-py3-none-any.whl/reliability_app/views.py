from .models import ChatSession,SimilarQuestion
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import inflect
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    p = inflect.engine()

    def convert_number_to_words(token):
        if token.isdigit():
            return p.number_to_words(token)
        else:
            return token

    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(convert_number_to_words(token.lower())) for token in tokens]
    # print('lemmatized_tokens',lemmatized_tokens)
    return ' '.join(lemmatized_tokens)


def extract_session_number(question):
    # Extracting session number from the question
    match = re.search(r'session\s*(\d+)', question, re.IGNORECASE)
    # print('match',match)
    return int(match.group(1)) if match else None



def get_answer_from_database(question,user_name):
    try:
        all_entries = ChatSession.objects.filter(user__username=user_name)

        
        if not all_entries:
            return None  # No questions in the database, return None
        
        current_question_session_number = extract_session_number(question)
        processed_current_question = preprocess_text(question)
        # print('processed_current_questions',processed_current_question)

        # Filter entries by session number if present
        relevant_entries = [entry for entry in all_entries if extract_session_number(entry.question) == current_question_session_number]
        # print('relevant_entries',relevant_entries)

        if not relevant_entries:
            return None  # No relevant entries found for the specific session

        processed_questions = [preprocess_text(entry.question) for entry in relevant_entries]
        processed_questions.append(processed_current_question)  # Adding the current question for similarity comparison
        # print('processed_questions',processed_questions)

        # Use SentenceTransformer for creating embeddings
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        question_embeddings = model.encode(processed_questions, convert_to_tensor=True)

        # Convert embeddings to NumPy arrays for similarity calculation
        question_embeddings_np = [embedding.cpu().detach().numpy() for embedding in question_embeddings]

        # Calculate cosine similarities
        similarities = cosine_similarity([question_embeddings_np[-1]], question_embeddings_np[:-1])
        # print('similarities',similarities)

        # Find the most similar question
        most_similar_index = similarities.argmax()
        most_similar_answer = relevant_entries[most_similar_index].answer
        # verification_count = relevant_entries[most_similar_index].verification_count
        # positive_count = relevant_entries[most_similar_index].positive_count
        # negative_feedback_count = relevant_entries[most_similar_index].negative_feedback_count

        # Adjust similarity threshold based on context
        similarity_threshold = 0.8 if 'session' in processed_current_question else 0.8

        if similarities[0][most_similar_index] >= similarity_threshold:
            retrieved_entry = relevant_entries[most_similar_index]
            # if not SimilarQuestion.objects.filter(question=retrieved_entry.question, user_session_id=user_identifier).exists():
            retrieved_entry.retrieval_count += 1
            retrieved_entry.save() 
            # existing_similar_question = SimilarQuestion.objects.filter(question=retrieved_entry.question, user_session_id=user_identifier).exists()
            # if not existing_similar_question:
            
            # Create a SimilarQuestion object
            match = SimilarQuestion.objects.create(
                    question=question,
                    answer=retrieved_entry.answer,
                    
                    user_name=user_name,
                    
                )

            return most_similar_answer
        else:
            return None

    except ChatSession.DoesNotExist:
        return None