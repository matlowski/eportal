def nav_links(request):
    if not request.user.is_authenticated:
        return {
            "nav_links": [
                {"name": "Login", "url": "login"},
                {"name": "Register", "url": "register"},
            ]
        }
    if request.user.role == "student":
        return {
            "nav_links": [
                {
                    "name": "My Results",
                    "url": "my_results",
                },
                {
                    "name": "My Courses",
                    "url": "my_courses",
                },
                {"name": "Edit Profile", "url": "edit_user"},
                {"name": "Logout", "url": "logout"},
            ]
        }
    else:
        return {
            "nav_links": [
                {
                    "name": "Add Course",
                    "url": "add_course",
                },
                {
                    "name": "My Courses",
                    "url": "author_courses",
                },
                {"name": "Edit Profile", "url": "edit_user"},
                {"name": "Logout", "url": "logout"},
            ]
        }
