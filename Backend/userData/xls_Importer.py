import pandas as pd

def Create_Xsl(*fields , **model ):
    """
    Create an Excel file (.xlsx) from a model.

    Args:
        *fields: Positional arguments (sequence of strings)
            - field1: Name of the first field in the model to include in the Excel file.
            - field2: Name of the second field in the model to include in the Excel file.
            - ...
        **model: Keyword arguments (dictionary)
            - model: The model class to export.

    Returns:
        True: If the Excel sheet is successfully created.
        Exception: If an error occurs during the file creation process
    """
    
    export_Model = model["model"]
    name = export_Model._meta.model_name +".xlsx"
    users = export_Model.objects.all()
    dicts = list(users.values(*fields))
    data_Frame = pd.DataFrame(dicts)
    try :
        data_Frame.to_excel(excel_writer=name,index=False)
        return (True) 
    except Exception as e:
        return (e)