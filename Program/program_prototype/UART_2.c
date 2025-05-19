#include "main.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

// UART handle (pastikan sudah di-generate oleh STM32CubeMX)
extern UART_HandleTypeDef huart1;

// Ukuran buffer
#define RX_BUFFER_SIZE 64

// Variabel global
char rx_data;                          // Data byte yang diterima
char rx_line[RX_BUFFER_SIZE];         // Buffer baris
uint8_t rx_index = 0;                 // Indeks buffer

int objek_x = 0, objek_y = 0;         // Koordinat objek dari kamera

// Fungsi mengirim status ke Raspberry Pi
void kirim_status(const char *status) {
    char msg[64];
    snprintf(msg, sizeof(msg), "$%s\n", status);  // Prefix $ untuk status
    HAL_UART_Transmit(&huart1, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
}

// Callback ketika data serial diterima
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART1) {
        if (rx_data == '\n') {
            rx_line[rx_index] = '\0';  // Akhiri string

            if (rx_line[0] == '#') {
                // Terima koordinat objek dari kamera
                int x = 0, y = 0;
                if (sscanf(rx_line + 1, "%d,%d", &x, &y) == 2) {
                    objek_x = x;
                    objek_y = y;

                    // Kirim ulang ke Pi (opsional debug)
                    char debug[64];
                    sprintf(debug, "Koordinat: x=%d, y=%d\r\n", objek_x, objek_y);
                    HAL_UART_Transmit(&huart1, (uint8_t*)debug, strlen(debug), 100);
                }
            }
            else if (rx_line[0] == '@') {
                // Perintah dari Raspberry Pi
                if (strstr(rx_line, "@cam") != NULL) {
                    kirim_status("CAM_ON");
                }
                else if (strstr(rx_line, "@cam_off") != NULL) {
                    kirim_status("CAM_OFF");
                }
                else if (strstr(rx_line, "@go") != NULL) {
                    kirim_status("GO_RECEIVED");
                }
                else if (strstr(rx_line, "@start") != NULL) {
                    kirim_status("START_RECEIVED");
                }
            }

            // Reset buffer
            rx_index = 0;
            memset(rx_line, 0, RX_BUFFER_SIZE);
        }
        else {
            if (rx_index < RX_BUFFER_SIZE - 1) {
                rx_line[rx_index++] = rx_data;
            } else {
                // Jika buffer overflow, reset
                rx_index = 0;
                memset(rx_line, 0, RX_BUFFER_SIZE);
            }
        }

        // Lanjutkan menerima data berikutnya
        HAL_UART_Receive_IT(&huart1, (uint8_t*)&rx_data, 1);
    }
}

// Inisialisasi UART dan lainnya
void System_Init(void) {
    HAL_UART_Receive_IT(&huart1, (uint8_t*)&rx_data, 1);
}

int main(void) {
    HAL_Init();
    SystemClock_Config();  // Dari STM32CubeMX
    MX_GPIO_Init();
    MX_USART1_UART_Init();

    System_Init();

    // Kirim status awal ke Pi
    kirim_status("STM32_READY");

    while (1) {
        // Di sini kamu bisa gunakan objek_x dan objek_y
        HAL_Delay(10);
    }
}
