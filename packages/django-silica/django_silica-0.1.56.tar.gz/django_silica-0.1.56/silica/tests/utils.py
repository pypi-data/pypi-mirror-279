from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import Context, Template


def create_test_view(inline_template_string, context_dict=None):
    """
    Dynamically creates a class-based view with the provided inline template string and context.

    :param inline_template_string: The template string to be rendered.
    :param context_dict: Optional dictionary to be used as context for rendering the template.
    :return: A class-based view dynamically generated.
    """
    if context_dict is None:
        context_dict = {}

    class DynamicTestView(TemplateView):
        def get(self, request, *args, **kwargs):
            context_dict['request'] = request

            template = Template("""
                {% load silica %}
                {% load silica_scripts %}
                {% silica_scripts %}    
            """ + inline_template_string)
            context = Context(context_dict)
            rendered_template = template.render(context)
            return HttpResponse(rendered_template)

    return DynamicTestView


def data_get(data, path, default=None):
    """
    Retrieves a value from a nested data structure using "dot" notation.
    This function is designed to work with dictionaries and tuples.
    Parameters
    ----------
    data : dict or tuple or None
        The data structure from which to retrieve the value.
        This can be a nested dictionary, tuple, or a combination of both.
    path : str
        The "dot" notation path to the value to be retrieved.
        For dictionaries, parts of the path are treated as keys.
        For tuples, parts of the path are treated as indices.
        For example, the path 'user.0' would get the first element from the 'user' key if it's a tuple.
    default : any, optional
        The default value to return if the specified path is not found in the data structure.
        By default, it is None.
    Returns
    -------
    any
        The value found at the specified path in the data structure.
        If the path is not found, the default value is returned.
    Examples
    --------
    # Nested dictionary example
    data = {'user': {'name': {'first': 'John', 'last': 'Doe'}}}
    print(data_get(data, 'user.name.first'))  # Outputs: John
    # Tuple example
    data = ('John', 'Doe')
    print(data_get(data, '0'))  # Outputs: John
    # Mixed example
    data = {'user': ('John', 'Doe')}
    print(data_get(data, 'user.0'))  # Outputs: John
    """

    parts = path.split(".")
    for part in parts:
        if isinstance(data, dict):
            data = data.get(part, default)
        elif isinstance(data, tuple) and part.isdigit():
            index = int(part)
            if index < len(data):
                data = data[index]
            else:
                return default
        elif hasattr(data, part):  # Check if data has the attribute
            data = getattr(data, part)  # Get the attribute
        else:
            return default
    return data
