import logging
import os

# v1.0 呼叫 log = yoyologging.getInstance() 可建立支援顏色的 logging 物件實體
# v1.1 初步支援 IS_CREATED_FILE，產出日誌檔案，可設定其檔名、位址、格式
# v2.0 yoyologging 物件化，LoggingConfig 別亂動
# v2.1 創立 DefaultLogger(object)，由他來建立所有 Logger 會使用到的通用函式庫
# v2.2 創立 AcuLogger(DefaultLogger)，由他來建立 ACU 專案上，會用到的客製化函式庫


class LoggingConfig(object):
    # 設定可觀看的日誌等級
    # 可用層級：DEBUG INFO WARNING ERROR CRITICAL
    # 只有DEBUG模式才會顯示行號
    LOG_LEVEL = logging.DEBUG

    # 設定輸出格式，只有DEBUG模式才會顯示行號
    if LOG_LEVEL == logging.DEBUG:
        FORMAT = "[%(asctime)s]" \
                 "%(levelname)-10s " \
                 "$BOLD%(message)s$RESET " \
                 "($BOLD%(filename)s$RESET:" \
                 "%(lineno)d)"
    else:
        FORMAT = "[%(asctime)s]" \
                 "%(levelname)-10s " \
                 "$BOLD%(message)s$RESET "

    # 設定日期時間的風格
    DATE_FMT = "%y/%m/%d %H:%M:%S"

    # 設定色碼從30開始遞增的顏色順序如此
    BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE = range(8)

    # 設定 LOG 各的層級顏色
    LEVEL_COLORS = {
        'CRITICAL': RED,
        'ERROR': RED,
        'WARNING': YELLOW,
        'INFO': GREEN,
        'DEBUG': PURPLE
    }

    # 設定色碼代號(粗體明亮，色碼歸零，色碼)
    BOLD_SEQ = "\033[1m"
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[%dm"

    # 設定是否要產出日誌檔案？在指定路徑下？
    # 日誌檔案並不會上色
    IS_CREATED_FILE = False
    FILE_RELDIR = "./"
    FILE_BASENAME = "yoyologgingFile.txt"
    FILE_RELPATHNAME = "%s%s" % (FILE_RELDIR, FILE_BASENAME)
    FILE_FORMAT = "[%(asctime)s]" \
                  "%(levelname)-4s " \
                  "%(message)s "


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg, datefmt=LoggingConfig.DATE_FMT)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in LoggingConfig.LEVEL_COLORS:
            levelname_color = LoggingConfig.COLOR_SEQ % (30 + LoggingConfig.LEVEL_COLORS[levelname]) + levelname
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class ColoredLogger(logging.Logger):
    COLOR_FORMAT = LoggingConfig.FORMAT.replace(
        "$RESET", LoggingConfig.RESET_SEQ).replace("$BOLD", LoggingConfig.BOLD_SEQ)

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)
        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        if LoggingConfig.IS_CREATED_FILE:
            non_color_formatter = ColoredFormatter(LoggingConfig.FILE_FORMAT, use_color=False)
            fh = logging.FileHandler(LoggingConfig.FILE_RELPATHNAME)
            fh.setFormatter(non_color_formatter)
            self.addHandler(fh)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)


logging.setLoggerClass(ColoredLogger)


class DefaultLogger(LoggingConfig):
    """ 一個預設的紀錄器，可以依靠 get_instance(self): 來產出 logging 的物件
        使得可以呼叫 logging.Logger.info("信息")、logging.Logger.debug("除錯信息")
        並且提供各式 Diag 專案上會碰到的通用日誌函式庫工具
    """
    def __init__(self):
        self.set_is_created_file(False)
        self.set_file_reldir("./")
        self.set_file_basename("defaultLog.txt")

    def set_file_reldir(self, file_relpath):
        """ 設定產出檔案的相對目錄

        :param file_relpath: 產出檔案的相對目錄
        :return: void
        """
        if not os.path.isdir(file_relpath):
            os.mkdir(file_relpath)
        LoggingConfig.FILE_RELDIR = file_relpath
        LoggingConfig.FILE_RELPATHNAME = "%s%s" % (LoggingConfig.FILE_RELDIR, LoggingConfig.FILE_BASENAME)

    def set_file_basename(self, file_basename):
        """ 設定產出檔案的本檔名

        :param file_basename: 產出檔案的本檔名
        :return: void
        """
        LoggingConfig.FILE_BASENAME = file_basename
        LoggingConfig.FILE_RELPATHNAME = "%s%s" % (LoggingConfig.FILE_RELDIR, LoggingConfig.FILE_BASENAME)

    def set_is_created_file(self, is_created_file):
        """ 設定是否要產出 log 檔？

        :param is_created_file: True or False
        :return: void
        """
        LoggingConfig.IS_CREATED_FILE = is_created_file

    def set_log_level(self, log_level):
        """ 設定日誌層級，可使得 log 僅顯示該層級以上的信息
            DEBUG < INFO < WARN < ERROR < FATAL

        :param log_level: 日誌層級，分為 logging.DEBUG logging.INFO 等等
        :return: void
        """
        LoggingConfig.LOG_LEVEL = log_level

    def get_file_reldir(self):
        """

        :return: 回傳建立的日誌檔(如果有必要的話)的相對目錄名
        """
        return LoggingConfig.FILE_RELDIR

    def get_file_basename(self):
        """

        :return: 回傳建立的日誌檔(如果有必要的話)的檔名
        """
        return LoggingConfig.FILE_BASENAME

    def get_instance(self):
        """ 取得 log 物件實體，取得後就可以 item_log.info("日誌訊息")

        :return: log 物件實體
        """
        item_log = logging.getLogger("DefaultLogger")
        item_log.setLevel(LoggingConfig.LOG_LEVEL)
        return


class AcuLogger(DefaultLogger):
    def __init__(self):
        DefaultLogger.__init__(self)
        self.set_is_created_file(True)
        self.set_file_reldir("./ACU_log/")
        self.set_file_basename("ACU_log001.txt")
        self.set_log_level(logging.DEBUG)

    def set_file_reldir(self, file_relpath):
        DefaultLogger.set_file_reldir(self, file_relpath)

    def set_file_basename(self, file_basename):
        DefaultLogger.set_file_basename(self, file_basename)

    def set_is_created_file(self, is_created_file):
        DefaultLogger.set_is_created_file(self, is_created_file)

    def set_log_level(self, log_level):
        DefaultLogger.set_log_level(self, log_level)

    def get_file_reldir(self):
        return DefaultLogger.get_file_reldir(self)

    def get_file_basename(self):
        return DefaultLogger.get_file_basename(self)

    def get_instance(self):
        item_log = logging.getLogger("AcuLogger")
        item_log.setLevel(LoggingConfig.LOG_LEVEL)
        return item_log


