from fastapi import FastAPI
# Documentation
from documentations.description import app_description
from documentations.tags import tags_metadata

#Routers
import routers.router_students, routers.router_attendances, routers.router_sessions
import routers.router_auth, routers.router_stripe

# API Initilization
app = FastAPI(
    title="Attendance Track",
    description=app_description,
    openapi_tags= tags_metadata,
    docs_url='/docs'
)
# Define app routes
app.include_router(routers.router_students.router)
app.include_router(routers.router_sessions.router)
app.include_router(routers.router_attendances.router)
app.include_router(routers.router_auth.router)
app.include_router(routers.router_stripe.router)


