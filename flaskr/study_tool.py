from flask import Blueprint, render_template, request, flash
from openai import OpenAI
client = OpenAI()


bp = Blueprint('study_tool', __name__, url_prefix='/study')

@bp.route('/')
def index():
    return render_template('study_tool/index.html')

@bp.route('/essay', methods=('GET', 'POST'))

def essay():
    if request.method == 'POST':
        topic = request.form['topic']
        if not topic:
            flash('Topic is required!')
        else:
            # Use AI to generate an essay (replace this with your model's implementation)
            essay = generate_essay(topic)
            return render_template('study_tool/essay.html', topic=topic, essay=essay)
    return render_template('study_tool/essay_form.html')

def generate_essay(topic):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",  # Use the correct model name available to your account
            messages=[
                {"role": "system", "content": "You are an essay writer. Write a detailed essay on the given topic."},
                {"role": "user", "content": topic}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating essay: {e}"
