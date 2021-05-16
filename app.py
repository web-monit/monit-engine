"""
    @Author : Manouchehr Rasouli
    @Date   : 10/july/2018
"""

# todo : use app scheduler...
# todo : minimize database access
# todo : change database access to use g
from datetime import timedelta
from flask import Flask
from flask_restful import Api
import config_loader
import service_starter
from restful_interface import url, checkpoint, result, user
from flask_cors import CORS
from flask_jwt_extended import JWTManager

loader = config_loader.ConfigLoader()
configuration = loader.get_config()

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['JWT_SECRET_KEY'] = configuration["monitor_engine.property"]["jtw_secret_key"]
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=configuration["monitor_engine.property"]["jwt_expire_delta"])
jwt = JWTManager(app)
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


# Add resources
api.add_resource(url.UrlRegister,
                 configuration["monitor_engine.restful_interface"]["url_register"],
                 resource_class_kwargs={'config_file': configuration})

api.add_resource(user.UserRegistry,
                 configuration["monitor_engine.restful_interface"]["user_registry"],
                 resource_class_kwargs={'config_file': configuration})

api.add_resource(checkpoint.CheckPoint,
                 configuration["monitor_engine.restful_interface"]["check_point"],
                 resource_class_kwargs={'config_file': configuration})

api.add_resource(url.GetUrl,
                 configuration["monitor_engine.restful_interface"]["url_for"],
                 resource_class_kwargs={'config_file': configuration})

api.add_resource(result.Result,
                 configuration["monitor_engine.restful_interface"]["result_for"],
                 resource_class_kwargs={'config_file': configuration})

api.add_resource(user.UserAuthentication,
                 configuration["monitor_engine.restful_interface"]["user_authentication"],
                 resource_class_kwargs={'config_file': configuration, 'blacklist': blacklist})

api.add_resource(user.ConfirmUserAuthentication,
                 configuration["monitor_engine.restful_interface"]["confirm_user"],
                 resource_class_kwargs={'config_file': configuration})

api.add_resource(url.DeleteUrl,
                 configuration["monitor_engine.restful_interface"]["url_delete"],
                 resource_class_kwargs={'config_file': configuration})

service_starter.StarterKit()
if __name__ == '__main__':
    app.run(debug=True)
