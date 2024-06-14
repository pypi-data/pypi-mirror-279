from __future__ import annotations
from flask import Flask, request
from sqlglot.optimizer.qualify_tables import qualify_tables
from sqlglot.optimizer.qualify_columns import quote_identifiers
from sqlglot import exp
import sqlglot
import logging
import json
import os
import sys
import configparser

app = Flask(__name__)
logger = logging.getLogger("sqlglot")
# Configure Logger
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

application_parent_path = os.path.dirname(application_path)
log_directory = os.path.join(application_parent_path, "log")
if not os.path.exists(log_directory):
    os.mkdir(log_directory)
log_file_path = os.path.join(log_directory, "audit.log")
logging.basicConfig(
    filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_extra_functions():
    config = configparser.ConfigParser()
    config_path = os.path.join(application_parent_path, "conf/udf_functions.conf")
    if not os.path.exists(config_path):
        print("The configuration file does not exist. Please create one. 'udf_functions.conf'.")
        logging.warning(f"Not find udf_functions.conf")
        return []
    config.read(config_path)
    extra_functions = config.get("Functions", "extra", fallback="")
    return [func.upper() for func in extra_functions.split(",")] if extra_functions else []


def transpile(sql_query, read, write, case_sensitive):
    global result, response_code
    # Check if the SQL contains DDL keywords
    ddl_keywords = ["CREATE", "ALTER", "DROP", "TRUNCATE", "COMMENT"]
    first_word = sql_query.strip().split()[0].upper()
    response_code = 0
    unknown_function = set()
    extra_functions = read_extra_functions()
    doris_functions_string = "ARRAY,ARRAY_MAX,ARRAY_MIN,ARRAY_MAP,ARRAY_FILTER,ARRAY_AVG,ARRAY_SUM,ARRAY_SIZE,ARRAY_REMOVE,ARRAY_SLICE,ARRAY_SORT,ARRAY_REVERSE_SORT,ARRAY_SORTBY,ARRAY_POSITION,ARRAY_CONTAINS,ARRAY_EXCEPT,ARRAY_PRODUCT,ARRAY_INTERSECT,ARRAY_RANGE,ARRAY_DISTINCT,ARRAY_DIFFERENCE,ARRAY_UNION,ARRAY_JOIN,ARRAY_WITH_CONSTANT,ARRAY_ENUMERATE,ARRAY_ENUMERATE_UNIQ,ARRAY_POPBACK,ARRAY_POPFRONT,ARRAY_PUSHFRONT,ARRAY_PUSHBACK,ARRAY_COMPACY,ARRAY_CONCAT,ARRAY_ZIP,ARRAY_SHUFFLE,ARRAY_CUM_SUM,ARRAY_EXISTS,ARRAY_FIRST_INDEX,ARRAY_LAST_INDEX,ARRAY_FIRST,ARRAY_LAST,ARRAYS_OVERLAP,ARRAY_COUNT,COUNTEQUAL,ELEMENT_AT,SEQUENCE,CONVERT_TZ,CURDATE,CURRENT_DATE,CURTIME,CURRENT_TIME,CURRENT_TIMESTAMP,LOCALTIME,LOCALTIMESTAMP,NOW,YEAR,QUARTER,MONTH,DAY,DAYOFYEAR,DAYOFMONTH,DAYOFWEEK,WEEK,WEEKDAY,WEEKOFYEAR,YEARWEEK,DAYNAME,MONTHNAME,HOUR,MINUTE,SECOND,FROM_DAYS,LAST_DAY,TO_MONDAY,FROM_SECOND,FROM_UNIXTIME,UNIX_TIMESTAMP,UTC_TIMESTAMP,TO_DATE,TO_DAYS,TIME_TO_SEC,SEC_TO_TIME,EXTRACT,MAKEDATE,STR_TO_DATE,TIME_ROUND,TIMEDIFF,TIMESTAMPADD,TIMESTAMPDIFF,DATE_ADD,DATE_SUB,DATE_TRUNC,DATE_FORMAT,DATEDIFF,MICROSECONDS_ADD,MICROSECONDS_DIFF,MICROSECONDS_SUB,MILLISECONDS_ADD,MILLISECONDS_DIFF,MILLISECONDS_SUB,MINUTES_ADD,MINUTES_DIFF,MINUTES_SUB,SECONDS_ADD,SECONDS_DIFF,SECONDS_SUB,HOURS_ADD,HOURS_DIFF,HOURS_SUB,DAYS_ADD,DAYS_DIFF,DAYS_SUB,WEEKS_ADD,WEEKS_DIFF,WEEKS_SUB,MONTHS_ADD,MONTHS_DIFF,MONTHS_SUB,YEARS_ADD,YEARS_DIFF,YEARS_SUB,ST_X,ST_Y,ST_CIRCLE,ST_DISTANCE_SPHERE,ST_ANGLE,ST_AZIMUTH,ST_ANGLE_SPHERE,ST_AREA,ST_POINT,ST_POLYGON,ST_POLYGONFROMTEXT,ST_ASTEXT,ST_ASWKT,ST_CONTAINS,ST_GEOMETRYFROMTEXT,ST_GEOMFROMTEXT,ST_LINEFROMTEXT,ST_LINESTRINGFROMTEXT,ST_ASBINARY,ST_GEOMETRYFROMWKB,ST_GEOMFROMWKB,TO_BASE64,FROM_BASE64,ASCII,LENGTH,BIT_LENGTH,CHAR_LENGTH,LPAD,RPAD,LOWER,LCASE,UPPER,UCASE,INITCAP,REPEAT,REVERSE,CHAR,CONCAT,CONCAT_WS,SUBSTRING,SUB_REPLACE,APPEND_TRAILING_CHAR_IF_ABSENT,ENDS_WITH,STARTS_WITH,TRIM,LTRIM,RTRIM,NULL_OR_EMPTY,NOT_NULL_OR_EMPTY,HEX,UNHEX,ELT,INSTR,LOCATE,FIELD,FIND_IN_SET,REPLACE,STRLEFT,STRRIGHT,SPLIT_PART,SPLIT_BY_STRING,SUBSTRING_INDEX,MONEY_FORMAT,PARSE_URL,url_decode,CONVERT_TO,EXTRACT_URL_PARAMETER,UUID,SPACE,SLEEP,ESQUERY,MULTI_SEARCH_ALL_POSITIONS,MULTI_MATCH_ANY,MASK,MASK_FIRST_N,MASK_LAST_N,LIKE,NOT LIKE,REGEXP,REGEXP_EXTRACT,REGEXP_EXTRACT_ALL,REGEXP_REPLACE,REGEXP_REPLACE_ONE,NOT REGEXP,STRUCT,NAMED_STRUCT,STRUCT_ELEMENT,STATE,MERGE,UNION,MIN,MIN_BY,MAX,MAX_BY,AVG,AVG_WEIGHTED,SUM,STDDEV,STDDEV_POP,STDDEV_SAMP,VARIANCE,VAR_POP,VARIANCE_POP,VAR_SAMP,VARIANCE_SAMP,COVAR,COVAR_SAMP,CORR,TOPN,TOPN_ARRAY,TOPN_WEIGHTED,COUNT,COUNT_BY_ENUM,APPROX_COUNT_DISTINCT,PERCENTILE,PERCENTILE_ARRAY,PERCENTILE_APPROX,HISTOGRAM,GROUP_BITMAP_XOR,GROUP_BIT_AND,GROUP_BIT_OR,GROUP_BIT_XOR,GROUP_CONCAT,BITMAP_UNION,HLL_UNION_AGG,GROUPING,GROUPING_ID,ANY_VALUE,ARRAY_AGG,MAP_AGG,BITMAP_AGG,COLLECT_SET,COLLECT_LIST,RETENTION,SEQUENCE_MATCH,SEQUENCE_COUNT,TO_BITMAP,BITMAP_HASH,BITMAP_FROM_STRING,BITMAP_TO_STRING,BITMAP_TO_ARRAY,BITMAP_FROM_ARRAY,BITMAP_EMPTY,BITMAP_OR,BITMAP_AND,BITMAP_UNION,BITMAP_XOR,BITMAP_NOT,BITMAP_AND_NOT,BITMAP_ANDNOT,BITMAP_SUBSET_LIMIT,BITMAP_SUBSET_IN_RANGE,SUB_BITMAP,BITMAP_COUNT,BITMAP_AND_COUNT,BITMAP_AND_NOT_COUNT,BITMAP_ANDNOT_COUNT,ORTHOGONAL_BITMAP_UNION_COUNT,BITMAP_XOR_COUNT,BITMAP_OR_COUNT,BITMAP_CONTAINS,BITMAP_HAS_ALL,BITMAP_HAS_ANY,BITMAP_MAX,BITMAP_MIN,INTERSECT_COUN,BITMAP_INTERSECT,ORTHOGONAL_BITMAP_INTERSECT,ORTHOGONAL_BITMAP_INTERSECT_COUNT,ORTHOGONAL_BITMAP_EXPR_CALCULATE,ORTHOGONAL_BITMAP_EXPR_CALCULATE_COUNT,BITMAP_HASH64,BITMAP_REMOVE,BITAND,BITOR,BITXOR,BITNOT,CASE,COALESCE,IF,IFNULL,NVL,NULLIF,JSON_PARSE,JSON_EXTRACT,JSON_EXISTS_PATH,JSON_TYPE,JSON_ARRAY,JSON_OBJECT,JSON_QUOTE,JSON_UNQUOTE,JSON_VALID,JSON_CONTAINS,JSON_LENGTH,GET_JSON_DOUBLE,GET_JSON_INT,GET_JSON_BIGINT,GET_JSON_STRING,JSON_INSERT,JSON_REPLACE,JSON_SET,MURMUR_HASH3_32,MURMUR_HASH3_64,XXHASH_32,XXHASH_64,HLL_CARDINALITY,HLL_EMPTY,HLL_HASH,CONV,BIN,SIN,COS,COSH,TAN,TANH,ASIN,ACOS,ATAN,ATAN2,E,PI,EXP,LOG,LOG2,LOG10,LN,CEIL,FLOOR,PMOD,ROUND,ROUND_BANKERS,TRUNCATE,ABS,SQRT,CBRT,POW,DEGREES,RADIANS,SIGN,POSITIVE,NEGATIVE,GREATEST,LEAST,RANDOM,MOD,RUNNING_DIFFERENCE,AES,MD5,MD5SUM,SM4,SM3,SM3SUM,SHA,SHA2,EXPLODE_JSON_ARRAY,EXPLODE,EXPLODE_SPLIT,EXPLODE_BITMAP,NUMBERS,EXPLODE_NUMBERS,Outer 组合器,S3,HDFS,local,ICEBERG_META,BACKENDS,FRONTENDS,WORKLOAD_GROUPS,CATALOGS,frontends_disks,ACTIVE_QUERIES,JOBS,MV_INFOS,TASKS,JOB,SUM,AVG,MAX,MIN,COUNT,RANK,DENSE_RANK,PERCENT_RANK,CUME_DIST,FIRST_VALUE,LAST_VALUE,LEAD,LAG,ROW_NUMBER,NTILE,WINDOW_FUNNEL,IPV4_NUM_TO_STRING,INET_NTOA,IPV4_STRING_TO_NUM,INET_ATON,IPV4_STRING_TO_NUM_OR_DEFAULT,IPV4_STRING_TO_NUM_OR_NULL,IPV6_NUM_TO_STRING,INET6_NTOA,IPV6_STRING_TO_NUM,INET6_ATON,IPV6_STRING_TO_NUM_OR_DEFAULT,IPV6_STRING_TO_NUM_OR_NULL,IS_IPV4_COMPAT,IS_IPV4_MAPPED,IPV4_CIDR_TO_RANGE,IPV6_CIDR_TO_RANGE,IS_IP_ADDRESS_IN_RANGE,IS_IPV4_STRING,IS_IPV6_STRING,TO_IPV4,TO_IPV4_OR_DEFAULT,TO_IPV4_OR_NULL,TO_IPV6,TO_IPV6_OR_DEFAULT,TO_IPV6_OR_NULL,cosine_distance,inner_product,l1_distance,l2_distance,CAST,DIGITAL_MASKING,WIDTH_BUCKET,SUBSTR,ISNULL"
    if extra_functions:
        doris_functions_string += "," + ",".join(extra_functions)
    doris_functions = set(doris_functions_string.split(","))
    if first_word in ddl_keywords:
        response_code = 1
        result = "DDL transformation is not supported. Only DML transformation is supported."
    else:
        try:
            result, unknown_function = transpile_text(
                sql_query, doris_functions, read=read, write=write, case_sensitive=case_sensitive
            )
        except Exception as e:
            response_code = 1
            result = f"Error transpiling query: {str(e).replace('sqlglot.', 'DorisSQLConvertor.')}"
    return result, unknown_function


def transpile_text(sql_query, doris_functions, read, write, case_sensitive):
    ast = sqlglot.parse_one(read=read, sql=sql_query)
    unknown_functions = set()
    # identify unknown functions
    for unknown in ast.find_all(exp.Anonymous):
        unknown_functions.add(unknown.name.upper())
        unknown_functions = unknown_functions - doris_functions
    case = None if case_sensitive == "0" else True if case_sensitive == "1" else False
    ast_1 = quote_identifiers(ast, dialect="doris", identify=True)
    result = qualify_tables(ast_1, case_sensitive=case).sql(write)
    return result, unknown_functions


@app.post("/api/v1/convert")
def convert():
    data = request.data
    j_data = json.loads(data)
    version = j_data["version"]
    audit = j_data["sql_query"]
    transformedSQL, unknown_function = transpile(
        j_data["sql_query"], j_data["from"], j_data["to"], j_data["case_sensitive"]
    )
    unknown_function_tag = 0
    # Record SQL statements to log file
    if response_code == 1:
        logging.error(
            f'Received SQL query: {audit},Version: {version},From {j_data["from"]},To {j_data["to"]}'
        )
    elif unknown_function:
        logging.warning(
            f"Unknown_function: {unknown_function}, Received SQL query: {audit},Version: {version},From {j_data['from']},To {j_data['to']}"
        )
        unknown_function_tag = 1
    else:
        logging.info(
            f"Received SQL query: {audit},Version: {version},From {j_data['from']},To {j_data['to']}"
        )

    if response_code == 0 and unknown_function_tag == 0:
        message_info = "success"
    elif unknown_function_tag == 1:
        message_info = "Unknown_function"
    else:
        message_info = "Error transpiling query"

    response = {
        "version": version,
        "data": transformedSQL,
        "code": 0 if response_code == 0 and unknown_function_tag == 0 else 1,
        "message": message_info,
    }

    return json.dumps(response)
