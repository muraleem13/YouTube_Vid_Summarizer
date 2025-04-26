from flask import Blueprint, render_template, request,session
from app.utils import youtube_video_id_extractor, youtube_transcript_extractor
from app.models import generate_flash_cards,generate_markdown_summary,generate_quiz
from app.logger.logger import logger
import json
logger = logger(__name__)


bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/generate_summary', methods=['POST'])
def generate_summary():
    url = request.form['youtube_url']
    generate_quiz_input = request.form['generate_quiz']
    difficulty = request.form['difficulty']
    no_of_questions = int(request.form['num_questions'])

    youtube_video_id = youtube_video_id_extractor.extract_video_id(url)

    if not youtube_video_id:
        return render_template('index.html', error="Invalid YouTube URL. Please provide a valid URL.")
    
    youtube_transcript = youtube_transcript_extractor.extract_transcript(youtube_video_id)

    if not youtube_transcript:
        return render_template('index.html', error="Transcript not available for this video.")  
    
    #ai_generated_quiz =[]
    ai_flashcards = []

    ai_markdown_summary = generate_markdown_summary.generate_markdown_summary(transcript_text=youtube_transcript,video_id=youtube_video_id)
    ai_generated_quiz = generate_quiz.generate_quiz(summary_text=ai_markdown_summary,difficulty=difficulty,num_questions=no_of_questions) if generate_quiz_input=='yes' else []
    ai_flashcards = generate_flash_cards.generate_flashcards(summary_text=ai_markdown_summary,max_cards=no_of_questions,complexity=difficulty)

    logger.info(f"AI Generated Summary: {ai_markdown_summary}")
    logger.info(f"AI Generated Quiz: {ai_generated_quiz}")
    logger.info(f"AI Generated Flashcards: {ai_flashcards}")

    session['quiz_answers'] = {str(i): q['answer'] for i, q in enumerate(ai_generated_quiz)}
    session['quiz_explanations'] = {str(i): q['explanation'] for i, q in enumerate(ai_generated_quiz)}
    session.modified = True

    return render_template('index.html', summary=ai_markdown_summary, quiz=ai_generated_quiz, flashcards=ai_flashcards)


@bp.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    quiz_answers = session.get('quiz_answers', {})
    quiz_explanations = session.get('quiz_explanations', {})
    results = []

    for key, correct_answer in quiz_answers.items():
        user_answer = request.form.get(f'q{key}')
        explanation = quiz_explanations.get(key, "")

        results.append({
            "question": f"Question {int(key) + 1}",
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": user_answer == correct_answer,
            "explanation": explanation
        })

    return render_template('index.html', results=results)