import click
import nepali_datetime
import datetime


today = nepali_datetime.date.today()


@click.group(invoke_without_command=True)
@click.pass_context
def date_group(ctx):
    if ctx.invoked_subcommand is None:
        ctx.invoke(today_date)

@click.command(name="cnv")
@click.option("--year", "-y", type=int, prompt="Year in AD ", help="Year in English.", required=True)
@click.option("--month", "-m", type=int, prompt="Month in AD ", help="Month in English.", required=True)
@click.option("--day", "-d", type=int, prompt="Day in AD ", help="Day in English.", required=True)
def convert_date(year, month, day):
    """Converts an English date to a Nepali date."""
    english_date = datetime.date(year, month, day)
    # np_date = nepali_datetime.date(year, month, day).to_datetime_date()
    np_date = nepali_datetime.date.from_datetime_date(english_date)
    formatted_date = np_date.strftime('%B %d %Y %A')
    click.echo()
    click.echo(click.style( formatted_date, fg="green", bold=True))

@click.command(name="today")
def today_date():
    """Get today's date in Nepali Calander."""
    today = nepali_datetime.date.today()
    formatted_date = today.strftime('%B %d %Y, %A')
    click.echo()
    click.echo(click.style(formatted_date, fg="green", bold=True))
    # click.echo(today.strftime('%K-%n-%D (%k %N %G)'))



@click.command(name="cal")
@click.option("--year", "-y", type=int, prompt="Year ", help="Year in English.",default=today.year )
@click.option("--month", "-m", type=int, prompt="Month ", help="Month in English.", default=today.month )
@click.option("--day", "-d", type=int, prompt="Day ", help="Day in English.", default=today.day )
def display_calander(year: int, month:int, day:int):
    """Display the nepali calander of the given date"""
    
    cal = nepali_datetime.date(year, month, day).calendar()
    click.echo(cal)
    # click.echo(click.style(cal))




date_group.add_command(today_date)
date_group.add_command(convert_date)
date_group.add_command(display_calander)

def main():
    # today_date()
    date_group()


if __name__ == '__main__':
    main()