def success_response(data=None, page=None, page_size=None, total=None):
    response = {
        "status": "success",
        "data": data
    }

    # Add pagination only if needed
    if page is not None:
        total_pages = (total + page_size - 1) // page_size if page_size else 1
        response.update({
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        })

    return response


def error_response(message, status="error"):
    return {
        "status": status,
        "message": message
    }
