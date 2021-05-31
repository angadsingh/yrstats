import os
from datetime import datetime, date, timedelta
import json
import watchdog.events
import watchdog.observers
import sys
import time
from json2html import *
import string,cgi,time
from http.server import HTTPServer, CGIHTTPRequestHandler
import webbrowser
import threading
import copy
import functools
import click
import yaml
import subprocess
import glob
import shutil
import ntpath
import colorama
import urllib

import statparser


COUNTABLE_HEAPS = [ "units_bought",
     "infantry_bought",
     "planes_bought",
     "ships_built",
     "buildings_bought",
     "units_killed",
     "infantry_killed",
     "planes_killed",
     "ships_killed",
     "buildings_killed",
     "buildings_captured",
     "units_lost",
     "infantry_lost",
     "planes_lost",
     "buildings_lost",
     "ships_lost",
     "crates_found" ]

TIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

def print_info(text):
    print(colorama.Fore.YELLOW + text)

def print_special(text):
    print(colorama.Fore.GREEN + text)

def print_special2(text):
    print(colorama.Fore.BLUE + text)    

def print_error(text):
    print(colorama.Fore.RED + text)

def _read_config_yaml(ctx, file):
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
            print_info("Loaded configuration yaml")
        except yaml.YAMLError as exc:
            print_error(exc)
            ctx.fail("Could not load configuration yaml")

def get_session_stats_json_file(sessionStatsFolder, start_time):
    return sessionStatsFolder + '/' + start_time.strftime('%Y-%m-%d %H-%M-%S') + '/' + str(int(start_time.timestamp())) + "_session_stats.json"

def get_session_stats_html_file(sessionStatsFolder, start_time):
    return sessionStatsFolder + '/' + start_time.strftime('%Y-%m-%d %H-%M-%S') + '/' + str(int(start_time.timestamp())) + "_session_stats.html"

def get_overall_stats_json_file(overallStatsFolder):
    return overallStatsFolder + '/' + "overall_stats.json"

def get_overall_stats_html_file(overallStatsFolder):
    return overallStatsFolder + '/' + "overall_stats.html"

def call_stat_dmp_parser(config, stat_dmp_file_path = None):
    dmp_file = stat_dmp_file_path if stat_dmp_file_path != None else config['statsDmpFilePath']
    cmd = '"{}" ./statparser.php "{}" "{}" "{}"'.format(config['phpExecutable'], config['thisPlayerName'],
                   dmp_file, config['gameStatsFolder'])
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result, err = process.communicate()
    print_special2(result.decode('utf-8'))
    if process.returncode != 0:
        print_error("Could not run statparser.php")
    else:
        return [l for l in result.decode('utf-8').split('\n') if 'stats_parsed' in l][0][14:]

def reset_xsplit_xml(config):
    xsplitXmlTemplate = config['xsplitXmlTemplate']
    xsplitXmlTargetPath = config['xsplitXmlTargetPath']

    with open(xsplitXmlTemplate,"r") as f:
        xsplitXmlTemplate = f.read()

    xsplitXmlTemplate = xsplitXmlTemplate.replace("{{timestamp}}", str(int(datetime.now().timestamp())))
    xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player1name}}", "--")
    xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player2name}}", "--")
    xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player1wins}}", "0")
    xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player2wins}}", "0")

    with open(xsplitXmlTargetPath, "w") as outfile:
        outfile.write(xsplitXmlTemplate)

def write_xsplit_xml(config, session_stats):
    if len(session_stats['player_stats'].items()) >= 2:
        playernames = []
        playerwins = []
        n = 1
        for name, stats in session_stats['player_stats'].items():
            if n <= 2:
                playernames.append(name)
                playerwins.append(stats['wins'])
                n += 1

        xsplitXmlTemplate = config['xsplitXmlTemplate']
        xsplitXmlTargetPath = config['xsplitXmlTargetPath']

        with open(xsplitXmlTemplate,"r") as f:
            xsplitXmlTemplate = f.read()

        xsplitXmlTemplate = xsplitXmlTemplate.replace("{{timestamp}}", str(int(datetime.now().timestamp())))
        xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player1name}}", str(playernames[0]))
        xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player2name}}", str(playernames[1]))
        xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player1wins}}", str(playerwins[0]))
        xsplitXmlTemplate = xsplitXmlTemplate.replace("{{player2wins}}", str(playerwins[1]))
    
        with open(xsplitXmlTargetPath, "w") as outfile:
            outfile.write(xsplitXmlTemplate)

class StatsDmpWatcher(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, ctx_obj, dmp_file, start_time):
        self.ctx_obj = ctx_obj
        self.config = ctx_obj['CONFIG']
        self.start_time = start_time
        self.processed_files = {}
        self.session_stats = {}
        self.overall_stats = self.load_overall_stats()
        self.last_notification_time = None

        gameStatsFolder = self.config['gameStatsFolder']
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*'+dmp_file+'*'])

    def load_overall_stats(self):
        file = get_overall_stats_json_file(self.config['overallStatsFolder'])
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                return data
            except Exception as e:
                print_error(file + " could not be parsed")
                print_error(e)

    def do(self, event):
        time_now = datetime.now()
        if self.last_notification_time != None:
            #ignore - watchdog bug causing repeat events for the same file update)
            if (time_now-self.last_notification_time).total_seconds() < 10:
                return

        self.last_notification_time = time_now

        gamestats = statparser.process_stats(
            event.src_path,
            self.config["gameStatsFolder"],
            self.config["thisPlayerName"],
        )
       
        if gamestats not in self.processed_files:
            print_special("Aggregating SESSION stats from parsed game stats: " + gamestats)
            aggregate_game_stats(self.config, self.session_stats, gamestats, self.start_time)
            print_special("Aggregating OVERALL stats from parsed game stats: " + gamestats)
            aggregate_game_stats(self.config, self.overall_stats, gamestats, self.start_time)
            
            session_stats_json = get_session_stats_json_file(self.config['sessionStatsFolder'], self.start_time)
            session_stats_html = get_session_stats_html_file(self.config['sessionStatsFolder'], self.start_time)
            report_aggregated_stats(self.session_stats, session_stats_json, session_stats_html, self.start_time, self.config['htmlTemplateSessions'], self.config['htmlResourcesRelPathSessions'])

            overall_stats_json = get_overall_stats_json_file(self.config['overallStatsFolder'])
            overall_stats_html = get_overall_stats_html_file(self.config['overallStatsFolder'])
            for game_history in self.overall_stats['game_history']:
                if 'relative_start_time' in game_history:
                    del game_history['relative_start_time']
            report_aggregated_stats(self.overall_stats, overall_stats_json, overall_stats_html, self.start_time, self.config['htmlTemplateOverall'], self.config['htmlResourcesRelPathOverall'])

            if self.config['write_xsplit_xml']:
                write_xsplit_xml(self.config, self.session_stats)

            self.ctx_obj['num_games'] += 1
            self.processed_files[gamestats] = {}

    def on_created(self, event):
        self.do(event)

    def on_modified(self, event):
        self.do(event)

    def on_moved(self, event):
        self.do(event)

def aggregate_game_stats_multi(config, since_when):
    aggregated_stats = {}
    processed_files = {}
    earliest_ts = None

    path = config['gameStatsFolder']
    allfiles =  [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0], '*_parsed.json'))]

    for file_path in allfiles:
        file = ntpath.basename(file_path)
        filets = file.split("_")[0]
        try:
            filets = datetime.fromtimestamp(int(filets))
        except:
            continue

        if filets > since_when:
            print_special("Aggregating SESSION/OVERALL stats from parsed game stats: " + file_path)
            aggregate_game_stats(config, aggregated_stats, file_path, since_when)
            processed_files[file_path] = {}
            if earliest_ts == None:
                earliest_ts = filets
    return (aggregated_stats, processed_files, earliest_ts)

def resolve_player_aliases(player_aliases, name):
    for aliases in player_aliases:
        if name in aliases:
            return aliases[0]
    return name

def aggregate_game_overall_stats(aggregated_stats, data):
    if 'games_played' not in aggregated_stats:
        aggregated_stats['games_played'] = 0
    aggregated_stats['games_played'] += 1

    if 'maps_played' not in aggregated_stats:
        aggregated_stats['maps_played'] = []

    if data['gameReport']['map'] not in aggregated_stats['maps_played']:
        aggregated_stats['maps_played'].append(data['gameReport']['map'])

    if 'total_duration' not in aggregated_stats:
        aggregated_stats['total_duration_secs'] = 0

    aggregated_stats['total_duration_secs'] += data['gameReport']['duration']
    aggregated_stats['total_duration'] = str(timedelta(seconds=aggregated_stats['total_duration_secs']))

def resolve_player_stats(data):
    playerStats = {}
    if isinstance(data['playerStats'], list):
        i = 0
        for stats in data['playerStats']:
            playerStats[i] = stats
            i += 1
    else:
        playerStats = data['playerStats']

    return playerStats

def aggregate_game_player_stats(config, aggregated_stats, data):
    if 'player_stats' not in aggregated_stats:
        aggregated_stats['player_stats'] = {}

    playerStats = resolve_player_stats(data)

    for i, stats in playerStats.items():
        name = resolve_player_aliases(config['playerAliases'], stats['name'])

        if name not in aggregated_stats['player_stats']:
            aggregated_stats['player_stats'][name] = {
                    "games_played": 0,
                    "funds_left": 0,
                    "funds_left_avg": 0,
                    "disconnections": 0,
                    "no_completions": 0,
                    "quits": 0,
                    "wins": 0,
                    "draws": 0,
                    "defeats": 0,
                    "sides": {},
                    "detailed_counts": {
                    }
                }

        for heap in COUNTABLE_HEAPS:
            aggregated_stats['player_stats'][name]['detailed_counts'][heap] = {}

        aggregated_stats['player_stats'][name]['games_played'] += 1
        aggregated_stats['player_stats'][name]['funds_left'] += stats['funds_left']
        aggregated_stats['player_stats'][name]['funds_left_avg'] = aggregated_stats['player_stats'][name]['funds_left'] / aggregated_stats['player_stats'][name]['games_played']
        aggregated_stats['player_stats'][name]['disconnections'] += 1 if stats['disconnected'] else 0
        aggregated_stats['player_stats'][name]['no_completions'] += 1 if stats['no_completion'] else 0
        aggregated_stats['player_stats'][name]['quits'] += 1 if stats['quit'] else 0
        aggregated_stats['player_stats'][name]['wins'] += 1 if stats['won'] else 0
        aggregated_stats['player_stats'][name]['draws'] += 1 if stats['draw'] else 0
        aggregated_stats['player_stats'][name]['defeats'] += 1 if stats['defeated'] else 0

        if stats['side'] not in aggregated_stats['player_stats'][name]['sides']:
            aggregated_stats['player_stats'][name]['sides'][stats['side']] = 0

        aggregated_stats['player_stats'][name]['sides'][stats['side']] += 1

        for heap in COUNTABLE_HEAPS:
            if heap in stats:
                if heap not in aggregated_stats['player_stats'][name]:
                    aggregated_stats['player_stats'][name][heap] = 0
                aggregated_stats['player_stats'][name][heap] += stats[heap]
            if heap in stats['detailed_counts']:
                for _type, count in stats['detailed_counts'][heap].items():
                    if _type not in aggregated_stats['player_stats'][name]['detailed_counts'][heap]:
                        aggregated_stats['player_stats'][name]['detailed_counts'][heap][_type] = 0

                    aggregated_stats['player_stats'][name]['detailed_counts'][heap][_type] += stats['detailed_counts'][heap][_type]

def aggregate_game_history(config, aggregated_stats, data, start_time):
    if 'game_history' not in aggregated_stats:
            aggregated_stats['game_history'] = []

    relative_start_time = data['gameReport']['epoch_time'] - start_time.timestamp()
    if relative_start_time < 0:
        relative_start_time = '-'+str(timedelta(seconds=int(abs(relative_start_time))))
    else:
        relative_start_time = str(timedelta(seconds=int(abs(relative_start_time))))

    game_history = {
        "map": data['gameReport']['map'],
        "players": [],
        "duration": str(timedelta(seconds=data['gameReport']['duration'])),
        "start_time": datetime.fromtimestamp(data['gameReport']['epoch_time']).strftime(TIME_FORMAT),
        "relative_start_time": relative_start_time
    }

    playerStats = resolve_player_stats(data)

    winner = "AI"
    for i, stats in playerStats.items():
        name = resolve_player_aliases(config['playerAliases'], stats['name'])
        if stats['won']:
            winner = name
        game_history['players'].append(name + "/" + stats['side'])

    game_history['winner'] = winner
    aggregated_stats['game_history'].append(game_history)

def retryable_file_open(file, max_times = 5, times = 0):
    f = None
    try:
        f = open(file, 'r')
    except PermissionError:
        #file still being written when we're reading it, retry
        time.sleep(1)
        if times < max_times:
            print_info ("Retrying opening file: " + file)
            return retryable_file_open(file, max_times = max_times, times = times + 1)
    return f

def aggregate_game_stats(config, aggregated_stats, file, start_time):
    f = retryable_file_open(file)
    if f == None:
        print_error ("Could not open file even after retries. Unrecoverable")
        sys.exit(1)

    with f:
        try:
            data = json.load(f)
        except Exception as e:
            print_error(file + " could not be parsed")
            print_error(e)
            return

        aggregate_game_overall_stats(aggregated_stats, data)
        aggregate_game_history(config, aggregated_stats, data, start_time)
        sorted(aggregated_stats['game_history'], key=lambda k: k['start_time']) 
        aggregate_game_player_stats(config, aggregated_stats, data)

def camel(snake_str):
    words = snake_str.split('_')
    return ' '.join([*map(str.title, words)])

def humanize(d, level = 1, start_level = -1, end_level = sys.maxsize):
    r = d
    op = functools.partial(humanize, level=level+1, start_level=start_level, end_level=end_level)
    if isinstance(d, list):
        r = [op(j) for j in d]
    elif isinstance(d, dict):
        r = {}
        for k, v in d.items():
            r[op(k) if level >= start_level and level <= end_level else k] = op(v) if isinstance(v, dict) or isinstance(v, list) else v

    elif isinstance(d, str):
        r = camel(d) if level >= start_level and level <= end_level else d
    
    return r

def report_aggregated_stats(aggregated_stats, aggregated_stats_json, aggregated_stats_html, start_time, template_html, htmlResourcesRelPath):
    base_dir = os.path.dirname(os.path.abspath(aggregated_stats_json))
    os.makedirs(base_dir, exist_ok=True)
    base_dir = os.path.dirname(os.path.abspath(aggregated_stats_html))
    os.makedirs(base_dir, exist_ok=True)

    with open(aggregated_stats_json, 'w') as outfile:
        json.dump(aggregated_stats, outfile, indent=4, sort_keys=True)

    overall_stats = copy.copy(aggregated_stats)
    del overall_stats['player_stats']
    del overall_stats['game_history']
    overall_stats_html = json2html.convert(json = humanize(overall_stats), table_attributes = "class=\"table table-condensed table-bordered table-hover\"")

    game_history = humanize(aggregated_stats['game_history'], start_level=2, end_level=2)
    game_history_html = json2html.convert(json = game_history, table_attributes = "class=\"table table-condensed table-bordered table-hover\"")

    player_stats = humanize(aggregated_stats['player_stats'], start_level=2, end_level=4)
    player_stats_html = json2html.convert(json = player_stats, table_attributes = "class=\"table table-condensed table-bordered table-hover\"")

    with open(template_html,"r") as f:
        template_html = f.read()

    template_html = template_html.replace("{{start_time}}", start_time.strftime(TIME_FORMAT))
    template_html = template_html.replace("{{overall_stats}}", overall_stats_html)
    template_html = template_html.replace("{{game_history}}", game_history_html)
    template_html = template_html.replace("{{player_stats}}", player_stats_html)
    template_html = template_html.replace("{{html_resources}}", htmlResourcesRelPath)
    
    with open(aggregated_stats_html, "w") as outfile:
        outfile.write(template_html)

def start_web_server(path, port=8000):
    '''Start a simple webserver serving path on port'''
    os.chdir(path)
    httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
    httpd.serve_forever()

def start_web_reporter(sessionStatsFolder, start_time, open_browser = False):
    # Start the server in a new thread
    port = 8000
    daemon = threading.Thread(name='daemon_server',
                              target=start_web_server,
                              args=('.', port))
    daemon.setDaemon(True) # Set as a daemon so it will be killed once the main thread is dead.
    daemon.start()

    # Open the web browser 
    if open_browser:
        webbrowser.open('http://localhost:{}/{}'.format(port, get_session_stats_html_file(sessionStatsFolder, start_time)))

def upload_to_surge(config, start_time, open_browser):
    print_info("Uploading to surge")
    oldcwd = os.getcwd()
    os.chdir(config['surgeFolder'])
    try:
        process = subprocess.Popen("surge .", shell=True, stdout=subprocess.PIPE)
        result, err = process.communicate()
        print_special2(result.decode('utf-8'))
        if process.returncode != 0:
            print_error("Could not run surge")
        else:
            surge_url = config['surgeSessionPath'] + urllib.parse.quote(start_time.strftime('%Y-%m-%d %H-%M-%S') + '/' + str(int(start_time.timestamp())) + "_session_stats")
            print_special("surged to: " + surge_url)
            if open_browser:
                webbrowser.open(surge_url)
    finally:
        os.chdir(oldcwd)

def report_youtube_summary(config, start_time):
    try:
        with open(get_session_stats_json_file(config['sessionStatsFolder'], start_time), 'r') as f:
            session_stats = json.load(f)
            game_history = session_stats['game_history']
            print_special("YOUTUBE SUMMARY")
            for game in game_history:
                summary = game['relative_start_time']
                summary = "{relative_start_time} \"{map}\": {players}, {winner} WON".format(
                        relative_start_time=game['relative_start_time'],
                        map=game['map'],
                        players=' vs '.join(game['players']),
                        winner=game['winner']
                    )
                print_special2(summary)
    except Exception as e:
        print_error("Could not report youtube summary")
        print_error(e)

def _get_since_when(since_today, since_last_n_days, since_time):
    if since_today == False and since_last_n_days == None and since_time == None:
        print_error("Atleast one since parameter needed")
        sys.exit(1)

    since_when = None
    if since_today:
        since_when = datetime.combine(date.today(), datetime.min.time())
    if since_last_n_days:
        since_when = datetime.combine(date.today() - timedelta(days=since_last_n_days), datetime.min.time())
    if since_time:
        since_when = since_time
    return since_when

@click.group()
@click.option('--config', required=True, type=click.Path(exists=True), default='config.yaml', help='Path to the config.yaml file containing configuration params for this utility')
@click.pass_context
def yrstats(ctx, config):
    ctx.obj['CONFIG'] = _read_config_yaml(ctx, config)

def extract_game_stats_params(func):
    @click.option('--stat-dmp-file', required=False, type=click.Path(exists=True), default='C:\\Program Files (x86)\\Origin Games\\Command and Conquer Red Alert II\\stats.dmp',
        help='Full path to RA2 Yuri\'s Revenge stat.dump file, e.g. C:\\Program Files (x86)\\Origin Games\\Command and Conquer Red Alert II\\stats.dmp')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@yrstats.command(short_help="Start the stat server to continuously monitor and parse stat.dmp and keep updating game-level, session-level as well as overall stats")
@extract_game_stats_params
@click.option('--start-web-server', is_flag=True)
@click.option('--open-browser', is_flag=True)
@click.option('--show-youtube-summary', is_flag=True)
@click.option('--publish-to-surge', is_flag=True)
@click.option('--write-xsplit-xml', is_flag=True)
@click.pass_context
def start_stat_watcher(ctx, stat_dmp_file, start_web_server, open_browser, show_youtube_summary, publish_to_surge, write_xsplit_xml):
    start_time = datetime.now()
    ctx.obj['num_games'] = 0
    dmp_file = stat_dmp_file if stat_dmp_file != None else config['statsDmpFilePath']
    ctx.obj['CONFIG']['write_xsplit_xml'] = write_xsplit_xml

    if write_xsplit_xml:
        reset_xsplit_xml(ctx.obj['CONFIG'])

    event_handler = StatsDmpWatcher(ctx.obj, ntpath.basename(dmp_file), start_time)

    dmp_file_base_dir = os.path.dirname(os.path.abspath(dmp_file))
    observer = watchdog.observers.Observer()
    print_info("Watching for changes to: " + dmp_file)
    observer.schedule(event_handler, path=dmp_file_base_dir, recursive=False)
    observer.start()

    if start_web_server:
        start_web_reporter(ctx.obj['CONFIG']['sessionStatsFolder'], start_time, open_browser = open_browser)

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    if ctx.obj['num_games'] > 0:
        if publish_to_surge:
            upload_to_surge(ctx.obj['CONFIG'], start_time, open_browser)

        if show_youtube_summary:
            report_youtube_summary(ctx.obj['CONFIG'], start_time)

@yrstats.command(short_help="Extract game stats for the last game from stats.dmp, save it in game stats folder and exit")
@extract_game_stats_params
@click.pass_context
def extract_game_stats(ctx, stat_dmp_file):
    config = ctx.obj['CONFIG']
    statparser.process_stats(stat_dmp_file, config["gameStatsFolder"], config['thisPlayerName'])

def base_update_stats_params(func):
    @click.option('--since-today', is_flag=True)
    @click.option('--since-last-n-days', type=click.INT)
    @click.option('--since-time', type=click.DateTime())
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@yrstats.command(short_help="Generate session stat data from the parsed games in the game stats folder")
@base_update_stats_params
@click.option('--show-youtube-summary', is_flag=True)
@click.pass_context
def update_session_stats(ctx, since_today, since_last_n_days, since_time, show_youtube_summary):
    since_when = _get_since_when(since_today, since_last_n_days, since_time)

    session_stats, processed_files, earliest_ts = aggregate_game_stats_multi(ctx.obj['CONFIG'], since_when)
    if processed_files:
        session_stats_json = get_session_stats_json_file(ctx.obj['CONFIG']['sessionStatsFolder'], since_when)
        session_stats_html = get_session_stats_html_file(ctx.obj['CONFIG']['sessionStatsFolder'], since_when)
        report_aggregated_stats(session_stats, session_stats_json, session_stats_html, since_when, ctx.obj['CONFIG']['htmlTemplateSessions'], ctx.obj['CONFIG']['htmlResourcesRelPathSessions'])

    if show_youtube_summary:
        report_youtube_summary(session_stats)

@yrstats.command(short_help="Generate overall stat data from the parsed games in the game stats folder")
@base_update_stats_params
@click.pass_context
def update_overall_stats(ctx, since_today, since_last_n_days, since_time):
    since_when = _get_since_when(since_today, since_last_n_days, since_time)

    overall_stats, processed_files, earliest_ts = aggregate_game_stats_multi(ctx.obj['CONFIG'], since_when)
    if processed_files:
        overall_stats_json = get_overall_stats_json_file(ctx.obj['CONFIG']['overallStatsFolder'])
        overall_stats_html = get_overall_stats_html_file(ctx.obj['CONFIG']['overallStatsFolder'])
        for game_history in overall_stats['game_history']:
            del game_history['relative_start_time']
        report_aggregated_stats(overall_stats, overall_stats_json, overall_stats_html, earliest_ts, ctx.obj['CONFIG']['htmlTemplateOverall'], ctx.obj['CONFIG']['htmlResourcesRelPathOverall'])

if __name__ == '__main__':
    colorama.init(autoreset=True)
    yrstats(obj={})