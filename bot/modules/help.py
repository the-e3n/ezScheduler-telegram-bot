class _HelpText:
    def __init__(self):
        self.StartText = '''Welcome to ezScheduler,
I can send you alert for new episode of all the shows you specify. With Where to download them 
Type /help to learn more about my abilities'''
        self.AddText = '''/add [show] - To add a show to your alert list.
Or
/add -  To show all your currently added shows
eg: /add stranger things
Note: Type Correct show names as on google
For example:
Stranger Things => stranger things => STRANGER THINGS => all right
strangerthings => not good'''
        self.RemoveText = '''/remove [show] - To remove a show from your alert list.
eg: /remove stranger things
Note: The name of show must be same as you entered in add Text.'''
        self.ResetText = '''/reset - To reset all your setting like quality and shows.'''
        self.ResetAllText = '/reset_all - Reset the whole server owner only'
        self.LatestText = '/latest - Show 50 or 100 most recent released episodes'
        self.SetQualityText = '/set_quality - To set the quality of your episodes'
        self.ListText = '/list - To show the match from latest'
        self.MyShowsText = '/myshows - To show all the shows you have added to your list'
        self.SetTimerText = '/set_timer - To set polling timer'
        self.RunText = '/run - To get alert for all the episodes from all of your show'
        self.StopText = '/stop - To stop receiving alerts'
        self.HelpText = f'''Help For ezScheduler BOT
You must run /start once to initialize the bot

{self.StartText}

{self.AddText}

{self.RemoveText}

{self.LatestText}

{self.ListText}

{self.SetQualityText}

{self.RunText}

{self.ResetText}

{self.MyShowsText}

{self.StopText}'''


help = _HelpText()