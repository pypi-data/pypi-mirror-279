import os


class Helper:
    PYSTACHO_CONFIG_FILE = 'pystacho_config.yml'

    @staticmethod
    def project_root():
        return os.getcwd()

    @staticmethod
    def config_file():
        return os.path.join(Helper.project_root(), Helper.PYSTACHO_CONFIG_FILE)

    @staticmethod
    def process_user_arguments(*args, **kwargs):
        if args and isinstance(args[0], str):
            if len(args) == 1:
                query = args[0]
                params = []
                user_args = {query: params}
            elif len(args) == 2 and isinstance(args[1], list):
                query = args[0]
                params = args[1]
                user_args = {query: params}
            else:
                raise ValueError("Invalid arguments passed.")
        elif kwargs:
            user_args = kwargs
        else:
            raise ValueError("Invalid arguments passed.")

        return user_args
