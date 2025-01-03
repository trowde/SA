
# include <unistd.h>

# define BIG_LOSS (3)
#include <stdio.h>
#include <stdlib.h>
#include <eggx.h>

/************
 *  macros  *
 ************/
#define ELEMENT_SIZE (100)
#define NUM_OF_ELEMENTS (8)
#define FIELD_SIZE (ELEMENT_SIZE * NUM_OF_ELEMENTS)
#define MESSAGE_SIZE (50) /* 盤面のメッセージ領域の高さ(pixel) */
#define MAX_MESSAGE (64) /* 盤面のメッセージ領域のメッセージ最大文字数 */
#define ROTATE_DIRECTION (1) /* 右回り */
#define MAX_BUF (256)

/* 色 */
#define BLACK (0)
#define WHITE (1)
#define GREEN (3)

/* 要素の状態 */
#define VACANT (0x00) /* 空き要素 */
#define WHITE_STONE (0x01) /* 白石が置かれた要素 */
#define BLACK_STONE (0x02) /* 黒石が置かれた要素 */
#define STONE_BITS (0x03) /* 石の色を示すビット */
#define BOUNDARY_BIT (0x04) /* 境界空白を示すビット */
#define STONE_INVERSION (STONE_BITS) /* XORで石の色を逆転させる */
#define NUM_OF_DIRECTIONS (8)
#define MAX_MARGINE (NUM_OF_ELEMENTS * NUM_OF_ELEMENTS)



/***************************
 *  prototype declaration  *
 ***************************/
int count_whiteStones(int [NUM_OF_ELEMENTS][NUM_OF_ELEMENTS]);
int display_situation(int, int, int);
int isBoundary(int);
int lookAround_directions(int, int [NUM_OF_ELEMENTS][NUM_OF_ELEMENTS], int, int, int);
int canTurnOver(int, int [NUM_OF_ELEMENTS][NUM_OF_ELEMENTS], int, int, int, int);
int *get_adjacent(int [NUM_OF_ELEMENTS][NUM_OF_ELEMENTS], int, int, int);
int place_stone(int, int [NUM_OF_ELEMENTS][NUM_OF_ELEMENTS], int, int, int);
int paint_element(int, int, int, int);
int display_message(int, char *);


/***************
 *  functions  *
 ***************/
int main(void)
{
    int mesh[NUM_OF_ELEMENTS][NUM_OF_ELEMENTS]; /* 盤面のメッシュ */
    int win; /* 描画用のWindow */
    int row, column, position;
    int stone;
    int availables; /* 空いているマスの数 */
    int white_stones; /* 白石の数 */
    int black_stones; /* 黒石の数 */
    char buf[MAX_BUF];

    win = gopen(FIELD_SIZE,FIELD_SIZE + MESSAGE_SIZE); /* メッセージ文だけフィールドを増やす */
    layer(win, 0,1); /* 表示用レイヤを0に，書き込み用レイヤを1に設定．
			書き込み用レイヤにしか書かないことで描画を速くする */
    
    gsetbgcolor(win,"GREEN") ;
    gclr(win) ; /* 背景色を反映 */

    /* すべての要素を初期化 */
    for(row = 0; row < NUM_OF_ELEMENTS; row++) {
      for(column = 0; column < NUM_OF_ELEMENTS; column++) {
	mesh[row][column] = VACANT;
	paint_element(win, row, column, GREEN); /* 緑の石を置く */
      }
    }

    place_stone(win, mesh, 3, 3, WHITE_STONE);
    mesh[3][3] = WHITE_STONE;

    place_stone(win, mesh, 4, 4, WHITE_STONE);
    mesh[4][4] = WHITE_STONE;

    place_stone(win, mesh, 3, 4, BLACK_STONE);
    mesh[3][4] = BLACK_STONE;

    place_stone(win, mesh, 4, 3, BLACK_STONE);
    mesh[4][3] = BLACK_STONE;

    availables = NUM_OF_ELEMENTS * NUM_OF_ELEMENTS - 4; /* ４個は置いたので引いておく */
    white_stones = 2;
    black_stones = 2;

    /* 戦況の表示 */
    display_situation(win, white_stones, black_stones); /* 内部で盤面を更新 */

    stone = BLACK_STONE;
    while(availables > 0) {
      if(stone == BLACK_STONE)
	printf("次は黒です．");
      else
	printf("次は白です．");
      printf("どこに置きますか? ");
      fgets(buf, MAX_BUF - 1, stdin);
      position = atoi(buf);
      row = position / 10;
      column = position % 10;

      /* 指定された要素に石がある，もしくは，境界でない  */
      if(isBoundary(mesh[row][column]) == 0)
	continue;

      /* 指定された位置に指定された色の石を置く */
      place_stone(win, mesh, row, column, stone);
      availables--; /* 空白を１つ減らす */

      /* 置いた石が相手の石を挟んでいれば，自分の石に替える */
      lookAround_directions(win, mesh, row, column, stone);
      
      /* 戦況を把握 */
      white_stones = count_whiteStones(mesh);
      black_stones = NUM_OF_ELEMENTS * NUM_OF_ELEMENTS - availables - white_stones;
      /* 戦況の表示 */
      display_situation(win, white_stones, black_stones); /* 内部で盤面を更新 */

      stone ^= STONE_INVERSION; /* 白黒反転 */
    }
    
    gclose(win);
    return 0;
}


/*--------------*
 |  論理レベル  |
 *--------------*/
/*******************************
 *  盤面上の白石の数をカウント *
 *******************************/
int
count_whiteStones(int mesh[NUM_OF_ELEMENTS][NUM_OF_ELEMENTS])
{
  int count = 0;
  int i, j;

  for(i = 0; i < NUM_OF_ELEMENTS; i++)
    for(j = 0; j < NUM_OF_ELEMENTS; j++)
      if(mesh[i][j] & WHITE_STONE)
	count++;
  return count;
}

/***********************
	 盤面上の戦況を表示 *
 ***********************/
Int
Display_situation(int win, int white, int black)
{
  Char message[MAX_MESSAGE * 2]; /* メッセージを書き込む領域は大きめに取っておく */
  Char situation[MAX_MESSAGE]; /* 対戦状況 */
  Char *former_cheering = “Good luck, “; /* 前半の応援メッセージ */
  Char *latter_cheering = “! You can still win.”; /* 後半の応援メッセージ */
  Int I, j;
  Char *top; /* 応援メッセージの先頭 */
  Char *tail; /* 応援メッセージの最後 */
  Char *loser; /* 負けているプレーヤ */
  Int length; /* 対戦状況と応援メッセージの全体の長さ */

  /* 白石と黒石の盤面上の数の表示 */
  Sprintf(situation, “white: %d,   black: %d   “, white, black);
  Strcpy(message, situation);
  Display_message(win, message); /* ここで盤面を再描画 */

  If(white * BIG_LOSS < black)  loser = “White”;
  Else if(black * BIG_LOSS < white) loser = “Black”;
  Else loser = NULL;

  If(loser != NULL) { /* どちらかが大負けしているならテロップ表示 */
    For(i=0;i<20;i++) {
      Sprintf(message,situation);
      Top=message+strlen(situation);
      For(j = 0; j < I; j++) { /* 応援メッセージを右に1文字ずらす */
      	Strcat(top,” “);
	  	Top++;
      }
      Strcat(top,former_cheering);
      Strcat(top,loser);
      Strcat(top,latter_cheering);
      Length=strlen(message);
      If(length >= MAX_MESSAGE) { /* バッファのサイズを超えたら */
       Message[MAX_MESSAGE]=’\0’;
      }
      Display_message(win, message); /* ここで盤面を再描画 */
      Usleep(100*1000); /* 100ミリ秒実行休止 */
    }
  }

  return 0;
}
/*************************************************
 *  石を置こうとしている要素は，空白でかつ境界か *
 *************************************************/
int
isBoundary(int status)
{
  if((status & STONE_BITS) > 0) {
    printf("そのマスには石が置かれています\n");
    return 0;
  } else if((status & BOUNDARY_BIT) == 0) {
    printf("離れたマスです\n");
    return 0;
  } else 
    return 1;
}


/***********************************
 *  置かれた石の周りの方向を調べる *
 ***********************************/
int
lookAround_directions(int win,
		      int mesh[NUM_OF_ELEMENTS][NUM_OF_ELEMENTS],
		      int row,    /* row, columnで指定された */
		      int column, /* 要素が相手を挟むか      */
		      int stone)  /* 自分の石 */
{
  int way;
  int adjacent_row, adjacent_column; /* 隣の要素 */
  int result = 0;

  /* すべての方向で */
  for(way = 0; way < NUM_OF_DIRECTIONS; way++) {
    /* 1つの方向で調べる */
    switch(way) { /* 隣接要素の位置計算 */
    case 0: adjacent_row = row+1; adjacent_column = column; break;
    case 1: adjacent_row = row+1; adjacent_column = column+1; break;
    case 2: adjacent_row = row; adjacent_column = column+1; break;
    case 3: adjacent_row = row-1; adjacent_column = column+1; break;
    case 4: adjacent_row = row-1; adjacent_column = column;  break;
    case 5: adjacent_row = row-1; adjacent_column = column-1; break;
    case 6: adjacent_row = row; adjacent_column = column-1; break;
    case 7: adjacent_row = row+1; adjacent_column = column-1; break;
    default: break;
    }
    /* 隣の要素が盤の外なら，次の方向へ */
    if((adjacent_row < 0) || (adjacent_row >= NUM_OF_ELEMENTS)) continue;
    if((adjacent_column < 0) || (adjacent_column >= NUM_OF_ELEMENTS)) continue;

    if((mesh[adjacent_row][adjacent_column] & STONE_BITS) == VACANT) /* 隣が空きなら */
      continue; /* 何もしない */
    if((mesh[adjacent_row][adjacent_column] & STONE_BITS) ^ stone) { /* 相手の石なら */
      /* 相手の石を挟んでいるか調査 */
      if(canTurnOver(win, mesh, adjacent_row, adjacent_column, way, stone) == 1) {
	place_stone(win, mesh, adjacent_row, adjacent_column, stone); /* 隣の石を自分の色へ */
	result++; /* 挟んでいる方向を1つ増やす */
      }
    }
  }

  return result; /* 挟んでいる方向の数を返す */
}

  
/******************************************************
 *  指定された方向で(row, column)上の石を獲得できるか *
 ******************************************************/
int
canTurnOver(int win, 
	    int mesh[NUM_OF_ELEMENTS][NUM_OF_ELEMENTS],
	    int row,
	    int column,
	    int way,
	    int stone) /* この色の石で (row, column) にある石を挟む */
{
  int *adjacent;  /* (row, column)のさらに隣の要素へのポインタ */
  int adjacent_row, adjacent_column; /* (row, column)のさらに隣 */

  if((adjacent = get_adjacent(mesh, row, column, way)) == NULL) /* 隣の要素が盤外なら */
    return 0; /* 獲得できない */
  else if((*adjacent & STONE_BITS) == VACANT) /* 隣の要素が空きなら */
    return 0;
  else if((*adjacent & STONE_BITS) == stone) { /* 隣の要素が自分の石なら */
    place_stone(win, mesh, row, column, stone); /* この石を自分の色に */
    return 1;
  } else {
    /* さらに調査 */
    
    switch(way) { /* 隣接要素の位置計算 */
    case 0: adjacent_row = row+1; adjacent_column = column; break;
    case 1: adjacent_row = row+1; adjacent_column = column+1; break;
    case 2: adjacent_row = row; adjacent_column = column+1; break;
    case 3: adjacent_row = row-1; adjacent_column = column+1; break;
    case 4: adjacent_row = row-1; adjacent_column = column;  break;
    case 5: adjacent_row = row-1; adjacent_column = column-1; break;
    case 6: adjacent_row = row; adjacent_column = column-1; break;
    case 7: adjacent_row = row+1; adjacent_column = column-1; break;
    default: break;
    }

    if(canTurnOver(win, mesh, adjacent_row, adjacent_column, way, stone)) {
      place_stone(win, mesh, row, column, stone); /* この石を自分の色に */
      return 1;
    } else
      return 0;
  }
}

/******************************
 *  指定された要素に石を置く  *
 ******************************/
int
place_stone(int win,
	    int mesh[NUM_OF_ELEMENTS][NUM_OF_ELEMENTS],
	    int row,
	    int column,
	    int stone)
{
  int color;
  int way;
  int *adjacent;  /* (row, column)の隣の要素へのポインタ */

  mesh[row][column] = stone; /* 石を置いたことを記憶 */
  
  if(stone == WHITE_STONE)
    color = WHITE;
  else
    color = BLACK;
  paint_element(win, row, column, color); /* この要素の石の色を変更 */

  /* すべての方向の隣接要素 */
  for(way = 0; way < NUM_OF_DIRECTIONS; way++) {
    /* 隣接要素 */
    adjacent = get_adjacent(mesh, row, column, way);
    
    /* 隣接要素がなければ何もしない */
    if(adjacent == NULL)
      continue;

    /* 隣接要素が空白要素なら，境界位置になったことを示す．*/
    if(*adjacent == VACANT)
      *adjacent = BOUNDARY_BIT;
  }

  return 0;
}


/**************************
 *  隣の要素へのポインタ  *
 **************************/
int *
get_adjacent(int mesh[NUM_OF_ELEMENTS][NUM_OF_ELEMENTS],
	     int row,
	     int column,
	     int way)
{
  int *adjacent;  /* (row, column)の隣の要素へのポインタ */
  int adjacent_row, adjacent_column; /* (row, column)の隣 */

  switch(way) { /* 隣接要素の位置計算 */
  case 0: adjacent_row = row+1; adjacent_column = column; break;
  case 1: adjacent_row = row+1; adjacent_column = column+1; break;
  case 2: adjacent_row = row; adjacent_column = column+1; break;
  case 3: adjacent_row = row-1; adjacent_column = column+1; break;
  case 4: adjacent_row = row-1; adjacent_column = column;  break;
  case 5: adjacent_row = row-1; adjacent_column = column-1; break;
  case 6: adjacent_row = row; adjacent_column = column-1; break;
  case 7: adjacent_row = row+1; adjacent_column = column-1; break;
  default: break;
  }

  if((adjacent_row < 0) || (adjacent_row > NUM_OF_ELEMENTS - 1))
    return (int *)NULL; /* 隣接要素がなければNULLを返す */
  if((adjacent_column < 0) || (adjacent_column > NUM_OF_ELEMENTS - 1))
    return (int *)NULL; /* 隣接要素がなければNULLを返す */

  adjacent = mesh[adjacent_row] + adjacent_column; /* 隣の要素のアドレス */
  return adjacent;
}


/*--------------*
 |  物理レベル  |
 *--------------*/
/******************************
 *  指定された要素に色を塗る  *
 ******************************/
int
paint_element(int win,
	      int row,
	      int column,
	      int color)
{
  float x, y;
  float center_x=0, center_y=0;
  float edge=0;
  float radian;
  float start_angle = 0.0;
  float end_angle = 0.0;

  x = column * (float)ELEMENT_SIZE; /* 要素の左下の座標 */
  y = row * (float)ELEMENT_SIZE;

  newpen(win, BLACK); /* 色を変える */
  edge = (float)ELEMENT_SIZE;
  drawrect(win,x,y, edge, edge); /* 正方形を描く */

  newpen(win, color); /* 色を変える */
  center_x = x + edge/2.0; center_y = y + edge/2.0;
  radian = edge/2.0 - 1;
  start_angle = 0.0; end_angle = 360.0;
  fillarc(win, center_x, center_y, radian, radian,
	  start_angle, end_angle, ROTATE_DIRECTION); /* 円を塗る */

  newpen(win, BLACK); /* 色を変える */
  drawstr(win, x+1, y+1, 8, 0.0, "%d%d",row, column);

  return 0;
}

/***************************
 *  盤面上のメッセージ表示 *
 ***************************/
int
display_message(int win,
		char message[MAX_MESSAGE])
{
  float x, y;

  x = 0; /* メッセージ領域の起点のx座標は盤面の左側 */
  y = (float)ELEMENT_SIZE * NUM_OF_ELEMENTS; /* メッセージ領域の起点のy座標は盤面の上側 */

  newpen(win, GREEN); /* ペンの色を緑色にする */
  fillrect(win, x, y, ELEMENT_SIZE * NUM_OF_ELEMENTS, MESSAGE_SIZE); /* 前の文字列を消す */

  newpen(win, BLACK); /* 弁の色を黒に変える */
  drawrect(win, x, y, ELEMENT_SIZE * NUM_OF_ELEMENTS, MESSAGE_SIZE); /* 塗りつぶした領域に枠を書く */

  x += (float)ELEMENT_SIZE / 2; /* メッセジージの左に要素の1/2の余白をつける */
  y += (float)MESSAGE_SIZE / 3; /* メッセジージの下に要素の1/3の余白をつける */
  drawstr(win, x, y, 16, 0.0, "%s", message); /* メッセージを描く */

  copylayer(win, 1, 0); /* 書き込み用レイヤから表示用レイヤに一気にコピー
			   これで描画を速くする */

  return 0;
}




