def all_tasks():
    try:
        import json
        from .settings import tasks, marks
        from .load_tasks import load_tasks
        
        load_tasks()  # Assuming this function initializes tasks and marks
        
        return {"tasks": tasks(), "marks": marks()}
    
    except FileNotFoundError as e:
        return {"error": f"File not found: {str(e)}"}
    
    except ImportError as e:
        return {"error": f"Import error: {str(e)}"}
    
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
