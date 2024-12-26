from django import forms
from .models import Student, Subject, Marks, BranchCode

class StudentForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=BranchCode.objects.all(), empty_label="Select Branch")

    class Meta:
        model = Student
        fields = ['prn', 'name', 'registration_number', 'roll_number', 'branch']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = [
            'student', 'subject', 'theory_or_practical', 'total_marks',
        ]

class TheoryMarksForm(forms.ModelForm):
    content = forms.IntegerField(required=False, min_value=0, max_value=4)
    organization = forms.IntegerField(required=False, min_value=0, max_value=4)
    design = forms.IntegerField(required=False, min_value=0, max_value=4)
    delivery = forms.IntegerField(required=False, min_value=0, max_value=4)
    audience_engagement = forms.IntegerField(required=False, min_value=0, max_value=2)
    qna = forms.IntegerField(required=False, min_value=0, max_value=2)
    
    class Meta:
        model = Marks
        fields = ['content', 'organization', 'design', 'delivery', 'audience_engagement', 'qna', 'total_marks']

class PracticalMarksForm(forms.ModelForm):
    content_knowledge = forms.IntegerField(required=False, min_value=0, max_value=5)
    communication_skills = forms.IntegerField(required=False, min_value=0, max_value=5)
    participation = forms.IntegerField(required=False, min_value=0, max_value=5)
    team_work = forms.IntegerField(required=False, min_value=0, max_value=5)
    content = forms.IntegerField(required=False, min_value=0, max_value=5)
    organization = forms.IntegerField(required=False, min_value=0, max_value=5)
    presentation_skills = forms.IntegerField(required=False, min_value=0, max_value=5)
    visual_aids = forms.IntegerField(required=False, min_value=0, max_value=3)
    response_to_questions = forms.IntegerField(required=False, min_value=0, max_value=2)
    mcqs = forms.IntegerField(required=False, min_value=0, max_value=10)
    short_answer_questions = forms.IntegerField(required=False, min_value=0, max_value=10)
    understanding = forms.IntegerField(required=False, min_value=0, max_value=4)
    analysis_and_application = forms.IntegerField(required=False, min_value=0, max_value=5)
    solution = forms.IntegerField(required=False, min_value=0, max_value=4)
    organization_case_study = forms.IntegerField(required=False, min_value=0, max_value=3)
    clarity = forms.IntegerField(required=False, min_value=0, max_value=2)
    references = forms.IntegerField(required=False, min_value=0, max_value=2)
    problem_definition = forms.IntegerField(required=False, min_value=0, max_value=4)
    ideation = forms.IntegerField(required=False, min_value=0, max_value=4)
    prototyping = forms.IntegerField(required=False, min_value=0, max_value=4)
    testing = forms.IntegerField(required=False, min_value=0, max_value=4)
    reflection = forms.IntegerField(required=False, min_value=0, max_value=4)
    originality = forms.IntegerField(required=False, min_value=0, max_value=4)
    impact = forms.IntegerField(required=False, min_value=0, max_value=4)
    feasibility = forms.IntegerField(required=False, min_value=0, max_value=4)
    implementation_strategy = forms.IntegerField(required=False, min_value=0, max_value=4)
    creativity = forms.IntegerField(required=False, min_value=0, max_value=4)
    
    total_marks = forms.IntegerField(required=False, min_value=0)
    
    class Meta:
        model = Marks
        fields = [
            'content_knowledge', 'communication_skills', 'participation', 'team_work',
            'content', 'organization', 'presentation_skills', 'visual_aids', 'response_to_questions',
            'mcqs', 'short_answer_questions', 'understanding', 'analysis_and_application', 'solution',
            'organization_case_study', 'clarity', 'references', 'problem_definition', 'ideation',
            'prototyping', 'testing', 'reflection', 'originality', 'impact', 'feasibility',
            'implementation_strategy', 'creativity', 'total_marks'
        ]
