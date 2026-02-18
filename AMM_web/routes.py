"""constants pertaining to the routes of the web application"""

# public pages
HOME_ROUTE = "/"
ABOUT_ROUTE = "/about"
LOGIN_ROUTE = "/login"
SIGNUP_ROUTE = "/signup"
PRIVACY_ROUTE = "/privacy"
TERMS_ROUTE = "/terms"

#behind authentication
CONTACT_ROUTE = "/contact"
DASHBOARD_ROUTE = "/dashboard"
SEARCH_ROUTE = "/search"

# admin pages
ADMIN_USERS_ROUTE = "/admin/users"
ADMIN_SYSTEM_ROUTE = "/admin/system"

# dynamic routes
TRACK_DETAIL_ROUTE = "/tracks/[track_id]"
ALBUM_DETAIL_ROUTE = "/albums/[album_id]"
PERSON_DETAIL_ROUTE = "/persons/[person_id]"
FILE_DETAIL_ROUTE = "/files/[file_id]"
LABEL_DETAIL_ROUTE = "/labels/[label_id]"
TRACK_EDIT_ROUTE = "/tracks/[track_id]/edit"
ALBUM_EDIT_ROUTE = "/albums/[album_id]/edit"
PERSON_EDIT_ROUTE = "/persons/[person_id]/edit"
FILE_EDIT_ROUTE = "/files/[file_id]/edit"
LABEL_EDIT_ROUTE = "/labels/[label_id]/edit"
