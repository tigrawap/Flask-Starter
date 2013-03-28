from starter import app

__author__ = 'tigra'

@app.context_processor
def register():
    return dict(
        len=len, #sometimes useful in templates
        int=int,
        str=str,
        unicode=unicode,
        LOCAL_SERVER=app.config.get('LOCAL_SERVER'),
        BASE_URL=app.config.get("BASE_URL"),
        config=app.config,
    )