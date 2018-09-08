from oscar.apps.shipping import repository, models
from . import methods

class Repository(repository.Repository):

    def get_available_shipping_methods(
            self, basket, user=None, shipping_addr=None,
            request=None, **kwargs):
        meths = (methods.Standard(), methods.Express())
        # if shipping_addr and shipping_addr.country.code == 'GB':
        #     # Express is only available in the UK
        #     methods = (methods.Standard(), methods.Express())
        return meths

