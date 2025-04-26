# app/utils/response.py

def success_response(data=None, message="Success", status_code=200):
    return {
        "status": "success",
        "message": message,
        "data": data,
        "status_code": status_code
    }

def error_response(message="An error occurred", status_code=400):
    return {
        "status": "error",
        "message": message,
        "data": None,
        "status_code": status_code
    }
