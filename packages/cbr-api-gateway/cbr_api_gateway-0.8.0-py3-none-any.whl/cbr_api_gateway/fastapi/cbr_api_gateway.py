import cbr_static
import cbr_website_beta
from cbr_athena.fastapi.FastAPI_Athena  import FastAPI_Athena
from cbr_website_beta.flask.Flask_Site  import Flask_Site
from fastapi.middleware.wsgi            import WSGIMiddleware
from osbot_utils.utils.Files            import path_combine
from starlette.staticfiles              import StaticFiles

flask_site  = Flask_Site()
cbr_flask   = flask_site.app()
app         = FastAPI_Athena().setup().app()
assets_path = path_combine(cbr_static      .path, 'assets')
dist_path   = path_combine(cbr_website_beta.path, 'static/dist')

app.mount("/web", WSGIMiddleware(cbr_flask))
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
app.mount("/dist"  , StaticFiles(directory=dist_path  ), name="dist"  )

print("------- in cbr_api_gateway.py ---- ")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)