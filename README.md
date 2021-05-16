Request format
--------------------------------------------------------------------------------------------------------------------
: Rest interface : url

dictionary = {
    data
}

#### Python Example ####################################################
# import requests                                                      #
# data = [('dictionary', json.dumps(dictionary)]                       #
# engine_result = requests.get('http://127.0.0.1:5000/url', data=data) #
########################################################################

--------------------------------------------------------------------------------------------------------------------
# Add new user into system
: Rest interface : /monitor_engine/user/register

user = {
    "user_name": "user name in system",
    "password": "user password",
    "email_address": "user email address",
    "phone_number": "user phone number"
}
--------------------------------------------------------------------------------------------------------------------
# Add new url
: Rest interface : /monitor_engine/url/register

url = {
    "url_owner": "0",
    "url": "https://golestan.znu.ac.ir/Forms/AuthenticateUser/main.htm",
}
--------------------------------------------------------------------------------------------------------------------
# Get url for user
: Rest interface : /monitor_engine/url

owner_id = {
    "id": "0"
}
--------------------------------------------------------------------------------------------------------------------
# Get results
: Rest interface : /monitor_engine/url/result

result = {
    "url_id": "url_id",
    "from_date": "starting date",
    "to_date": "ending date"
}
--------------------------------------------------------------------------------------------------------------------
# Do Authentication
: Rest interface : /monitor_engine/user/authentication

authenticate = {
    "user_name": "user name in engine system",
    "password" : "user defined password"
}
--------------------------------------------------------------------------------------------------------------------
# Confirm user after authentication
: Rest interface : /monitor_engine/user/confirm

confirm = {
    "user_name": "registered user name",
    "confirm_code": "mailed confirm code"
}
--------------------------------------------------------------------------------------------------------------------
# Update url
: Rest interface : /monitor_engine/url/update

update = {
    "url_id": "the url id in  system",
    "fields": {
        "url": "new_url"
    }
}
--------------------------------------------------------------------------------------------------------------------
# Add credit
: Rest interface : /monitor_engine/credit/register put

credit = {
    "user_id": "user id in system",
    "requested_finance": "free or superior or busines"
}
--------------------------------------------------------------------------------------------------------------------
# Credit status
: Rest interface : /monitor_engine/credit/register get

credit = {
    "user_id": "user_id inside the engine system"
}
--------------------------------------------------------------------------------------------------------------------
# Update credit
: Rest interface : /monitor_engine/credit/update

credit = {
    "user_id": "user id in system",
    "requested_finance": "free or superior or busines"
}
--------------------------------------------------------------------------------------------------------------------
