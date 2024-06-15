from colorama import Fore, Style

class Logger:
    QUERY_COLORS = {
        'insert': Fore.GREEN,
        'update': Fore.YELLOW,
        'delete': Fore.RED,
        'select': Fore.CYAN
    }

    def sprint(self, text, color):
        codes = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'reset': '\033[0m'
        }
        print(f"{codes[color]}{text}{codes['reset']}")

    def log(self, text, color='black'):
        self.sprint(text, color)

    @staticmethod
    def duration_color(duration):
        if duration < 10:
            return Fore.GREEN
        elif duration < 100:
            return Fore.YELLOW
        else:
            return Fore.RED

    @staticmethod
    def log_sql(query, values, duration, engine_name='SQL'):
        query_type = query.split()[0].lower()
        query_color = Logger.QUERY_COLORS[query_type]
        print(f"{Fore.MAGENTA}{engine_name}-->{Style.RESET_ALL} {Logger.duration_color(duration)}Load ({round(duration, 2)}ms){Style.RESET_ALL} {query_color} %s {Style.RESET_ALL} {Fore.BLUE} %s {Style.RESET_ALL}" % (query, values))
