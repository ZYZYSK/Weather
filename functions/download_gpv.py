from .download_gpvclass import *

if __name__ == "__main__":
    print("please execute main.py")
    sys.exit()


def download_gpv():
    print("#####GPV Downloader#####")
    # SIGINTシグナルを受け取る
    signal.signal(signal.SIGINT, handler_sigint)
    # 設定ファイルの読み込み
    with open("settings_gpv.json") as fp:
        settings = json.load(fp)
    # ディレクトリが存在しなければ作成
    try:
        for dirs in settings["path"].values():
            os.makedirs(dirs, exist_ok=True)
    except FileNotFoundError:
        exit_program(f'{settings["path"]}は存在しないパスです.')
    # ダウンロード開始時刻の設定
    try:
        time_start = datetime.datetime(settings["time_start"]["year"], settings["time_start"]["month"], settings["time_start"]["day"], 0, 0)
    except Exception as e:
        exit_program(e, sys.exc_info())
    print(f'ダウンロード開始日時(UTC): {time_start}')
    # ダウンロード終了時刻は一日前
    time_end = datetime.date.today() - datetime.timedelta(days=1)
    # ダウンロードと天気図作成
    while time_start.date() < time_end:
        try:
            t = DownloadGPV(time_start, settings["fig_x"], settings["fig_y"], settings["path"]["tmp"])
            t.download_grib2()
            t.j_300_hw(settings["path"]["j300hw"])
            t.j_500_ht(settings["path"]["j500ht"])
            t.j_500_hv(settings["path"]["j500hv"])
            t.j_500_t_700_dewp(settings["path"]["j500t700td"])
            t.j_850_ht(settings["path"]["j850ht"])
            t.j_850_tw_700_vv(settings["path"]["j850tw700vv"])
            t.j_850_eptw(settings["path"]["j850eptw"])
        except Exception as e:
            exit_program(e, sys.exc_info())
        time_start += datetime.timedelta(hours=6)
    # grib2ファイルの削除
    if(settings["delete_tmp"]):
        shutil.rmtree(settings["path"]["tmp"])
    # 設定の更新
    update_settings(settings, time_start)


def update_settings(settings, time_start):
    # 設定の更新
    settings["time_start"]["year"] = time_start.year
    settings["time_start"]["month"] = time_start.month
    settings["time_start"]["day"] = time_start.day
    with open("settings_gpv.json", "w") as fp:
        json.dump(settings, fp)
    print("#####完了#####")