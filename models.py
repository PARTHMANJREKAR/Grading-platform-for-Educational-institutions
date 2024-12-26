from django.db import models

# Model for Student Table
class Student(models.Model):
    prn = models.CharField(max_length=20, primary_key=True, default='Unknown PRN')
    name = models.CharField(max_length=100, default='Unknown Student')
    registration_number = models.CharField(max_length=20, default='N/A')
    roll_number = models.CharField(max_length=20, default='N/A')
    branch = models.ForeignKey('BranchCode', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} ({self.prn})'

# Model for Branch Code Mapping Table
class BranchCode(models.Model):
    YEAR_CHOICES = [
        ('FE', 'First Year'),
        ('SE', 'Second Year'),
        ('TE', 'Third Year'),
        ('BE', 'Fourth Year'),
    ]

    BRANCH_CHOICES = [
        ('AI/DS', 'Artificial Intelligence/Data Science'),
        ('IT', 'Information Technology'),
        ('Comps', 'Computer Science'),
        ('ACT', 'Actuarial Science'),
        ('VLSI', 'VLSI Design'),
    ]

    year = models.CharField(max_length=2, choices=YEAR_CHOICES)
    branch_code = models.CharField(max_length=4, unique=True)
    branch_name = models.CharField(max_length=50, choices=BRANCH_CHOICES)

    def __str__(self):
        return f'{self.year} - {self.branch_code} ({self.branch_name})'

# Model for Component Selection Table
class ComponentSelection(models.Model):
    branch = models.OneToOneField(BranchCode, on_delete=models.CASCADE, primary_key=True)
    component_1 = models.CharField(max_length=50, default='Power Point Presentation')
    component_2 = models.CharField(max_length=50, default='Group Discussion')
    component_3 = models.CharField(max_length=50, default='Seminar presentation')
    component_4 = models.CharField(max_length=50, default='Quiz')
    component_5 = models.CharField(max_length=50, default='Case study')
    component_6 = models.CharField(max_length=50, default='Design thinking')
    component_7 = models.CharField(max_length=50, default='Innovation')

    def __str__(self):
        components = ', '.join([
            self.component_1, self.component_2, self.component_3,
            self.component_4, self.component_5, self.component_6,
            self.component_7
        ])
        return f'Branch: {self.branch.branch_code}, Components: {components}'


# Model for Subject Table
class Subject(models.Model):
    name = models.CharField(max_length=100, default='Unknown Subject')
    code = models.CharField(max_length=10, default='Unknown Code', unique=True)
    
    def __str__(self):
        return self.name

# Model for Theory/Practical Table
class TheoryPractical(models.Model):
    TYPE_CHOICES = [
        ('Theory', 'Theory'),
        ('Practical', 'Practical'),
    ]
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Theory')

    def __str__(self):
        return self.name

# Model for Marks Table
class Marks(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    theory_or_practical = models.ForeignKey(TheoryPractical, on_delete=models.CASCADE, default=1)
    mid_sem_marks = models.FloatField(default=0.0)
    cce_marks = models.FloatField(default=0.0)
    end_sem_marks = models.FloatField(default=0.0)
    practical_write_up = models.FloatField(default=0.0)  # Out of 5
    attendance = models.FloatField(default=0.0)  # Out of 5
    end_sem_practical = models.FloatField(default=0.0)
    
    # Fields for Theory Marks
    ppt_content = models.IntegerField(default=0)
    ppt_organization = models.IntegerField(default=0)
    ppt_design = models.IntegerField(default=0)
    ppt_delivery = models.IntegerField(default=0)
    ppt_audience_engagement = models.IntegerField(default=0)
    ppt_qna = models.IntegerField(default=0)
    
    group_discussion_content_knowledge = models.IntegerField(default=0)
    group_discussion_communication_skills = models.IntegerField(default=0)
    group_discussion_participation = models.IntegerField(default=0)
    group_discussion_team_work = models.IntegerField(default=0)
    
    seminar_content = models.IntegerField(default=0)
    seminar_organization = models.IntegerField(default=0)
    seminar_presentation_skills = models.IntegerField(default=0)
    seminar_visual_aids = models.IntegerField(default=0)
    seminar_response_to_questions = models.IntegerField(default=0)
    
    quiz_mcqs = models.IntegerField(default=0)
    quiz_short_answer_questions = models.IntegerField(default=0)
    
    case_study_understanding = models.IntegerField(default=0)
    case_study_analysis_and_application = models.IntegerField(default=0)
    case_study_solution = models.IntegerField(default=0)
    case_study_organization = models.IntegerField(default=0)
    case_study_clarity = models.IntegerField(default=0)
    case_study_references = models.IntegerField(default=0)
    
    design_thinking_problem_definition = models.IntegerField(default=0)
    design_thinking_ideation = models.IntegerField(default=0)
    design_thinking_prototyping = models.IntegerField(default=0)
    design_thinking_testing = models.IntegerField(default=0)
    design_thinking_reflection = models.IntegerField(default=0)
    
    innovation_originality = models.IntegerField(default=0)
    innovation_impact = models.IntegerField(default=0)
    innovation_feasibility = models.IntegerField(default=0)
    innovation_implementation_strategy = models.IntegerField(default=0)
    innovation_creativity = models.IntegerField(default=0)

    mse_marks = models.FloatField(default=0.0)
    ese_marks = models.FloatField(default=0.0)
    
    # Field to store the total marks
    total_marks = models.IntegerField(default=0)

    def __str__(self):
        return (f"Student: {self.student}, Subject: {self.subject}, "
                f"Theory/Practical: {self.theory_or_practical}, "
                f"Mid-Sem Marks: {self.mid_sem_marks}, CCE Marks: {self.cce_marks}, "
                f"End-Sem Marks: {self.end_sem_marks}, Practical Write-Up: {self.practical_write_up}, "
                f"Attendance: {self.attendance}, End-Sem Practical: {self.end_sem_practical}, "
                f"MSE Marks: {self.mse_marks}, ESE Marks: {self.ese_marks}, "
                f"Total Marks: {self.total_marks}")
