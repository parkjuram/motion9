# the decorator
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect


def mobile_login_required(f):
    def wrap(request, *args, **kwargs):
        if not (request.user.is_authenticated()):
            return HttpResponseRedirect(reverse('mobile_login_page') + "?next=" + request.get_full_path())
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap