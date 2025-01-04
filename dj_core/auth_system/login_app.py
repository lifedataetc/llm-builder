from dash import dcc, html, ALL, Input, Output, State
from dash import no_update as nup
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from django.contrib.auth import authenticate, login
import traceback
import bleach

from apps.utils.misc import email_validator, update_or_create_session_data, get_session_data
from apps.utils.models import ErrorLog
from auth_system.utils import email_opt
from apps.backoffice.models import Role


########################################################################################################################
# layout
########################################################################################################################
def make_pass_div(stage):
    if stage == 1:
        return html.Div([
            html.H2('Enter your Email to Log in', className='text-center text-white'),
            dbc.Card(
                [
                    dbc.CardBody([
                        dbc.Row([dbc.Input(id={'type': 'login_email', 'index': 1}, type='email',
                                           placeholder='Email')]),
                        html.Br(), dcc.Loading(html.Div(id='message', className='text-center')), html.Br(),
                        html.Div([
                            dbc.Button('Send One Time Password', id={'type': 'log_req', 'index': 1})
                        ], className='text-center')

                    ])], className='card bg-secondary border-0 mb-0 px-lg-5 py-lg-5')
        ])
    elif stage == 2:
        return html.Div([
            html.H2('Enter your One Time Password', className='text-center text-white'),
            dbc.Card(
                [
                    dbc.CardBody([
                        html.P('The password was sent to your email', className='text-center'),
                        dbc.Row([dbc.Input(id={'type': 'otp_input', 'index': 1}, #type='password',
                                           placeholder='One Time Password')]),
                        html.Br(), dcc.Loading(html.Div(id='message', className='text-center')), html.Br(),
                        html.Div([
                            dbc.Button('Submit', id={'type': 'log_in', 'index': 1})
                        ], className='text-center')

                    ])], className='card bg-secondary border-0 mb-0 px-lg-5 py-lg-5')
        ])

########################################################################################################################
# layout
########################################################################################################################
external_css = ['/static/assets/css/argon.css']
app = DjangoDash('login', external_stylesheets=external_css)

layout = html.Div([
    html.Div(id='outer'), html.Div(id='redirector'),
    html.Div(id='main_div', children = [make_pass_div(1)]), html.Div(id='dummy')
])


########################################################################################################################
# callbacks
########################################################################################################################
@app.callback(
    Output('redirector', 'children'),
    Output('main_div', 'children'),
    Output('message', 'children'),
    [Input({'type': 'log_req', 'index': ALL}, 'n_clicks'),
     Input({'type': 'log_in', 'index': ALL}, 'n_clicks'),
    State({'type': 'login_email', 'index': ALL}, 'value'),
    State({'type': 'otp_input', 'index': ALL}, 'value'),]
)
def manager(n_clicks_email, n_clicks_pass, email, otp_val, **kwargs):
    #print(kwargs['callback_context'])
    session_key = kwargs['request'].session._SessionBase__session_key
    is_authenticated = kwargs['request'].user.is_authenticated
    trigger = kwargs['callback_context'].triggered
    if len(trigger) > 0:
        prop_id = eval(trigger[0]['prop_id'].split('.')[0])['type']
    else:
        prop_id = None
    # already logged in so we send you back to home page
    if is_authenticated:
        return dcc.Location(pathname='/', id='redir'), nup, ''

    if prop_id == 'log_req':
        # TODO: change the logic to NOT validate if the email exists in the system
        if email[0] is not None:
            email = bleach.clean(email[0]).lower()
            is_valid = email_validator(email)
            if is_valid:
                try:
                    # confirm that user exists
                    usr = Role.objects.get(email=email)
                    # create or update session data for this session
                    sd = update_or_create_session_data(session_key, 'auth_session',
                                                       {'email': email, 'username': usr.username,
                                                        'login_attempts': 0})
                    # generate a new secure password
                    # set the new password
                    # send the email
                    #msg = html.B('User exists', className='text-success')
                    email_opt(usr)
                    out_div = make_pass_div(2)
                    return nup, out_div, ''
                except Role.DoesNotExist:
                    msg = html.B('User does not exist', className='text-danger')
                    return nup, nup, msg
                except Exception as e:
                    err = ErrorLog.objects.create(error=traceback.format_exc(), error_function='login_app')
                    err.save()
                    msg = html.B(['An error occurred and has been logged. Please contact support at',
                                 f' support@telperionscientific.com with error id {err.id}'], className='text-danger')
                    return nup, nup, msg
            else:
                msg = html.B('Please enter a valid email address', className='text-danger')
                return nup, nup, msg
        else:
            return nup, nup, ''

    elif prop_id == 'log_in':
        sd = get_session_data(session_key, 'auth_session')
        sd.session_data['login_attempts'] += 1
        l_atts = sd.session_data['login_attempts']
        username = sd.session_data['username']
        sd.save()
        otp_val = otp_val[0]
        # TODO: Limit how long the auth session lasts
        user = authenticate(username=username, password=otp_val)
        if user is not None:
            login(kwargs['request'], user)
            return dcc.Location(pathname='/', id='redir'), nup, ''
        elif user is None and l_atts <= 5:
            return nup, nup, html.B(f'Invalid Password. {6-l_atts} Attempts Remaining', className='text-danger')
        elif user is None and l_atts > 5:
            email = sd.session_data['email']
            usr = Role.objects.get(email=email)
            email_opt(usr)
            return nup, nup, html.B('Max login attempts reached. A new password was send to your email.',
                                    className='text-danger')

    return nup, nup, ''


app.layout = layout

