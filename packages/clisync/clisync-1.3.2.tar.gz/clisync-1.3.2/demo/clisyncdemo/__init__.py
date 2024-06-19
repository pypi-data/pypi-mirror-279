import sys
import click
from clisync import CliSync

# from .client import group


def main():
    import clisyncdemo
    from clisyncdemo.objects import ObjectControlled, Object
    group = CliSync(classes=[ObjectControlled], 
                    module=clisyncdemo)

    uncontrolled_group = CliSync(classes=[Object], 
                    module=clisyncdemo,
                    requires_decorator=False)

    cli = click.CommandCollection(sources=[group, uncontrolled_group])
    # Standalone mode is False so that the errors can be caught by the runs
    cli(standalone_mode=False)
    sys.exit()

if __name__ == "__main__":
    main()
