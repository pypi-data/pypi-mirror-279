from os import getenv

#########################################################################
#   DATABASE                                                            #
#########################################################################
SIMPLES_DABASE_URL = getenv("SIMPLES_DABASE_URL", None)

#########################################################################
#   REDIS                                                               #
#########################################################################
SIMPLESAPI_CACHE_URL = getenv("SIMPLESAPI_CACHE_URL", None)
SIMPLESAPI_CACHE_SSL = str(getenv("SIMPLESAPI_CACHE_SSL", "true")).lower() in ["1","true"]

#########################################################################
#   AWS                                                                 #
#########################################################################
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_DEFAULT_REGION = getenv("AWS_DEFAULT_REGION", None)


#########################################################################
#   ENCRYPT                                                             #
#########################################################################
INTERNAL_SERVICE_TOKEN = getenv("INTERNAL_SERVICE_TOKEN", None)