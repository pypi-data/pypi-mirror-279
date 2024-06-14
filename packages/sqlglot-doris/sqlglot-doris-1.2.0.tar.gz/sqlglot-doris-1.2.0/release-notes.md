Changelog
=========
## [v1.0.5] - 2024-06-14
#### Summarize:
##### Presto/Trino Improvements
- Added Function Translations: Added conversion support for URL series functions (#28), support for transforming json_value, bitwise_and_agg, bitwise_or_agg, repeat functions (#30), as well as configuration support for UDF function lists (#36), and introduced bit_count function support (#34).
- Conversion Fixes: Fixed transformation for regexp_extract function (#29), improved HTTP response messages (#31), corrected format issues with date_parse and fixes for the split_part function converter (#32), enhanced Trino's day_of_week and replace function transformations (#37, #38), addressed the absence of the named_selects attribute in explain's expression issue (#35).
- Date Format and Function Fix: Repaired date formats (#34).
##### ClickHouse Improvements
- Function Transformation Additions and Corrections:
  - Added transformation for arrayShuffle, ArrayMin and ArrayMax, and fixes to ArrayConcat conversion (#3).
  - Introduced support for arrayjoin function (#5), transformations for neighbor function and fixes for var_len_args in arrayZip (#6).
  - Introduced sumForeach, accurateCastOrDefault, retention function transformations, along with various other ClickHouse function conversions (#16, #17, #18, #20).
  - Added IP series function conversion (#8).
- Date Function Fix: Fixed Date_add and DateAdd transformations (#4), enhanced conversion for toStartOfInterval function (#9).
- Column Reference Fix: Addressed pre and post column reference issues in ClickHouse (#7).
- Performance Fix: Improved performance degradation after converting if to case when (#22).
##### DDL Improvements
- Constraints and Partitioning Support: Fixed extra whitespace bugs after merging upstream commits and missing autoincrement column constraints issue (#21), added orderBy and partitionBy conversion for ClickHouse (#23).
- HIVE and Other Partitioning Type Support: Added support for HIVE list partitioning types, as well as Presto, PostgreSQL, Spark, and others (#26).
- Primary Key Partitioned Table Conversion: Added conversion support for PostgreSQL primary key partitioned tables (#33).

## [v1.0.3] - 2024-04-12
#### Summarize:
  1. Supports the conversion of DDL statements. Supported dialects include hive, presto, clickhouse, pracle, and postgres.
  2. Optimized the prompts for unconverted functions in online services
  3. For the compatibility of clickhouse’s various type conversion functions, the bitmap-related functions have been fully covered, and some array functions, map functions, ip functions, and conversion processing of numbers table functions have been added.
  4. For the processing of Oracle system tables, the problem caused by the case sensitivity of the date format has been repaired, and the conversion of listagg functions has been supplemented.
  5. Supplemented the JsonAgg conversion of postgres and the conversion of special type fixeddecimal, and fixed the problem of different case of return results caused by the difference of to_hex function.
### :sparkles: New Features and :bug: Bug Fixes
#### Postgres
  1. add JSONAgg function convertor
  2. add fixeddecimal type parse
  3. Fix to_hex function convertor
#### Clickhouse
  1. support numbers table function convertor
  2. add toint8、toint16 and toint32 function transform
  3. add toDecimal32\64,toDecimal32\64OrNull,toDecimal32\64OrZero
  4. add toDate\toDate32\toDateime64
  5. add bitcount function convertor
  6. add bitmapSubsetInRange function convertor
  7. add bitmapSubsetLimit function convertor
  8. add subBitmap function convertor
  9. add bitmapMax and bitmapMin function convertor
  10. add arrayEnumerateUniq function convertor
  11. add IPv4NumToString(),IPv4StringToNum() ,IPv6StringToNum() ,IPv6StringToNum(),toIPv4(),toIPv6() to  IPv4NumToString(),IPv4StringToNum() ,IPv6StringToNum() ,IPv6StringToNum(),toIPv4(),toIPv6()
  12. fix arrayCompact function convertor
  13. add mapContains to MAP_CONTAINS_KEY
  14. add mapKeys to MAP_KEYS
  15. add mapValues to MAP_VALUES
  16. add arrayCount and hasany function convertor
  17. add arrayReverse and Reverse function convertor
  18. add subtractdays|weeks|hours|minutes
  19. fix length|char_length
  20. add JSONHas to JSON_CONTAINS
#### Oracle
  1. dd listagg function transfrom
  2. Remove oracle's dual system table
  3. Fix oracle date format size insensitivity
#### DDL
  1. Support convertor of ddl statements of hive、presto、clickhouse、oracle、and postgres

## [v1.0.2] - 2024-03-29
#### Summarize:
The compatibility for ClickHouse has been greatly improved. It provides good compatibility conversion for the to_char function of Oracle and Postgres. It has made many differentiated adaptations for date format conversion in all dialects. At the same time, it can be regarded as Backticks are automatically added to keyword fields, which greatly improves the compatibility of the converted SQL to be executed directly in doris.
### :sparkles: New Features and :bug: Bug Fixes
#### Presto/Trino
  1. fix JSON function transform
  2. fix array_range and regexp_extract function
#### Clickhouse
  1. fix clickhouse's trim function transform
  2. add generateUUIDv4 function transform
  3. add mutiif function transform
  4. add final clause generator
  5. add countdistinct function transform
  6. fix date_sub function transform eg.  date_sub(toDate('2018-01-01'), interval 1 month)
  7. add TOINT64 and TOINT64ORZEROfunction transform
  8. add modulo function transform
  9. add minif function transform
  10. Fix doris does not support global in
  11. fix positionCaseInsensitiveUTF8 and positionCaseInsensitive function transform
  12. add intDiv function transfrom
  13. fix arrayElement and indexof  transform
  14. add ARRAYENUMERATE -> ARRAY_ENUMERATE,IsNotNull -> NOT_NULL_OR_EMPTY
  15. add formatDateTime -> DATE_FORMA
  16. add flatten conversion to doris
  17. add toStartOfInterval conversion to doris
  18. add the implementation of toFloat32
#### Postgres
  1. fix to_char function transform
  2. fix identifiers parse
#### Oracle
  1. add oracle's trim function transform
  2. fix to_char and to_date functions transform
#### Hive
  1. add bigint function transform
#### Spark
  1. Add spark3 dialect support
  2. Add quote_identifier to doris keywords


## [v1.0.1] - 2024-02-18
### :sparkles: New Features
- [`4a8eb691`](https://github.com/selectdb/sqlglot/commit/4a8eb691961e624a7b5d569b2bd8a67386235788) - support explain verbose,explain memo plan,explain physical plan,explain shape plan
  - Automatic conversion of explain statements is supported, including
    - explain
    - explain verbose
    - explain mem plan
    - explain physical plan
    - explain shape plan
- [`10b4e690`](https://github.com/selectdb/sqlglot/commit/10b4e6900913ec4b08b80ebbd254a4b054cb4976) - support match_any/match_all parse
### :bug: Bug Fixes
- Fixed format conversion conflicts in the date function
- Improved the json type function path parsing and conversion function
- Repaired several conversion error cases in actual scenarios, optimized the analytic generation of multiple cases, and improved the compatibility to a greater extent
