def project_context(request):
    return {
        'logged_in': request.session.get("logged_in", None),
    }
