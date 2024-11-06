from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample Data (for demonstration purposes)
users = [
    {
        "id": 1,
        "name": "kani",
        "email": "kani@gmail.com",
        "password": "123",
        "profile": {"mental_health_history": [], "mood_tracking": []}
    }
    
]

# Sample resources data
resources = [
    {"id": 1, "title": "Coping Strategies", "content": "Learn how to manage anxiety and depression using these strategies."},
    {"id": 2, "title": "Meditation Guide", "content": "Steps to mindfulness meditation for mental health."},
    {"id": 3, "title": "Yoga for Anxiety", "content": "Explore how yoga can help alleviate anxiety and improve well-being."},
    {"id": 4, "title": "Healthy Sleep Habits", "content": "Tips for getting a good night's sleep to improve mental health."}
]

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# User Management - Register and Login
@app.route('/users/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        data = request.form
        user = {
            "id": len(users) + 1,
            "name": data["name"],
            "email": data["email"],
            "password": data["password"],
            "profile": {"mental_health_history": [], "mood_tracking": []}
        }
        users.append(user)
        return jsonify({"message": "User registered successfully!", "user": user}), 201
    return render_template('register.html')

@app.route('/users/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        data = request.form
        for user in users:
            if user["email"] == data["email"] and user["password"] == data["password"]:
                return jsonify({"message": "Login successful", "user": user})
        return jsonify({"message": "Invalid credentials"}), 401
    return render_template('login.html')

# User Profile (Mental Health History and Mood Tracking Data)
@app.route('/users/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id', 1)  # Defaults to 1 for now, adjust as needed.
    user = next((u for u in users if u["id"] == int(user_id)), None)
    
    if user:
        return render_template('profile.html', user=user)
    return jsonify({"message": "User not found"}), 404

# Mood Tracking
@app.route('/mood', methods=['GET', 'POST'])
def record_mood():
    if request.method == 'POST':
        data = request.form
        mood_entry = {
            "user_id": 1,
            "mood": data["mood"],
            "thoughts": data["thoughts"],
            "timestamp": "2024-10-23"  # Static date for placeholder; use actual date in production
        }
        users[0]["profile"]["mood_tracking"].append(mood_entry)
        return render_template('mood_success.html', message="Mood recorded successfully!")
    
    return render_template('mood.html')

# Mood History
@app.route('/mood/history', methods=['GET'])
def mood_history():
    user_id = 1
    history = users[user_id - 1]["profile"]["mood_tracking"]
    return render_template('mood_history.html', moods=history)

# Mental Health Resources
@app.route('/resources', methods=['GET'])
def get_resources():
    return render_template('resources.html', resources=resources)

@app.route('/resources/<int:id>', methods=['GET'])
def get_resource_by_id(id):
    resource = next((r for r in resources if r["id"] == id), None)
    if resource:
        return render_template('resource_detail.html', resource=resource)
    return jsonify({"message": "Resource not found"}), 404

# Counselor Support
@app.route('/counselor/connect', methods=['GET', 'POST'])
def connect_counselor():
    if request.method == 'POST':
        return jsonify({"message": "Connecting to counselor..."})
    return render_template('counselor_chat.html')

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

@app.route('/counselor/availability', methods=['GET'])
def counselor_availability():
    return jsonify({"availability": "Available"})

@app.route('/counselor/session', methods=['POST'])
def book_counselor_session():
    return jsonify({"message": "Session booked successfully"})

# Crisis Support
@app.route('/crisis/help', methods=['GET', 'POST'])
def crisis_help():
    if request.method == 'POST':
        message = "Crisis alert sent"
        return render_template('crisis_success.html', message=message)  # Renders success template
    return render_template('crisis_help.html')

@app.route('/crisis/hotlines', methods=['GET'])
def get_crisis_hotlines():
    hotlines = {
        "international": "1-800-273-8255",
        "local": "911"
    }
    return jsonify(hotlines)

# Notifications and Reminders
@app.route('/notifications/reminders', methods=['GET', 'POST'])
def set_reminder():
    if request.method == 'POST':
        reminder_type = request.form.get('reminder_type')
        time = request.form.get('time')
        message = f"Reminder set for {reminder_type} at {time}"
        return render_template('notifications_success.html', message=message)
    return render_template('notifications.html')

@app.route('/notifications/schedule', methods=['GET'])
def get_reminders():
    reminders = [
        {"type": "meditation", "time": "7:00 AM"},
        {"type": "medication", "time": "9:00 AM"}
    ]
    return jsonify(reminders)

if __name__ == '__main__':
    app.run(debug=True)
