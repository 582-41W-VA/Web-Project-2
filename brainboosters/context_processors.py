from .models import Subject, Level

def dropdown_options(request):
    subjects = Subject.objects.all()
    levels = Level.objects.all()


    # Define choices for Price, Gender, and Method
    price_ranges = [
        {'value': '20-29', 'label': '$20 - $29'},
        {'value': '30-39', 'label': '$30 - $39'},
        {'value': '40-49', 'label': '$40 - $49'},
        {'value': '50-59', 'label': '$50 - $59'},
        {'value': '60-69', 'label': '$60 - $69'},
        {'value': '70-99', 'label': '$70 - $99'},
    ]

    genders = [
        {'value': 'Male', 'label': 'Male'},
        {'value': 'Female', 'label': 'Female'},
        {'value': 'Other', 'label': 'Other'},
    ]

    methods = [
        {'value': 'Online', 'label': 'Online'},
        {'value': 'In-Person', 'label': 'In-Person'},
        {'value': 'Online & In-Person', 'label': 'Online & In-Person'},
    ]

    return {
        'subjects': subjects,
        'levels': levels,
        'price_ranges': price_ranges,
        'genders': genders,
        'methods': methods,
    }
