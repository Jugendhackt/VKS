from app.models import entrys, terms

from app import app

info = """
###########################
#     VKS-Development     #
#     by Chasotheorie     #
###########################

###########################
#    Development build    #
#       Do Not use        #
# in prduction enviroment #
###########################

###########################
#     Licensed under      #
#     GNU GENERAL         #
#     PUBLIC LICENSE      #
###########################

###########################
#      Version 0.0.1      #
###########################
"""
print(info)

# Refresh the elasticsearch indicies
from app.models import User, terms, entrys
User.reindex()
entrys.reindex()
terms.reindex()

print("Indicies refreshed")

app.run(debug=False, host="0.0.0.0", port=5000)
