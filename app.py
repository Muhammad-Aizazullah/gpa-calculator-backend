from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

courses_data = []

grade_mapping = {
    "A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0
}

@app.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    course_name = data.get('course')
    credit_hours = data.get('credit')
    grade = data.get('grade')

    if not all([course_name, credit_hours, grade]):
        return jsonify({"error": "Missing data"}), 400

    grade_point = grade_mapping.get(grade, 0.0)

    new_course = {
        "course_name": course_name,
        "credit_hours": int(credit_hours),
        "grade": grade,
        "grade_point": grade_point
    }
    courses_data.append(new_course)

    return jsonify({"message": "Course added successfully."}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses_data)

@app.route('/gpa', methods=['GET'])
def get_gpa():
    current_points = sum(course['grade_point'] * course['credit_hours'] for course in courses_data)
    current_credits = sum(course['credit_hours'] for course in courses_data)

    total_points = current_points
    total_credits = current_credits
    
    try:
        prior_gpa = float(request.args.get('prior_gpa', 0))
        completed_credits = int(request.args.get('completed_credits', 0))

        if prior_gpa > 0 and completed_credits > 0:
            prior_points = prior_gpa * completed_credits
            total_points += prior_points
            total_credits += completed_credits

    except (ValueError, TypeError):
        pass

    gpa = (total_points / total_credits) if total_credits > 0 else 0.0
    return jsonify({"gpa": gpa})

@app.route('/reset', methods=['POST'])
def reset_courses():
    global courses_data
    courses_data = []
    return jsonify({"message": "All courses have been cleared."}), 200
    
# if __name__ == "__main__":
#     app.run(port=5000, debug=True)
