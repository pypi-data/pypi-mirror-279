import argparse
from . import __version__
from . application import Application



parser = argparse.ArgumentParser(
	prog='wgtk',
	description='WireGuard Toolkit'
)

parser.add_argument(
	'--version',
	action='version',
	version=f'%(prog)s {__version__}'
)

subparser = parser.add_subparsers(
	dest='command',
)

parser_template = subparser.add_parser('template')

parser_generate = subparser.add_parser('generate')
parser_generate.add_argument('configuration')



def run(args):

	if args.command is None:
		return

	if args.command == 'template':
		application = Application.GenerateTemplate()

	if args.command == 'generate':
		application = Application.GenerateConfiguration(args.configuration)

	application.run()



args = parser.parse_args()
run(args)
