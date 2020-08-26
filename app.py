# import libraries
import dash

# define the app
app = dash.Dash(__name__)

# suppress callback exceptions as they are spread throughout the files
app.config.suppress_callback_exceptions = True

