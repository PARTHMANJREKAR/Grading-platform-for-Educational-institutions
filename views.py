from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .forms import TheoryMarksForm, PracticalMarksForm
from .models import Marks, Student

def enter_marks_view(request):
    if request.method == 'POST':
        # Retrieve all session data
        year = request.session.get('year')
        branch = request.session.get('branch')
        semester = request.session.get('semester')
        subject = request.session.get('subject')
        type_ = request.session.get('type')
        component = request.session.get('component')
        roll_number = request.POST.get('roll_number')  # Retrieve roll number from POST data

        # Validate that all required session data is present
        if not all([year, branch, semester, subject, type_, component, roll_number]):
            return HttpResponse("Incomplete session data or missing roll number.")

        # Fetch the student record
        try:
            student = Student.objects.get(roll_number=roll_number)
        except Student.DoesNotExist:
            return HttpResponse("Student with the provided roll number does not exist.")

        # Create form instances based on type
        if type_ == 'Theory':
            form = TheoryMarksForm(request.POST)
            if form.is_valid():
                # Save theory marks
                theory_marks = form.save(commit=False)
                theory_marks.year = year
                theory_marks.branch = branch
                theory_marks.semester = semester
                theory_marks.subject = subject
                theory_marks.component = component
                theory_marks.student = student  # Associate marks with the student
                theory_marks.save()
                return HttpResponse("Theory marks submitted successfully.")
            else:
                return render(request, 'enter_marks.html', {'form': form, 'type': type_, 'component': component})

        elif type_ == 'Practical':
            form = PracticalMarksForm(request.POST)
            if form.is_valid():
                # Extract component-specific marks from the form
                data = form.cleaned_data
                component_marks = {}
                
                # Update component-specific marks
                if component == 'PPT':
                    component_marks = {
                        'ppt_content': data.get('ppt_content', 0),
                        'ppt_organization': data.get('ppt_organization', 0),
                        'ppt_design': data.get('ppt_design', 0),
                        'ppt_delivery': data.get('ppt_delivery', 0),
                        'ppt_audience_engagement': data.get('ppt_audience_engagement', 0),
                        'ppt_qna': data.get('ppt_qna', 0),
                    }
                elif component == 'Group discussion':
                    component_marks = {
                        'group_discussion_content_knowledge': data.get('group_discussion_content_knowledge', 0),
                        'group_discussion_communication_skills': data.get('group_discussion_communication_skills', 0),
                        'group_discussion_participation': data.get('group_discussion_participation', 0),
                        'group_discussion_team_work': data.get('group_discussion_team_work', 0),
                    }
                elif component == 'Seminar presentation':
                    component_marks = {
                        'seminar_content': data.get('seminar_content', 0),
                        'seminar_organization': data.get('seminar_organization', 0),
                        'seminar_presentation_skills': data.get('seminar_presentation_skills', 0),
                        'seminar_visual_aids': data.get('seminar_visual_aids', 0),
                        'seminar_response_to_questions': data.get('seminar_response_to_questions', 0),
                    }
                elif component == 'Quiz':
                    component_marks = {
                        'quiz_mcqs': data.get('quiz_mcqs', 0),
                        'quiz_short_answer_questions': data.get('quiz_short_answer_questions', 0),
                    }
                elif component == 'Case study':
                    component_marks = {
                        'case_study_understanding': data.get('case_study_understanding', 0),
                        'case_study_analysis_and_application': data.get('case_study_analysis_and_application', 0),
                        'case_study_solution': data.get('case_study_solution', 0),
                        'case_study_organization': data.get('case_study_organization', 0),
                        'case_study_clarity': data.get('case_study_clarity', 0),
                        'case_study_references': data.get('case_study_references', 0),
                    }
                elif component == 'Design thinking':
                    component_marks = {
                        'design_thinking_problem_definition': data.get('design_thinking_problem_definition', 0),
                        'design_thinking_ideation': data.get('design_thinking_ideation', 0),
                        'design_thinking_prototyping': data.get('design_thinking_prototyping', 0),
                        'design_thinking_testing': data.get('design_thinking_testing', 0),
                        'design_thinking_reflection': data.get('design_thinking_reflection', 0),
                    }
                elif component == 'Innovation':
                    component_marks = {
                        'innovation_originality': data.get('innovation_originality', 0),
                        'innovation_impact': data.get('innovation_impact', 0),
                        'innovation_feasibility': data.get('innovation_feasibility', 0),
                        'innovation_implementation_strategy': data.get('innovation_implementation_strategy', 0),
                        'innovation_creativity': data.get('innovation_creativity', 0),
                    }

                # Calculate total marks
                total_marks = sum(component_marks.values())

                # Save practical marks
                practical_marks = form.save(commit=False)
                practical_marks.year = year
                practical_marks.branch = branch
                practical_marks.semester = semester
                practical_marks.subject = subject
                practical_marks.component_marks = component_marks
                practical_marks.total_marks = total_marks
                practical_marks.student = student  # Associate marks with the student
                practical_marks.save()
                return HttpResponse("Practical marks submitted successfully.")
            else:
                return render(request, 'enter_marks.html', {'form': form, 'type': type_, 'component': component})

        else:
            return HttpResponse("Invalid marks type.")

    # Handle GET request or invalid POST request
    type_ = request.session.get('type')
    if type_ == 'Theory':
        form = TheoryMarksForm()
    elif type_ == 'Practical':
        form = PracticalMarksForm()
    else:
        return HttpResponse("Invalid marks type or missing type in session.")

    # Pass the type and component to the template context
    component = request.session.get('component')
    return render(request, 'enter_marks.html', {'form': form, 'type': type_, 'component': component})

def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        return redirect('main_page')
    return render(request, 'login.html')


def main_page_view(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        division = request.POST.get('division')
        prn = request.POST.get('prn')

        if year and division and prn:
            request.session['year'] = year
            request.session['division'] = division
            request.session['prn'] = prn
            return redirect('select_theory_practical')
        else:
            return HttpResponse("Please select all the fields before submitting.", status=400)
    else:
        # Prepopulate the form with session data if available
        context = {
            'selected_year': request.session.get('year', ''),
            'selected_division': request.session.get('division', ''),
            'selected_prn': request.session.get('prn', ''),
        }
    return render(request, 'main_page.html', context)

def enter_cce_marks_view(request):
    if request.method == 'POST':
        # Retrieve all session data
        year = request.session.get('year')
        branch = request.session.get('branch')
        semester = request.session.get('semester')
        subject = request.session.get('subject')
        type_ = request.session.get('type')
        component = request.session.get('component')
        roll_number = request.POST.get('roll_number')  # Retrieve roll number from POST data

        # Validate that all required session data is present
        if not all([year, branch, semester, subject, type_, component, roll_number]):
            return HttpResponse("Incomplete session data or missing roll number.")

        # Fetch the student record
        try:
            student = Student.objects.get(roll_number=roll_number)
        except Student.DoesNotExist:
            return HttpResponse("Student with the provided roll number does not exist.")

        # Handle CCE marks submission and save to the database here
        # Example: Save CCE marks to the database
        # Save logic for CCE marks would go here

        return HttpResponse("CCE Marks submitted successfully.")
    
    # Store the current step in the session
    request.session['current_step'] = 'enter_cce_marks'

    # Pass context data if needed, e.g., list of students
    students = [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
    return render(request, 'enter_cce_marks.html', {'students': students})

def enter_exam_marks_view(request):
    if request.method == 'POST':
        # Retrieve all session data
        year = request.session.get('year')
        branch = request.session.get('branch')
        semester = request.session.get('semester')
        subject = request.session.get('subject')
        type_ = request.session.get('type')
        component = request.session.get('component')
        roll_number = request.POST.get('roll_number')  # Retrieve roll number from POST data

        # Validate that all required session data is present
        if not all([year, branch, semester, subject, type_, component, roll_number]):
            return HttpResponse("Incomplete session data or missing roll number.")

        # Fetch the student record
        try:
            student = Student.objects.get(roll_number=roll_number)
        except Student.DoesNotExist:
            return HttpResponse("Student with the provided roll number does not exist.")

        # Handle exam marks submission and save to the database here
        # Example: Save exam marks to the database
        # Save logic for exam marks would go here

        return HttpResponse("Exam Marks submitted successfully.")
    
    # Store the current step in the session
    request.session['current_step'] = 'enter_exam_marks'

    # Pass context data if needed, e.g., list of students
    students = [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
    return render(request, 'enter_exam_marks.html', {'students': students})

def enter_ese_marks_view(request):
    if request.method == 'POST':
        marks = request.POST.get('marks')
        if marks:
            try:
                marks = float(marks)
            except ValueError:
                return render(request, 'enter_ese_marks.html', {'error': 'Invalid marks value.'})

            # Retrieve or create the Marks object
            student = request.session.get('student')  # Ensure you set this in your flow
            subject = request.session.get('subject')
            type_ = request.session.get('type')
            
            try:
                marks_entry = Marks.objects.get(student=student, subject=subject, theory_or_practical__name=type_)
                marks_entry.ese_marks = marks
                marks_entry.save()
            except Marks.DoesNotExist:
                # Handle the case where the Marks entry does not exist
                return render(request, 'enter_ese_marks.html', {'error': 'Marks entry does not exist.'})

            return redirect('next_page')  # Redirect to the next appropriate page

    # Store the current step in the session
    request.session['current_step'] = 'enter_ese_marks'

    return render(request, 'enter_ese_marks.html')

def enter_mse_marks_view(request):
    if request.method == 'POST':
        marks = request.POST.get('marks')
        if marks:
            try:
                marks = float(marks)
            except ValueError:
                return render(request, 'enter_mse_marks.html', {'error': 'Invalid marks value.'})

            # Retrieve or create the Marks object
            student = request.session.get('student')  # Ensure you set this in your flow
            subject = request.session.get('subject')
            type_ = request.session.get('type')
            
            try:
                marks_entry = Marks.objects.get(student=student, subject=subject, theory_or_practical__name=type_)
                marks_entry.mse_marks = marks
                marks_entry.save()
            except Marks.DoesNotExist:
                # Handle the case where the Marks entry does not exist
                return render(request, 'enter_mse_marks.html', {'error': 'Marks entry does not exist.'})

            return redirect('next_page')  # Redirect to the next appropriate page

    # Store the current step in the session
    request.session['current_step'] = 'enter_mse_marks'

    return render(request, 'enter_mse_marks.html')

def select_theory_practical_view(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        division = request.POST.get('division')
        prn = request.POST.get('prn')

        # Fetch the student based on the provided details
        try:
            student = Student.objects.get(year=year, division=division, prn=prn)
        except Student.DoesNotExist:
            return HttpResponse("Student not found", status=404)

        # Pass the student object to the template
        context = {
            'student': student,
            'year': year,
            'division': division,
            'prn': prn,
        }
        return render(request, 'select_theory_practical.html', context)

    # Handle GET requests or invalid POST requests
    return render(request, 'select_theory_practical.html')

def theory_marks_view(request, prn=None):
    students = Student.objects.all()
    if not prn:
        prn = students.first().prn

    student = get_object_or_404(Student, prn=prn)
    if request.method == 'POST':
        mid_sem_marks = request.POST['mid_sem_marks']
        cce_marks = request.POST['cce_marks']
        end_sem_marks = request.POST['end_sem_marks']

        marks, created = Marks.objects.get_or_create(student=student, theory_or_practical='Theory')
        marks.mid_sem_marks = mid_sem_marks
        marks.cce_marks = cce_marks
        marks.end_sem_marks = end_sem_marks
        marks.save()

        return redirect('theory_marks', prn=next_student_prn(student.prn))

    context = {
        'students': students,
        'next_student_prn': next_student_prn(student.prn),
    }
    return render(request, 'theory_marks.html', context)

def practical_marks_view(request, prn=None):
    students = Student.objects.all()
    if not prn:
        prn = students.first().prn

    student = get_object_or_404(Student, prn=prn)
    if request.method == 'POST':
        practical_write_up = request.POST['practical_write_up']
        component1_marks = request.POST['component1_marks']
        component2_marks = request.POST['component2_marks']
        attendance = request.POST['attendance']
        end_sem_practical = request.POST['end_sem_practical']

        marks, created = Marks.objects.get_or_create(student=student, theory_or_practical='Practical')
        marks.practical_write_up = practical_write_up
        marks.ppt_content = component1_marks
        marks.ppt_organization = component2_marks
        marks.attendance = attendance
        marks.end_sem_practical = end_sem_practical
        marks.save()

        return redirect('practical_marks', prn=next_student_prn(student.prn))

    context = {
        'students': students,
        'next_student_prn': next_student_prn(student.prn),
    }
    return render(request, 'practical_marks.html', context)

def next_student_prn(current_prn):
    students = list(Student.objects.order_by('prn'))
    current_index = students.index(Student.objects.get(prn=current_prn))
    next_index = (current_index + 1) % len(students)
    return students[next_index].prn

def main_page_2_view(request):
    if request.method == 'POST':
        prn = request.POST.get('prn')
        exam_type = request.POST.get('Type')  # Change 'exam_type' to 'Type' to match your form

        if exam_type == 'Theory':
            return redirect(reverse('theory_marks', args=[prn]))
        elif exam_type == 'Practical':
            return redirect(reverse('practical_marks', args=[prn]))

    students = Student.objects.all()
    return render(request, 'main_page_2.html', {'students': students})