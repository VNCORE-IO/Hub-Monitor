#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <lvgl.h>  //V7.7.2
/* Copy lv_conf.h to path:
Arduino/
└── libraries/
    ├── lv_conf.h          ← must be HERE
    └── lvgl/
        ├── lv_conf_template.h
        ├── src/
        └── ...
*/
#include <TFT_eSPI.h>
#include <SPI.h>
#include <WiFiManager.h>
#include <EEPROM.h>
#define KEY_1 12
#define KEY_2 2

TFT_eSPI tft = TFT_eSPI(); /* TFT instance */

WiFiServer server(8877);
WiFiClient client;
static lv_disp_buf_t disp_buf;
static lv_color_t buf[LV_HOR_RES_MAX * 10];
static lv_indev_t *my_indev;
// 定义页面
static lv_obj_t *CPU_page = NULL;
static lv_obj_t *GPU_page = NULL;
static lv_obj_t *login_page = NULL;


static lv_obj_t *ucpu_label;
static lv_obj_t *tcpu_label;
static lv_obj_t *ugpu_label;
static lv_obj_t *tgpu_label;
static lv_obj_t *ip_label;
static lv_obj_t *ip1_label;
static lv_obj_t *cpu_label;
static lv_obj_t *gpu_label;
static lv_obj_t *preload;

static lv_obj_t *wifi_label;
static lv_obj_t *wifi_ap_label;
static lv_obj_t *wifi_ip_label;

static lv_obj_t *t_cpu_arc;
static lv_obj_t *u_cpu_arc;
static lv_obj_t *t_gpu_arc;
static lv_obj_t *u_gpu_arc;

static lv_obj_t *img1;
static lv_obj_t *img2;

static lv_style_t arc_indic_style;
static lv_style_t arc_indic_style_T;
static lv_style_t arc_indic_style1;
static lv_style_t arc_indic_style1_T;
LV_FONT_DECLARE(tencent_w7_24);
//LV_FONT_DECLARE(tencent_hz);
LV_IMG_DECLARE(cpu2);  //声明图片
LV_IMG_DECLARE(GPU);   //声明图片
// 监测数值
int ucpu;
int tcpu;
int ugpu;
int tgpu;
int mode = 0;
const long interval = 6000;
unsigned long lastTime = 0;
uint16_t cg = 0;
long currentMillis = 0;

#if LV_USE_LOG != 0
/* Serial debugging */
void my_print(lv_log_level_t level, const char *file, uint32_t line, const char *dsc, const char *params) {
}
#endif
#define EEPROM_WIFI_Name_Addr 10  //WIFI名字的地址
#define EEPROM_WIFI_Key_Addr 40   //WIFI密码的地址
#define EEPROM_Name_Size_Addr 0   //WIFI名字的长度地址
#define EEPROM_Key_Size_Addr 1    //WIFI密码的长度地址
String WIFI_Name = "";            //WIFI名字
String WIFI_Key = "";             //密码
// 页面初始化
void setupPages() {

  CPU_page = lv_cont_create(lv_scr_act(), NULL);

  lv_obj_set_size(CPU_page, 240, 135);  // 设置容器大小
  lv_obj_set_style_local_bg_color(CPU_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_BLACK);
  lv_obj_set_style_local_border_color(CPU_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_BLACK);
  lv_obj_set_style_local_radius(CPU_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, 0);




  GPU_page = lv_cont_create(lv_scr_act(), NULL);

  lv_obj_set_size(GPU_page, 240, 135);
  lv_obj_set_style_local_bg_color(GPU_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_BLACK);
  lv_obj_set_style_local_border_color(GPU_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_BLACK);
  lv_obj_set_style_local_radius(GPU_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, 0);

  login_page = lv_cont_create(lv_scr_act(), NULL);
  lv_obj_set_size(login_page, 240, 135);  // 设置容器大小
  lv_obj_set_style_local_bg_color(login_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_BLACK);
  lv_obj_set_style_local_border_color(login_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_BLACK);
  lv_obj_set_style_local_radius(login_page, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, 0);


  lv_obj_set_hidden(login_page, false);
  lv_obj_set_hidden(CPU_page, true);
  lv_obj_set_hidden(GPU_page, true);
}
// 设置login_page显示组件
void initLoginPage() {
  /*
  lv_style_t login_spinner_style;
  lv_style_init(&login_spinner_style);
  lv_style_set_line_width(&login_spinner_style, LV_STATE_DEFAULT, 5);
  lv_style_set_pad_left(&login_spinner_style, LV_STATE_DEFAULT, 5);
  lv_style_set_line_color(&login_spinner_style, LV_STATE_DEFAULT, lv_color_hex(0xff5d18));

  preload = lv_spinner_create(login_page, NULL);
  lv_obj_set_size(preload, 100, 100);
  lv_obj_align(preload, NULL, LV_ALIGN_CENTER, 0, 0);
  */
  static lv_style_t font_hz_24;
  lv_style_init(&font_hz_24);
  //lv_style_set_text_font(&font_hz_24, LV_STATE_DEFAULT, &tencent_hz);

  lv_obj_t *btn1 = lv_btn_create(login_page, NULL);
  lv_obj_set_event_cb(btn1, ser_event_handler);
  lv_obj_set_pos(btn1, 60, 10);
  lv_obj_t *label = lv_label_create(btn1, NULL);
  lv_label_set_text(label, "SERIAL");
  lv_obj_add_style(label, LV_LABEL_PART_MAIN, &font_hz_24);
  lv_obj_t *btn2 = lv_btn_create(login_page, NULL);
  lv_obj_set_event_cb(btn2, wifi_event_handler);
  lv_obj_set_pos(btn2, 60, 80);
  lv_obj_t *label1 = lv_label_create(btn2, NULL);
  lv_label_set_text(label1, "WIFI");
  lv_obj_add_style(label1, LV_LABEL_PART_MAIN, &font_hz_24);
}
static void ser_event_handler(lv_obj_t *obj, lv_event_t event) {
  if (event == LV_EVENT_CLICKED) {
    mode = 1;
    lv_obj_set_hidden(CPU_page, false);
    lv_obj_set_hidden(GPU_page, true);
    lv_obj_set_hidden(login_page, true);
    lv_label_set_text(ip_label, "");
    lv_label_set_text(ip1_label, "");
  }
}
static void wifi_event_handler(lv_obj_t *obj, lv_event_t event) {
  if (event == LV_EVENT_CLICKED) {

    if (WiFi.status() != WL_CONNECTED) {
      if (!AutoConfig()) {
        SmartConfig();
        /*
        if (EEPROM.read(EEPROM_Key_Size_Addr) != 0xff)  //如果WIFI密码长度有改变，则读取密码
        {
          WIFI_Key = Read_String(EEPROM_Key_Size_Addr, EEPROM_WIFI_Key_Addr);  //读取WIFI密码，
        }
        if (EEPROM.read(EEPROM_Name_Size_Addr) != 0xff)  //如果WIFI密码长度有改变，则读取密码
        {
          WIFI_Name = Read_String(EEPROM_Name_Size_Addr, EEPROM_WIFI_Name_Addr);  //读取WIFI密码，
        }
        //连接WiFi
        WiFi.setAutoConnect(autoConnect);  //启用自动连接模式
        WiFi.begin(WIFI_Name, WIFI_Key);   //设置WiFi名和密码
        */
      }

      server.begin();
      server.setNoDelay(true);
      //char string[25];
      lv_obj_set_hidden(CPU_page, false);
      lv_obj_set_hidden(GPU_page, true);
      lv_obj_set_hidden(login_page, true);

      lv_label_set_text(ip_label, (WiFi.localIP().toString()).c_str());
      lv_label_set_text(ip1_label, (WiFi.localIP().toString()).c_str());
    }
    mode = 2;
  }
}
// 设置cpu_page显示组件
void initCPU_page() {
  // 绘制温度表盘
  static lv_style_t arc_style;
  lv_style_reset(&arc_style);
  lv_style_init(&arc_style);
  lv_style_set_bg_opa(&arc_style, LV_STATE_DEFAULT, LV_OPA_TRANSP);
  lv_style_set_border_opa(&arc_style, LV_STATE_DEFAULT, LV_OPA_TRANSP);
  lv_style_set_line_width(&arc_style, LV_STATE_DEFAULT, 14);
  lv_style_set_line_color(&arc_style, LV_STATE_DEFAULT, lv_color_hex(0x1e232d));
  lv_style_set_line_rounded(&arc_style, LV_STATE_DEFAULT, false);



  lv_style_init(&arc_indic_style);
  lv_style_set_line_width(&arc_indic_style, LV_STATE_DEFAULT, 10);
  lv_style_set_pad_left(&arc_indic_style, LV_STATE_DEFAULT, 2);
  lv_style_set_line_color(&arc_indic_style, LV_STATE_DEFAULT, lv_color_hex(0x00FF00));

  lv_style_init(&arc_indic_style_T);
  lv_style_set_line_width(&arc_indic_style_T, LV_STATE_DEFAULT, 10);
  lv_style_set_pad_left(&arc_indic_style_T, LV_STATE_DEFAULT, 2);
  lv_style_set_line_color(&arc_indic_style_T, LV_STATE_DEFAULT, lv_color_hex(0x00FF00));


  t_cpu_arc = lv_arc_create(CPU_page, NULL);
  lv_arc_set_bg_angles(t_cpu_arc, 120, 420);
  lv_arc_set_start_angle(t_cpu_arc, 120);
  lv_arc_set_end_angle(t_cpu_arc, 420);
  lv_obj_set_size(t_cpu_arc, 110, 110);
  lv_obj_set_pos(t_cpu_arc, 10, 20);
  lv_obj_add_style(t_cpu_arc, LV_ARC_PART_BG, &arc_style);
  lv_obj_add_style(t_cpu_arc, LV_ARC_PART_INDIC, &arc_indic_style_T);


  static lv_style_t font_24;
  lv_style_init(&font_24);
  lv_style_set_text_font(&font_24, LV_STATE_DEFAULT, &tencent_w7_24);

  tcpu_label = lv_label_create(t_cpu_arc, NULL);
  lv_label_set_text(tcpu_label, "78℃");
  lv_obj_add_style(tcpu_label, LV_LABEL_PART_MAIN, &font_24);
  lv_obj_set_style_local_text_color(tcpu_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);

  lv_obj_align(tcpu_label, t_cpu_arc, LV_ALIGN_CENTER, 0, 0);

  u_cpu_arc = lv_arc_create(CPU_page, NULL);
  lv_arc_set_bg_angles(u_cpu_arc, 120, 420);
  lv_arc_set_start_angle(u_cpu_arc, 120);
  lv_arc_set_end_angle(u_cpu_arc, 420);
  lv_obj_set_size(u_cpu_arc, 135, 135);
  lv_obj_set_pos(u_cpu_arc, 120, 2);
  lv_obj_add_style(u_cpu_arc, LV_ARC_PART_BG, &arc_style);
  lv_obj_add_style(u_cpu_arc, LV_ARC_PART_INDIC, &arc_indic_style);


  ucpu_label = lv_label_create(u_cpu_arc, NULL);
  lv_label_set_text(ucpu_label, "56%");
  lv_obj_add_style(ucpu_label, LV_LABEL_PART_MAIN, &font_24);
  lv_obj_set_style_local_text_color(ucpu_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);
  //lv_obj_set_pos(tcpu_label, 160, 170);
  lv_obj_align(ucpu_label, u_cpu_arc, LV_ALIGN_CENTER, 0, 0);

  ip_label = lv_label_create(CPU_page, NULL);
  //lv_obj_add_style(ip_label, LV_LABEL_PART_MAIN, &font_24);
  lv_obj_set_style_local_text_color(ip_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);
  lv_obj_set_pos(ip_label, 30, 115);

  cpu_label = lv_label_create(CPU_page, NULL);
  lv_label_set_text(cpu_label, "CPU");
  lv_obj_set_style_local_text_color(cpu_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);
  lv_obj_set_pos(cpu_label, 36, 3);

  img1 = lv_img_create(CPU_page, NULL);  //创建一个图像对象
  lv_img_set_src(img1, &cpu2);           //设置图片源
  lv_obj_set_pos(img1, 12, 2);

  static lv_point_t line_points[] = { { 6, 0 }, { 6, 21 }, { 3, 23 }, { 3, 94 }, { 6, 96 }, { 6, 126 }, { 14, 133 }, { 239, 133 } };
  lv_obj_t *obj1 = lv_line_create(CPU_page, NULL);
  lv_line_set_points(obj1, line_points, sizeof(line_points) / sizeof(lv_point_t));

  static lv_style_t style_line;
  lv_style_init(&style_line);
  lv_style_set_line_width(&style_line, LV_STATE_DEFAULT, 3);
  lv_style_set_line_color(&style_line, LV_STATE_DEFAULT, lv_color_hex(0x50ff7d));

  lv_obj_add_style(obj1, LV_LINE_PART_MAIN, &style_line);
}

void initGPU_page() {
  // 绘制温度表盘
  static lv_style_t arc_style;
  lv_style_reset(&arc_style);
  lv_style_init(&arc_style);
  lv_style_set_bg_opa(&arc_style, LV_STATE_DEFAULT, LV_OPA_TRANSP);
  lv_style_set_border_opa(&arc_style, LV_STATE_DEFAULT, LV_OPA_TRANSP);
  lv_style_set_line_width(&arc_style, LV_STATE_DEFAULT, 14);
  lv_style_set_line_color(&arc_style, LV_STATE_DEFAULT, lv_color_hex(0x1e232d));
  lv_style_set_line_rounded(&arc_style, LV_STATE_DEFAULT, false);

  lv_style_init(&arc_indic_style1);
  lv_style_set_line_width(&arc_indic_style1, LV_STATE_DEFAULT, 10);
  lv_style_set_pad_left(&arc_indic_style1, LV_STATE_DEFAULT, 2);

  lv_style_set_line_color(&arc_indic_style1, LV_STATE_DEFAULT, lv_color_hex(0x800080));

  lv_style_init(&arc_indic_style1_T);
  lv_style_set_line_width(&arc_indic_style1_T, LV_STATE_DEFAULT, 10);
  lv_style_set_pad_left(&arc_indic_style1_T, LV_STATE_DEFAULT, 2);

  lv_style_set_line_color(&arc_indic_style1_T, LV_STATE_DEFAULT, lv_color_hex(0x800080));


  t_gpu_arc = lv_arc_create(GPU_page, NULL);
  lv_arc_set_bg_angles(t_gpu_arc, 120, 420);
  lv_arc_set_start_angle(t_gpu_arc, 120);
  lv_arc_set_end_angle(t_gpu_arc, 420);
  lv_obj_set_size(t_gpu_arc, 110, 110);
  lv_obj_set_pos(t_gpu_arc, 10, 20);
  lv_obj_add_style(t_gpu_arc, LV_ARC_PART_BG, &arc_style);
  lv_obj_add_style(t_gpu_arc, LV_ARC_PART_INDIC, &arc_indic_style1_T);


  static lv_style_t font_24;
  lv_style_init(&font_24);
  lv_style_set_text_font(&font_24, LV_STATE_DEFAULT, &tencent_w7_24);

  tgpu_label = lv_label_create(t_gpu_arc, NULL);
  lv_label_set_text(tgpu_label, "8℃");
  lv_obj_add_style(tgpu_label, LV_LABEL_PART_MAIN, &font_24);
  lv_obj_set_style_local_text_color(tgpu_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);

  lv_obj_align(tgpu_label, t_gpu_arc, LV_ALIGN_CENTER, 0, 0);

  u_gpu_arc = lv_arc_create(GPU_page, NULL);
  lv_arc_set_bg_angles(u_gpu_arc, 120, 420);
  lv_arc_set_start_angle(u_gpu_arc, 120);
  lv_arc_set_end_angle(u_gpu_arc, 420);
  lv_obj_set_size(u_gpu_arc, 135, 135);
  lv_obj_set_pos(u_gpu_arc, 120, 2);
  lv_obj_add_style(u_gpu_arc, LV_ARC_PART_BG, &arc_style);
  lv_obj_add_style(u_gpu_arc, LV_ARC_PART_INDIC, &arc_indic_style1);


  ugpu_label = lv_label_create(u_gpu_arc, NULL);
  lv_label_set_text(ugpu_label, "8%");
  lv_obj_add_style(ugpu_label, LV_LABEL_PART_MAIN, &font_24);
  lv_obj_set_style_local_text_color(ugpu_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);
  //lv_obj_set_pos(tcpu_label, 160, 170);
  lv_obj_align(ugpu_label, u_gpu_arc, LV_ALIGN_CENTER, 0, 0);

  ip1_label = lv_label_create(GPU_page, NULL);
  //lv_obj_add_style(ip_label, LV_LABEL_PART_MAIN, &font_24);
  lv_obj_set_style_local_text_color(ip1_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);
  lv_obj_set_pos(ip1_label, 30, 115);

  gpu_label = lv_label_create(GPU_page, NULL);
  lv_label_set_text(gpu_label, "GPU");
  lv_obj_set_style_local_text_color(gpu_label, LV_OBJ_PART_MAIN, LV_STATE_DEFAULT, LV_COLOR_WHITE);
  lv_obj_set_pos(gpu_label, 36, 3);

  img2 = lv_img_create(GPU_page, NULL);  //创建一个图像对象
  lv_img_set_src(img2, &GPU);            //设置图片源
  lv_obj_set_pos(img2, 12, 2);

  static lv_point_t line_points[] = { { 6, 0 }, { 6, 21 }, { 3, 23 }, { 3, 94 }, { 6, 96 }, { 6, 126 }, { 14, 133 }, { 239, 133 } };
  lv_obj_t *obj1 = lv_line_create(GPU_page, NULL);
  lv_line_set_points(obj1, line_points, sizeof(line_points) / sizeof(lv_point_t));

  static lv_style_t style_line;
  lv_style_init(&style_line);
  lv_style_set_line_width(&style_line, LV_STATE_DEFAULT, 3);
  lv_style_set_line_color(&style_line, LV_STATE_DEFAULT, lv_color_hex(0x50ff7d));
  lv_obj_add_style(obj1, LV_LINE_PART_MAIN, &style_line);
}
static int my_btn_read(void)  // btn ID  0,1,2...
{
  if (digitalRead(KEY_1) == 0) {
    return 1;
  }
  if (digitalRead(KEY_2) == 0) {
    return 0;
  }

  return -1;
}
static bool button_read(lv_indev_drv_t *drv, lv_indev_data_t *data) {
  static uint32_t last_btn = 0; /*Store the last pressed button*/
  //Serial.println("444444444");
  int btn_pr = my_btn_read();           /*Get the ID (0,1,2...) of the pressed button*/
  if (btn_pr >= 0) {                    /*Is there a button press? (E.g. -1 indicated no button was pressed)*/
    last_btn = btn_pr;                  /*Save the ID of the pressed button*/
    data->state = LV_BTN_STATE_PRESSED; /*Set the pressed state*/
  } else {
    data->state = LV_BTN_STATE_RELEASED; /*Set the released state*/
  }
  data->btn_id = last_btn; /*Save the last button*/
  return false;
}
void indev_init(void) {
  pinMode(KEY_1, INPUT_PULLUP);
  pinMode(KEY_2, INPUT_PULLUP);
  //Serial.println("55555555");

  // 注册输入设备
  static lv_indev_drv_t indev_drv;
  lv_indev_drv_init(&indev_drv);
  indev_drv.type = LV_INDEV_TYPE_BUTTON;
  indev_drv.read_cb = button_read;
  my_indev = lv_indev_drv_register(&indev_drv);

  // 设置每个按键对应坐标
  /*Assign buttons to points on the screen*/
  static const lv_point_t btn_points[2] = {
    { 70, 20 }, /*Button 0 -> x:10; y:10*/
    { 70, 90 }, /*Button 1 -> x:40; y:100*/
  };
  lv_indev_set_button_points(my_indev, btn_points);
  //Serial.println("11111111111");
  //设置默认组
  lv_group_t *g = lv_group_create();
  //lv_group_add_obj(g,label);
  //lv_group_set_default(g);
  lv_indev_set_group(my_indev, g);
  // lv_group_add_obj(g,btn1);
  // lv_group_add_obj(g,btn2);
  //Serial.println("22222222");
}

/* Display flushing */
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p) {
  uint32_t w = (area->x2 - area->x1 + 1);
  uint32_t h = (area->y2 - area->y1 + 1);

  tft.startWrite();
  tft.setAddrWindow(area->x1, area->y1, w, h);
  tft.pushColors(&color_p->full, w * h, true);
  tft.endWrite();

  lv_disp_flush_ready(disp);
}
void get_hard_data(DynamicJsonDocument &doc) {
  String UCPU = doc["UCPU"];
  String TCPU = doc["TCPU"];
  String UGPU = doc["UGPU"];
  String TGPU = doc["TGPU"];
  int iUCPU = UCPU.toInt();
  int iTCPU = TCPU.toInt();
  int iUGPU = UGPU.toInt();
  int iTGPU = TGPU.toInt();
  UCPU = (String)iUCPU + "%";
  TCPU = (String)iTCPU + "℃";
  UGPU = (String)iUGPU + "%";
  TGPU = (String)iTGPU + "℃";

  lv_label_set_text(ucpu_label, UCPU.c_str());
  lv_label_set_text(tcpu_label, TCPU.c_str());
  lv_label_set_text(ugpu_label, UGPU.c_str());
  lv_label_set_text(tgpu_label, TGPU.c_str());

  uint16_t end_value = 120 + 300 * iUCPU / 100.0f;
  lv_color_t arc_color = iUCPU > 80 ? lv_color_hex(0xFF0000) : lv_color_hex(0x00FF00);
  lv_style_set_line_color(&arc_indic_style, LV_STATE_DEFAULT, arc_color);
  lv_obj_add_style(u_cpu_arc, LV_ARC_PART_INDIC, &arc_indic_style);
  lv_arc_set_end_angle(u_cpu_arc, end_value);

  end_value = 120 + 300 * iTCPU / 100.0f;
  lv_color_t arc_color1 = iTCPU > 80 ? lv_color_hex(0xFF0000) : lv_color_hex(0x00FF00);
  lv_style_set_line_color(&arc_indic_style_T, LV_STATE_DEFAULT, arc_color1);
  lv_obj_add_style(t_cpu_arc, LV_ARC_PART_INDIC, &arc_indic_style_T);
  lv_arc_set_end_angle(t_cpu_arc, end_value);

  end_value = 120 + 300 * iUGPU / 100.0f;
  lv_color_t arc_color2 = iUGPU > 80 ? lv_color_hex(0xFF0000) : lv_color_hex(0x800080);
  lv_style_set_line_color(&arc_indic_style1, LV_STATE_DEFAULT, arc_color2);
  lv_obj_add_style(u_gpu_arc, LV_ARC_PART_INDIC, &arc_indic_style1);
  lv_arc_set_end_angle(u_gpu_arc, end_value);

  end_value = 120 + 300 * iTGPU / 100.0f;
  lv_color_t arc_color3 = iTGPU > 80 ? lv_color_hex(0xFF0000) : lv_color_hex(0x800080);
  lv_style_set_line_color(&arc_indic_style1_T, LV_STATE_DEFAULT, arc_color3);
  lv_obj_add_style(t_gpu_arc, LV_ARC_PART_INDIC, &arc_indic_style1_T);
  lv_arc_set_end_angle(t_gpu_arc, end_value);



  currentMillis = millis();
  if (lastTime == 0 || currentMillis - lastTime >= interval) {

    lastTime = currentMillis;
    if (cg == 0) {
      cg = 1;

      lv_obj_set_hidden(GPU_page, false);
      lv_obj_set_hidden(CPU_page, true);
      lv_obj_set_hidden(login_page, true);

      lv_task_handler();

    } else {
      cg = 0;

      lv_obj_set_hidden(CPU_page, false);
      lv_obj_set_hidden(GPU_page, true);
      lv_obj_set_hidden(login_page, true);

      lv_task_handler();
    }
  }
}
// task循环执行的函数
static void task_cb(lv_task_t *task) {
  String message = "";
  if (mode == 1) {
    if (Serial.available() > 0) {
      message = Serial.readStringUntil('\n');
      DynamicJsonDocument doc(4096);
      DeserializationError err = deserializeJson(doc, message);
      get_hard_data(doc);
    }
  }
  if (mode == 2) {
    /*
    if (WiFi.status() != WL_CONNECTED) {
      initSmartWiFi();

      server.begin();
      server.setNoDelay(true);
      char string[25];

      itoa(ESP.getChipId(), string, 10);
      lv_label_set_text(ip_label, (WiFi.localIP().toString() + ".   Id:" + string).c_str());
      lv_label_set_text(ip1_label, (WiFi.localIP().toString() + ".   Id:" + string).c_str());

      // lv_label_set_text(ip_label, string);
    }
    */
    if (WiFi.status() == WL_CONNECTED) {

      if (!client) {
        client = server.available();
      }


      if (client) {

        if (client.available()) {

          message = client.readStringUntil('\n');

          DynamicJsonDocument doc(4096);
          DeserializationError err = deserializeJson(doc, message);
          get_hard_data(doc);
        }
      }
    }
  }
}

void setup() {
  Serial.begin(115200); /* prepare for possible serial debug */
#if LV_USE_LOG != 0
  lv_log_register_print_cb(my_print); /* register print function for debugging */
#endif
  EEPROM.begin(1024);
  tft.begin();        /* TFT init */
  tft.setRotation(3); /* Landscape orientation */
                      // tft.loadFont(weather_font16);

  lv_init();
  lv_disp_buf_init(&disp_buf, buf, NULL, LV_HOR_RES_MAX * 10);

  /*Initialize the display*/
  lv_disp_drv_t disp_drv;
  lv_disp_drv_init(&disp_drv);
  disp_drv.hor_res = 240;
  disp_drv.ver_res = 135;
  disp_drv.flush_cb = my_disp_flush;
  disp_drv.buffer = &disp_buf;
  lv_disp_drv_register(&disp_drv);

  indev_init();
  setupPages();
  initLoginPage();
  initCPU_page();
  initGPU_page();
  lv_task_t *t = lv_task_create(task_cb, 1000, LV_TASK_PRIO_MID, 0);
}

void loop() {
  lv_task_handler(); /* let the GUI do its work */
}

bool AutoConfig() {
  WiFi.begin();
  if (EEPROM.read(EEPROM_Key_Size_Addr) != 0xff)  //如果WIFI密码长度有改变，则读取密码
  {
    WIFI_Key = Read_String(EEPROM_Key_Size_Addr, EEPROM_WIFI_Key_Addr);  //读取WIFI密码，
  }
  if (EEPROM.read(EEPROM_Name_Size_Addr) != 0xff)  //如果WIFI密码长度有改变，则读取密码
  {
    WIFI_Name = Read_String(EEPROM_Name_Size_Addr, EEPROM_WIFI_Name_Addr);  //读取WIFI密码，
  }
RECONNECT:
  if (WIFI_Name.length() > 1 && WIFI_Key.length() > 6) {
    WiFi.setAutoConnect(true);        //启用自动连接模式
    WiFi.begin(WIFI_Name, WIFI_Key);  //设置WiFi名和密码
  }
  for (int i = 0; i < 20; i++) {
    int wstatus = WiFi.status();
    if (wstatus == WL_CONNECTED) {
      Serial.println("WIFI SmartConfig Success");
      Serial.printf("SSID:%s", WiFi.SSID().c_str());
      Serial.printf(", PSW:%s\r\n", WiFi.psk().c_str());
      Serial.print("LocalIP:");
      Serial.print(WiFi.localIP());
      Serial.print(" ,GateIP:");
      Serial.println(WiFi.gatewayIP());
      return true;
    } else {
      if (Serial.available()) {
        String strCOM = Serial.readStringUntil('\n');  //WF:SSID#PASS\n
        strCOM.trim();
        if (strCOM.indexOf("WF:") > -1) {
          size_t indL = strCOM.indexOf('#');
          WIFI_Name = strCOM.substring(3, indL);
          WIFI_Key = strCOM.substring(indL + 1);
          if (WIFI_Name.length() > 1 && WIFI_Key.length() > 6) {
            Write_String(WIFI_Key.length(), EEPROM_WIFI_Key_Addr, WIFI_Key);
            Write_String(WIFI_Name.length(), EEPROM_WIFI_Name_Addr, WIFI_Name);
            Serial.println("WIFI:" + WIFI_Name + "/" + WIFI_Key);
            goto RECONNECT;
          }
        }
      }
      Serial.print("WIFI AutoConfig Waiting......");
      Serial.println(wstatus);
      delay(1000);
    }
  }
  Serial.println("WIFI AutoConfig Faild!");
  return false;
}
void SmartConfig() {
  WiFi.mode(WIFI_STA);
  Serial.println("\r\nWait for Smartconfig...");
  WiFi.beginSmartConfig();
  while (1) {
    Serial.print(".");
    delay(500);  // wait for a second
    if (WiFi.smartConfigDone()) {
      Serial.println("SmartConfig Success");
      Serial.printf("SSID:%s\r\n", WiFi.SSID().c_str());
      Serial.printf("PSW:%s\r\n", WiFi.psk().c_str());
      WiFi.setAutoConnect(true);
      break;
    }
  }
}

//length写入记录字符串长度的地址，addr是字符串的地址，str为要保存的字符串
void Write_String(int len_addr, int addr, String str) {
  //  EEPROM.write(len_addr, str.length());//写入str字符串的长度
  EEPROM.write(len_addr, str.length() - 1);  //写入str字符串的长度
  //把str所有数据逐个保存在EEPROM
  for (int i = 0; i < str.length(); i++) {
    EEPROM.write(addr + i, str[i]);
  }
  EEPROM.commit();
}

//length位是字符串长度，addr是起始位(字符串首地址)
String Read_String(int len_addr, int addr) {
  String data = "";
  char length = EEPROM.read(len_addr);  //读取记录在EEPROM中的数据长度
  //从EEPROM中逐个取出每一位的值，并链接
  for (int i = 0; i < length; i++) {
    data += char(EEPROM.read(addr + i));
  }
  return data;
}
