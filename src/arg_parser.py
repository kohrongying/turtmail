import argparse


class ArgParser():
    arg_file_path = ""
    arg_to_send_email = False

    def __init__(self, args) -> None:
        self.parser = argparse.ArgumentParser(description='Job to send out payslips email')
        self.parser.add_argument('file_path', type=str, help='excel file path')
        self.parser.add_argument('--send-email',
                                 nargs='?',
                                 type=bool,
                                 const=True,
                                 default=False,
                                 help='Boolean to send email or not'
                                 )
        self.args = vars(self.parser.parse_args(args))

    def get_args(self):
        return self.args['file_path'], self.args['send_email']
