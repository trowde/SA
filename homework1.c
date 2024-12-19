#include <stdio.h>
#include<string.h>
#include <stdlib.h>
#include <ctype.h>

/**********
 * マクロ *
 **********/
#define MAX_EMPLOYEE (8) /* 最大従業員数 */
#define DAYS_IN_MONTH (31) /* １ヶ月の最大の日数 */
#define CUT_OFF_DATE (15) /* 給与締め日 */
#define PAYMENT_DATE (25) /* 給与支払い日 */
#define INVALID (-1) /* 時刻データ無効 */
#define MANAGER (0) /* 管理者 */
#define MAX_STRING (32)
#define PAYMENT_BY_HOUR (1000) /* 時給 */
#define PAY_SLIP_FILE "payslip_"
#define MAX_LINE (256)

/* コマンド */
#define START_TIME (1) /* 始業時刻の登録 */
#define END_TIME (2) /* 退社時刻の登録 */
#define EMPLOYEE (3) /* 従業員ごとの作業時間 */
#define DATE (4) /* 日付ごとの作業時間 */

/* 就業状態 */
#define  ENGAGING 'e' /* 就業中 */
#define  NON_ENGAGING 'n' /* 退社済 */
#define  VACANT '\0' /* 非雇用(この番号の従業員は雇用していない) */

/********************
 * プロトタイプ宣言 *
 ********************/
int get_command(void);
int get_today(const char*);
int get_time(void);
int get_employee(char[MAX_EMPLOYEE]);
int record_start(int, int[MAX_EMPLOYEE], int[MAX_EMPLOYEE]);
int record_end(int, int[MAX_EMPLOYEE], int[MAX_EMPLOYEE]);
int initialize_timeData(double[DAYS_IN_MONTH]);
int load_timeData(double[MAX_EMPLOYEE][DAYS_IN_MONTH],char[MAX_EMPLOYEE]);
int save_timeData(double[MAX_EMPLOYEE][DAYS_IN_MONTH], char[MAX_EMPLOYEE]);
double calculate_workingTime(int, int, int, int);
int sumUp_employeeWorking(double[MAX_EMPLOYEE][DAYS_IN_MONTH]);
int sumUp_dateWorking(double[MAX_EMPLOYEE][DAYS_IN_MONTH]);
int create_paySlip(int, double[MAX_EMPLOYEE][DAYS_IN_MONTH]);
int is_firstDayAfterCutoff(int);
int is_firstDayAfterPayment(int);
int count_engaging(char[MAX_EMPLOYEE]);

/********
 * 関数 *
 ********/
int
main(int argc,char const*argv[])
{
  int date; /* 今日の日付(yyyymmddのddのみ) */
  int employee; /* 従業員番号 */
  int start_hour[MAX_EMPLOYEE]; /* 出社の時間 */
  int start_minute[MAX_EMPLOYEE]; /* 出社の分 */
  int end_hour[MAX_EMPLOYEE]; /* 退社の時間 */
  int end_minute[MAX_EMPLOYEE]; /* 退社の分 */
  int command; /* タイムレコーダへのコマンド */

  /* この部分は終了時にファイルに保存 */
  int paySlip; /* 給与明細を作成したことをしめすフラグ(作成していれば1) */
  double working[MAX_EMPLOYEE][DAYS_IN_MONTH] = {{0.0}}; /* 作業時間
							    すべて0.0で初期化 */
  char engagement[MAX_EMPLOYEE]; /* 各従業員が就業中かの就業状態 */


  /* 前日までのデータをファイルからロード */
  load_timeData(working, engagement);
  paySlip = 0; /* 初期化 */
  
  date = get_today(argv[1]);  /* 今日の日付を取得する. */

  /* 給与明細の作成制御 */
  /* 　給与締め日以降の最初の出勤日に給与明細を作成 */
  /* 　給与支払い日以降の最初の出勤日に，給与締め日になれば次月の給与明細を作成すべきことを示す */
  if(is_firstDayAfterCutoff(date) && (! paySlip)) { /* 給与締め日以降の最初の出勤日か */
    for(employee = 0; employee < MAX_EMPLOYEE; employee++) { /* 全員分の給与明細作成 */
      if(engagement[employee] == VACANT)
	continue;
      if(create_paySlip(employee, working) == INVALID)
	return INVALID;
      else {
	/* 給与計算した従業員の作業データを初期化 */
	initialize_timeData(working[employee]);
	start_hour[employee] = INVALID; /* 無効に設定 */ 
	start_minute[employee] = INVALID; /* 無効に設定 */ 
	end_hour[employee] = INVALID; /* 無効に設定 */ 
	end_minute[employee] = INVALID; /* 無効に設定 */ 
      }
      paySlip = 1; /* 給与明細を作ったことを示す */
    }
  } else if(is_firstDayAfterPayment(date)) /* 給与支払い日以降の最初の出勤日か */
    paySlip = 0; /* 次の月の給与明細を未作成であることを示す */
  
  do {
    printf("** タイムレコーダ ** \n ");
    if((employee = get_employee(engagement)) == INVALID) /* 従業員番号 */
      continue;
    
    switch(command = get_command()) {  /* コマンドの取得 */
    case START_TIME:
      if(engagement[employee] != NON_ENGAGING) {
	printf("従業員%dはすでに就業しています\n", employee);
	continue;
      } else 
	engagement[employee] = record_start(employee, start_hour, start_minute);
      break;
    case END_TIME:
      if(engagement[employee] != ENGAGING) {
	printf("従業員%dはすでに退社しています\n", employee);
	continue;
      } else {
	engagement[employee] = record_end(employee, end_hour, end_minute);
	/* 作業時間を時間単位で計算 */
	working[employee][date] = calculate_workingTime(start_hour[employee], start_minute[employee],
							end_hour[employee], end_minute[employee]);
      }
      break;
    case EMPLOYEE:
    case DATE:
      if(employee != MANAGER) {
	printf("この機能は管理者だけが使えます\n");
      } else {
	if(engagement[MANAGER] != ENGAGING) {
	  printf("従業員%dは出勤時刻を登録してください\n", MANAGER);
	  engagement[employee] = record_start(employee, start_hour, start_minute);
	}
	if(command == EMPLOYEE)
	  sumUp_employeeWorking(working); /* 従業員ごとの作業時間表示 */
	else
	  sumUp_dateWorking(working); /* 日ごとの作業時間表示 */
      }
      break;
    default:
      printf("正しい操作を指定してください\n");
      break;
    }
  } while( count_engaging(engagement) > 0 ); /* 従業員が全員退社すればループを抜ける */

  save_timeData(working, engagement);
  
  return 0;
}

/****************
 * コマンド取得 *
 ****************/
int
get_command(void)
{
  int command;
  char line[MAX_LINE];
  
  printf("コマンド[");
  printf("%d(出勤) ", START_TIME);
  printf("%d(退社) ", END_TIME);
  printf("%d(従業員毎就業時間) ", EMPLOYEE);
  printf("%d(日毎就業時間)] ", DATE);

  fgets(line, MAX_LINE - 1, stdin);
  command = atoi(line);

  return command;
}

/********************
 * 就業中の従業員数 *
 ********************/
int
count_engaging(char engagement[MAX_EMPLOYEE])
{
  int i;
  int number = 0; /* 就業中の従業員数 */

  for(i = 0; i < MAX_EMPLOYEE; i++) {
    if(engagement[i] == ENGAGING)
      number++;
  }
  return number;
}

/**************************
 * その日の労働時間を計算 *
 **************************/
double
calculate_workingTime(int start_hour, int start_minute, int end_hour, int end_minute)
{
  double hour;
  int minute;

  minute = (end_hour - start_hour) * 60;  /* 分単位に変換 */
  minute = minute + (end_minute - start_minute);

  hour = minute / 60.0; /* 時間単位に変換 */

  return hour;
}

/******************************
 * 従業員ごとの労働時間を計算 *
 ******************************/
int
sumUp_employeeWorking(double working[MAX_EMPLOYEE][DAYS_IN_MONTH])
{
  int employee;
  int date;
  double time;
  double *element; /* 配列workingの要素へのポインタ */

  printf("従業員\t勤務時間合計\n");
  for(employee = 0; employee < MAX_EMPLOYEE; employee++) {
    element = working[employee];
    time = 0.0;
    for(date = 0; date < DAYS_IN_MONTH; date++)
      time += *element++;
    printf("%4d\t%10f\n", employee, time);
  }
  puts("");
  return 0;
}

/******************************
 * 日ごとの労働時間を計算 *
 ******************************/
int
sumUp_dateWorking(double working[MAX_EMPLOYEE][DAYS_IN_MONTH])
{
  int employee;
  int date;
  double time;
  double *element; /* 配列workingの要素へのポインタ */

  printf("日付\t勤務時間合計\n");
  for(date = 0; date < DAYS_IN_MONTH; date++) {
    element = (double *)working + date;
    time = 0.0;
    for(employee = 0; employee < MAX_EMPLOYEE; employee++) {
      time += *element;
      element += DAYS_IN_MONTH;
    }
    printf("%4d\t%10f\n", date+1, time);
  }
  puts("");
  return 0;
}

/*****************************************
 * 従業員の給与明細を計算・CSV形式で作成 *
 *****************************************/
int create_paySlip(int employee, double working[MAX_EMPLOYEE][DAYS_IN_MONTH])
{
  /* 今は何もしない */

  return 0;
}



/******************
 * 従業員番号取得 *
 ******************/
int get_employee(char engagement[MAX_EMPLOYEE])
{
  int employee;
  char line[MAX_LINE];

  do {
    printf("従業員番号: ");

    fgets(line, MAX_LINE - 1, stdin);
    employee = atoi(line);

    if((employee < 0) || (employee>= MAX_EMPLOYEE)) {
      printf("正しい従業員番号を指定してください\n");
      continue;
    } else if(engagement[employee] == VACANT) {
      printf("従業員%dは雇用されていません\n", employee);
      return INVALID;
    } else
      return employee;  
  } while(1);
}


/****************************
 * 日付取得(1日ならdateは0) *
 ****************************/
int
get_today(const char* today)
{
  int full; /* 年月日(yyyymmdd) */
  int date; /* 日のみ */
  int month; /* 月のみ */


    full = atoi(today); /* 整数に変換 */
    date = full % 100;
    month = (full / 100) % 100;

     return date - 1; /* 1日なら0 */
}


/************
 * 時刻取得 *
 ************/
int get_time()
{
  char string[MAX_STRING];
  int time; /* hhmm形式の時刻(24時間60分表記) */
  int hour;
  int minute;
  int length;

  do {
    printf("(hhmm): ");
    fgets(string, MAX_STRING-1, stdin);
    if((length = strlen(string)) != strlen("hhmm")) { /* 長さ比較 */
      printf("正しい時間を指定してください\n");
      continue;
    }

    time = atoi(string); /* 整数に変換 */
    hour = time /100; /* 時間パート抽出 */
    minute = time % 100; /* 分パート抽出 */

    if((hour < 0) || (hour> 23)) {
      printf("正しい時間を指定してください\n");
    } else if((minute < 0) || (minute> 59)) {
      printf("正しい分を指定してください\n");
    } else
      return time;
  } while(1);
}
  
  
  
  
/****************
 * 出勤時刻取得 *
 ****************/
int
record_start(int employee,
	     int start_hour[MAX_EMPLOYEE],
	     int start_minute[MAX_EMPLOYEE])
{
  int time;

  printf("出勤時刻");
  time = get_time();
  start_hour[employee] = time / 100;
  start_minute[employee] = time % 100;

  puts("");

  return ENGAGING; /* 就業中へ */
}

/****************
 * 退社時刻取得 *
 ****************/
int
record_end(int employee,
	   int end_hour[MAX_EMPLOYEE],
	   int end_minute[MAX_EMPLOYEE])
{
  int time;

  printf("退社時刻");
  time = get_time();
  end_hour[employee] = time / 100;
  end_minute[employee] = time % 100;
  puts("");

  return NON_ENGAGING; /* 非就業へ */
}

/****************************
 * 締め日後の最初の出勤日か *
 ****************************/
int
is_firstDayAfterCutoff(int date)
{
  if(date+1 > CUT_OFF_DATE)
    return 1;
  else
    return 0;
}

/****************************
 * 給料日後の最初の出勤日か *
 ****************************/
int
is_firstDayAfterPayment(int date)
{
  if(date+1 > PAYMENT_DATE)
    return 1;
  else
    return 0;
}

/************************************
 * 任意の従業員の時間データの初期化 *
 ************************************/
/* 雇用していない従業員については初期化しない */
int
initialize_timeData(double working[DAYS_IN_MONTH])
{
  int date;

  for(date = 0; date < DAYS_IN_MONTH; date++) {
    working[date] = 0.0;
  }

  return 0;
}

/**********************
 * 時間データのロード *
 **********************/
int
load_timeData(double working[MAX_EMPLOYEE][DAYS_IN_MONTH],
	      char engagement[MAX_EMPLOYEE])
{
  int employee;
  int date;

  /* メモリをクリア */
  for(employee = 0; employee < MAX_EMPLOYEE; employee++) {
    for(date = 0; date < DAYS_IN_MONTH; date++) {
      working[employee][date] = 0.0;
    }
    engagement[employee] = VACANT;
  }
  
  /* 従業員0(管理者)は 1日（配列上は0）に */
  working[0][0] = 11.5; /* これだけ働いた */
  engagement[0] = NON_ENGAGING;

  /* 従業員1は1日（配列上は0）に */
  working[1][0] = 8.5; /* これだけ働いた */
  engagement[1] = NON_ENGAGING;
  
  /* 従業員2は1日（配列上は0）に */
  working[2][0] = 8.5; /* これだけ働いた */
  engagement[2] = NON_ENGAGING;
  
  /* 従業員3は1日（配列上は0）に */
  working[3][0] = 10.2; /* これだけ働いた */
  engagement[3] = NON_ENGAGING;

  return 0;
}

/**********************
 * 時間データのセーブ *
 **********************/
int
save_timeData(double working[MAX_EMPLOYEE][DAYS_IN_MONTH],
	      char engagement[MAX_EMPLOYEE])
{
  /* 現時点では，何もしない */
  return 0;
}