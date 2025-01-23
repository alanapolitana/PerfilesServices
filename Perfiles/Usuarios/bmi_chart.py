import pandas as pd
from .models import BMI

def generate_bmi_dataframe():
    # Queryset con los registros de BMI
    bmi_records = BMI.objects.select_related('user').all()
    
    # Convertir el queryset a un DataFrame
    data = [
        {
            "User": bmi.user.email,
            "Weight": bmi.weight,
            "Height": bmi.height,
            "BMI": bmi.bmi,
            "Date": bmi.date,
        }
        for bmi in bmi_records
    ]
    
    df = pd.DataFrame(data)
    return df
